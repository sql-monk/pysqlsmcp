# pysqlsmcp

Python MCP (Model Context Protocol) сервер для безпечного, орієнтованого на читання доступу до Microsoft SQL Server. Побудований на [FastMCP](https://github.com/jlowin/fastmcp) та [`mssql-python`](https://pypi.org/project/mssql-python/), комунікує через stdio транспорт.

## Ключові принципи проєктування

1. **Безпека через імперсоналізацію** — кожен запит виконується під `EXECUTE AS`, ніколи під правами логіна, що підключається.
2. **Захисний SET-преамбул** — налаштування сесії примусово встановлюються перед кожним запитом, щоб запобігти блокуванням та ескалації пріоритетів.

---

## Швидкий старт

```bash
pip install -r requirements.txt

# інтерактивний інсталятор (SQL-користувачі, конфіг агентів)
python deploy/install.py
```

Сервер запускається автоматично MCP-клієнтом (VS Code, Claude Desktop тощо) через stdio — ручний запуск не потрібен.

---

## Встановлення (`deploy/install.py`)

Інтерактивний інсталятор виконує всі кроки налаштування. Запустіть один раз після клонування:

```bash
pip install -r requirements.txt

# інтерактивний інсталятор (SQL-користувачі, конфіг агентів)
python deploy/install.py
```

Інсталятор проходить через два етапи:

### 1. SQL Server користувачі

Інсталятор запитує ім'я екземпляра SQL Server, а потім пропонує створити:

| Опція | Скрипт | Що створює |
|-------|--------|------------|
| **На базу даних** | [`deploy/scripts/mcp-database.sql`](deploy/scripts/mcp-database.sql) | Логін `mcp-{database}`, користувач, роль із правами лише на метадані; читання/запис даних заборонено |

Можна створити користувачів для декількох баз за один сеанс.

> **Безпека:** паролі генеруються під час виконання за допомогою `secrets` (40 символів, змішаний регістр + цифри + спецсимволи). Вони передаються до `mssql_python` у пам'яті й **ніколи не зберігаються та не відображаються**.

З'єднання з SQL Server використовує Windows Authentication (`Trusted_Connection=yes`), тому запускайте інсталятор під обліковим записом із правами `sysadmin` або `securityadmin` на цільовому екземплярі.

Після створення користувачів потрібно надати право `IMPERSONATE` логіну, що підключається:

```sql
GRANT IMPERSONATE ON USER::[mcp-YourDatabase] TO [connecting_user];
```

### 2. Інтеграція з агентами

Інсталятор може зареєструвати сервери pysqlsmcp у конфігураційних файлах агентів, щоб MCP-сервери були доступні одразу.

**MCP-сервери:**
- `sqlsmcp.py` — Основний сервер із інструментом `executeQuery` для ad-hoc SQL-запитів
- `sqlscriptmcp.py` — Скриптовий сервер, який автоматично реєструє всі `.sql` файли з `sql_tools/` як MCP-інструменти

Виконується пошук конфігураційних файлів:

| Агент | Конфігураційний файл | Ключ |
|-------|---------------------|------|
| VS Code | `mcp.json` | `servers.pysqlsmcp`, `servers.pysqlsmcp-scripts` |
| Claude Desktop | `claude_desktop_config.json` | `mcpServers.pysqlsmcp`, `mcpServers.pysqlsmcp-scripts` |

Пошук починається з `%APPDATA%` (відомі розташування) та директорії, вказаної користувачем (за замовчуванням: домашня папка). Можна обрати, які знайдені конфіги оновити та які MCP-сервери зареєструвати.

**Швидка реєстрація з параметрами за замовчуванням:**
```bash
python deploy/config_agnet.py --default
```
Це автоматично реєструє всі знайдені MCP-сервери у всіх знайдених конфігах агентів.

Приклад результату для VS Code (`.vscode/mcp.json`):

```json
{
  "servers": {
    "pysqlsmcp": {
      "type": "stdio",
      "command": "python",
      "args": ["path/to/pysqlsmcp/sqlsmcp.py"]
    },
    "pysqlsmcp-scripts": {
      "type": "stdio",
      "command": "python",
      "args": ["path/to/pysqlsmcp/sqlscriptmcp.py"]
    }
  }
}
```

---

## Безпечне виконання запитів

### SET-преамбул

Кожна сесія запитів починається з примусового преамбулу (`_SET_PREAMBLE` у `sqlsprovider.py`):

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

Імперсоналізація — це основний механізм безпеки. Логін, що підключається (Windows auth або SQL auth), **ніколи** не є ідентичністю, під якою виконуються запити користувачів. Замість цього `SQLSProvider` негайно перемикає контекст безпеки після SET-преамбулу.

Кожен інструмент вимагає параметр `impersonate` — ім'я користувача бази даних для імперсоналізації:

```
EXECUTE AS USER = N'{impersonate}'
```

#### Як це працює покроково

1. Встановлюється з'єднання з обліковими даними того, хто викликає (SQL auth або Windows auth).
2. Виконується `_SET_PREAMBLE` (ізоляція, таймаут блокувань, пріоритет deadlock).
3. `EXECUTE AS USER` перемикає контекст безпеки на вказаного користувача.
4. Перевірка підтверджує, що перемикання дійсно відбулось: `USER_NAME()` повинен дорівнювати значенню `impersonate`.
5. Якщо перевірка не пройшла — `REVERT` + `RAISERROR` — запит ніколи не виконується.
6. Запит користувача виконується під імперсоналізованою ідентичністю.
7. `REVERT` відновлює початковий контекст (виконується завжди, навіть при помилці через `finally`).

#### Чому це важливо

- Логін, що підключається, потребує лише права `IMPERSONATE`, а не прямий доступ до даних.
- Права централізовано керуються на користувачах `mcp-{database}`.
- Навіть якщо AI-агент сформує зловмисний запит, він виконається під обмеженою імперсоналізованою ідентичністю.
- Крок верифікації запобігає тихим збоям, коли `EXECUTE AS` синтаксично успішний, але контекст не відповідає очікуваному.

---

## Інструменти

### Основний сервер (`sqlsmcp.py`)

| Інструмент | Додаткові параметри | Опис |
|------------|-------------------|------|
| `executeQuery` | `database`, `query`, `params?` | Виконує довільний запит під імперсоналізацією та повертає рядки + колонки у JSON |

### Скриптовий сервер (`sqlscriptmcp.py`)

Автоматично реєструє всі `.sql` файли з `sql_tools/` як MCP-інструменти. Кожен SQL-файл стає інструментом з власними параметрами.

**Формат SQL-файлу:**
```sql
/*
Опис інструменту (може бути багаторядковим)

@param_name - опис параметра
@another    - опис іншого параметра
*/

DECLARE
    @param_name INT,
    @another    NVARCHAR(128);

SELECT ... WHERE col = @param_name AND another = @another
```

**Вбудовані SQL-інструменти:**

| Інструмент | Параметри | Опис |
|------------|-----------|------|
| `getIndexUsage` | `database`, `table_name?` | Отримати статистику використання індексів для таблиць |
| `getTableSizes` | `database`, `schema_name?`, `table_name?` | Отримати розміри таблиць включно з кількістю рядків та використанням простору |
| `getWaitStats` | `database` | Отримати статистику очікувань SQL Server |
| `getDatabasePermission` | `database`, `user_filter?`, `object_filter?` | Виводить членство в ролях та права для бази даних |
| `requiredAdditionalPermission` | `database`, `object` | Виводить крос-схемні та крос-базові залежності |

### Застарілі інструменти

Наступні інструменти все ще доступні в директорії `tools/`, але більше не є частиною основних MCP-серверів:
- `explainQuery` — Повертає XML-план виконання без виконання запиту
- `getAllDatabasePermission` — Виконує `getDatabasePermission` по всіх доступних базах даних

Усі інструменти приймають параметри `server` та `impersonate`. Завжди використовується Windows Authentication (`Trusted_Connection=yes`).

---

## Структура проєкту

```
sqlsmcp.py                 — Точка входу для основного MCP-сервера (лише executeQuery)
sqlscriptmcp.py            — Точка входу для скриптового MCP-сервера (авто-завантаження sql_tools/)
sqlsprovider.py            — З'єднання, SET-преамбул, EXECUTE AS, виконання запитів
sqlscriptprovider.py       — Парсер SQL-файлів та реєстрація інструментів
sql_tools/                 — SQL-файли, які стають MCP-інструментами
  getIndexUsage.sql        — Статистика використання індексів
  getTableSizes.sql        — Розміри таблиць та використання простору
  getWaitStats.sql         — Статистика очікувань SQL Server
  getDatabasePermission.sql       — Права бази даних
  requiredAdditionalPermission.sql — Крос-схемні/базові залежності
deploy/
  config_agnet.py          — Реєстрація конфігу агентів (підтримує прапорець --default)
  scripts/
    mcp-database.sql       — DDL-шаблон для користувача/ролі
tools/
  execute_query.py         — Реалізація інструменту executeQuery
  explain_query.py         — Інструмент explainQuery (застарілий)
  get_database_permission.py       — Інструмент getDatabasePermission (застарілий)
  get_all_database_permission.py   — Інструмент getAllDatabasePermission (застарілий)
  required_additional_permission.py — Інструмент requiredAdditionalPermission (застарілий)
  sql/
    get_database_permission.sql      — Запит прав (застарілий)
    required_additional_permission.sql — Запит залежностей (застарілий)
tests/
  test_sqlscriptprovider.py — Тести для парсера SQL-файлів
```

## Логи

Активність запитів дописується у файл `sqlsmcp.log` у кореневій директорії проєкту.
