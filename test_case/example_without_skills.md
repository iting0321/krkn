# Example of without using skills
---

**User**: We need to see if the app crashes when it can't resolve hostnames. Can you kill all outgoing name resolution for this pod

**GitHub Copilot**: Searched for regex `dns|name resolution|network chaos`, 20 results

Read [](file:///Users/iting0321/Desktop/krkn/scenarios)

Read [](file:///Users/iting0321/Desktop/krkn/scenarios/kube)

Read [](file:///Users/iting0321/Desktop/krkn/scenarios/kube/container_dns.yml)

Searched for regex `block.*dns|dns.*block|port.*53|egress.*dns`, 1 result

Read [](file:///Users/iting0321/Desktop/krkn/scenarios/kube/pod-network-filter.yml)

I found exactly what you need. The pod-network-filter.yml scenario can block DNS resolution by filtering egress traffic on port 53 (which is the DNS port). Let me show you how to configure this for your specific pod: 

Read [](file:///Users/iting0321/Desktop/krkn/krkn/scenario_plugins/network_chaos_ng/modules/pod_network_filter.py)

Now I have a clear picture. Let me create a scenario file that will block all outgoing DNS resolution (port 53) for your target pod. You'll need to customize the pod selector and namespace: 

Created [](file:///Users/iting0321/Desktop/krkn/scenarios/kube/block-dns-outage.yml)

I've created a scenario file at block-dns-outage.yml that will block all outgoing DNS resolution for a pod.

**To use it:**

1. Edit the file and set either:
   - `target: "your-pod-name"` - for a specific pod
   - `label_selector: "app=your-app"` - to target pods by label

2. Update `namespace` to match your pod's namespace

3. Run krkn with this scenario:
   ```bash
   python run_kraken.py --config config/config.yaml --scenario scenarios/kube/block-dns-outage.yml
   ```

**What it does:**
- Blocks all **egress** traffic on **port 53** (UDP and TCP)
- This prevents the pod from making DNS queries to resolve any hostnames
- The block lasts for `test_duration` seconds (currently set to 120 seconds)
- Any `requests.get("https://example.com")` or similar hostname lookups will fail

**Expected app behavior when DNS is blocked:**
- Network calls using hostnames will fail with errors like `Name or service not known`
- Connections using IP addresses directly will still work
- This helps identify if your app has proper error handling and retry logic for DNS failures

Would you like me to help you configure this for a specific pod?

Made changes.
