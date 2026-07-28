# Cloud, Container, Kubernetes, And SaaS Operations: Attack Primitives: Serverless

> Apply [../module-continuity.md](../module-continuity.md). Inherit the engagement, parent path, current capability, evidence, authorization profile, and module stack. Do not initialize a separate workflow. Checkpoint material results and return them to the parent path before leaving this card.

## Attack Primitives: Serverless

### Lambda / Azure Function / Cloud Function Exploitation

Serverless functions are single-purpose code running with a specific IAM role. Common attack vectors:

1. **Insecure function triggers**: HTTP API Gateway, S3 events, DynamoDB streams, SNS/SQS, CloudWatch Events, Cognito events, IoT events. Can you invoke a function via an unauthenticated or low-privileged trigger?
2. **Event injection**: If an S3 upload triggers a Lambda, and you can upload to that S3 bucket → you control the event passed to the Lambda → exploit processing logic
3. **Dependency hijacking**: Functions often import libraries. Can you publish a malicious version to the package registry the function pulls from?
4. **Environment variables**: Function env vars often contain database credentials, API keys, and other secrets. Extract them if you can invoke or modify the function.
5. **Unused/old versions**: Lambda versions are immutable. Old versions may still be invocable via aliases or directly — and may have more vulnerable code or broader permissions.

```bash
# AWS Lambda — list functions and extract env
aws lambda list-functions --query 'Functions[*].[FunctionName,Role,Environment]'
aws lambda get-function --function-name <name>
aws lambda invoke --function-name <name> --payload '{"key":"value"}' output.txt

# Check if function URL (public invocation) exists
aws lambda list-function-url-configs --function-name <name>
```

---


## Card Exit

Classify the result, update evidence and attempted methods, record capability or risk changes, identify affected paths, and apply the return contract in [../module-continuity.md](../module-continuity.md).
