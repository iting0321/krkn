# DNS Outages

## Overview

This scenario blocks all outgoing DNS traffic from a specific pod, effectively preventing it from resolving any hostnames or service names. This uses the pod network filter scenario configured to block DNS port 53 on both TCP and UDP protocols.

## Category

**Network Chaos** - This scenario targets DNS resolution at the pod level.

## Use Cases

- Test application resilience when DNS resolution fails
- Validate DNS caching behavior and TTL configurations
- Verify fallback mechanisms when service discovery is unavailable
- Test circuit breaker patterns for DNS-dependent operations
- Understand application behavior during DNS infrastructure outages

## Usage

### Basic Command

```bash
krknctl run pod-network-filter --pod-name <target-pod> --egress true --protocols tcp,udp --ports 53
```

### With Options

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name <target-pod> --ingress false --egress true --protocols tcp,udp --ports 53
```

### View All Options

```bash
krknctl run pod-network-filter --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--pod-name` | Name of the target pod to disrupt | string | **Yes** | - |
| `--chaos-duration` | Duration of the chaos test (in seconds) | number | No | 60 |
| `--ingress` | Block incoming traffic | boolean | No | false |
| `--egress` | Block outgoing traffic | boolean | No | true |
| `--protocols` | Network protocols to block (tcp,udp for DNS) | string | No | tcp,udp |
| `--ports` | Ports to block (53 for DNS) | string | No | 53 |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Block DNS Resolution for 60 Seconds

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name my-app-pod --ingress false --egress true --protocols tcp,udp --ports 53
```

### Block DNS for a Longer Duration

```bash
krknctl run pod-network-filter --chaos-duration 300 --pod-name my-app-pod --ingress false --egress true --protocols tcp,udp --ports 53
```

### Block DNS for Multiple Pods (run separately)

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name frontend-pod --ingress false --egress true --protocols tcp,udp --ports 53
krknctl run pod-network-filter --chaos-duration 60 --pod-name backend-pod --ingress false --egress true --protocols tcp,udp --ports 53
```

## Tips

- DNS uses port 53 on both TCP and UDP protocols, so always include both in `--protocols`
- Set `--ingress false` and `--egress true` to specifically block outgoing DNS queries
- Applications with DNS caching may not immediately show effects; consider cache TTL when setting duration

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/dns-outage/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/dns-outage/dns-outage-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
