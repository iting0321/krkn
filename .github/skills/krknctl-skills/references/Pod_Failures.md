# Pod Failures

## Overview

Pod scenario disrupts pods matching the label, excluded label, or pod name in the specified namespace on a Kubernetes/OpenShift cluster. This scenario helps validate whether ReplicaSets or Deployments automatically create replacements and ensures continuous service availability.

## Category

**Pod & Container Chaos** - This scenario targets pod-level disruptions to test application resilience.

## Use Cases

- Simulate unplanned deletion of single or multiple pods
- Validate automatic pod rescheduling by ReplicaSet/Deployment
- Test pod eviction during node upgrades or scaling
- Verify readiness/liveness probes and PodDisruptionBudgets (PDBs)
- Measure pod recovery timing and scheduling efficiency

## Usage

### Basic Command

```bash
krknctl run pod-scenarios --namespace <target-namespace>
```

### With Options

```bash
krknctl run pod-scenarios --namespace <target-namespace> --pod-label "app=myapp" --disruption-count 2
```

### View All Options

```bash
krknctl run pod-scenarios --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--namespace` | Targeted namespace in the cluster (supports regex) | string | No | openshift-* |
| `--pod-label` | Label of the pod(s) to target. Example: `"app=test"` | string | No | - |
| `--exclude-label` | Pods matching this label will be excluded from chaos | string | No | "" |
| `--name-pattern` | Regex pattern to match pods when pod-label is not specified | string | No | .* |
| `--disruption-count` | Number of pods to disrupt | number | No | 1 |
| `--kill-timeout` | Timeout to wait for the target pod(s) to be removed (seconds) | number | No | 180 |
| `--expected-recovery-time` | Fails if pods do not recover within this timeout | number | No | 120 |
| `--node-label-selector` | Label of the node(s) to target | string | No | "" |
| `--node-names` | Name of the node(s) to target. Example: `["worker-1","worker-2"]` | string | No | [] |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Kill Pods by Label

```bash
krknctl run pod-scenarios --namespace production --pod-label "app=backend" --disruption-count 1
```

### Kill Multiple Pods Simultaneously

```bash
krknctl run pod-scenarios --namespace production --pod-label "tier=frontend" --disruption-count 3
```

### Exclude Critical Pods

```bash
krknctl run pod-scenarios --namespace production --pod-label "app=backend" --exclude-label "critical=true"
```

### Target Pods on Specific Nodes

```bash
krknctl run pod-scenarios --namespace production --node-label-selector "node-role.kubernetes.io/worker"
```

## Rollback Support

Krkn supports rollback for Pod scenarios. For more details, refer to the [Rollback Scenarios](https://krkn-chaos.dev/docs/rollback-scenarios/) documentation.

## Tips

- Krkn tracks recovery metrics including `pod_rescheduling_time`, `pod_readiness_time`, and `total_recovery_time`
- Use `--exclude-label` to protect critical pods like database leaders or monitoring components

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/pod-scenario/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/pod-scenario/pod-scenarios-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
