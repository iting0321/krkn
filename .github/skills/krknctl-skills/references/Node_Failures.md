# Node Failures

## Overview

Node scenario disrupts node(s) matching the label or node name(s) on a Kubernetes/OpenShift cluster. These scenarios can be performed via cloud provider APIs or through common commands that work on any cluster.

## Category

**Node-Level Chaos** - This scenario targets node-level disruptions using cloud provider operations or generic commands.

## Supported Actions

| Action | Description | Requirements |
|--------|-------------|--------------|
| `node_start_scenario` | Start a stopped node | Cloud provider access |
| `node_stop_scenario` | Stop a running node | Cloud provider access |
| `node_stop_start_scenario` | Stop then start a node | Cloud provider access |
| `node_termination_scenario` | Terminate a node | Cloud provider access |
| `node_reboot_scenario` | Reboot a node | Cloud provider access |
| `stop_kubelet_scenario` | Stop the kubelet service | Cloud provider access |
| `stop_start_kubelet_scenario` | Stop and start kubelet | Cloud provider access |
| `restart_kubelet_scenario` | Restart kubelet | Generic (no cloud access needed) |
| `node_crash_scenario` | Crash the node | Generic (no cloud access needed) |

## Supported Clouds

AWS, Azure, GCP, OpenStack, VMware, Alibaba, IBM Cloud, IBM Cloud Power, Bare Metal, Docker

## Usage

### Basic Command

```bash
krknctl run node-scenarios --action <action-name>
```

### With Options

```bash
krknctl run node-scenarios --action node_stop_start_scenario --label-selector "node-role.kubernetes.io/worker" --cloud-type aws
```

### View All Options

```bash
krknctl run node-scenarios --help
```

## Parameters

| Parameter | Description | Type | Required | Default |
|-----------|-------------|------|----------|---------|
| `--action` | Action to perform on the node | enum | **Yes** | - |
| `--label-selector` | Node label to target | string | No | node-role.kubernetes.io/worker |
| `--exclude-label` | Excludes nodes marked by this label from chaos | string | No | - |
| `--node-name` | Node name to target (comma-separated for multiple) | string | No | - |
| `--instance-count` | Number of instances matching the label selector | number | No | 1 |
| `--runs` | Iterations to perform action on a single node | number | No | 1 |
| `--cloud-type` | Cloud platform (aws, azure, gcp, vmware, ibmcloud, bm) | enum | No | aws |
| `--timeout` | Duration to wait for node scenario completion | number | No | 180 |
| `--duration` | Duration for the scenario | number | No | 120 |
| `--kube-check` | Check node status via Kubernetes API (set False for SNO) | enum | No | true |

### Cloud-Specific Parameters

**AWS:**
- `--aws-access-key-id`, `--aws-secret-access-key`, `--aws-default-region`

**Azure:**
- `--azure-tenant`, `--azure-client-id`, `--azure-client-secret`, `--azure-subscription-id`

**GCP:**
- `--gcp-application-credentials`

**Bare Metal:**
- `--bmc-user`, `--bmc-password`, `--bmc-address`

> **Note:** Global parameters can also be applied. See [Krknctl All Scenarios Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/) for details.

## Examples

### Stop and Start Worker Nodes (AWS)

```bash
krknctl run node-scenarios --action node_stop_start_scenario --label-selector "node-role.kubernetes.io/worker" --cloud-type aws --instance-count 1
```

### Reboot a Specific Node (Azure)

```bash
krknctl run node-scenarios --action node_reboot_scenario --node-name "worker-node-1" --cloud-type azure
```

### Restart Kubelet (No Cloud Access)

```bash
krknctl run node-scenarios --action restart_kubelet_scenario --label-selector "node-role.kubernetes.io/worker"
```

### Crash a Node

```bash
krknctl run node-scenarios --action node_crash_scenario --label-selector "node-role.kubernetes.io/worker"
```

## Recovery Time Metrics

Krkn tracks the following metrics:
- `not_ready_time`: Time for node to become NotReady after stop
- `ready_time`: Time for node to become Ready after restart
- `stopped_time`: Time for cloud provider to stop the node
- `running_time`: Time for cloud provider to start the node

## Tips

- If a node does not recover from `node_crash_scenario`, manually reboot the node to restore it
- Use `--kube-check false` for Single Node OpenShift (SNO) deployments

## Documentation
- [Official Documentation](https://krkn-chaos.dev/docs/scenarios/node-scenarios/)
- [Krknctl Specific Guide](https://krkn-chaos.dev/docs/scenarios/node-scenarios/node-scenarios-krknctl/)
- [All Krknctl Scenario Variables](https://krkn-chaos.dev/docs/scenarios/all-scenario-env-krknctl/)
