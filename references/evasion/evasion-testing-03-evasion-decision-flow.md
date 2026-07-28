# Authorized Control-Evasion And Environment Adaptation: Evasion Decision Flow

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Evasion Decision Flow

```
Is the control blocking necessary testing?
├─ NO → Skip evasion. Find another way to answer the question.
└─ YES → 
    ├─ Can we test the same hypothesis from a different network position?
    │   └─ YES → Use the alternative. Don't bypass.
    ├─ Can we use a native/LOLBin method to achieve the same result?
    │   └─ YES → Use the native method.
    ├─ Can we simulate the attack locally (lab environment) and infer target behavior?
    │   └─ YES → Simulate. Only test confirmed hypotheses on target.
    └─ Must evade → Choose the minimal evasion needed.
        └─ Document: what was blocked, why evasion was necessary, what was done, detection result
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
