# Business Logic, Workflow, And State Machine Operations: Decision Framework

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Decision Framework

Business-logic vulnerabilities are defects in how an application models and enforces its own rules. They bypass technical controls — no injection, no broken crypto, no memory corruption. The exploit is the application's own intended functionality, used in an unintended sequence or with unintended values.

### Decision Entry

Trigger this framework from the calling domain when:

- [FACT] A **value action** is identified: an operation that changes ownership, balance, inventory, identity state, or approval status
- [FACT] The client can **influence business parameters**: price, amount, quantity, discount code, currency, fee, tax rate, shipping cost
- [FACT] A **multi-step workflow** exposes individual API endpoints per step
- [FACT] A **state field** is visible in client-controlled data (request body, URL parameter, hidden form field)
- [FACT] An **incentive** exists with limits (coupon, voucher, loyalty points, referral bonus, signup credit, free trial)

The cross-domain trigger is the same regardless of whether the entry point is a Web form, a mini-program API call, a mobile app request, or a CI/CD pipeline parameter. The decision framework is platform-agnostic; platform-specific iteration methods are noted where relevant.

### Step 1: Model The Business Process

Before testing, document the intended flow. Do not skip this step.

For each value action, answer:
1. **What is the flow?** List every step from initiation to completion. Which actor performs each step?
2. **What does each step assume?** "After payment confirmation, the order is shipped." What if payment confirmation arrives twice?
3. **Where are the trust boundaries?** Which values does the server recalculate vs. accept from the client? Which steps assume the previous step completed legitimately?
4. **What is the cost of a violation?** One extra discount? Inventory oversold below zero? An unverified account with full privileges?

### Step 2: Side-Effect Controls — Read Before Any Business-Logic Test

Business-logic testing manipulates real business objects (orders, payments, accounts, inventory, coupons). Unlike injection testing — which leaves the underlying data unchanged — a business-logic test can create real financial or operational side effects. Apply these controls before any test:

1. **Use test-only resources**: If the application supports sandbox/test environments, test accounts, or test payment methods, use them. A test coupon applied to a test order with a test payment method isolates side effects from production data.
2. **Identify the server-side source of truth**: Before attempting to manipulate a value, determine whether the server recalculates it independently. A price that is always looked up from a product catalog is not client-controllable regardless of what the request body contains.
3. **Single minimal proof per test**: Prove the violation once with the smallest possible value (e.g., $0.01 price modification, not $9999). Do not repeat a financially meaningful transaction to "confirm" it — one confirmed instance is sufficient evidence.
4. **Track reversibility**: Before the test, identify how to reverse the change (cancel the order, void the transaction, restore the inventory count). Record the reversal in the change ledger.
5. **Escalate by real impact**: Tests that would create real financial movement (balance changes, actual charges, inventory depletion, coupon consumption at scale), trigger external settlement, or affect non-test users are L3 — require explicit approval.
6. **Concurrent transaction caution**: Race-condition testing that submits simultaneous payment/refund/redemption requests may produce unrecoverable states. Use the lowest-value test resource available and assume the test may produce an irreversible result.

### Step 3: Classify The Attack Surface

Four categories — test in order of expected impact:

#### A. State Machine Abuse

The application allows a transition that the business model should prohibit.

| Pattern | Test | Signal |
|---|---|---|
| **Skip intermediate state** | Call the "completed" endpoint directly after "initiated" (skip "payment_confirmed") — using a test account and test resource | 200 + state changed to an unauthorized target state |
| **Reverse completed state** | From "completed"/"cancelled"/"refunded" → call the "modify" or "reactivate" endpoint | 200 + previously-final state is now mutable |
| **Replay terminal action** | After refund completed → call refund endpoint again with same order ID — use a minimal-value test order | Second refund succeeds, balance mismatch — record the violation, do not repeat to "verify" |
| **Concurrent state conflict** | Send "confirm" and "cancel" simultaneously for the same resource — use a test resource with minimal value | Both succeed, resource enters inconsistent state — do not repeat the test across production resources |
| **State rollback via update** | PUT/PATCH the resource with `{"status":"pending"}` when current status is "completed" | State field in response reflects the injected value |
| **Expired/time-limited state bypass** | Submit action after expiration (expired coupon, ended auction, closed enrollment period) | Action succeeds despite timestamp-based restriction |

#### B. Workflow Bypass

The application enforces a sequence on the client side but not on the server side.

| Pattern | Test | Signal |
|---|---|---|
| **Step enumeration jump** | Workflow uses `step=1`, `step=2`... → call `step=4` directly | Step 4 executes without steps 2-3 completing |
| **API-direct invocation** | The client UI guides through steps A→B→C; call endpoint-C directly | Endpoint-C processes without A and B completing |
| **Callback/manipulation of webhook flow** | Call the callback URL manually with fabricated success data from the payment/shipping provider | Server trusts callback without origin verification |
| **Modify workflow identifier** | Change `workflow_id` or `flow_type` in the request to a different (more permissive) workflow | Server applies rules from a different workflow to this request |

#### C. Semantic Constraint Violation

The application accepts a value that the business model should forbid.

