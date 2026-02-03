# Power Outages

## Overview

This scenario shuts down Kubernetes/OpenShift cluster for the specified duration to simulate power outages, brings it back online and checks if it's healthy. It supports multiple cloud providers including AWS, Azure, GCP, VMware, IBM Cloud, and Baremetal.

## Category

**Cloud Provider Specific (AWS)** - This scenario targets cluster-wide power outage simulation across multiple cloud platforms.

## Use Cases

- Test cluster recovery after complete power loss
- Validate data persistence and consistency after unexpected shutdowns
- Verify application state recovery mechanisms
- Test infrastructure automation and self-healing capabilities
- Validate disaster recovery procedures
- Understand cluster bootstrap and initialization timing

## Usage

### Basic Command

```bash
krknctl run power-outages --cloud-type aws
```

### With Options

```bash
krknctl run power-outages --cloud-type aws --shutdown-duration 1200 --timeout 180 --aws-access-key-id <key> --aws-secret-access-key <secret> --aws-default-region us-east-1
```

### View All Options

```bash
krknctl run power-outages --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--cloud-type` | Cloud platform (aws, azure, gcp, vmware, ibmcloud, bm) | enum | No | aws |
| `--shutdown-duration` | Duration to keep the cluster shut down (in seconds) | number | No | 1200 |
| `--timeout` | Duration to wait for completion of node scenario injection | number | No | 180 |

### AWS Specific Parameters

| Parameter | Description | Type |
|-----------|-------------|------|
| `--aws-access-key-id` | AWS Access Key Id | string (secret) |
| `--aws-secret-access-key` | AWS Secret Access Key | string (secret) |
| `--aws-default-region` | AWS default region | string |

### Azure Specific Parameters

| Parameter | Description | Type |
|-----------|-------------|------|
| `--azure-tenant` | Azure Tenant | string |
| `--azure-client-id` | Azure Client ID | string (secret) |
| `--azure-client-secret` | Azure Client Secret | string (secret) |
| `--azure-subscription-id` | Azure Subscription ID | string (secret) |

### GCP Specific Parameters

| Parameter | Description | Type |
|-----------|-------------|------|
| `--gcp-application-credentials` | GCP application credentials file location | file |

### VMware Specific Parameters

| Parameter | Description | Type |
|-----------|-------------|------|
| `--vsphere-ip` | VSphere IP Address | string |
| `--vsphere-username` | VSphere username | string (secret) |
| `--vsphere-password` | VSphere password | string (secret) |

### IBM Cloud Specific Parameters

| Parameter | Description | Type |
|-----------|-------------|------|
| `--ibmc-address` | IBM Cloud URL | string |
| `--ibmc-api-key` | IBM Cloud API Key | string (secret) |

### Baremetal Specific Parameters

| Parameter | Description | Type |
|-----------|-------------|------|
| `--bmc-user` | IPMI/BMC username | string (secret) |
| `--bmc-password` | IPMI/BMC password | string (secret) |
| `--bmc-address` | IPMI/BMC address | string |

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### AWS Power Outage for 20 Minutes

```bash
krknctl run power-outages --cloud-type aws --shutdown-duration 1200 --aws-access-key-id <key> --aws-secret-access-key <secret> --aws-default-region us-east-1
```

### Azure Power Outage

```bash
krknctl run power-outages --cloud-type azure --shutdown-duration 600 --azure-tenant <tenant> --azure-client-id <client-id> --azure-client-secret <secret> --azure-subscription-id <subscription>
```

### GCP Power Outage

```bash
krknctl run power-outages --cloud-type gcp --shutdown-duration 900 --gcp-application-credentials /path/to/credentials.json
```

### Short Duration Test (5 Minutes)

```bash
krknctl run power-outages --cloud-type aws --shutdown-duration 300 --timeout 120 --aws-access-key-id <key> --aws-secret-access-key <secret> --aws-default-region us-east-1
```

## Tips

- Start with shorter shutdown durations to understand recovery behavior before running longer tests
- Ensure you have proper cloud provider credentials configured before running
- Secret parameters (credentials) will be masked when the scenario is run
- Monitor cluster health checks after the cluster comes back online

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/power-outage-scenarios/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/power-outage-scenarios/power-outage-scenario-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
