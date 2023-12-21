import csv
import sqlite3
import pandas as pd
import ipaddress

netflow_df = pd.read_csv('archive/test-rules.csv')
conn = sqlite3.connect("archive/netflow-records.db")
    
subnets_dev_str = [
    '10.20.42.0/23'
]

subnets_acc_str = [
    '10.20.44.0/24'
]

subnets_prod_str = [
    '10.20.30.0/23',
    '10.20.128.0/24'
]

subnets_dev = []
for subnet_dev_str in subnets_dev_str:
    subnets_dev.append(ipaddress.ip_network(subnet_dev_str))
print(subnets_dev)

subnets_acc = []
for subnet_acc_str in subnets_acc_str:
    subnets_acc.append(ipaddress.ip_network(subnet_acc_str))
print(subnets_acc)  

subnets_prod = []
for subnet_prod_str in subnets_prod_str:
    subnets_prod.append(ipaddress.ip_network(subnet_prod_str))
print(subnets_prod)

# Raw Netflow records
netflow_df.to_sql("netflow", conn, if_exists='replace', index=False)
print("Number of netflow records: " + str(len(netflow_df)))

# Unique Netflow records
netflow_unique_df = netflow_df.drop_duplicates()
print("Unique number of netflow records: " + str(len(netflow_unique_df)))

# Drop records where source subnet equals destination subnet
netflow_unique_external_df = pd.DataFrame(columns=['src_ip', 'dst_ip', 'protocol', 'dst_port'])
for index, row in netflow_unique_df.iterrows():
    src_ip = ipaddress.ip_address(row['src_ip'])
    dst_ip = ipaddress.ip_address(row['dst_ip'])
    keeprecord = 1
    for subnet_dev in subnets_dev:
        if src_ip in subnet_dev and dst_ip in subnet_dev:
            #print("Removed " + row['src_ip'] + "->" + row['dst_ip'])
            keeprecord = 0
    for subnet_acc in subnets_acc:
        if src_ip in subnet_acc and dst_ip in subnet_acc:
            #print("Removed " + row['src_ip'] + "->" + row['dst_ip'])
            keeprecord = 0
    for subnet_prod in subnets_prod:
        if src_ip in subnet_prod and dst_ip in subnet_prod:
            #print("Removed " + row['src_ip'] + "->" + row['dst_ip'])
            keeprecord = 0
    #if not keeprecord:
    #    print(row['src_ip'] + "->" + row['dst_ip'] + " not found")
    if keeprecord: 
        netflow_unique_external_df = pd.concat([netflow_unique_external_df, pd.DataFrame([row], columns=['src_ip', 'dst_ip', 'protocol', 'dst_port'])])


unique_dst_ip_values = netflow_unique_external_df['dst_ip'].unique()
print("Unique destination IP's: " + str(len(unique_dst_ip_values)))


for dst_ip_str in unique_dst_ip_values:
    found = 0
    dst_ip = ipaddress.ip_address(dst_ip_str)
    for subnet_dev in subnets_dev:
        if dst_ip in subnet_dev:
            print(dst_ip_str + " in dev")
            found = 1
    for subnet_acc in subnets_acc:
        if dst_ip in subnet_acc:
            print(dst_ip_str + " in acc")
            found = 1
    for subnet_prod in subnets_prod:
        if dst_ip in subnet_prod:
            print(dst_ip_str + " in prod")
            found = 1
    if not found:
        print(dst_ip_str + " not found")



conn.close()