import csv
base=r"C:\Users\madlyn\Downloads\RecSys Final Project\data\FAR-Trans"
target="053789536FAA9E9B3023"
# customer_information row numbers
with open(base+"\\customer_information.csv",newline='',encoding='utf-8') as f:
    r=csv.reader(f)
    header=next(r)
    for i,row in enumerate(r, start=2):
        if row and row[0]==target:
            print("CUSTOMER ROW", i)
            print("HEADER:", header)
            print("VALUES:", row)
# transactions row numbers
with open(base+"\\transactions.csv",newline='',encoding='utf-8') as f:
    r=csv.reader(f)
    header=next(r)
    for i,row in enumerate(r, start=2):
        if row and row[0]==target:
            print("TX ROW", i, row)
# asset info for ISINs
assets={}
with open(base+"\\asset_information.csv",newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        assets[row['ISIN']]=row
for isin in ["GRS434003000","GRC4971221B3"]:
    print("ASSET", isin, assets.get(isin))