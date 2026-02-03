# Aurora Disruption

## Overview

This scenario blocks a pod's outgoing MySQL and PostgreSQL traffic, effectively preventing it from connecting to any AWS Aurora SQL engine. It works just as well for standard MySQL and PostgreSQL connections too. This uses the pod network filter scenario but set with specific parameters to disrupt Aurora.

## Category

**Cloud Provider Specific (AWS)** - This scenario targets AWS Aurora database connectivity.

## Use Cases

- Test application resilience when Aurora database becomes unreachable
- Validate connection timeout and retry logic for database connections
- Verify application behavior during database failover scenarios
- Test circuit breaker patterns for database connections
- Understand how applications handle lost database connectivity

## Usage

### Basic Command

```bash
krknctl run pod-network-filter --pod-name <target-pod> --egress true --protocols tcp --ports 3306,5432
```

### With Options

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name <target-pod> --ingress false --egress true --protocols tcp --ports 3306,5432
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
| `--protocols` | Network protocols to block | string | No | tcp |
| `--ports` | Ports to block (3306 for MySQL, 5432 for PostgreSQL) | string | No | 3306,5432 |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Block Aurora MySQL Connection for 60 Seconds

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name my-app-pod --ingress false --egress true --protocols tcp --ports 3306
```

### Block Aurora PostgreSQL Connection

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name my-app-pod --ingress false --egress true --protocols tcp --ports 5432
```

### Block Both MySQL and PostgreSQL Connections

```bash
krknctl run pod-network-filter --chaos-duration 120 --pod-name my-app-pod --ingress false --egress true --protocols tcp --ports 3306,5432
```

## Tips

- Use port 3306 for MySQL/Aurora MySQL and port 5432 for PostgreSQL/Aurora PostgreSQL
- Set `--ingress false` and `--egress true` to specifically block outgoing database connections
- Start with shorter durations to understand application behavior before running longer tests

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/aurora-disruption/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/aurora-disruption/aurora-disruption-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)

