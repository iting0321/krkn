# Pod Network Chaos

## Overview

Pod Network Chaos scenario blocks the traffic (Ingress/Egress) of a pod matching the labels for the specified duration of time to understand the behavior of the service/other services which depend on it during downtime. This helps with planning the requirements accordingly, be it improving the timeouts or tweaking the alerts etc. It supports OpenShiftSDN and OVNKubernetes based networks.

## Category

**Network Chaos** - This scenario targets pod-level network disruption using OVS flow rules.

## Use Cases

- Test application resilience during network isolation
- Validate timeout configurations for dependent services
- Verify alerting mechanisms during pod network downtime
- Understand cascading failure behavior in microservices
- Test resiliency while keeping critical monitoring pods operational
- Enable targeted chaos without affecting auxiliary services

## Usage

### Basic Command

```bash
krknctl run pod-network-chaos --namespace <target-namespace>
```

### With Options

```bash
krknctl run pod-network-chaos --namespace <target-namespace> --label-selector "app=myapp" --test-duration 120
```

### View All Options

```bash
krknctl run pod-network-chaos --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--namespace` | Namespace of the pod to which filter need to be applied | string | **Yes** | - |
| `--label-selector` | When pod_name is not specified, pod matching the label will be selected for the chaos scenario | string | No | - |
| `--pod-name` | When label_selector is not specified, pod matching the name will be selected for the chaos scenario | string | No | - |
| `--exclude-label` | Pods matching this label will be excluded from the chaos even if they match other criteria | string | No | "" |
| `--traffic-type` | List of directions to apply filters - egress/ingress (needs to be a list) | string | No | `[ingress,egress]` |
| `--ingress-ports` | Ingress ports to block (needs to be a list) | string | No | - |
| `--egress-ports` | Egress ports to block (needs to be a list) | string | No | - |
| `--test-duration` | Duration of the test run (in seconds) | number | No | 120 |
| `--wait-duration` | Ensure that it is at least about twice of test_duration | number | No | 300 |
| `--instance-count` | Targeted instance count matching the label selector | number | No | 1 |
| `--image` | Image used to disrupt network on a pod | string | No | quay.io/krkn-chaos/krkn:tools |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Block All Traffic for Pods with Label Selector

```bash
krknctl run pod-network-chaos --namespace my-application --label-selector "app=my-service" --test-duration 120
```

### Block Only Ingress Traffic on Specific Ports

```bash
krknctl run pod-network-chaos --namespace openshift-console --label-selector "component=ui" --traffic-type "[ingress]" --ingress-ports "[8443]" --test-duration 600
```

### Exclude Critical Pods from Chaos

```bash
krknctl run pod-network-chaos --namespace my-application --label-selector "app=my-service" --exclude-label "critical=true" --traffic-type "[egress]" --test-duration 600
```

### Target a Specific Pod by Name

```bash
krknctl run pod-network-chaos --namespace my-application --pod-name "my-pod-abc123" --traffic-type "[ingress,egress]" --test-duration 300
```

## Tips

- Use `--exclude-label` to preserve critical monitoring or control plane pods during chaos testing
- Set `--wait-duration` to at least twice of `--test-duration` for proper cleanup
- Use specific ports with `--ingress-ports` or `--egress-ports` for more targeted testing

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/pod-network-scenario/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/pod-network-scenario/pod-network-chaos-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)

