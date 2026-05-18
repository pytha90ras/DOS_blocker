def firewall():
    from os import geteuid
    from time import time
    from sys import exit
    from scapy.all import sniff, IP
    from subprocess import run


    print("Starting Firewall")


    Max_packet_per_sec=100
    print(f"Threshold: {Max_packet_per_sec}")

    def packet_check(packet):
        src_ip=packet[IP].src
        if src_ip in whitelist:
            return
        current_time=time()
        if src_ip in Blocked:
            if current_time - Blocked[src_ip] >= 15*60:
                Blocked.pop(src_ip)
                run(["iptables", "-D", "INPUT", "-s", src_ip, "-j", "DROP"])
                packet_count[src_ip]=[1,current_time,current_time]
            return
        if not src_ip in packet_count:
            packet_count[src_ip]=[1,current_time,current_time]
            return

        packet_count[src_ip][0],packet_count[src_ip][2]=packet_count[src_ip][0]+1,current_time
        time_diff=packet_count[src_ip][2]-packet_count[src_ip][1]
        rate=packet_count[src_ip][0]/time_diff
        if time_diff < 3*60:
            return 
        elif time_diff>8*60:
            packet_count[src_ip]=[1,current_time,current_time]
            return
        if rate >= Max_packet_per_sec:
            print(f'Blocking {src_ip} for transmitting {rate} pps')
            run(["iptables", "-A", "INPUT", "-s", src_ip, "-j", "DROP"])
            Blocked[src_ip]=current_time

 
    if geteuid() !=0:
        exit(1) 
    packet_count={}
    Blocked={}
    whitelist={'172.16.78.1','172.16.78.3'}
    iface=input("Input the interface to sniff from: ")
    try:
        sniff(filter='ip',prn=packet_check,iface=iface)
    except ValueError:
        print('Interface not found')
        return
firewall()
