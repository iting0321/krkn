# Node Memory Hog

## Overview

The Memory Hog scenario creates virtual memory pressure on one or more nodes in your Kubernetes/OpenShift cluster for a specified duration. This scenario deploys stress workload pods using stress-ng to allocate and consume memory resources.

## Category

**Node-Level Chaos** - This scenario targets node memory resources to test cluster behavior under memory pressure.

## Use Cases

- Test cluster's behavior under memory pressure
- Validate memory resource limits and quotas
- Test pod eviction policies when nodes run out of memory
- Verify kubelet correctly evicts pods based on memory pressure
- Evaluate impact of memory contention on application performance
- Test monitoring systems for memory saturation detection
- Simulate rogue pods consuming excessive memory without limits
- Validate memory-based horizontal pod autoscaling

## Usage

### Basic Command

```bash
krknctl run node-memory-hog
```

### With Options

```bash
krknctl run node-memory-hog --node-selector "node-role.kubernetes.io/worker" --memory-consumption "80%" --chaos-duration 120
```

### View All Options

```bash
krknctl run node-memory-hog --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--chaos-duration` | Duration of the stress test (seconds) | number | No | 60 |
| `--memory-workers` | Total number of stress-ng workers (threads) | number | No | 1 |
| `--memory-consumption` | Memory to consume (% or absolute: b, k, m, g) | string | No | 90% |
| `--namespace` | Namespace where scenario container will be deployed | string | No | default |
| `--node-selector` | Node selector in format "key=value" | string | No | (random node) |
| `--taints` | List of taints for tolerations | string | No | [] |
| `--number-of-nodes` | Restricts number of selected nodes | number | No | - |
| `--image` | Hog container image | string | No | quay.io/krkn-chaos/krkn-hog |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Consume 80% Memory on Worker Nodes

```bash
krknctl run node-memory-hog --node-selector "node-role.kubernetes.io/worker" --memory-consumption "80%" --chaos-duration 120
```

### Consume 2GB of Memory

```bash
krknctl run node-memory-hog --memory-consumption "2g" --chaos-duration 300
```

### Consume 512MB with Multiple Workers

```bash
krknctl run node-memory-hog --memory-consumption "512m" --memory-workers 4
```

## Rollback Support

Krkn supports rollback for Memory Hog scenarios. For more details, refer to the [Rollback Scenarios](https://krkn-chaos.dev/docs/rollback-scenarios/) documentation.

## Tips

- Memory consumption can be expressed as percentage (%) or absolute units (b, k, m, g)
- Monitor for OOM (Out of Memory) events and pod evictions during the test

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/hog-scenarios/memory-hog-scenario/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/hog-scenarios/memory-hog-scenario/memory-hog-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
