# RQ4 results: Arm C vs Arm D

Teaching settings: cutoff **2021-06-01**, 30-day evaluation window, **100 users** (starter defaults, not the final project protocol).

Protocol hash identical across baseline, arm C and arm D: **yes**

## Results table

| Method | Users | Users with future purchases | nDCG@10 (all users) | nDCG@10 (nonempty truth) | Runtime | Failed cases |
|---|---:|---:|---:|---:|---:|---:|
| Popularity | 100 | 11 | 0.0286 | 0.2599 | not timed separately | 0 |
| CBF | 100 | 11 | 0.0201 | 0.1827 | not timed separately | 0 |
| Latest buy | 100 | 11 | 0.0277 | 0.2520 | not timed separately | 0 |
| Latest buy or sell | 100 | 11 | 0.0271 | 0.2464 | not timed separately | 0 |
| Arm C | 100 | 11 | 0.0248 | 0.2257 | 8367.7 s | 0 |
| Arm D | 100 | 11 | 0.0220 | 0.1996 | 11205.8 s | 0 |

## Paired comparison: Arm D minus Arm C (same 100 users)

- Mean nDCG@10 difference (all users): **-0.0029**
- Mean nDCG@10 difference (nonempty truth, 11 users): **-0.0262**
- Users where D scored higher: **1**
- Users where D scored lower: **2**
- Users where D scored equal: **97**
- Identical top-10 lists (same order): **43**
- Same set of assets in a different order: **1**
- Mean top-10 overlap (out of 10): **8.1200**
- Invalid model outputs (CBF fallbacks): arm C **0**, arm D **0**
- Arm D users with an unavailable profile at the cutoff: **13**
- Rough profile-keyword count in D summaries (100 summaries): **790**
  - risk: 170, conservative: 6, aggressive: 12, balanced: 63, moderate: 60, capacity: 108, profile: 93, income: 48, growth: 8, investor: 198, suitability: 2, tolerance: 22

## Users with future purchases

| User | CBF nDCG@10 | C nDCG@10 | D nDCG@10 | D - C | C and D identical top-10 |
|---|---:|---:|---:|---:|---|
| 870E814DB274CFA95600 | 0.6131 | 0.6131 | 0.6131 | 0.0000 | no |
| 6BAA2D5FBCCEAB57C473 | 0.5000 | 0.6309 | 0.4307 | -0.2003 | no |
| 94A16DE0F59F24BB77C2 | 0.5000 | 0.6309 | 0.5000 | -0.1309 | no |
| 6FA5BF73C309CE8E9ED5 | 0.1078 | 0.1078 | 0.1513 | 0.0435 | no |
| 6B15913A38A56CB253E0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no |
| 29C0592F254DB2430C00 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no |
| 0E72D1BF99E858EEE1AA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | yes |
| D63DFAE7E53493A5ADD5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | yes |
| 5087D23F907F90F3DDD1 | 0.2891 | 0.5000 | 0.5000 | 0.0000 | no |
| 8A220D47B1644E4FD349 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no |
| 5180B50A10AAD1C7D0F8 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no |
