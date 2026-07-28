# Internal Network, Host, And Identity Operations: Active Directory Certificate Services (AD CS) Attack Primitives

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Active Directory Certificate Services (AD CS) Attack Primitives

AD CS is one of the most common AD privilege escalation surfaces. A certificate with a suitable EKU, correct subject or SAN-to-principal mapping, and a trusted issuance chain may authenticate the mapped principal via PKINIT or other certificate-based mechanisms. Whether a particular certificate enables impersonation depends on template configuration, CA issuance policy, certificate mapping mode, DC support, and current patching — not on certificate existence alone.

### Authorization Levels

| Level | Scope | Examples |
|---|---|---|
| **L1** | Read-only enumeration of CA, templates, and enrollment rights | `certipy find`, `Certify.exe find /vulnerable` |
| **L2** | Certificate enrollment using an existing identity with legitimate enrollment rights on a non-privileged template | Requesting a certificate that does not impersonate another principal or grant elevated privilege |
| **L2→L3 boundary** | Enrollment on a template that enables impersonation of a higher-privileged identity, even without modifying CA or template configuration — authorization depends on the actual impact and the engagement's authorization profile | ESC1 enrollment as Domain Admin, ESC3 enrollment-agent chaining |
| **L3** | Modification of templates, CA settings, enrollment permissions, issuance policies, or extraction of CA private key material | ESC4, ESC5, ESC6, ESC7 (CA-level), ESC12, key extraction |

### ESC Classification Reference

Treat ESC identifiers as versioned research labels, not protocol constants. Record the taxonomy/tool version used for a finding and judge the underlying rights, configuration, mapping behavior, and capability when labels differ.

| ESC | Required Rights | Template/CA Conditions | Enrollment Conditions | Identity Mapping Conditions | Capability Gained | Control-Plane Change? |
|---|---|---|---|---|---|
| **ESC1** | Enrollment right on the template | Template has `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`; EKU suitable for domain authentication (Client Authentication, Smart Card Logon, PKINIT Client Authentication, or Any Purpose); CA is configured to issue the template | Enrollee can supply an arbitrary Subject Alternative Name (SAN) in the certificate request | The SAN maps to a domain principal via the CA's certificate mapping method; strong certificate mapping (SID extension) and `CT_FLAG_NO_SECURITY_EXTENSION` absence may block arbitrary SAN mapping | Certificates authenticate as the SAN-specified principal | No — uses existing template and CA configuration |
| **ESC2** | Enrollment right on the template | Template has Any Purpose EKU or no EKU restriction | Enrollee can obtain the certificate under the existing template; do not assume the requester can add a new EKU | Authentication still requires a consumer that accepts the certificate purpose and a valid principal-mapping path | Broad-use certificate whose actual capability must be validated against the intended consumer | No |
| **ESC3** | Enrollment Agent certificate + enrollment right on a target template | An Enrollment Agent template the principal can enroll in; a target authentication template that permits enrollment-on-behalf-of and maps to a higher-privileged identity | Enroll in the Enrollment Agent template, then use it to sign a certificate request for another principal | The target template must accept agent-signed requests; the requested principal must be mappable | Certificate authenticates as the requested target principal | No when agent templates already exist |
| **ESC4** | Write permission over a certificate template object — may be GenericAll, GenericWrite, WriteDacl, WriteOwner, or WriteProperty on the template's AD object | The writable template is or can be modified to become vulnerable (add SAN-supply, add authentication EKU, remove security extension requirements) | After modification, the enrollee must have or obtain enrollment rights on the now-dangerous template | Depends on the modifications made to the template | Varies — up to full impersonation of any principal if ESC1 conditions are created | **Yes — L3** (template modification is a control-plane change affecting all current and future enrollees) |
| **ESC5** | Control over the PKI/CA infrastructure — may include access to the CA server host, the CA's AD objects, the CA's RPC/DCOM interfaces, or privileged CA service accounts | The specific control path determines what can be changed — host admin access differs from CA object ACL abuse | N/A — the attacker controls the CA rather than enrolling through it | Depends on the specific control obtained | May range from certificate issuance, to configuration changes, to CA private key extraction — depends on the control path | **Yes — L3** |
| **ESC6** | Enrollment right on a suitable template; CA already has `EDITF_ATTRIBUTESUBJECTALTNAME2` set | The existing flag permits SAN attributes in requests beyond normal template subject controls | Enrollee supplies a SAN and completes enrollment | Strong mapping and SID security extensions can prevent the requested SAN from mapping to another principal | Potential impersonation subject to mapping enforcement | No when only using an existing flag; enabling or changing the flag is an **L3** CA configuration change |
| **ESC7** | `ManageCA` or `ManageCertificates` permission on the CA | `ManageCA` allows modifying CA configuration (flags, templates, security). `ManageCertificates` allows approving pending certificate requests and managing issued certificates | With `ManageCertificates`: an enrollee submits a request that requires approval; the holder approves it | Same mapping conditions as the underlying template | Depends on the underlying template and the specific permission held; `ManageCA` alone does not grant the ability to approve pending requests (that requires `ManageCertificates`) | **Yes — L3** for both `ManageCA` and `ManageCertificates` usage |
| **ESC8** | Network position to coerce or intercept NTLM authentication to the CA; AD CS HTTP Web Enrollment or Certificate Enrollment Service (CES) endpoint reachable; the relayed principal has enrollment rights on at least one template | The enrollment endpoint accepts NTLM authentication; Extended Protection for Authentication (EPA) and channel binding are not enforced; the target template does not require the principal to sign the CSR with a private key | The relayed NTLM authentication is used to enroll in a template as the relayed principal | The certificate authenticates as the relayed principal via normal mapping | Certificate authenticates as the coerced principal | No — uses existing templates and configuration |
| **ESC9** | Enrollment on a template without the SID security extension plus control over a target account attribute used by weak mapping | DC mapping mode permits fallback when the certificate lacks the strong SID extension | Modify only the evidence-supported target attribute, enroll, validate mapping, and restore the attribute under L3 change tracking | The modified account attribute and certificate identity must resolve through the enabled weak mapping method | Potential authentication as the controlled target account | Account-attribute modification is **L3**; certificate enrollment alone does not prove the chain |
| **ESC10** | Control over a target account attribute and a DC configured for a weak certificate mapping method | The specific mapping method and patch state accept an attribute-based mapping without strong SID binding | Build the path around the exact enabled mapping rule; do not infer it from Issuer/Subject similarity alone | Certificate fields and target account attributes must satisfy that rule | Potential authentication as the target account | Existing weak configuration may be used without CA change, but target-account or registry changes are **L3** |
| **ESC11** | NTLM relay position to the CA's RPC certificate enrollment interface (`ICertPassage` via DCOM) | `IF_ENFORCEENCRYPTICERTREQUEST` is not set on the CA — the RPC enrollment interface does not require encryption | The relayed NTLM authentication is used for RPC-based certificate enrollment as the relayed principal | Same mapping conditions as the underlying template | Certificate authenticates as the coerced principal | No |
| **ESC12** | Capability defined by the selected taxonomy/tool version, commonly involving CA-host access and protected CA key material | Verify software-backed versus hardware-backed key storage, provider/HSM behavior, and the exact local privilege before claiming key access | Validate only the bounded capability authorized for the CA host; do not infer exportability from shell access alone | Result depends on whether usable signing operations or key material are actually obtained | Potential CA signing capability or key compromise, only when independently demonstrated | **L3**; cite the taxonomy version and concrete capability rather than relying on the ESC number |
| **ESC13** | Enrollment right on a template linked to an issuance policy OID; the OID is linked to a privileged AD group | Template has an issuance policy OID configured; the OID is mapped (via `msDS-OIDToGroupLink`) to a privileged AD group | Enrollee successfully enrolls in the template | The issued certificate grants membership in the linked AD group at the time of authentication | Certificate grants group membership in addition to the enrollee's existing groups | No when the OID link already exists |

