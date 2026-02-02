---
name: krknctlscenario-finding
description: Find the corresponding krkn chaos scenario
---

## Workflow
1. **Identify scenario**: Match user's chaos testing need to an available scenario
2. **Return scenario reference**: 
Return the associated documentation from the available set and also all the important details in corresponding documentation.
3. **Include official documentation**: Always include the official documentation link from the Documentation section of the matched scenario reference file.

Return no result when the request does not match any existing scenario.


## Available Scenarios

### Node-Level Chaos
- [Node CPU Hog](references/Node_CPU_Hog.md)
- [Node IO Hog](references/Node_IO_Hog.md)
- [Node Memory Hog](references/Node_Memory_Hog.md)
- [Node Failures](references/Node_Failures.md)
- [Time skew](references/Time_skew.md)

### Pod & Container Chaos
- [Pod Failures](references/Pod_Failures.md)
- [Container failures](references/Container_failures.md)
- [Application outages](references/Application_outages.md)

### Network Chaos
- [Network Chaos](references/Network_Chaos.md)
- [Network Chaos NG](references/Network_Chaos_NG.md)
- [Pod Network Chaos](references/Pod_Network_Chaos.md)
- [DNS outages](references/DNS_outages.md)
- [Syn Flood](references/Syn_Flood.md)

### Service & Infrastructure Chaos
- [Service Disruption](references/Service_Disruption.md)
- [Service Hijacking](references/Service_Hijacking.md)
- [PVC disk fill](references/PVC_disk_fill.md)
- [ETCD Split Brain](references/ETCD_Split_Brain.md)
- [KubeVirt VM Outage](references/KubeVirt_VM_Outage.md)

### Cloud Provider Specific (AWS)
- [Zone outages](references/Zone_outages.md)
- [Power Outages](references/Power_Outages.md)
- [Aurora Disruptions](references/Aurora_Disruptions.md)
- [EFS Disruption](references/EFS_Disruption.md)

