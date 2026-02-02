# Application Outages

## Overview

Application Outage scenario blocks the traffic (Ingress/Egress) of an application matching the specified labels for a defined duration. This helps you understand the behavior of your service and dependent services during downtime, enabling better planning for requirements such as improving timeouts or tweaking alerts.

## Category

**Pod & Container Chaos** - This scenario targets application-level network isolation.

## Use Cases

- Test application resilience during network isolation
- Validate timeout configurations for dependent services
- Verify alerting mechanisms during application downtime
- Understand cascading failure behavior in microservices
- Plan disaster recovery and failover strategies

## Usage

### Basic Command

```bash
krknctl run application-outages --namespace <target-namespace>
```

### With Options
Based on your requirements, you can customize the command with various options. Here’s an example that targets specific pods and sets a custom chaos duration:

```bash
krknctl run application-outages --namespace <target-namespace> --pod-selector "{app: myapp}" --chaos-duration 300
```

### View All Options

```bash
krknctl run application-outages --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--namespace` | Namespace to target - all application routes will become inaccessible if pod selector is empty | string | **Yes** | - |
| `--chaos-duration` | Set chaos duration (in seconds) | number | No | 600 |
| `--pod-selector` | Pods to target. Example: `"{app: foo}"` | string | No | - |
| `--exclude-label` | Pods to exclude after using pod-selector. Example: `"{app: foo}"` | string | No | - |
| `--block-traffic-type` | Traffic type to block: `[Ingress]`, `[Egress]`, or `[Ingress, Egress]` | string | No | `[Ingress, Egress]` |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Block All Traffic in a Namespace

```bash
krknctl run application-outages --namespace my-application
```

### Target Specific Pods with Label Selector

```bash
krknctl run application-outages --namespace my-application --pod-selector "{app: frontend}"
```

### Block Only Ingress Traffic for 5 Minutes

```bash
krknctl run application-outages --namespace my-application --pod-selector "{app: api}" --block-traffic-type "[Ingress]" --chaos-duration 300
```

### Exclude Certain Pods from Chaos

```bash
krknctl run application-outages --namespace my-application --pod-selector "{tier: backend}" --exclude-label "{critical: true}"
```

## Rollback Support

Krkn supports rollback for Application Outages. For more details, refer to the [Rollback Scenarios](https://krkn-chaos.dev/docs/rollback-scenarios/) documentation.

## Tips

- Add your application's URL to the health checks section of the config to track downtime during this scenario

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/application-outage/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/application-outage/application-outage-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
