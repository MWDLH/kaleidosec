# Failure Recovery

## Classify Failure

- execution: syntax, dependency, tool crash, malformed input, or local runtime.
- environment: OS, architecture, version, sandbox, policy, or compatibility.
- access: identity, privilege, authentication, authorization, or session.
- reachability: routing, proxy, DNS, firewall, protocol, TLS, or availability.
- method: technique unsuitable while the hypothesis remains plausible.
- prerequisite: required configuration or state absent.
- hypothesis: independent evidence contradicts the issue.
- route_value: route may work but no longer merits current investment.

## Recover Deliberately

1. Capture exact error, response, timeout behavior, and environment.
2. Separate target behavior from local tool behavior.
3. Identify which assumption the result tests.
4. Choose the cheapest discriminating check.
5. Change one meaningful variable when practical.
6. Update the path with evidence, not only attempt count.

Use an alternative tool only for an independent implementation or better diagnostics. Park rather than discard a path when missing access, version data, network position, or another prerequisite may later change the result.
