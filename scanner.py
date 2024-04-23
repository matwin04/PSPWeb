import scapy.all as scapy
import sqlite3
import time
import subprocess
import socket
import platform
import json


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for client in results_list:
        print(client['ip'] + "\t\t" + client["mac"])

def create_table(cursor):
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT,
                    mac TEXT)''')

def insert_data(cursor, ip, mac, status, hostname):
    try:
        # Check if the device entry already exists
        cursor.execute("SELECT * FROM devices WHERE ip=?", (ip,))
        existing_entry = cursor.fetchone()
        if not existing_entry:
            cursor.execute('''INSERT INTO devices (ip, mac, status, hostname)
                            VALUES (?, ?, ?, ?)''', (ip, mac, status, hostname))
            print("Inserted:", ip, mac, status, hostname)
        else:
            print("Skipped insertion for existing entry:", ip)
    except Exception as e:
        print("Error occurred during insertion:", e)

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return "Unknown"
def update_status(cursor):
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    for device in devices:
        ip = device[1]
        # Ping the device to check its status
        if platform.system() == 'Darwin':  # macOS
            ping_result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        elif platform.system() == 'Windows':  # Windows
            ping_result = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        else:
            ping_result = 1  # Unknown system, assume device is offline

        if ping_result == 0:
            status = "online"
        else:
            status = "offline"
        cursor.execute("UPDATE devices SET status=? WHERE ip=?", (status, ip))
# Load Config
conn = sqlite3.connect('net.db')
cursor = conn.cursor()
# Adjusted IP range to exclude router's IP
# Main loop to scan and reload every 15 seconds
while True:
    # Connect to the database
    conn = sqlite3.connect('net.db')
    cursor = conn.cursor()

    try:
        # Adjusted IP range to exclude router's IP
        scan_result = scan("192.168.10.1/24")

        for client in scan_result:
            hostname = get_hostname(client["ip"])
            insert_data(cursor, client["ip"], client["mac"], 'unknown', hostname)

        update_status(cursor)

        conn.commit()
        print("Results saved")
        
        # Print the results after saving
        print_result(scan_result)
    except Exception as e:
        print("Error occurred:", e)
    finally:
        # Close the database connection
        conn.close()

    # Wait for 15 seconds before the next scan
    time.sleep(15)
