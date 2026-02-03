```
**User**: We need to see if the app crashes when it can't resolve hostnames. Can you kill all outgoing name resolution for this pod?

**GitHub Copilot**: This is a DNS outage chaos engineering scenario. Let me search for how krkn implements DNS disruption scenarios. 

Searched codebase for "DNS outage block name resolution network chaos scenario pod", 11 results

I found the DNS outages scenario. This is exactly what you need to block all outgoing name resolution for a pod. Here's how to do it using **krknctl**:

## DNS Outage Chaos Scenario

To block all DNS resolution for a pod, use the `pod-network-filter` scenario targeting port 53 (DNS):

```bash
krknctl run pod-network-filter --pod-name <your-pod-name> --egress true --protocols tcp,udp --ports 53
```

### With a specific duration (e.g., 60 seconds):

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name <your-pod-name> --ingress false --egress true --protocols tcp,udp --ports 53
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--pod-name` | Your target pod name | The pod to disrupt |
| `--egress` | `true` | Block outgoing DNS queries |
| `--protocols` | `tcp,udp` | DNS uses both protocols |
| `--ports` | `53` | Standard DNS port |
| `--chaos-duration` | seconds (default: 60) | How long to block DNS |

### Tips:
- DNS uses **port 53** on both TCP and UDP, so always include both protocols
- Applications with DNS caching may not immediately show effects—consider cache TTL when setting duration
- Set `--ingress false` and `--egress true` to specifically block outgoing DNS queries only

Replace `<your-pod-name>` with your actual pod name to run this chaos test.
```

```
**User**: Our database is acting up. Let's block all traffic to the Aurora cluster from our application pods and see how they handle it.

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Aurora_Disruptions.md)

## Aurora Disruption Chaos Scenario

To block all traffic from your application pods to the Aurora cluster, use the `pod-network-filter` scenario targeting database ports:

```bash
krknctl run pod-network-filter --pod-name <your-app-pod> --egress true --protocols tcp --ports 3306,5432
```

### With a specific duration (e.g., 60 seconds):

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name <your-app-pod> --ingress false --egress true --protocols tcp --ports 3306,5432
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--pod-name` | Your application pod name | The pod to disrupt |
| `--egress` | `true` | Block outgoing database connections |
| `--protocols` | `tcp` | Database connections use TCP |
| `--ports` | `3306,5432` | MySQL (3306) and/or PostgreSQL (5432) |
| `--chaos-duration` | seconds (default: 60) | How long to block traffic |

### For specific database types:

**Aurora MySQL only:**
```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name <your-app-pod> --egress true --protocols tcp --ports 3306
```

**Aurora PostgreSQL only:**
```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name <your-app-pod> --egress true --protocols tcp --ports 5432
```

### Tips:
- This works for both AWS Aurora and standard MySQL/PostgreSQL connections
- Start with shorter durations to understand application behavior before running longer tests
- Use this to validate connection timeout logic, retry mechanisms, and circuit breaker patterns

Replace `<your-app-pod>` with your actual application pod name to run this chaos test.
```

```
**User**: I want to test how our application behaves when the main service goes down. Can you take down the deployment for 2 minutes?

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Application_outages.md)

## Application Outages Chaos Scenario

To take down your deployment for 2 minutes (120 seconds), use the `application-outages` scenario:

```bash
krknctl run application-outages --namespace <your-namespace> --chaos-duration 120
```

### Target a specific deployment with label selector:

```bash
krknctl run application-outages --namespace <your-namespace> --pod-selector "{app: <your-app-name>}" --chaos-duration 120
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--namespace` | Your target namespace | Required - where the app lives |
| `--pod-selector` | `"{app: myapp}"` | Target specific pods by label |
| `--chaos-duration` | `120` | 2 minutes in seconds |
| `--block-traffic-type` | `[Ingress, Egress]` | What traffic to block (default: both) |

### Examples:

**Block all traffic to a deployment for 2 minutes:**
```bash
krknctl run application-outages --namespace production --pod-selector "{app: main-service}" --chaos-duration 120
```

**Block only incoming traffic (Ingress):**
```bash
krknctl run application-outages --namespace production --pod-selector "{app: main-service}" --block-traffic-type "[Ingress]" --chaos-duration 120
```

**Exclude critical pods from the outage:**
```bash
krknctl run application-outages --namespace production --pod-selector "{tier: backend}" --exclude-label "{critical: true}" --chaos-duration 120
```

### Tips:
- This scenario blocks both ingress and egress traffic by default, fully isolating the application
- Add your application's URL to health checks to track downtime during the scenario
- Krkn supports rollback for this scenario if needed

Replace `<your-namespace>` and `<your-app-name>` with your actual values to run this chaos test.
```

