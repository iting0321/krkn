# Node IO Hog

## Overview

The IO Hog scenario creates disk I/O pressure on one or more nodes in your Kubernetes/OpenShift cluster for a specified duration. This scenario deploys stress workload pods using stress-ng to perform intensive write operations to disk.

## Category

**Node-Level Chaos** - This scenario targets node disk I/O resources to test cluster behavior under I/O pressure.

## Use Cases

- Test cluster's behavior under disk I/O pressure
- Validate I/O resource limits are properly configured
- Evaluate impact of disk I/O contention on application performance
- Test monitoring systems for disk saturation detection
- Verify storage performance meets requirements under stress
- Simulate pods performing excessive disk writes
- Test resilience of persistent volume configurations
- Validate disk I/O quotas and rate limiting

## Usage

### Basic Command

```bash
krknctl run node-io-hog
```

### With Options

```bash
krknctl run node-io-hog --node-selector "node-role.kubernetes.io/worker" --io-write-bytes "50%" --chaos-duration 120
```

### View All Options

```bash
krknctl run node-io-hog --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--chaos-duration` | Duration of the stress test (seconds) | number | No | 60 |
| `--io-block-size` | Size of each write (suffix: b, k, m) | string | No | 1m |
| `--io-workers` | Number of stressor instances | number | No | 5 |
| `--io-write-bytes` | Data to write (% of free space or units: b, k, m, g) | string | No | 10m |
| `--node-mount-path` | Path in node to mount in pod for I/O operations | string | No | /root |
| `--namespace` | Namespace where scenario container will be deployed | string | No | default |
| `--node-selector` | Node selector in format "key=value" | string | No | (random node) |
| `--taints` | List of taints for tolerations | string | No | [] |
| `--number-of-nodes` | Restricts number of selected nodes | number | No | - |
| `--image` | Hog container image | string | No | quay.io/krkn-chaos/krkn-hog |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Write 50% of Free Disk Space

```bash
krknctl run node-io-hog --node-selector "node-role.kubernetes.io/worker" --io-write-bytes "50%" --chaos-duration 120
```

### Write 10GB with 1MB Blocks

```bash
krknctl run node-io-hog --io-write-bytes "10g" --io-block-size "1m" --io-workers 10
```

### Write with Small Block Size (4KB)

```bash
krknctl run node-io-hog --io-block-size "4k" --io-write-bytes "1g" --chaos-duration 300
```

## Rollback Support

Krkn supports rollback for IO Hog scenarios. For more details, refer to the [Rollback Scenarios](https://krkn-chaos.dev/docs/rollback-scenarios/) documentation.

## Tips

- Ensure kubelet has write permissions to the `--node-mount-path`
- Block size affects I/O pattern: smaller blocks = more IOPS, larger blocks = higher throughput

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/hog-scenarios/io-hog-scenario/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/hog-scenarios/io-hog-scenario/io-hog-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
