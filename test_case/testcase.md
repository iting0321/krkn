

### Test Cases 

| # | User Prompt (The "Input") | Expected Scenario |
| --- | --- | --- |
| **1** | "We need to see if the app crashes when it can't resolve hostnames. Can you kill all outgoing name resolution for this pod?" | **DNS outages** |
| **2** | "Our database is acting up. Let's block all traffic to the Aurora cluster from our application pods and see how they handle it." | **Aurora Disruptions** |
| **3** | "I want to test how our application behaves when the main service goes down. Can you take down the deployment for 2 minutes?" | **Application Outages** |
| **4** | "One of our nodes is acting flaky. Can you simulate a disk I/O bottleneck on worker-node-02 to see how pods recover?" | **Node IO Hog** |
| **5** | "Let's see how our services handle network issues. Can you create packet loss and latency between the frontend and backend pods?" | **Pod Network Chaos** |
| **6** | "The node is getting sluggish. Can you intentionally spike the CPU usage to 100% on worker-node-01?" | **Node CPU Hog** |
| **7** | "We're testing database resilience. Block all egress traffic from the pods to our Aurora cluster." | **Aurora Disruption** |
| **8** | "I want to see how our application handles a sudden loss of memory. Can you consume all available memory on worker-node-03?" | **Node Memory Hog** |
| **9** | "Can you simulate a network outage for the service by blocking all incoming traffic to its pods?" | **Service Disruption** |

| **10** | "Just kill a random container in that deployment. I want to make sure the restart policy is working as expected." | **Container failures** |
| **11** | "Hey, can you recommend a good pizza place near the office?" | **No result** |
| **12** | "Simulate a complete blackout. Shut down the entire cluster and bring it back up after 5 minutes to check health." | **Power Outages** |