```
**User**: One of our nodes is acting flaky. Can you simulate a disk I/O bottleneck on worker-node-02 to see how pods recover?

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Node_IO_Hog.md)

## Node IO Hog Chaos Scenario

To simulate a disk I/O bottleneck on `worker-node-02`, use the `node-io-hog` scenario:

```bash
krknctl run node-io-hog --node-selector "kubernetes.io/hostname=worker-node-02"
```

### With custom I/O pressure settings:

```bash
krknctl run node-io-hog --node-selector "kubernetes.io/hostname=worker-node-02" --io-write-bytes "50%" --chaos-duration 120
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--node-selector` | `"kubernetes.io/hostname=worker-node-02"` | Target the specific node |
| `--io-write-bytes` | `"50%"` or `"10g"` | Amount of data to write (% of free space or size) |
| `--io-block-size` | `"1m"` or `"4k"` | Size of each write operation |
| `--io-workers` | `5` | Number of concurrent stressor instances |
| `--chaos-duration` | seconds (default: 60) | How long to run the I/O stress |

### Examples:

**Heavy I/O stress for 2 minutes:**
```bash
krknctl run node-io-hog --node-selector "kubernetes.io/hostname=worker-node-02" --io-write-bytes "50%" --io-workers 10 --chaos-duration 120
```

**High IOPS with small block writes:**
```bash
krknctl run node-io-hog --node-selector "kubernetes.io/hostname=worker-node-02" --io-block-size "4k" --io-write-bytes "1g" --chaos-duration 120
```

**High throughput with large block writes:**
```bash
krknctl run node-io-hog --node-selector "kubernetes.io/hostname=worker-node-02" --io-block-size "1m" --io-write-bytes "10g" --chaos-duration 120
```

### Tips:
- **Block size** affects I/O pattern: smaller blocks (4k) = more IOPS, larger blocks (1m) = higher throughput
- Ensure kubelet has write permissions to `--node-mount-path` (default: `/root`)
- Krkn supports rollback for this scenario if needed

This will create disk I/O pressure on `worker-node-02` so you can observe how pods recover from the bottleneck.
```

```
**User**: Let's see how our services handle network issues. Can you create packet loss and latency between the frontend and backend pods?

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Pod_Network_Chaos.md)

I see that `pod-network-chaos` focuses on blocking traffic. For packet loss and latency, let me check the Network Chaos NG scenario which has more advanced traffic shaping capabilities: 

Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Network_Chaos_NG.md)

Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Network_Chaos.md)

## Pod Network Chaos Scenario

To create packet loss and latency between your frontend and backend pods, you can use the `network-chaos` scenario:

### Combined packet loss and latency:

```bash
krknctl run network-chaos --label-selector "app=frontend" --network-params "{latency: 100ms, loss: 0.05}" --duration 120
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--label-selector` | `"app=frontend"` | Target nodes running specific pods |
| `--node-name` | `"worker-node-1"` | Target specific node(s) |
| `--network-params` | `"{latency: 50ms, loss: 0.02}"` | Combined network disruptions |
| `--egress` | `"{latency: 100ms}"` | Egress-specific parameters |
| `--duration` | seconds (default: 300) | How long to apply the chaos |

### Examples:

**Add 100ms latency with 5% packet loss:**
```bash
krknctl run network-chaos --label-selector "node-role.kubernetes.io/worker" --network-params "{latency: 100ms, loss: 0.05}" --duration 120
```

**Latency only (100ms delay):**
```bash
krknctl run network-chaos --label-selector "node-role.kubernetes.io/worker" --egress "{latency: 100ms}" --duration 120
```

**Packet loss only (5% drop rate):**
```bash
krknctl run network-chaos --node-name "worker-node-1" --egress "{loss: 0.05}" --duration 120
```

**Combined disruption on multiple nodes:**
```bash
krknctl run network-chaos --node-name "frontend-node,backend-node" --network-params "{latency: 50ms, loss: 0.02, bandwidth: 100mbit}" --duration 180
```

### Tips:
- **Latency** is specified in milliseconds (e.g., `100ms`, `50ms`)
- **Packet loss** is a decimal fraction (e.g., `0.05` = 5% loss, `0.10` = 10% loss)
- Set `--wait-duration` to at least twice the test duration for proper cleanup
- Start with lower disruption values and gradually increase to identify thresholds
- Krkn supports rollback for this scenario if needed

This will introduce network degradation affecting traffic between your frontend and backend services, helping you test timeout logic, retry mechanisms, and overall resilience.
```

