import csv, collections
base=r"C:\Users\madlyn\Downloads\RecSys Final Project\data\FAR-Trans"
# load sparse customers
sparse=set()
with open(base+"\\..\\sparse_customers.txt") as f:
    for line in f:
        sparse.add(line.strip())
# transactions by customer
tx_by=collections.defaultdict(list)
with open(base+"\\transactions.csv",newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['customerID'] in sparse:
            tx_by[row['customerID']].append(row)
# customer info
cust_by=collections.defaultdict(list)
with open(base+"\\customer_information.csv",newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cust_by[row['customerID']].append(row)
# find a sparse customer with 2-3 buys and profile with non-missing risk/capacity
found=0
for cid,txs in tx_by.items():
    if len(txs)<2 or len(txs)>3: 
        continue
    infos=cust_by.get(cid,[])
    if not infos: 
        continue
    # choose latest info before first tx? We'll just show last info
    # require riskLevel not Not_Available and capacity not Not_Available
    info=infos[-1]
    if info['riskLevel']=='Not_Available' or info['investmentCapacity']=='Not_Available':
        continue
    # ensure at least one Buy
    if not any(t['transactionType']=='Buy' for t in txs):
        continue
    print("CUSTOMER:", cid)
    print("NUM TX:", len(txs))
    print("--- customer_information rows ---")
    for r in infos:
        print(r)
    print("--- transactions ---")
    for t in txs:
        print(t)
    found+=1
    if found>=3:
        break
print("found", found)