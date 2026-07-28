# Action Safety Gates

Use actual impact, scope, scale, persistence, and reversibility rather than tool names. Practicality comes from a clear authorization profile, not from asking before every command.

## L0: Offline And Passive

Proceed autonomously when relevant to the objective:

- offline source, binary, package, configuration, capture, and artifact analysis;
- passive asset discovery and supplied-evidence review;
- local PoC construction, syntax checks, mock testing, and result interpretation;
- state maintenance, path planning, reporting, and cleanup planning.

L0 may continue while active scope is incomplete, provided it does not contact or modify a target.

## L1: Bounded Low-Impact Active Testing

Proceed autonomously inside confirmed scope unless the authorization profile excludes the action:

- bounded low-rate enumeration and read-only service or identity queries;
- representative request replay, role comparison, and minimal authorization checks;
- single-account or single-endpoint credential validation with lockout awareness;
- minimal vulnerability validation that does not create durable access or business change;
- retrieving the smallest test-owned or synthetic sample needed to prove access.

Stop when observed impact, target count, traffic, or data sensitivity exceeds the recorded limit.

## L2: Controlled Exploitation And Movement

Proceed without per-command reconfirmation only when L2 or the specific action class is pre-authorized for the engagement. L2 may include:

- non-persistent command-execution proof using bounded identity or environment observations;
- one-target lateral validation with an approved identity and explicit stop condition;
- temporary tunnel, proxy, runtime hook, certificate-pinning bypass, or process-local control adaptation;
- controlled credential use, exploitation, or privilege-path validation that leaves no durable control;
- bounded access to a real resource when synthetic proof cannot establish impact.

Before an L2 action, record target, parent path, purpose, expected result, likely artifacts, rollback, and stop condition. Reconfirm only when target class, scale, persistence, method risk, or business effect changes materially.

## L3: Explicit Action Approval

Require explicit approval for the bounded action or phase before:

- creating accounts, adding privileged group membership, deploying a WebShell or agent, or establishing durable access;
- modifying IAM, ACL, GPO, network policy, security groups, production configuration, startup behavior, scheduled tasks, services, or shared trust;
- disabling, mutating, or centrally bypassing logging, endpoint protection, monitoring, approval controls, or security policy;
- restarting or interrupting services, triggering lockout or exhaustion risk, or changing production data;
- batch exploitation, broad password testing, high-volume scanning, or expansion across many hosts, accounts, tenants, or a new scope boundary;
- exporting or transferring a material volume of real sensitive data.

One approval may cover a clearly bounded set of equivalent L3 actions. Record approval scope, approver, time, limits, and expiry. Reconfirm only when those terms change materially.

## Professional Floor

Do not use destructive data operations, self-propagation, activity concealment, log clearing, evidence removal, or unnecessary real-data exfiltration as routine proof. If an engagement explicitly requires destructive resilience testing, treat it as a separately designed exercise with dedicated approval, rollback, observers, and stop authority rather than an ordinary pentest step.

## Minimize And Track

Use the smallest proof that establishes the issue at the approved level. Record every account, file, task, service, process, configuration, cloud resource, access policy, mobile modification, deployed component, tunnel, and temporary control adaptation created by the test. Cleanup means reverting test changes, not deleting audit evidence or concealing activity.