```
**User**: The node is getting sluggish. Can you intentionally spike the CPU usage to 100% on worker-node-01?

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Node_CPU_Hog.md)

## Node CPU Hog Chaos Scenario

To spike CPU usage to 100% on `worker-node-01`, use the `node-cpu-hog` scenario:

```bash
krknctl run node-cpu-hog --node-selector "kubernetes.io/hostname=worker-node-01" --cpu-percentage 100
```

### With a specific duration:

```bash
krknctl run node-cpu-hog --node-selector "kubernetes.io/hostname=worker-node-01" --cpu-percentage 100 --chaos-duration 120
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--node-selector` | `"kubernetes.io/hostname=worker-node-01"` | Target the specific node |
| `--cpu-percentage` | `100` | Percentage of CPU to consume |
| `--cores` | number | Specific number of CPU cores to stress |
| `--chaos-duration` | seconds (default: 60) | How long to run the CPU stress |

### Examples:

**100% CPU for 2 minutes:**
```bash
krknctl run node-cpu-hog --node-selector "kubernetes.io/hostname=worker-node-01" --cpu-percentage 100 --chaos-duration 120
```

**Stress all worker nodes at 80% CPU:**
```bash
krknctl run node-cpu-hog --node-selector "node-role.kubernetes.io/worker" --cpu-percentage 80 --chaos-duration 120
```

**Stress specific number of cores:**
```bash
krknctl run node-cpu-hog --node-selector "kubernetes.io/hostname=worker-node-01" --cpu-percentage 100 --cores 4 --chaos-duration 120
```

### Tips:
- If `--node-selector` is not specified, a random schedulable node will be selected
- Use `--cores` to limit the stress to a specific number of CPU cores instead of all available
- Krkn supports rollback for this scenario if needed

This will max out the CPU on `worker-node-01` so you can observe how pods and the scheduler behave under CPU pressure.
```

```
**User**: We're testing database resilience. Block all egress traffic from the pods to our Aurora cluster.

**GitHub Copilot**: ## Aurora Disruption Chaos Scenario

To block all egress traffic from your pods to the Aurora cluster, use the `pod-network-filter` scenario targeting database ports:

```bash
krknctl run pod-network-filter --pod-name <your-app-pod> --egress true --protocols tcp --ports 3306,5432
```

### With a specific duration:

```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name <your-app-pod> --ingress false --egress true --protocols tcp --ports 3306,5432
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--pod-name` | Your application pod name | The pod to disrupt |
| `--egress` | `true` | Block outgoing database connections |
| `--ingress` | `false` | Don't block incoming traffic |
| `--protocols` | `tcp` | Database connections use TCP |
| `--ports` | `3306,5432` | MySQL (3306) and/or PostgreSQL (5432) |
| `--chaos-duration` | seconds (default: 60) | How long to block traffic |

### Examples:

**Block Aurora MySQL egress:**
```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name my-app-pod --ingress false --egress true --protocols tcp --ports 3306
```

**Block Aurora PostgreSQL egress:**
```bash
krknctl run pod-network-filter --chaos-duration 60 --pod-name my-app-pod --ingress false --egress true --protocols tcp --ports 5432
```

**Block both MySQL and PostgreSQL egress for 2 minutes:**
```bash
krknctl run pod-network-filter --chaos-duration 120 --pod-name my-app-pod --ingress false --egress true --protocols tcp --ports 3306,5432
```

### Tips:
- Use port **3306** for MySQL/Aurora MySQL and port **5432** for PostgreSQL/Aurora PostgreSQL
- Set `--ingress false` and `--egress true` to specifically block only outgoing database connections
- This helps validate connection timeout logic, retry mechanisms, and circuit breaker patterns

Replace `<your-app-pod>` with your actual application pod name to run this chaos test.
```

