# Network Chaos

## Overview

Network Chaos scenario introduces network disruptions such as latency, packet loss, and bandwidth restriction on cluster nodes. This helps test the resilience of your applications and services under degraded network conditions, simulating real-world network issues that can affect distributed systems.

## Category

**Node & Network Chaos** - This scenario targets node-level network disruption including latency, packet loss, and bandwidth limitations.

## Use Cases

- Test application resilience under network latency conditions
- Validate service behavior during packet loss scenarios
- Verify application performance with bandwidth restrictions
- Simulate network degradation between cluster nodes
- Test microservice communication under adverse network conditions
- Validate timeout and retry logic in distributed systems

## Usage

### Basic Command

```bash
krknctl run network-chaos
```

### With Options

```bash
krknctl run network-chaos --label-selector "node-role.kubernetes.io/worker" --duration 300 --egress "{latency: 100ms}"
```

### View All Options

```bash
krknctl run network-chaos --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--traffic-type` | Selects the network chaos scenario type (ingress or egress) | enum | No | ingress |
| `--image` | Image used to disrupt network on a pod | string | No | quay.io/krkn-chaos/krkn:tools |
| `--duration` | Duration in seconds during which network chaos will be applied | number | No | 300 |
| `--label-selector` | When NODE_NAME is not specified, a node with matching label_selector is selected | string | No | node-role.kubernetes.io/master |
| `--execution` | Execute each egress option as parallel or serial | enum | No | parallel |
| `--node-name` | Node name to inject faults (can set multiple separated by comma) | string | No | - |
| `--interfaces` | List of interfaces to apply network restriction (e.g., [eth0,eth1]) | string | No | - |
| `--egress` | Network parameters: latency, packet loss, bandwidth (e.g., {bandwidth: 100mbit}) | string | No | "{bandwidth: 100mbit}" |
| `--target-node-interface` | Dictionary with node name(s) and list of interfaces | string | No | - |
| `--network-params` | Network parameters to alter (e.g., {latency: 50ms, loss: 0.02}) | string | No | - |
| `--wait-duration` | Wait duration (should be at least twice test_duration) | number | No | 300 |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Add Network Latency to Worker Nodes

```bash
krknctl run network-chaos --label-selector "node-role.kubernetes.io/worker" --egress "{latency: 100ms}" --duration 300
```

### Introduce Packet Loss on Specific Node

```bash
krknctl run network-chaos --node-name "worker-node-1" --egress "{loss: 0.05}" --duration 180
```

### Restrict Bandwidth on Master Nodes

```bash
krknctl run network-chaos --label-selector "node-role.kubernetes.io/master" --egress "{bandwidth: 50mbit}" --duration 600
```

### Combined Network Disruption

```bash
krknctl run network-chaos --node-name "worker-node-1,worker-node-2" --network-params "{latency: 50ms, loss: 0.02, bandwidth: 100mbit}"
```

## Rollback Support

Krkn supports rollback for Network Chaos scenarios. For more details, refer to the [Rollback Scenarios](https://krkn-chaos.dev/docs/rollback-scenarios/) documentation.

## Tips

- Ensure wait-duration is at least twice the test duration for proper cleanup
- Start with lower disruption values and gradually increase to identify thresholds
- Monitor your applications during chaos to identify weaknesses

## Documentation

- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/network-chaos-scenario/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/network-chaos-scenario/network-chaos-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
