import datetime
import os
import psutil
import re
import socket
import threading
from netaddr import IPAddress

from qnapdisplay import QnapDisplay


class QnapLCDDaemon:
    Lcd = QnapDisplay()
    infoIndex = 0
    t = None
    blankLcdTimeout = 5
    Running = False
    Logging = None

    def __init__(self, _logging):
        self.Logging = _logging

    def getDataArray(self):
        output = []
        output.append([socket.gethostname(), "Load(5m): " + str(psutil.getloadavg()[1])])
        output.append(["Last boot:", datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")])
        output.append(["Memory: " + str(psutil.virtual_memory().percent) + "%",
                       "Swap: " + str(psutil.swap_memory().percent) + "%"])
        disk_usage = self.getUsage()
        for pool in disk_usage:
            pool_name = pool["pool_name"]
            pool_data = pool["data"]
            output.append([pool_name, pool_data["health"]])
            output.append([pool_name + " Size", pool_data["size"]])
            output.append([pool_name + " Alloc", pool_data["allocated"]])
            output.append([pool_name + " Free", pool_data["free"]])
            output.append([pool_name + " Frag %", pool_data["frag"]])
            output.append([pool_name + " Cap %", pool_data["cap"]])
        networks = self.getNetworks()
        for network in networks:
            output.append([network['network'], "{}/{}".format(network['address'], network['netmask'])])
        return (output)

    def getNetworks(self, network_regex="^eth|^enp|^bond|^br|^vlan"):
        cleaned_networks = []
        networks = psutil.net_if_addrs()
        for idx, network in enumerate(networks):
            is_valid = re.search(network_regex, network)
            if (is_valid):
                network_details = networks[network]
                for address_details in network_details:
                    if (address_details.netmask and address_details.family == 2):
                        netmask_bits = IPAddress(address_details.netmask).netmask_bits()
                        network_details = dict(network=network, netmask=netmask_bits, address=address_details.address)
                        cleaned_networks.append(network_details)
        return cleaned_networks

    def getUsage(self):
        zfs_pools = []
        pool_raw_rows = ((os.popen('zpool list -H')).read()).strip().split('\n')
        pool_names = self.getPoolNames()
        for row in pool_names:
            row_index = row["id"]
            pool_name = row["pool_name"]
            indexed_row = self.parsePoolData(pool_raw_rows[row_index])
            zfs_pools.append(dict(pool_name=pool_name, data=indexed_row))
        return zfs_pools

    def poolNameSorter(self, val):
        return val["cleaned_name"]

    def getPoolNames(self):
        pool_names_raw = ((os.popen("zpool list -H | awk '{print$1}'")).read()).strip().split('\n')
        pool_names_clean = []
        for idx, pool in enumerate(pool_names_raw):
            cleaned_name = pool.lower().replace("-", "-")
            dict_obj = dict(pool_name=pool, id=idx, cleaned_name=cleaned_name)
            pool_names_clean.append(dict_obj)
        pool_names_clean.sort(key=self.poolNameSorter)
        return pool_names_clean

    def getEmptyDictionary(self):
        return dict(size="", allocated="", free="", health="", frag="", cap="")

    def parsePoolData(self, pool_data):
        pool_data_dict = self.getEmptyDictionary()
        formatted_data = pool_data.strip().split('\t')
        # TOTAL POOL SIZE
        pool_data_dict["size"] = formatted_data[1].strip()
        # TOTAL POOL CAP ALLOCATED
        pool_data_dict["allocated"] = formatted_data[2].strip()
        # TOTAL POOL CAP FREE
        pool_data_dict["free"] = formatted_data[3].strip()
        # POOL FRAGMENTATION PERCENTAGE
        pool_data_dict["frag"] = formatted_data[6].strip()
        # AMOUNT OF POOL USED PERCENTAGE
        pool_data_dict["cap"] = formatted_data[7].strip()
        # HEALTH STATUS
        pool_data_dict["health"] = formatted_data[9].strip()
        return pool_data_dict

    def timerCallback(self):
        self.Lcd.disable()

    def timerReset(self, t=None):
        if t:
            t.cancel()
        t = threading.Timer(self.blankLcdTimeout, self.timerCallback)
        t.start()
        return t

    def run(self):
        while self.Running:
            self.t = self.timerReset(self.t)
            self.Lcd.enable()
            data = self.getDataArray()
            self.Lcd.write(0, data[self.infoIndex][0])
            self.Lcd.write(1, data[self.infoIndex][1])
            if self.Lcd.read() == "Up":
                delta = -1
            else:
                delta = +1
            self.infoIndex = (self.infoIndex + delta) % len(data)
