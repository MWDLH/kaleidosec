# Field Decision Examples

## High-Privilege Internal Host

Situation: local administrative access exists on a Windows host, but domain position and objective progress are unclear.

Good decision: first establish identity, domain membership, network position, reachable management boundaries, defensive controls, high-value role of the host, and what has already been collected. Generate paths only after these facts. Do not start broad credential collection or lateral activity merely because privilege is available.

Next-action reasoning: prefer the smallest collection action that distinguishes whether this host is a useful identity, trust, session, management, or network bridge.

## A Tool Does Not Work

Situation: the selected collector or validator returns an error.

Good decision: capture exact error and environment, then separate local dependency, architecture, privilege, protocol, reachability, target configuration, and control interference. Keep the vulnerability or path as a hypothesis unless the failed result actually tests its prerequisite.

Next-action reasoning: change one meaningful variable or use an independent implementation. Do not cycle through tool names without gaining information.

## A Low-Value Finding Competes With A Chain

Situation: an isolated issue is technically interesting, while another evidence-backed route may unlock a privileged role or high-value boundary.

Good decision: preserve evidence for the isolated issue, park deeper work with a reactivation condition, and prioritize the route with stronger objective contribution and chain leverage. Revisit the parked issue if new evidence raises its impact or removes its cost.

## Reverse Engineering Inside A Mobile Path

Situation: a mobile application uses a native library to construct authenticated requests.

Good decision: keep the mobile attack path as parent, invoke reverse/protocol analysis with the narrow question of how the request identity and integrity fields are derived, and define the deliverable and return condition. Return confirmed behavior and assumptions to the mobile path, then test whether the backend trusts client-controlled material.

Do not let reverse engineering become an open-ended artifact tour disconnected from the engagement objective.