| Pattern | Test | Signal |
|---|---|---|
| **Negative amount** | Set price/amount/quantity to -100 | Refund direction reversed; balance increases instead of decreasing |
| **Zero price** | Set price to 0.00 when server should look it up from product catalog | Order completes at $0 |
| **Integer overflow** | Set quantity to 9999999999 or 2^31+1 | Total price wraps to zero or negative, or validation fails revealing unsafe type |
| **Precision attack** | If the system rounds fractional units, test with a single minimal-value transfer (e.g., 0.009 in a 2-decimal system) and observe the rounding outcome. Document the rounding behavior as an invariant violation — do not repeat to accumulate value | In `round(0.009, 2)` = 0.01, the transfer of 0.009 credits 0.01 — confirm the discrepancy once with the smallest possible unit |
| **Currency unit confusion** | Send amount in cents when server expects dollars (or vice versa) — 100000 becomes $1,000.00 or $1000.00 becomes charged as 1000 cents | Mismatch between client-intended value and server-processed value |
| **Type confusion** | Pass an array `[1,2,3]` where a single integer is expected; pass a JSON object where a string ID is expected | Server coerces the type in an unexpected way, or the error reveals type handling |

#### D. Incentive Abuse

The application limits a benefit, but the limit is client-enforced or identity-based without device/binding checks. **For each pattern, verify the invariant with a single minimal test — do not accumulate value or create chains of dependent accounts.**

| Pattern | Test | Signal (Invariant Verification) |
|---|---|---|
| **Coupon reuse** | Apply the same coupon code to a second test order from the same account — use a 0-value or minimum-value test coupon if available | Server accepts the coupon against a second order. Record the violation once — do not apply to multiple orders to "confirm" |
| **Coupon stacking** | Apply two coupons to a single test order that should be mutually exclusive per the business rules | Server applies both discounts. Record the invariant violation — do not test with high-value combinations |
| **Referral fraud** | Create one test account B referred by account A; verify whether A receives credit without real person referral. Test the minimal referral unit (one referral) — do not create chains | Credit is granted based solely on account creation, not on actual human referral. Record the violation with one referral pair |
| **Trial reuse** | After a test trial expires, attempt to sign up again. Test with a single variant of identity — do not iterate through multiple identity mutations | Second trial is granted. Record the violation — do not verify with additional variants |
| **Loyalty point redemption + refund** | Redeem minimal points for a discount on a test order → request refund. Check: are points returned, or is cash equivalent refunded? Test with the smallest available point increment | Points not returned OR cash refunded at full value. Record the net effect once — do not repeat with larger point amounts |
| **Bulk-action absence** | A single-item operation has a limit. Test whether a bulk operation with one item respects the same limit | Bulk endpoint applies no limit to the single item. Record the discrepancy — do not submit bulk requests at scale |

### Step 3: Platform-Specific Iteration Methods

The same logic flaw manifests differently depending on the calling domain:

| Domain | Iteration Method |
|---|---|
| **Web/API** | Replay requests via Burp/curl; modify hidden form fields and JavaScript-disabled form submissions; alter `step` or `workflow_id` parameters; send concurrent requests via HTTP/2 single-packet attack |
| **Mini-program** | Capture and replay API calls outside the mini-program runtime via standard HTTP client; modify `wx.request` data payloads; test cloud function authorization with modified user identifiers |
| **Mobile** | Replay API calls outside the app via intercepting proxy; modify client-submitted purchase receipts before they reach the backend; test deep-link parameters for workflow state injection |
| **Supply-chain / CI/CD** | Modify pipeline parameters, build arguments, or deployment manifests that the pipeline trusts without validation |

### Failure Branches

| Failure Signal | Likely Cause | Next Variable |
|---|---|---|
| State change rejected with 403/422 | Server validates the state transition — the state machine is correctly enforced for this transition | Test a different state pair (the server may validate some transitions but not all); test concurrent transitions; test with a different role |
| Parameter modification ignored (silent strip) | Server recalculates the value from its own source of truth | This is correct behavior. Record the parameter as not client-controllable. Test: does a different API endpoint for the same resource accept client values? |
| Coupon/limit returns "already used" | The limit is enforced server-side with a reliable identity check | Test: does the identity check have a bypass? (use a variant email, a different device fingerprint, a guest session vs. authenticated session) |
| Workflow step jump returns 404 or redirects | The step endpoint requires intermediate state (e.g., a session variable set by the previous step) | Test: call step 1 (to initialize state), then jump to step 4 without steps 2-3. Some workflows only verify the first step completed |
| Concurrent requests processed sequentially (no race) | Server uses a mutex, queue, or serializable transaction — the race condition is not exploitable at this endpoint | Test a different endpoint handling the same resource; some operations on the same resource may use different locking strategies |
| Bulk endpoint applies same limit as single endpoint | Server enforces per-item limits correctly in bulk operations | Record as defense-in-depth. Test: does the bulk endpoint count toward rate limits the same as single? Can the bulk ordering be used to bypass per-hour limits? |

### Result Interpretation And Parent-Path Return

| Result Class | Signal | Return To Parent Path |
|---|---|---|
| **Confirmed** | A business rule was violated: state transition accepted, negative amount processed, coupon reused, workflow step skipped | Record the exact violation, affected business value, and reproducibility. Rerank the parent path: a confirmed logic flaw often outranks injection opportunities because it bypasses all technical controls |
| **Partial** | A state violation or value manipulation was accepted by one endpoint but blocked by another; or accepted for one role but not another | Record the inconsistency pattern. Inconsistent enforcement is itself a finding when it creates a privilege differential |
| **Ambiguous** | The server accepted the modified request but the business outcome is unclear (no visible balance change, async processing, queued job) | Park with a reactivation condition: monitor for the business outcome; test with a controlled resource whose state you can fully observe |
| **Failure** | Business rules consistently enforced across all tested dimensions | Does NOT prove all workflows are secure. Record which workflows were tested and which were not. Park unreachable workflows |

## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
