# HW3 analysis

## 1. nDCG@10
n = 13 labelled users out of 100.

| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0399 | 0.3066 |
| Latest buy | 0.0670 | 0.5153 |
| Latest buy or sell | 0.0697 | 0.5361 |
| CBF (initial candidate order, matched control) | 0.0408 | 0.3141 |
| B (raw history, no summary) | 0.0379 | 0.2916 |
| C (summary only) | 0.0324 | 0.2494 |
| D (summary + risk level and capacity) | 0.0308 | 0.2366 |
| E (D with shuffled profiles) | 0.0308 | 0.2366 |

## 2. Paired differences (first minus second)
No significance test is reported because of the small number of labelled users.
D - C: all -0.0017, labelled -0.0128, higher 0 lower 2 equal 98
E - D: all 0.0000, labelled 0.0000, higher 0 lower 0 equal 100
C - B: all -0.0055, labelled -0.0422, higher 0 lower 3 equal 97
B - cbf: all -0.0029, labelled -0.0225, higher 4 lower 2 equal 94

## 3. Top-10 list overlap
B vs cbf: identical 43 of 100, mean overlap 7.23
C vs cbf: identical 21 of 100, mean overlap 6.32
D vs cbf: identical 27 of 100, mean overlap 6.30
E vs cbf: identical 21 of 100, mean overlap 6.06
D vs C: identical 36 of 100, mean overlap 7.62
E vs D: identical 54 of 100, mean overlap 8.42
C vs B: identical 31 of 100, mean overlap 7.26

## 4. Candidate coverage
users with future purchases and none of their purchases among the 50 candidates: 4
oracle ceiling nDCG@10: all 0.0671, labelled 0.5162

## 5. LLM runs
| Arm | users | invalid_outputs | wall_seconds_whole_arm | resolved_commit | risk | capacity |
|---|---:|---:|---:|---|---:|---:|
| B | 100 | 0 | 4985.8 | 70d244cc86cc | 0 | 0 |
| C | 100 | 0 | 8682.8 | 70d244cc86cc | 0 | 0 |
| D | 100 | 0 | 9993.8 | 70d244cc86cc | 100 | 97 |
| E | 100 | 0 | 9939.8 | 70d244cc86cc | 99 | 96 |

## 6. Profile availability
users with a profile: 91, without: 9
D differs from C in the top-10: with profile 59, without 5
E vs D: prompt differs for 80 users, keeps own profile 0, identical prompt 20
among prompt-differing users, different top-10 in E vs D: 46
among identical-prompt users, identical ranking in E and D: 20
mean E - D on prompt-differing users: 0.0000

## 7. Labelled users
| Label | future purchases | in candidates | CBF | B | C | D | E |
|---|---|---|---|---|---|---|---:|
| U010 | 3 | 2 | 0.3172 | 0.2021 | 0.1564 | 0.1564 | 0.1564 |
| U017 | 1 | 1 | 0.3010 | 0.5000 | 0.3869 | 0.3010 | 0.3010 |
| U027 | 2 | 1 | 0.3066 | 0.3869 | 0.3869 | 0.3066 | 0.3066 |
| U035 | 5 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U040 | 2 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U045 | 1 | 1 | 0.6309 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U048 | 4 | 1 | 0.2463 | 0.3904 | 0.0000 | 0.0000 | 0.0000 |
| U064 | 6 | 2 | 0.2381 | 0.2684 | 0.2684 | 0.2684 | 0.2684 |
| U076 | 5 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U091 | 1 | 1 | 0.6309 | 0.6309 | 0.6309 | 0.6309 | 0.6309 |
| U094 | 4 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U096 | 1 | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| U098 | 7 | 2 | 0.4123 | 0.4123 | 0.4123 | 0.4123 | 0.4123 |

## 8. Hand-worked nDCG@10
user U017, 1 future purchase(s)
ideal DCG terms: 1.0000 -> ideal DCG = 1.0000
cbf: rank 9 GRS496003005 0.3010 -> DCG = 0.3010, nDCG = 0.3010 (script 0.3010)
B: rank 3 GRS496003005 0.5000 -> DCG = 0.5000, nDCG = 0.5000 (script 0.5000)
C: rank 5 GRS496003005 0.3869 -> DCG = 0.3869, nDCG = 0.3869 (script 0.3869)
D: rank 9 GRS496003005 0.3010 -> DCG = 0.3010, nDCG = 0.3010 (script 0.3010)
E: rank 9 GRS496003005 0.3010 -> DCG = 0.3010, nDCG = 0.3010 (script 0.3010)

