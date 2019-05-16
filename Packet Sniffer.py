import socket
import struct

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '



def get_mac_addr(mac_raw):
    byte_str = map('{:02x}'.format, mac_raw)
    mac_addr = ':'.join(byte_str).upper()
    return mac_addr

def ether(self, raw_data):
    dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
    dest_mac = get_mac_addr(dest)
    src_mac = get_mac_addr(src)
    proto = socket.htons(prototype)
    data = raw_data[14:]
    return dest_mac, src_mac, proto, data

## Ip header analysis
def netl(raw_data):
    version_header_length = raw_data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
    src = ipv4(src)
    target = ipv4(target)
    data = raw_data[header_length:]
    return version, header_length, ttl, proto, src, target, data

#make ip address, its authentical shape
def ipv4(addr):
    return '.'.join(map(str, addr))

#icmp header 
def icmp(raw_data):
    icmp_type, code, checksum = struct.unpack('! B B H', raw_data[:4])
    data = raw_data[4:]
    return icmp_type, code, checksum, data[4:]


#tcp header
def tcp(raw_data):
    (src_port, dest_port, sequence, acknowledgment, offset_reserved_flags) = struct.unpack('! H H L L H', raw_data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1
    data = raw_data[offset:]
    return src_port, dest_port, sequence, acknowledgment, offset_reserved_flags, offset, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data


#http header 
def http(raw_data):
    try:
        data = raw_data.decode('utf-8')
        return data
    except:
        data = raw_data
        return data

#udp header
def udp(raw_data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', raw_data[:8])
    data = raw_data[8:]
    return src_port, dest_port, size, data


#main body of the sniffer
def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while 1:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ether(raw_data)
        print('Etherenet:')
        print(TAB_1, 'Destination Address: {1}{0}{5}Source Address: {2}{0}{5}etherenet protocol: {3}{0}{5}data {4}{0}{5}'.format('\n', dest_mac, src_mac, eth_proto, data, '\t'))
        
        if eth_proto == 8:
            version, header_length, ttl, proto, src, target, data = netl(data)
            print(TAB_1 + 'IPv4 Packet:')
            print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {},'.format(version, header_length, ttl))
            print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(proto, src, target))
    ### TCP
            if proto == 6:
                src_port, dest_port, sequence, acknowledgment, offset_reserved_flags, offset, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data = tcp(data)
                print(TAB_1 + 'TCP Segment:')
                print(TAB_2 + 'Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
                print(TAB_2 + 'Sequence: {}, Acknowledgment: {}'.format(sequence, acknowledgment))
                print(TAB_2 + 'Flags:')
                print(TAB_3 + 'URG: {}, ACK: {}, PSH: {}'.format(flag_urg, flag_ack, flag_psh))
                print(TAB_3 + 'RST: {}, SYN: {}, FIN:{}'.format(flag_rst, flag_syn, flag_fin))
                if len(data) > 0:
    ### HTTP
                    if src_port == 80 or dest_port == 80:
                        print(TAB_2 + 'HTTP Data:')
                        try:
                            data = http(data)
                            http_info = str(data).split('\n')
                            for line in http_info:
                                print(DATA_TAB_3 + str(line))
                        except:
                            print(data))
                    else:
                        print(TAB_2 + 'TCP Data:')
                        print(data))

    ### ICMP
            elif proto ==1:
                icmp_type, code, checksum, data = icmp(data)
                print(TAB_1 + 'ICMP Packet:')
                print(TAB_2 + 'Type: {}, Code: {}, Checksum: {},'.format(icmp_type, code, checksum))
                print(TAB_2 + 'ICMP Data:')
                print(data))
    ### UDP
            elif proto == 17:
                src_port, dest_port, size, data = udp(data)
                print(TAB_1 + 'UDP Segment:')
                print(TAB_2 + 'Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, size))
                
                
                
main()