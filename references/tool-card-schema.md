# Tool And Capability Cards

Choose a tool only after defining the needed capability.

~~~yaml
capability: task the tool performs
stage: collection, validation, exploitation, analysis, or evidence
environments: supported OS, architecture, runtime, and access context
prerequisites: privilege, reachability, credentials, dependencies, and target conditions
recommended_when: evidence-backed use cases
avoid_when: conditions producing noise, false results, or unnecessary risk
invocation_pattern: command or API pattern with parameter meaning
expected_output: success, negative, partial, and ambiguous signals
failure_diagnostics: common causes and discriminating checks
alternatives: independent tools or native implementations
risk_and_noise: traffic, artifacts, alerts, state changes, and cleanup
evidence_capture: exact output or artifact to retain
~~~

Prefer an available, compatible, low-impact method producing interpretable evidence. Never assume a named tool is installed. Check availability before building a workflow around it. Do not copy large tool distributions into the engagement workspace.
