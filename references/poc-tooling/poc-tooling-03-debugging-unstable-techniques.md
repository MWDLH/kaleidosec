# PoC, Debugging, And Tool Engineering Capability: Debugging Unstable Techniques

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Debugging Unstable Techniques

### Classification → Action Matrix

| Symptom | Most Likely Cause | First Diagnostic Step |
|---|---|---|
| Works locally, fails against target | Environmental difference (OS, library version, architecture) | Compare `uname -a`, `python --version`, library versions, PATH |
| Works once, fails on retry | Race condition, state machine, token expiration, WAF rate limiting | Add delay, check if session/token is still valid, add unique value per attempt |
| Partial output, then crash | Memory corruption, buffer size mismatch, encoding | Check exact buffer sizes, add debugging output at each allocation |
| Different result at different times | Load balancer, caching, A/B deployment, randomized backend behavior | Send request 10×, check response distribution, check headers for cache hit/miss, server identity |
| Timeout | Network filtering, MTU issue, protocol mismatch | Test from different network position, reduce packet size, try alternate protocol |
| Segfault/crash in exploit | Wrong architecture, ASLR, stack layout, bad ROP gadgets | Check architecture (ARM vs x86 vs x64), check ASLR status, verify gadget offsets against target's exact binary version |
| "Should work" but doesn't | Assumption about target is wrong | List every assumption. Test each one independently. |

### Rule: Change One Variable

When debugging, change exactly one variable per attempt. If you change the payload AND the encoding AND the request method simultaneously, you won't know which change mattered. This is tedious but it's the only way to isolate issues.

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
