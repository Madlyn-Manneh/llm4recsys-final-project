import csv, collections
base=r"C:\Users\madlyn\Downloads\RecSys Final Project\data\FAR-Trans"
counts=collections.Counter()
buy_counts=collections.Counter()
with open(base+"\\transactions.csv",newline='',encoding='utf-8') as f:
    r=csv.DictReader(f)
    for row in r:
        counts[row['customerID']]+=1
        if row['transactionType']=='Buy':
            buy_counts[row['customerID']]+=1
print("unique customers in transactions:", len(counts))
print("min/max/mean counts:", min(counts.values()), max(counts.values()), sum(counts.values())/len(counts))
dist=collections.Counter(counts.values())
print("first 20 count distribution:", sorted(dist.items())[:20])
sparse=[c for c,n in counts.items() if n<=5]
print("customers with <=5 tx:", len(sparse))
print("example sparse customers:", sparse[:10])
# save sparse list
with open(base+"\\..\\sparse_customers.txt","w") as f:
    for c in sparse:
        f.write(c+"\n")