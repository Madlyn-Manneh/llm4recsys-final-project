# cand2_check

## Step 1: users whose top-10 contains candidate p (p=1..10)

| Arm | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---:|
| B | 195 | 147 | 148 | 139 | 146 | 152 | 152 | 129 | 106 | 133 |
| C | 196 | 134 | 145 | 114 | 128 | 129 | 135 | 114 | 78 | 106 |
| D | 196 | 137 | 139 | 120 | 127 | 133 | 134 | 113 | 79 | 103 |
| E | 192 | 135 | 138 | 115 | 124 | 130 | 131 | 112 | 76 | 94 |

## Step 2

| Arm | top10 has 1 and 3, not 2 | top10 does not contain 2 |
|---|---:|---:|
| B | 9 | 53 |
| C | 27 | 66 |
| D | 20 | 63 |
| E | 20 | 65 |

## Step 3

users with at least one future purchase: 24
of those, none of their future ISINs among the 50 candidates: 9
users with a future purchase at candidate position 2: 3

| Arm | of those, with candidate 2 in top 10 |
|---|---:|
| B | 2 |
| C | 1 |
| D | 1 |
| E | 1 |
