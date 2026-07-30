# Business Logic, Workflow, And State Machine Operations

## Continuity And Loading Rules

Read [../module-continuity.md](../module-continuity.md) before invoking a card. Keep one engagement state and one attack-path graph across all cards and domains.

1. Load the decision framework card on entry.
2. Keep the calling domain's parent path — business-logic is a supporting capability, not a replacement domain.
3. Return results to the parent path and rerank affected paths before leaving.
4. Checkpoint before invoking and after returning material evidence.
5. Multiple domains may call this capability from different parent paths.

## Card Router

| Card | Load condition | Required return |
|---|---|---|
| [Decision Framework](business-logic-01-decision-framework.md) | Load when evidence supports a business-logic path: a value action (payment, order, transfer, redemption, refund, approval) whose integrity relies on client-enforced sequence, client-supplied amounts, or client-respected state transitions. | Return evidence, capability changes, affected paths, and the next decision. |

## When To Invoke This Capability

Invoke from any domain (Web/API, mini-program, mobile, supply-chain) when:

- [FACT] A multi-step business process is exposed (checkout, KYC, loan application, reward redemption, account upgrade, invoice approval)
- [FACT] The client specifies a price, amount, quantity, discount, or currency value that should be server-determined
- [FACT] A coupon, voucher, loyalty point, or incentive has a usage limit enforced only on the client
- [FACT] A state field is visible in requests or responses (order_status, payment_state, verification_level)
- [INFERENCE] The API exposes endpoints for individual workflow steps without server-side sequence validation

Do not invoke solely because an application has a "payment page" or "order form" — there must be a specific signal that the server trusts client-supplied business data or sequence.
