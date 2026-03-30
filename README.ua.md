# pysqlsmcp

Python MCP (Model Context Protocol) сервер для безпечного, орієнтованого на читання доступу до Microsoft SQL Server. Побудований на [FastMCP](https://github.com/jlowin/fastmcp), [`mssql-python`](https://pypi.org/project/mssql-python/) та обслуговується через HTTPS за допомогою Uvicorn.

## Ключові принципи проєктування

1. **Безпека через імперсоналізацію** — кожен запит виконується під `EXECUTE AS`, ніколи під правами логіна, що підключається.
2. **Захисний SET-преамбул** — налаштування сесії примусово встановлюються перед кожним запитом, щоб запобігти блокуванням та ескалації пріоритетів.
3. **Тільки TLS** — сервер вимагає сертифікат; HTTP без шифрування не підтримується.

---

## Швидкий старт

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

python gen_cert.py             # створює cert.pem + key.pem (самопідписаний, localhost/127.0.0.1)
python server.py --certfile cert.pem --keyfile key.pem
```

| Прапорець | За замовчуванням | Опис |
|-----------|-----------------|------|
| `--host` | `0.0.0.0` | Адреса прив'язки |
| `--port` | `8444` | Порт |
| `--certfile` | *(обов'язковий)* | Шлях до TLS-сертифіката |
| `--keyfile` | *(обов'язковий)* | Шлях до приватного ключа TLS |

---

## Встановлення та конфігурація

### Налаштування SQL Server

Файл [`tools/sql/login_and_user_creation.sql`](tools/sql/login_and_user_creation.sql) містить еталонний DDL.

#### Рівень сервера — логін `mcp-server`

```sql
CREATE LOGIN [mcp-server] WITH PASSWORD = '[strong pwd]', CHECK_POLICY = ON;

-- Серверні ролі тільки для читання (SQL Server 2022+)
ALTER SERVER ROLE [##MS_ServerStateReader##]            ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_ServerPerformanceStateReader##] ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DefinitionReader##]             ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_SecurityDefinitionReader##]     ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DatabaseConnector##]            ADD MEMBER [mcp-server];
```

#### Рівень бази даних — користувач `mcp-{database}`

Для кожної бази даних, де використовується `mcplevel=1`:

```sql
CREATE LOGIN  [mcp-YourDatabase] WITH PASSWORD = '[strong pwd]', CHECK_POLICY = ON;
CREATE USER   [mcp-YourDatabase] FROM LOGIN [mcp-YourDatabase];
CREATE ROLE   [db_mcp_YourDatabase];

ALTER ROLE [db_mcp_YourDatabase] ADD MEMBER [mcp-YourDatabase];

GRANT VIEW DATABASE STATE             TO [db_mcp_YourDatabase];
GRANT VIEW ANY DEFINITION             TO [db_mcp_YourDatabase];
GRANT VIEW DATABASE PERFORMANCE STATE TO [db_mcp_YourDatabase];
GRANT VIEW DATABASE SECURITY STATE    TO [db_mcp_YourDatabase];

-- Заборона доступу до даних — лише метадані
ALTER ROLE [db_denydatareader] ADD MEMBER [mcp-YourDatabase];
ALTER ROLE [db_denydatawriter] ADD MEMBER [mcp-YourDatabase];
```

Логіну, що підключається, також потрібно надати:

```sql
-- Для mcplevel=0:
GRANT IMPERSONATE ON LOGIN::[mcp-server] TO [connecting_login];

-- Для mcplevel=1 (для кожної бази):
GRANT IMPERSONATE ON USER::[mcp-YourDatabase] TO [connecting_user];
```

### Конфігурація MCP у VS Code

Додайте до `.vscode/mcp.json`:

```json
{
  "servers": {
    "pysqlsmcp": {
      "type": "http",
      "url": "https://localhost:8444/mcp"
    }
  }
}
```

---

## Безпечне виконання запитів

### SET-преамбул

Кожна сесія запитів починається з примусового преамбулу (`_SET_PREAMBLE` у `db_provider.py`):

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET LOCK_TIMEOUT 1000;
SET DEADLOCK_PRIORITY LOW;
```

| Інструкція | Призначення |
|------------|-------------|
| `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED` | Брудне читання — MCP-сервер ніколи не потребує транзакційної узгодженості і не повинен встановлювати shared-блокування, які блокують продуктивні записи. |
| `SET LOCK_TIMEOUT 1000` | Якщо блокування все ж потрібне (метадані DDL тощо), запит завершується з помилкою через 1 секунду замість безкінечного очікування. |
| `SET DEADLOCK_PRIORITY LOW` | Якщо виникає deadlock, SQL Server першим завершує MCP-сесію, захищаючи продуктивні навантаження. |

Ці налаштування гарантують, що MCP-активність не може погіршити продуктивність — жодних блокувань, швидкий таймаут, найнижчий пріоритет при deadlock.

Додатково, `explain_query` обгортає запит користувача:

```sql
SET SHOWPLAN_XML ON;
-- запит користувача (фактично не виконується)
SET SHOWPLAN_XML OFF;
```

Це повертає XML-план виконання без запуску самого запиту.

### Імперсоналізація (`EXECUTE AS`)

Імперсоналізація — це основний механізм безпеки. Логін, що підключається (Windows auth або SQL auth), **ніколи** не є ідентичністю, під якою виконуються запити користувачів. Замість цього `DbProvider` негайно перемикає контекст безпеки після SET-преамбулу.

#### Два рівні імперсоналізації (`mcplevel`)

Кожен інструмент приймає параметр `mcplevel` (за замовчуванням `0`):

| `mcplevel` | Інструкція `EXECUTE AS` | Ефективна ідентичність | Випадок використання |
|------------|-------------------------|----------------------|---------------------|
| `0` | `EXECUTE AS LOGIN = N'mcp-server'` | Серверний логін `mcp-server` | Широкий доступ тільки для читання через серверні ролі |
| `1` | `EXECUTE AS USER = N'mcp-{database}'` | Користувач бази даних `mcp-{database}` | Детальні права на рівні конкретної бази через ролі бази даних |

#### Як це працює покроково

1. Встановлюється з'єднання з обліковими даними того, хто викликає (SQL auth або Windows auth).
2. Виконується `_SET_PREAMBLE` (ізоляція, таймаут блокувань, пріоритет deadlock).
3. `EXECUTE AS LOGIN` або `EXECUTE AS USER` перемикає контекст безпеки.
4. Перевірка підтверджує, що перемикання дійсно відбулось:
   - Рівень 0: `SYSTEM_USER` повинен дорівнювати `mcp-server`
   - Рівень 1: `USER_NAME()` повинен дорівнювати `mcp-{database}`
5. Якщо перевірка не пройшла — `REVERT` + `RAISERROR` — запит ніколи не виконується.
6. Запит користувача виконується під імперсоналізованою ідентичністю.
7. `REVERT` відновлює початковий контекст (виконується завжди, навіть при помилці через `finally`).

#### Чому це важливо

- Логін, що підключається, потребує лише права `IMPERSONATE`, а не прямий доступ до даних.
- Права централізовано керуються на логіні `mcp-server` / користувачах `mcp-{database}`.
- Навіть якщо AI-агент сформує зловмисний запит, він виконається під обмеженою імперсоналізованою ідентичністю.
- Крок верифікації запобігає тихим збоям, коли `EXECUTE AS` синтаксично успішний, але контекст не відповідає очікуваному.

---

## Інструменти

Усі інструменти приймають `server`, `username?`, `password?` та `mcplevel?` (за замовчуванням `0`).
Коли `username`/`password` не вказані, використовується Windows Authentication (`Trusted_Connection=yes`).

| Інструмент | Додаткові параметри | Опис |
|------------|-------------------|------|
| `executeQuery` | `database`, `query` | Виконує довільний запит під імперсоналізацією та повертає рядки + колонки у JSON |
| `explainQuery` | `database`, `query` | Повертає XML-план виконання (`SHOWPLAN_XML`) без виконання запиту |
| `getDatabasePermission` | `database`, `user_filter?`, `object_filter?` | Виводить членство в ролях та права для однієї бази даних (запитує `sys.database_role_members` + `sys.database_permissions`) |
| `getAllDatabasePermission` | `user_filter?`, `object_filter?` | Виконує `getDatabasePermission` по всіх доступних базах даних та агрегує результати |
| `requiredAdditionalPermission` | `database`, `object` | Виводить крос-схемні та крос-базові залежності для збереженої процедури або представлення (через `sys.sql_expression_dependencies`) |

---

## Структура проєкту

```
server.py                  — HTTPS точка входу Uvicorn, реєструє всі інструменти
db_provider.py             — З'єднання, SET-преамбул, EXECUTE AS, виконання запитів
gen_cert.py                — Генерує самопідписаний TLS-сертифікат (cert.pem + key.pem)
tools/
  execute_query.py         — інструмент executeQuery
  explain_query.py         — інструмент explainQuery
  get_database_permission.py       — інструмент getDatabasePermission
  get_all_database_permission.py   — інструмент getAllDatabasePermission
  required_additional_permission.py — інструмент requiredAdditionalPermission
  sql/
    get_database_permission.sql      — Запит прав
    required_additional_permission.sql — Запит залежностей
    login_and_user_creation.sql      — Еталонний DDL для налаштування mcp-server
```

## Логи

Активність запитів дописується у файл `sqlsmcp.log` у кореневій директорії проєкту.
