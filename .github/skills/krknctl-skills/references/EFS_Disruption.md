# EFS Disruption

## Overview

This scenario creates an outgoing firewall rule on specific nodes in your cluster, chosen by node name or a selector. This rule blocks connections to AWS EFS (Elastic File System), leading to a temporary failure of any EFS volumes mounted on those affected nodes. It uses the node network filter scenario configured to block NFS port 2049.

## Category

**Cloud Provider Specific (AWS)** - This scenario targets AWS EFS storage connectivity at the node level.

## Use Cases

- Test application resilience when EFS storage becomes unreachable
- Validate application behavior during shared storage outages
- Verify failover mechanisms for stateful applications using EFS
- Test pod behavior when persistent volumes become unavailable
- Understand recovery patterns after EFS connectivity is restored

## Usage

### Basic Command

```bash
krknctl run node-network-filter --node-name <target-node> --egress true --protocols tcp,udp --ports 2049
```

### With Options

```bash
krknctl run node-network-filter --chaos-duration 60 --node-name <target-node> --ingress false --egress true --protocols tcp,udp --ports 2049
```

### View All Options

```bash
krknctl run node-network-filter --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--node-name` | Name of the target node to disrupt | string | **Yes** | - |
| `--chaos-duration` | Duration of the chaos test (in seconds) | number | No | 60 |
| `--ingress` | Block incoming traffic | boolean | No | false |
| `--egress` | Block outgoing traffic | boolean | No | true |
| `--protocols` | Network protocols to block (tcp,udp for NFS) | string | No | tcp,udp |
| `--ports` | Ports to block (2049 for NFS/EFS) | string | No | 2049 |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Block EFS Connection on a Specific Node for 60 Seconds

```bash
krknctl run node-network-filter --chaos-duration 60 --node-name worker-node-1 --ingress false --egress true --protocols tcp,udp --ports 2049
```

### Block EFS on Control Plane Node

```bash
krknctl run node-network-filter --chaos-duration 60 --node-name kind-control-plane --ingress false --egress true --protocols tcp,udp --ports 2049
```

### Block EFS for a Longer Duration

```bash
krknctl run node-network-filter --chaos-duration 300 --node-name worker-node-1 --ingress false --egress true --protocols tcp,udp --ports 2049
```

## Tips

- EFS uses NFS port 2049 on both TCP and UDP protocols
- Set `--ingress false` and `--egress true` to specifically block outgoing NFS connections
- This affects all pods running on the targeted node that use EFS volumes
- Consider testing on worker nodes first before targeting control plane nodes

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/efs-disruption/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/efs-disruption/efs-disruption-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)

