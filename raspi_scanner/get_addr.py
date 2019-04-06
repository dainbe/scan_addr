# coding:utf-8
import subprocess
import socket


def str_upper(str):
    return str.replace("\n", "").upper()


def get_addr():
    mac_cmd = "sudo arp-scan -l --interface eth0 | grep -i '[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}' | tr '\t' '|' | cut -d '|' -f2 | cut -d '|' -f1"
    mac_list = (str(subprocess.check_output(mac_cmd, stderr=subprocess.STDOUT,
                                            shell=True, universal_newlines=True)).split("\n"))[0:-1]

    mac_list = map(str_upper, mac_list)
    return mac_list
