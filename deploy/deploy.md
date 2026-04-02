# pysqlsmcp — deploy
Інструкції для розгортання та налаштування MCP-сервера `pysqlsmcp` і пов'язаних ресурсів.

## `deploy_sql_login.py`

Інтерактивно створює SQL Server логін `mcp-<database>` з автоматично згенерованим паролем для кожної вказаної бази даних. Використовує скрипт `scripts/mcp-database.sql`.

**Запуск:**
```bash
python deploy/deploy_sql_login.py
```

**Інтерактивні запити:**
| Запит | Опис |
|---|---|
| `Create MCP users on a SQL Server instance?` | Підтвердження запуску |
| `SQL Server instance` | Ім'я або адреса інстанції, наприклад `localhost` або `srv\MSSQLSERVER` |
| `Create MCP user for a database?` | Повторюється для кожної БД |
| `Database name` | Ім'я цільової БД; буде створено логін `mcp-<database>` |

Пароль генерується автоматично і **не зберігається** — копіювати не потрібно, він одразу вписується в БД.

---

## `config_agnet.py`

Реєструє MCP сервер (`pysqlsmcp`) у конфігураційних файлах агентів (VS Code, Claude Desktop тощо). Автоматично знаходить відомі конфіги в `%APPDATA%` та по дереву каталогів.

**Запуск:**
```bash
python deploy/config_agnet.py
```

**Інтерактивні запити:**
| Запит | Опис |
|---|---|
| `Register pysqlsmcp in an agent config?` | Підтвердження запуску |
| `Search for config files in [<home>]` | Коренева тека для пошуку; Enter = домашній каталог |
| `Which to patch?` | Номери файлів через кому або `all` |

**Підтримувані конфіги:**
| Файл | Агент | Шлях |
|---|---|---|
| `mcp.json` | VS Code | `%APPDATA%\Code\User\mcp.json` |
| `claude_desktop_config.json` | Claude Desktop | `%APPDATA%\Claude\claude_desktop_config.json` |

**Що додається в конфіг:**
```json
"pysqlsmcp": {
  "command": "<python exe>",
  "args": ["<repo>/sqlsmcp.py"]
}
```

---

## `deploy_testenv.py`

Розгортає тестові бази даних `mcp_test_main` і `mcp_test_aux` для інтеграційного тестування. Виконує скрипти:
- `scripts/deploy-testenv-server.sql` — логіни на рівні сервера
- `scripts/deploy-testenv-mcp-test-main.sql` — основна тестова БД
- `scripts/deploy-testenv-mcp-test-aux.sql` — допоміжна тестова БД

**Запуск:**
```bash
python deploy/deploy_testenv.py
```

**Інтерактивні запити:**
| Запит | Опис |
|---|---|
| `Deploy test databases (mcp_test_main, mcp_test_aux)?` | Підтвердження; за замовчуванням `N` |
| `SQL Server instance` | Ім'я або адреса інстанції, наприклад `localhost` |

**Створювані об'єкти:**
| Логін | Роль |
|---|---|
| `mcp-test-reader` | тільки читання |
| `mcp-test-writer` | читання + запис |
| `mcp-test-admin` | повний доступ |

> Після розгортання необхідно видати `GRANT IMPERSONATE` на ці логіни підключальному логіну.

---
