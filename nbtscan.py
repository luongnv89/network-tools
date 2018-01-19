import json
import subprocess

class LiveNode:
    """LiveNode is the class presents a Live Node in network
    """
    name = ""
    ip = ""
    mac = ""
    
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

def nb_parse_line(line):
    """Parse an nbtscan line to get information of a node in network
    
    Arguments:
        line {String} -- A string contains information of a node in network
    """
    values = line.split()
    return LiveNode(values[1].strip(),values[0],values[len(values)-1])

def nb_parse_output(nb_output):
    """Parse nbtscan output to get information in JSON format

    Arguments:
        nb_output {String} -- nbtscan output
        192.168.56.0	Sendto failed: Permission denied
        Doing NBT name scan for addresses from 192.168.0.0/16

        IP address       NetBIOS Name     Server    User             MAC address      
        ------------------------------------------------------------------------------
        192.168.0.28     MYBOOKLIVEDUO    <server>  MYBOOKLIVEDUO    000000000000
        192.168.0.40     PCARVALLO                  <unknown>        38c9861f8552
        192.168.0.20     MACBOOKPRO-6D19            <unknown>        4c3275946d19
        192.168.0.1      SAGEMCOM         <server>  SAGEMCOM         000000000000
        192.168.0.57     HN-MP13                    <unknown>        60f81daaa622
        192.168.0.14     BRN008077D141A0  <server>  <unknown>        008077d141a0
        192.168.0.58     MACBOOKPRO-91D3            <unknown>        4c32758b91d3
    """
    all_nodes = []
    lines = nb_output.split("\n")
    start_data = False
    for line in lines:
        if (start_data == True and line != ""):
            # print(line + '\n')
            new_node = nb_parse_line(line)
            all_nodes.append(new_node)
        if (line == "------------------------------------------------------------------------------"):
            start_data = True
    return all_nodes

def nb_scan(scan_range):
    """Scan local network and return in JSON format the information of all device in the network.
    Each device has informations:
    - Name (hostname)
    - IP address
    - Mac address
    
    Arguments:
        scan_range {String} -- 	what to scan. Can either be single IP
			like 192.168.1.1 or
			range of addresses in one of two forms: 
			xxx.xxx.xxx.xxx/xx or xxx.xxx.xxx.xxx-xxx.
    
    Returns:
        list -- List of LiveNode in network
    """
    nbtscan = subprocess.Popen(["nbtscan",scan_range], stdout=subprocess.PIPE)
    scan_output = nbtscan.communicate()[0]
    # print(scan_output)
    nodes = nb_parse_output(scan_output)
    return json.dumps([node.__dict__ for node in nodes])

print (nb_scan("192.168.0.14"))