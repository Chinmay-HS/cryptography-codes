### 1. `ipconfig /all`
Shows your own machine's full network configuration: IP address, subnet mask, default gateway, MAC address, and DNS servers. This is almost always the first command run, because it tells you what network you're actually on before you probe anything else. The default gateway is usually the router, and a good next target to investigate. Running plain `ipconfig` gives a shorter version with just IP, mask and gateway.

### 2. `ping`
Sends ICMP echo-request packets to a host and waits for a reply, confirming whether it's reachable and measuring round-trip time. Example: `ping 192.168.1.1`. The TTL value in the reply is a rough OS fingerprint — around 128 usually means Windows, around 64 usually means Linux/macOS, since each OS sets a different starting TTL that decreases by 1 per hop. A host that doesn't reply isn't necessarily down, since many firewalls block ICMP by default.

A one-line loop sweeps an entire subnet to find which hosts are alive:
```
for /L %i in (1,1,254) do @ping -n 1 -w 100 192.168.1.%i | find "TTL="
```
This pings .1 through .254 with a 1-packet, 100ms-timeout ping each, and only prints lines containing "TTL=", i.e. the hosts that actually responded.

### 3. `arp -a`
Displays the ARP cache: a table mapping IP addresses to MAC addresses for devices your computer has recently communicated with on the local network. Run this right after a ping sweep, since every host that replied will now have an entry here, giving you both its IP and its hardware (MAC) address. The first 6 hex digits of a MAC address (the OUI) can be looked up to identify the device manufacturer.

### 4. `tracert`
Shows the path (sequence of routers/hops) a packet takes to reach a destination, along with the latency at each hop. Example: `tracert google.com`. It works by sending packets with increasing TTL values, so each router along the way sends back a "TTL expired" message, revealing itself. This maps network topology and can reveal internal routers, VPN gateways or unexpected hops. Add `-d` (`tracert -d`) to skip reverse-DNS lookups at each hop, making it run much faster.

### 5. `nslookup`
Resolves domain names to IP addresses and queries specific DNS record types. Plain `nslookup example.com` gives the A record (IP address). Adding `-type=` lets you request other records: `nslookup -type=MX example.com` finds mail servers, `-type=NS` finds authoritative name servers, and `-type=TXT` shows TXT records (often used for SPF/domain verification). You can also do a reverse lookup by passing an IP instead of a name, e.g. `nslookup 8.8.8.8`, to find its hostname.

### 6. `netstat -ano`
Lists every active network connection and listening port on your machine, along with the PID (process ID) of the program using it. The `-a` shows all connections and listening ports, `-n` shows addresses/ports as numbers instead of resolving names (much faster), and `-o` adds the owning PID. This is the main way to check what's actually open and talking on your own machine — pair the PID with `tasklist` (below) to find which program it belongs to. It's a local-recon tool, not something you run against a remote host.

### 7. `tasklist`
Lists all running processes with their PIDs. Used together with `netstat -ano`: once you spot a suspicious or unexpected open connection/port, look up its PID here to identify the responsible program. Example: `tasklist /fi "PID eq 1234"` filters the list down to just that one process.

### 8. `net view \\<target>`
Lists the shared folders/resources on a remote Windows machine on the LAN. Plain `net view` (no target) lists other computers visible in your workgroup or domain. This relies on SMB/NetBIOS, so it mostly works inside a local network or Windows domain rather than over the internet, and may be blocked by modern firewall defaults.

### 9. `Test-NetConnection` (PowerShell)
The PowerShell equivalent of ping, but with an extra ability: checking whether a *specific port* is open. Example: `Test-NetConnection 192.168.1.1 -Port 443` tells you if port 443 (HTTPS) is reachable, returning `TcpTestSucceeded : True/False`. This is the main built-in substitute for a dedicated port scanner (like nmap) when you can't install anything. Add `-TraceRoute` to get hop-by-hop path info in the same command.

### 10. `curl -I`
Sends an HTTP HEAD request to a URL and shows only the response headers, not the page content. Example: `curl -I https://example.com`. The headers often reveal the web server software and version (e.g. `Server: nginx/1.18.0`), which is useful for identifying what's running on a web host. Built into Windows 10 and later, no installation needed.

---

**Typical order of use:** `ipconfig /all` (know your own network) → `ping` sweep + `arp -a` (find live hosts) → `tracert` / `nslookup` (map routes and domains) → `Test-NetConnection -Port` (check specific ports) → `netstat -ano` + `tasklist` (inspect your own machine) → `net view` / `curl -I` (enumerate shares and web services).