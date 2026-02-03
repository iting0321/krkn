# Container Failures

## Overview

Container scenario uses the `kill` command to terminate specific containers within a pod. This can target containers based on namespace, labels, container name, or pod name. This scenario tests how applications recover from container-level failures without disrupting the entire pod.

## Category

**Pod & Container Chaos** - This scenario targets container-level disruptions within pods.

## Use Cases

- Test container restart behavior within a pod
- Validate init container dependencies
- Verify sidecar container resilience
- Test application recovery from individual container crashes
- Measure container restart timing

## Usage

### Basic Command

```bash
krknctl run container-scenarios --namespace <target-namespace>
```

### With Options

```bash
krknctl run container-scenarios --namespace <target-namespace> --label-selector "app=myapp" --container-name "main"
```

### View All Options

```bash
krknctl run container-scenarios --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--namespace` | Targeted namespace in the cluster | string | No | openshift-etcd |
| `--label-selector` | Label of the container(s) to target | string | No | k8s-app=etcd |
| `--exclude-label` | Label of pod/container to exclude. Example: `"app=foo"` | string | No | False |
| `--disruption-count` | Number of containers to disrupt | number | No | 1 |
| `--container-name` | Name of the container to disrupt | string | No | etcd |
| `--action` | Kill signal to run. Example: `1` (hang up) or `9` (kill) | string | No | 1 |
| `--expected-recovery-time` | Time to wait before checking if containers recover properly | number | No | 60 |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Kill etcd Container

```bash
krknctl run container-scenarios --namespace openshift-etcd --label-selector "k8s-app=etcd" --container-name etcd
```

### Kill Container with SIGKILL (Signal 9)

```bash
krknctl run container-scenarios --namespace production --label-selector "app=api" --container-name main --action 9
```

### Kill Multiple Containers

```bash
krknctl run container-scenarios --namespace production --label-selector "tier=backend" --disruption-count 3
```

### Exclude Monitoring Containers

```bash
krknctl run container-scenarios --namespace production --label-selector "app=backend" --exclude-label "component=monitoring"
```

## Rollback Support

Krkn supports rollback for Container scenarios. For more details, refer to the [Rollback Scenarios](https://krkn-chaos.dev/docs/rollback-scenarios/) documentation.

## Tips

- Krkn tracks recovery metrics including `pod_rescheduling_time`, `pod_readiness_time`, and `total_recovery_time`
- Container kills may not always cause full pod rescheduling, so `pod_rescheduling_time` may be 0.0 seconds

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/container-scenario/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/container-scenario/container-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