## 9. Where the purchased assets sit
| Label | future purchases | in eligible | repeat | candidate positions |
|---|---:|---:|---:|---|
| U010 | 3 | 3 | 2 | 5, 10 |
| U017 | 1 | 1 | 1 | 9 |
| U027 | 2 | 2 | 2 | 3 |
| U035 | 5 | 5 | 2 | - |
| U040 | 2 | 2 | 1 | - |
| U045 | 1 | 1 | 0 | 2 |
| U048 | 4 | 4 | 4 | 2 |
| U064 | 6 | 6 | 2 | 4, 6 |
| U076 | 5 | 5 | 5 | - |
| U091 | 1 | 1 | 1 | 2 |
| U094 | 4 | 4 | 3 | - |
| U096 | 1 | 1 | 1 | 1 |
| U098 | 7 | 7 | 2 | 1, 3 |

totals: future purchases 42, in eligible 42, repeat 26, among 50 candidates 12, of those in positions 1-10 12

## 11. How the ranker changes the candidate order
| Method | mean avg candidate position | slots 1-10 | slots 11-20 | slots 21-50 | users with >=1 asset in 11-50 |
|---|---:|---:|---:|---:|---:|
| cbf | 5.50 | 1000 | 0 | 0 | 0 |
| B | 8.70 | 723 | 202 | 75 | 51 |
| C | 9.83 | 632 | 270 | 98 | 76 |
| D | 9.44 | 630 | 286 | 84 | 73 |
| E | 9.88 | 606 | 294 | 100 | 77 |

| Arm | improved | worsened | stayed same | remained outside |
|---|---:|---:|---:|---:|
| B | 6 | 2 | 4 | 0 |
| C | 5 | 3 | 4 | 0 |
| D | 3 | 3 | 6 | 0 |
| E | 3 | 3 | 6 | 0 |

## 12. By history size
Descriptive only; the groups are small.
### 1 to 5 assets
users 82, labelled 5
| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0230 | 0.3767 |
| Latest buy | 0.0338 | 0.5544 |
| Latest buy or sell | 0.0324 | 0.5316 |
| CBF (initial candidate order, matched control) | 0.0325 | 0.5323 |
| B (raw history, no summary) | 0.0258 | 0.4229 |
| C (summary only) | 0.0238 | 0.3911 |
| D (summary + risk level and capacity) | 0.0228 | 0.3740 |
| E (D with shuffled profiles) | 0.0228 | 0.3740 |
### 6 or more assets
users 18, labelled 8
| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.1168 | 0.2628 |
| Latest buy | 0.2182 | 0.4909 |
| Latest buy or sell | 0.2395 | 0.5389 |
| CBF (initial candidate order, matched control) | 0.0790 | 0.1777 |
| B (raw history, no summary) | 0.0931 | 0.2096 |
| C (summary only) | 0.0715 | 0.1608 |
| D (summary + risk level and capacity) | 0.0670 | 0.1507 |
| E (D with shuffled profiles) | 0.0670 | 0.1507 |

## 13. Bootstrap intervals
Descriptive intervals only; no significance test is performed.
D - C, all: n=100 mean=-0.0017 2.5%=-0.0042 97.5%=0.0000 share<0=0.8696
D - C, labelled: n=13 mean=-0.0128 2.5%=-0.0317 97.5%=0.0000 share<0=0.8897
E - D, all: n=100 mean=0.0000 2.5%=0.0000 97.5%=0.0000 share<0=0.0000
E - D, labelled: n=13 mean=0.0000 2.5%=0.0000 97.5%=0.0000 share<0=0.0000
C - B, all: n=100 mean=-0.0055 2.5%=-0.0149 97.5%=0.0000 share<0=0.9510
C - B, labelled: n=13 mean=-0.0422 2.5%=-0.1075 97.5%=0.0000 share<0=0.9644
B - cbf, all: n=100 mean=-0.0029 2.5%=-0.0186 97.5%=0.0080 share<0=0.6202
B - cbf, labelled: n=13 mean=-0.0225 2.5%=-0.1421 97.5%=0.0593 share<0=0.6297
