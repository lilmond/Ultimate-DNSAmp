# Ultimate-DNSAmp
A basic guide to simulate DNS amplification.

![image](https://github.com/user-attachments/assets/e84574cb-f96e-4813-96ce-e6b5cc892e11)

# Disclaimer

This repository is created and maintained for educational purposes only. It is intended to provide learning resources, demonstrate concepts, and support research in cybersecurity, network protocols, or related fields.

Use responsibly: The code and information provided in this repository should never be used for malicious purposes or any unauthorized activity. The owner of this repository disclaims any liability for misuse of the information or code contained herein. All users are responsible for ensuring their use of this content complies with applicable laws, regulations, and ethical guidelines.

If you are using this repository for testing or development purposes, please do so only in a controlled environment where you have explicit permission to do so (e.g., your own private network, lab setup, or properly authorized systems).

Respect others' rights and privacy by refraining from using this repository for any activity that could disrupt services, invade privacy, or cause harm to individuals or organizations.

Thank you for using this repository responsibly and for contributing to a safer, more informed community.

# How does DNS amplification work?

A DNS amplification attack is a type of Distributed Denial of Service (DDoS) attack where attackers exploit open DNS resolvers to overwhelm a target system or network with a massive amount of traffic. This attack takes advantage of the fact that DNS queries can be very small, but the responses can be significantly larger. By "amplifying" the amount of data sent to a victim, attackers can magnify their impact without needing a large amount of resources.

## Here’s how a DNS amplification attack works:

### 1. Choosing Open DNS Resolvers

Attackers look for open DNS resolvers—DNS servers that respond to queries from any IP address, not just those on a specific network. Many DNS servers are intentionally configured as open resolvers for public access, but they can be exploited if not properly secured.

### 2. Crafting Spoofed DNS Requests

The attacker crafts a DNS request that has a spoofed source IP address—specifically, the IP address of the intended victim. When the DNS resolver receives the request, it thinks it came from the victim’s IP address.

### 3. Sending Small Queries with Large Responses

The attacker sends small DNS queries to the open DNS resolvers. These queries are crafted to return large responses (usually by requesting information about DNS records with lots of data, such as the ANY record type). For example, a 60-byte DNS query could produce a 4,000-byte response, resulting in an amplification factor of about 70 times.

### 4. Amplifying Traffic to Overwhelm the Victim

Since the DNS requests are sent with the victim’s IP address, the open DNS resolvers send the large DNS responses directly to the victim’s server or network. Because multiple DNS resolvers are often used, this can result in massive volumes of traffic directed at the victim in a very short time.

The victim's server or network can be overwhelmed by this traffic, leading to:

Bandwidth exhaustion: The target’s internet connection becomes saturated, slowing down or blocking legitimate traffic.
Resource exhaustion: The target’s server may run out of processing power or memory, causing it to crash or become unresponsive.

## Why DNS Amplification is Effective

Amplification Factor: By using small DNS queries that result in large responses, attackers can amplify their impact without needing significant resources.

Anonymity: Attackers can use spoofed IP addresses, making it difficult to trace the attack back to its source.

High Availability of Open Resolvers: Thousands of improperly configured DNS resolvers are available on the internet, making them easy to exploit.

## Example of a DNS Amplification Attack

Let’s say an attacker wants to target a website with IP address `203.0.113.5`.

The attacker sends a DNS query to multiple open DNS resolvers, requesting information about a large record (like ANY) but using the IP address `203.0.113.5` as the source address.

Each DNS resolver receives the small query and sends a much larger response to `203.0.113.5` (the victim).

The victim receives a flood of these large responses from multiple DNS resolvers, overwhelming their server or network.

## Mitigating DNS Amplification Attacks

DNS Server Configuration: Configure DNS servers to only respond to queries from trusted IP addresses and disable support for the ANY query type, which often generates large responses.

Rate Limiting: Implement rate limiting on DNS servers to restrict the number of responses sent to any single IP address in a given period.

IP Spoofing Prevention: ISPs can implement egress filtering to block packets with spoofed IP addresses, which can prevent attackers from spoofing the victim’s IP.

Use of DNSSEC: DNSSEC (DNS Security Extensions) can help by ensuring the integrity of DNS responses, though it does not directly prevent amplification attacks.

Deploying Firewalls and Anti-DDoS Services: Firewalls and anti-DDoS services can detect and mitigate unusually high volumes of DNS responses directed at a single IP.

DNS amplification attacks exploit the design of DNS and the openness of many DNS resolvers on the internet. By leveraging both the amplification effect and IP spoofing, attackers can create a powerful and hard-to-trace DDoS attack.

# Installation

Let's get started by installing the basic components for performing a DNS amplification attack. Please follow the steps below.

## 1. Create a directory:
```bash
mkdir dnsamp
cd ./dnsamp
```

## 2. Setting up venv and scapy
```bash
python3 -m venv venv
source venv/bin/activate
pip install scapy
```

## 3. Download the required files:
```bash
curl https://raw.githubusercontent.com/lilmond/Ultimate-DNSAmp/refs/heads/main/dnsamp.py > dnsamp.py
curl https://raw.githubusercontent.com/lilmond/Nameservers_50k/refs/heads/main/nameservers_50k.txt > nameservers_50k.txt
```

## 4. Set up the firewall in your server.

This is important to allow IP spoofing in your network. Also, please note that this doesn't work for all types of devices, so I recommend using a dedicated server.

Enabling spoofed packets is generally not recommended, as spoofing refers to forging the source IP address of packets, which is commonly associated with malicious activities (e.g., DDoS attacks, man-in-the-middle attacks). Allowing or enabling spoofed packets can also lead to network security vulnerabilities and routing issues.

However, if you're configuring a lab environment or have a legitimate reason for simulating spoofed traffic (e.g., for testing and educational purposes), you can configure iptables to permit packets with mismatched or unexpected source IPs. Be very cautious when doing this, and only do it in a controlled environment, as it bypasses a common security measure.

### A. Disable Reverse Path Filtering

Linux has a built-in mechanism called reverse path filtering that prevents spoofed packets by ensuring that incoming packets on an interface have a source IP address reachable through that same interface. To allow spoofed packets, you need to disable this filtering.

To disable reverse path filtering, you can run:
```bash
# Disable reverse path filtering
echo 0 | sudo tee /proc/sys/net/ipv4/conf/all/rp_filter
```

### B. Or, to make it persistent across reboots, add the following to `/etc/sysctl.conf`:

```
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.default.rp_filter = 0
net.ipv4.conf.eth0.rp_filter = 0  # Replace eth0 with your interface
```

Then apply the changes with:

```bash
sudo sysctl -p
```

And finally, you can run the script:
```bash
python3 dnsamp.py
```

Enjoy!
