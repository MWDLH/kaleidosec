# Common Anti-Patterns And Mistakes

## Contents

- [1. Scanner-Result-As-Finding](#1-scanner-result-as-finding)
- [2. Tool-Driven Testing](#2-tool-driven-testing)
- [3. Confirmation Bias In Testing](#3-confirmation-bias-in-testing)
- [4. Premature Exploitation](#4-premature-exploitation)
- [5. Depth-First Tunneling](#5-depth-first-tunneling)
- [6. Credential Blindness](#6-credential-blindness)
- [7. Clean-Environment Assumption](#7-clean-environment-assumption)
- [8. Assuming Defense Absence](#8-assuming-defense-absence)
- [9. Skipping The Basics Because They're "Basic"](#9-skipping-the-basics-because-theyre-basic)
- [10. Reporting What You Wanted To Find, Not What You Found](#10-reporting-what-you-wanted-to-find-not-what-you-found)


These are mistakes that even experienced testers make. Recognize them, avoid them, and correct them when you see them in your own engagement flow.

---

## 1. Scanner-Result-As-Finding

**What it looks like**: AWVS/Burp Scanner/nuclei reports 47 "vulnerabilities." Operator copies them directly into the report without verification. "The scanner said it's XSS, so it's XSS."

**Why it's wrong**: Scanners produce hypotheses, not confirmed findings. A scanner matches patterns — it doesn't verify preconditions, reachability, or impact. 80% of scanner findings are false positives or unexploitable in context.

**What to do instead**: Each scanner finding is a **lead to investigate**. Verify: does the payload actually reach a dangerous sink? Is there a control that neutralizes it? What's the actual impact? Report only what you've confirmed.

---

## 2. Tool-Driven Testing

**What it looks like**: nmap → nothing obvious? Run masscan. Then run RustScan. Then try unicornscan. Each tool produces slightly different output, but the operator learns nothing new.

**Why it's wrong**: Running more tools is not collecting more information. It's collecting more formats of the same information. Port 445 is either open or it isn't — running five port scanners doesn't change that. The operator is substituting tool variety for actual thinking.

**What to do instead**: When a tool doesn't give you useful output, ask: what question am I trying to answer? Is there a tool that answers that exact question? Is there a native command or manual check that would be faster? If you caught yourself opening a third port scanner, stop.

---

## 3. Confirmation Bias In Testing

**What it looks like**: Operator finds a version string that matches a known-vulnerable version. Excited, they craft an exploit. It fails three times. Each time they tweak the payload slightly, convinced the vulnerability "should be there." Four hours later, they discover the version is false (Apache banner on an nginx server) or backport-patched.

**Why it's wrong**: The operator is looking for evidence that confirms their hypothesis, not evidence that disproves it. A version string is a fingerprint — a clue, not a conclusion. Each failed attempt is evidence, but the operator ignores it.

**What to do instead**: For any hypothesis, define the **falsification test** first: "If X is true, then Y should happen. If Y doesn't happen, X is false or blocked." When further attempts stop changing a meaningful variable or producing information, switch from "how do I make this work?" to "which prerequisite, control, or assumption should I test next?" Several distinct evidence-producing attempts may still justify a deep dive.

---

## 4. Premature Exploitation

**What it looks like**: Operator discovers an upload form that accepts .php files. Immediately uploads a webshell. The server returns 200. Operator celebrates. But wait: where is the file stored? Is PHP installed? Does the upload directory have execute permissions? Is the file served with the right Content-Type? Was the file actually written to disk?

**Why it's wrong**: The operator tested step 1 (upload) without understanding steps 2-4 (storage, execution, accessibility). A 200 OK on upload doesn't mean the file executed.

**What to do instead**: Before exploiting, map the full attack chain: entry → processing → output/effect. Test each link. An upload without understanding the storage and serving pipeline is half a test.

---

## 5. Depth-First Tunneling

**What it looks like**: Operator finds a promising SSRF endpoint. Spends 6 hours trying to reach metadata, internal APIs, and Redis, trying 30 different bypass techniques. Meanwhile, they haven't checked if the application has an IDOR in its user profile API (which would take 5 minutes and might actually work).

**Why it's wrong**: The operator is optimizing for technical interest, not engagement progress. A clever SSRF chain is more satisfying than a boring IDOR — but the IDOR might be the finding that actually matters to the customer.

**What to do instead**: Before committing to a deep dive, set a decision checkpoint rather than a fixed stop: define the evidence or capability change that would justify continued investment. At the checkpoint, continue while independent branches or material information gain remain; otherwise park the path with a concrete reactivation condition and test stronger routes.

---

## 6. Credential Blindness

**What it looks like**: Operator has a low-privilege domain user account. Instead of methodically testing what that account can see (shares, LDAP, SPNs, user lists), they immediately start trying privilege escalation exploits. None of them work because they skipped the basics.

**Why it's wrong**: Most privilege escalation failures come from not understanding the current position. Before trying to escalate, exhaust what your current identity can see — the escalation path is often visible from where you are, but you need to look.

**What to do instead**: After obtaining ANY new identity, run a basic enumeration checklist before attempting escalation. For AD: `whoami /all`, `net user %USERNAME% /domain`, `net group "Domain Admins" /domain`, find accessible shares, enumerate SPNs. For cloud: `get-caller-identity`, list accessible resources, enumerate attached policies.

---

## 7. Clean-Environment Assumption

**What it looks like**: Operator uses a public PoC exploit. It fails. They assume the target "isn't vulnerable." Actually, the PoC was written for Python 3.6 and they're running 3.11 — the exploit crashed on an API change. The target IS vulnerable, but the tool failed.

**Why it's wrong**: The operator didn't verify whether the failure was in the target (hypothesis wrong) or in the tool (execution/environment failure). The [failure-recovery.md](failure-recovery.md) classification exists exactly for this reason.

**What to do instead**: After any tool failure, quickly check: does this tool work against a known-good target? (A local test environment, a different endpoint on the same target, a different path that should work?) This distinguishes tool failure from target behavior.

---

## 8. Assuming Defense Absence

**What it looks like**: Operator runs Mimikatz on a Windows 11 host. It gets flagged and quarantined instantly. Operator is surprised. In 2026, every major EDR product detects default Mimikatz.

**Why it's wrong**: The operator assumed the target environment is defenseless. Modern Windows environments have Defender, AMSI, Credential Guard, and often third-party EDR. You should assume defenses are present and plan accordingly.

**What to do instead**: Before deploying any tool with a known signature, test the defensive posture: check running processes for AV/EDR, test AMSI, check PowerShell language mode, check if LSASS is protected. Choose techniques appropriate to the environment.

---

## 9. Skipping The Basics Because They're "Basic"

**What it looks like**: Operator spends two days on a complex JWT key confusion attack while the application stores session tokens in `localStorage` without HttpOnly flags, has an exposed `.git` directory with the full source code, and allows password reset without email verification.

**Why it's wrong**: The operator is chasing the interesting technical challenge instead of the actual attack surface. Most real-world compromises don't involve advanced techniques — they involve misconfigurations, missing authorization checks, and exposed sensitive data.

**What to do instead**: For every target, run through the basics before going deep: robots.txt, sitemap.xml, .git/.svn exposure, default credentials, missing authorization on profile endpoints, verbose errors, exposed admin panels. These take 20 minutes and often yield the best findings.

---

## 10. Reporting What You Wanted To Find, Not What You Found

**What it looks like**: Operator spends 3 days on a promising path. It ultimately fails — the target wasn't vulnerable. To justify the time spent, they report the failed attempt as a "potential vulnerability" or "theoretical risk" with inflated severity.

**Why it's wrong**: A failed attack is NOT a finding. "If the configuration were different, this would be vulnerable" is not a vulnerability — it's speculation. Reporting failures as findings erodes credibility and wastes the client's time.

**What to do instead**: A disproven hypothesis is valid intelligence — but it goes in the "Parked and Rejected Paths" section of the report, not in "Findings." Be honest about what was tested and what didn't work. The client needs accurate information, not a padded report.


