# Import library
import re
import sys
import telnetlib
import time
import datetime
import os
from pyzabbix import ZabbixAPI
from netmiko import Netmiko


# Variables
# Waiting time before considering that there is a timeout (in seconds)
timeout = 10
# Name of input file where they are IP address of switches
utc = datetime.datetime.now()
utc = utc.strftime('%d-%m-%y-%f')


# Zabbix Server Conection
url = '<url-zabbix>'
username = "<user-name-zabbix>"
password = '<password-zabbix>'

# Testing Conection
try:
    zapi = ZabbixAPI(url, timeout=4)
    zapi.login(username, password)
except Exception as err:
    print("Failed connect Zabbix API")
    print(f"Error: {err}")

# Host requests from Zabbix
try:
    req_host = zapi.host.get(
        filter={"status": "0"}, output=["host"], groupids="129", selectInterfaces=["ip"])
#    print(req_host[0])
except:
    print("Requesition fail")

for host in req_host:
    ip = host["interfaces"][0]["ip"]
    host_name = host["host"]
    try:
        hostname = host_name+"-"+ip+"-"+utc+".cfg"
        print(">Start Mikrotik - Hostname {}".format(host_name))
        router = {
            "host": ip,
            "port": <port>,
            "username": "<user>",
            "password": "<password>",
            "device_type": "mikrotik_routeros"}
        net_connect = Netmiko(**router)
        output = net_connect.send_command_timing("export terse")
        filename = "<folder-path>"+hostname
        file = open(filename, 'w')
        file.write(output + "\n")
        file.close()
        net_connect.disconnect()
        os.system(
            'zabbix_sender -z <url-zabbix> -p <port> -s {} -k  <variable-zabbix> -o Success'.format(host_name))

        print("--------------------------------------------------------")
    except Exception as e:
        os.system(
            'zabbix_sender -z <url-zabbix> -p <port> -s {} -k  <variable-zabbix> -o Failure'.format(host_name))
        print("Hostname:{} com o IP: {} deu o erro: {}".format(
            host_name, ip, str(e)))
        print("--------------------------------------------------------")

if __name__ == "__main__":
    pass
