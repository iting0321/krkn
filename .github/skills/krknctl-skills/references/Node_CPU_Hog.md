# Node CPU Hog

## Overview

The CPU Hog scenario creates CPU pressure on one or more nodes in your Kubernetes/OpenShift cluster for a specified duration. This scenario deploys stress workload pods using stress-ng to consume CPU resources according to your configuration.

## Category

**Node-Level Chaos** - This scenario targets node CPU resources to test cluster behavior under CPU pressure.

## Use Cases

- Test cluster's ability to handle CPU resource contention
- Validate CPU resource limits and quotas are properly configured
- Evaluate impact of CPU pressure on application performance
- Test monitoring and alerting systems for CPU saturation
- Verify Kubernetes scheduler handling of CPU-constrained nodes
- Simulate rogue pods consuming excessive CPU without limits

## Usage

### Basic Command

```bash
krknctl run node-cpu-hog
```

### With Options

```bash
krknctl run node-cpu-hog --node-selector "node-role.kubernetes.io/worker" --cpu-percentage 80 --chaos-duration 120
```

### View All Options

```bash
krknctl run node-cpu-hog --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--chaos-duration` | Duration of the stress test (seconds) | number | No | 60 |
| `--cores` | Number of CPU cores (workers) to consume | number | No | (all available) |
| `--cpu-percentage` | Percentage of total CPU to consume | number | No | 50 |
| `--namespace` | Namespace where scenario container will be deployed | string | No | default |
| `--node-selector` | Node selector in format "key=value" | string | No | (random node) |
| `--taints` | List of taints for tolerations. Example: `["node-role.kubernetes.io/master:NoSchedule"]` | string | No | [] |
| `--number-of-nodes` | Restricts number of selected nodes | number | No | - |
| `--image` | Hog container image | string | No | quay.io/krkn-chaos/krkn-hog |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Consume 80% CPU on Worker Nodes

```bash
krknctl run node-cpu-hog --node-selector "node-role.kubernetes.io/worker" --cpu-percentage 80 --chaos-duration 120
```

### Stress All CPU Cores for 5 Minutes

```bash
krknctl run node-cpu-hog --cpu-percentage 100 --chaos-duration 300
```

### Target Master Nodes with Taints

```bash
krknctl run node-cpu-hog --node-selector "node-role.kubernetes.io/master" --taints '["node-role.kubernetes.io/master:NoSchedule"]' --cpu-percentage 70
```

## Rollback Support

Krkn supports rollback for CPU Hog scenarios. For more details, refer to the [Rollback Scenarios](https://krkn-chaos.dev/docs/rollback-scenarios/) documentation.

## Tips

- If `--node-selector` is not specified, a random schedulable node will be selected
- Multiple nodes matching the selector will all be subjected to stress

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/hog-scenarios/cpu-hog-scenario/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/hog-scenarios/cpu-hog-scenario/cpu-hog-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