```
**User**: I want to see how our application handles a sudden loss of memory. Can you consume all available memory on worker-node-03?

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Node_Memory_Hog.md)

## Node Memory Hog Chaos Scenario

To consume all available memory on `worker-node-03`, use the `node-memory-hog` scenario:

```bash
krknctl run node-memory-hog --node-selector "kubernetes.io/hostname=worker-node-03" --memory-consumption "100%"
```

### With a specific duration:

```bash
krknctl run node-memory-hog --node-selector "kubernetes.io/hostname=worker-node-03" --memory-consumption "100%" --chaos-duration 120
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--node-selector` | `"kubernetes.io/hostname=worker-node-03"` | Target the specific node |
| `--memory-consumption` | `"100%"` or `"90%"` | Percentage or absolute amount to consume |
| `--memory-workers` | number (default: 1) | Number of stress-ng worker threads |
| `--chaos-duration` | seconds (default: 60) | How long to run the memory stress |

### Examples:

**Consume all memory for 2 minutes:**
```bash
krknctl run node-memory-hog --node-selector "kubernetes.io/hostname=worker-node-03" --memory-consumption "100%" --chaos-duration 120
```

**Consume 90% memory (safer, avoids immediate OOM):**
```bash
krknctl run node-memory-hog --node-selector "kubernetes.io/hostname=worker-node-03" --memory-consumption "90%" --chaos-duration 120
```

**Consume a specific amount (e.g., 8GB):**
```bash
krknctl run node-memory-hog --node-selector "kubernetes.io/hostname=worker-node-03" --memory-consumption "8g" --chaos-duration 120
```

**Multiple memory workers for faster consumption:**
```bash
krknctl run node-memory-hog --node-selector "kubernetes.io/hostname=worker-node-03" --memory-consumption "100%" --memory-workers 4 --chaos-duration 120
```

### Tips:
- Memory consumption can be expressed as percentage (`%`) or absolute units (`b`, `k`, `m`, `g`)
- Monitor for **OOM (Out of Memory) events** and **pod evictions** during the test
- Using `100%` will likely trigger OOM killer and pod evictions—use `90%` for less aggressive testing
- Krkn supports rollback for this scenario if needed

This will exhaust memory on `worker-node-03` so you can observe how your application handles memory pressure and how pods recover from evictions.
```

```
**User**: Can you simulate a network outage for the service by blocking all incoming traffic to its pods?

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Service_Disruption.md)

Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Application_outages.md)

## Service Disruption Chaos Scenario

To simulate a network outage by blocking all incoming traffic to your service's pods, use the `application-outages` scenario with `--block-traffic-type "[Ingress]"`:

```bash
krknctl run application-outages --namespace <your-namespace> --pod-selector "{app: <your-service>}" --block-traffic-type "[Ingress]"
```

### With a specific duration:

```bash
krknctl run application-outages --namespace <your-namespace> --pod-selector "{app: <your-service>}" --block-traffic-type "[Ingress]" --chaos-duration 120
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--namespace` | Your target namespace | Required - where the service lives |
| `--pod-selector` | `"{app: my-service}"` | Target specific pods by label |
| `--block-traffic-type` | `"[Ingress]"` | Block only incoming traffic |
| `--chaos-duration` | seconds (default: 600) | How long to block traffic |

### Examples:

**Block all incoming traffic to a service:**
```bash
krknctl run application-outages --namespace production --pod-selector "{app: my-service}" --block-traffic-type "[Ingress]" --chaos-duration 120
```

**Block ingress to all pods in a namespace:**
```bash
krknctl run application-outages --namespace my-application --block-traffic-type "[Ingress]" --chaos-duration 120
```

**Block ingress but exclude critical pods:**
```bash
krknctl run application-outages --namespace production --pod-selector "{tier: frontend}" --exclude-label "{critical: true}" --block-traffic-type "[Ingress]" --chaos-duration 120
```

### Tips:
- Use `--block-traffic-type "[Ingress]"` to block **only incoming** traffic (simulates service being unreachable)
- Use `--block-traffic-type "[Egress]"` to block **only outgoing** traffic
- Use `--block-traffic-type "[Ingress, Egress]"` to block **both** (complete isolation)
- Krkn supports rollback for this scenario if needed

Replace `<your-namespace>` and `<your-service>` with your actual values to simulate the network outage.
```