### Path Selection

Rank AD CS paths by current evidence rather than by ESC number:

- **Evidence for**: enrollment rights discovered on a specific template; template configuration visible; CA flag status known; mapping mode identified; known-coercible principals within network reach.
- **Evidence against**: EPA enforced on HTTP endpoints; SID extension required; strong mapping enforced on patched DCs; no enrollment rights on any template; no CA endpoint reachable.
- Select the path whose prerequisites are most supported by current evidence and whose verification cost is lowest. ESC1 and ESC8 are common, but do not override a shorter, evidence-supported path on another ESC.

### Primary ESC Tooling

```bash
# Enumerate AD CS environment
certipy find -u <user>@<domain> -p <password> -dc-ip <dc_ip> -vulnerable
# Request certificate (ESC1 example)
certipy req -u <user>@<domain> -p <password> -ca <ca_name> -target <ca_host> \
  -template <vulnerable_template> -upn <target_user>@<domain>
# Authenticate with obtained certificate
certipy auth -pfx <target_user>.pfx -dc-ip <dc_ip>
```

```powershell
# Windows: Certify
Certify.exe find /vulnerable
Certify.exe request /ca:<ca_server>\<ca_name> /template:<template> /altname:<target_user>@<domain>
```

### Failure Branches

| Failure | Likely Cause | Next Variable |
|---|---|---|
| `certipy find` returns no CA or no vulnerable templates | No AD CS deployed, or the current user lacks read access to the CA and Enrollment Services containers | Verify CA existence via `certutil -dump` on a reachable CA host; check LDAP permissions to `CN=Enrollment Services,CN=Public Key Services` |
| Template appears vulnerable but enrollment fails with `CERTSRV_E_TEMPLATE_DENIED` | The template's ACL does not grant enrollment rights to the calling principal or its groups | Enumerate the template's ACL; check whether a group the user belongs to has enrollment rights; try a different template |
| Certificate obtained but PKINIT fails with `KDC_ERR_CLIENT_NAME_MISMATCH` | The requested UPN/SAN does not map to a valid domain account, or the DC enforces strong mapping via SID extension | Verify the target UPN is a valid domain user; check whether the principal is protected (AdminSDHolder, sAMAccountName spoofing mitigations); try a non-privileged target user first to confirm the chain works |
| Certificate obtained but the resulting TGT has unexpected or limited group membership | The target principal's group membership limits privilege — the certificate authenticates the identity but does not grant group membership beyond what the principal has (unless ESC13 applies) | Document the effective privilege of the obtained identity; if it does not escalate, the path may be a dead end unless a higher-privileged target is available |
| ESC8 NTLM relay to HTTP endpoint fails with authentication error or connection refused | EPA enforced on the CA's IIS endpoint (channel binding); or the HTTP enrollment endpoint is not reachable; or the relayed principal lacks enrollment rights | Check whether non-HTTP enrollment endpoints (RPC, per ESC11) are reachable; if EPA is enforced and no unauthenticated enrollment path exists, ESC8 is blocked |


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