```
**User**: Just kill a random container in that deployment. I want to make sure the restart policy is working as expected.

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Container_failures.md)

## Container Failures Chaos Scenario

To kill a random container in your deployment and test the restart policy, use the `container-scenarios` scenario:

```bash
krknctl run container-scenarios --namespace <your-namespace> --label-selector "app=<your-deployment>"
```

### With specific container name:

```bash
krknctl run container-scenarios --namespace <your-namespace> --label-selector "app=<your-deployment>" --container-name <container-name>
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--namespace` | Your target namespace | Where the deployment lives |
| `--label-selector` | `"app=my-deployment"` | Target pods by label |
| `--container-name` | Container name | Target a specific container |
| `--disruption-count` | number (default: 1) | How many containers to kill |
| `--action` | `1` or `9` | Kill signal (1=SIGHUP, 9=SIGKILL) |
| `--expected-recovery-time` | seconds (default: 60) | Time to wait before checking recovery |

### Examples:

**Kill a random container in the deployment:**
```bash
krknctl run container-scenarios --namespace production --label-selector "app=my-app"
```

**Kill with SIGKILL (immediate termination):**
```bash
krknctl run container-scenarios --namespace production --label-selector "app=my-app" --action 9
```

**Kill a specific container:**
```bash
krknctl run container-scenarios --namespace production --label-selector "app=my-app" --container-name main
```

**Kill multiple containers:**
```bash
krknctl run container-scenarios --namespace production --label-selector "app=my-app" --disruption-count 3
```

### Tips:
- Krkn tracks recovery metrics including `pod_rescheduling_time`, `pod_readiness_time`, and `total_recovery_time`
- Use `--action 9` (SIGKILL) for immediate termination, or `--action 1` (SIGHUP) for graceful shutdown
- Container kills may not cause full pod rescheduling—the container restarts within the same pod

Replace `<your-namespace>` and `<your-deployment>` with your actual values to test the restart policy.
```

```
**User**: Hey, can you recommend a good pizza place near the office?

**GitHub Copilot**: I'm a chaos engineering assistant focused on helping you run krkn scenarios to test your Kubernetes/OpenShift cluster resilience. I can help you with things like:

- **Node chaos**: CPU hog, memory hog, I/O hog, node failures
- **Pod/Container chaos**: Pod failures, container kills, application outages
- **Network chaos**: DNS outages, packet loss, latency, traffic blocking
- **Cloud-specific chaos**: Aurora disruptions, zone outages, power outages

Unfortunately, I can't help with pizza recommendations! 🍕

Is there a chaos engineering scenario you'd like to run instead?
```

```
**User**: Simulate a complete blackout. Shut down the entire cluster and bring it back up after 5 minutes to check health.

**GitHub Copilot**: Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Power_Outages.md#1-1), lines 1 to 100

Read [](file:///Users/iting0321/Desktop/krkn/.github/skills/krknctl-skills/references/Power_Outages.md#100-100), lines 100 to 133

## Power Outages Chaos Scenario

To simulate a complete blackout and shut down the entire cluster for 5 minutes (300 seconds), use the `power-outages` scenario:

```bash
krknctl run power-outages --cloud-type <your-cloud> --shutdown-duration 300
```

### For AWS (5 minute blackout):

```bash
krknctl run power-outages --cloud-type aws --shutdown-duration 300 --aws-access-key-id <key> --aws-secret-access-key <secret> --aws-default-region <region>
```

### Key Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--cloud-type` | `aws`, `azure`, `gcp`, `vmware`, `ibmcloud`, `bm` | Your cloud platform |
| `--shutdown-duration` | `300` | 5 minutes in seconds |
| `--timeout` | seconds (default: 180) | Time to wait for node scenario completion |

### Cloud-Specific Examples:

**AWS:**
```bash
krknctl run power-outages --cloud-type aws --shutdown-duration 300 --aws-access-key-id <key> --aws-secret-access-key <secret> --aws-default-region us-east-1
```

**Azure:**
```bash
krknctl run power-outages --cloud-type azure --shutdown-duration 300 --azure-tenant <tenant> --azure-client-id <client-id> --azure-client-secret <secret> --azure-subscription-id <subscription>
```

**GCP:**
```bash
krknctl run power-outages --cloud-type gcp --shutdown-duration 300 --gcp-application-credentials /path/to/credentials.json
```

**VMware:**
```bash
krknctl run power-outages --cloud-type vmware --shutdown-duration 300 --vsphere-ip <ip> --vsphere-username <user> --vsphere-password <password>
```

### Tips:
- The scenario will shut down the cluster, wait for the specified duration, bring it back online, and check health
- Ensure you have proper cloud provider credentials configured before running
- Secret parameters (credentials) will be masked when the scenario runs
- Monitor cluster health checks after the cluster comes back online
- Start with shorter durations to understand recovery behavior before running longer tests

Replace the cloud credentials with your actual values to simulate the complete blackout.
```
