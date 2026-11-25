# HW3 analysis

## 0. Samples
| Sample | users | labelled | protocol_hash |
|---|---:|---:|---|
| 1 | 100 | 11 | 50efd4aeb415 |
| 2 | 100 | 13 | 5bae3e69d666 |

## 1. nDCG@10
n = 24 labelled users out of 200.

| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0342 | 0.2852 |
| Latest buy | 0.0474 | 0.3946 |
| Latest buy or sell | 0.0484 | 0.4033 |
| CBF (initial candidate order, matched control) | 0.0305 | 0.2539 |
| B (raw history, no summary) | 0.0304 | 0.2531 |
| C (summary only) | 0.0286 | 0.2385 |
| D (summary + risk level and capacity) | 0.0264 | 0.2196 |
| E (D with shuffled profiles) | 0.0258 | 0.2152 |

## 2. Paired differences (first minus second)
No significance test is reported because of the small number of labelled users.
D - C: all -0.0023, labelled -0.0189, higher 1 lower 4 equal 195
E - D: all -0.0005, labelled -0.0044, higher 1 lower 1 equal 198
C - B: all -0.0018, labelled -0.0146, higher 1 lower 3 equal 196
B - cbf: all -0.0001, labelled -0.0008, higher 7 lower 2 equal 191

## 3. Top-10 list overlap
B vs cbf: identical 88 of 200, mean overlap 7.24
C vs cbf: identical 49 of 200, mean overlap 6.39
D vs cbf: identical 57 of 200, mean overlap 6.41
E vs cbf: identical 49 of 200, mean overlap 6.24
D vs C: identical 79 of 200, mean overlap 7.87
E vs D: identical 116 of 200, mean overlap 8.46
C vs B: identical 71 of 200, mean overlap 7.48

## 4. Candidate coverage
users with future purchases and none of their purchases among the 50 candidates: 9
oracle ceiling nDCG@10: all 0.0581, labelled 0.4844

## 5. LLM runs
| Arm | sample | users | invalid_outputs | wall_seconds_whole_arm | resolved_commit | risk | capacity |
|---|---:|---:|---:|---:|---|---:|---:|
| B | 1 | 100 | 0 | 5568.4 | 70d244cc86cc | 0 | 0 |
| B | 2 | 100 | 0 | 4985.8 | 70d244cc86cc | 0 | 0 |
| B | sum | 200 | 0 | 10554.2 | | 0 | 0 |
| C | 1 | 100 | 0 | 8367.7 | 70d244cc86cc | 0 | 0 |
| C | 2 | 100 | 0 | 8682.8 | 70d244cc86cc | 0 | 0 |
| C | sum | 200 | 0 | 17050.5 | | 0 | 0 |
| D | 1 | 100 | 0 | 11205.8 | 70d244cc86cc | 98 | 97 |
| D | 2 | 100 | 0 | 9993.8 | 70d244cc86cc | 100 | 97 |
| D | sum | 200 | 0 | 21199.6 | | 198 | 194 |
| E | 1 | 100 | 0 | 10194.0 | 70d244cc86cc | 100 | 100 |
| E | 2 | 100 | 0 | 9939.8 | 70d244cc86cc | 99 | 96 |
| E | sum | 200 | 0 | 20133.8 | | 199 | 196 |

## 6. Profile availability
users with a profile: 178, without: 22
D differs from C in the top-10: with profile 107, without 14
E vs D: prompt differs for 157 users, keeps own profile 0, identical prompt 43
among prompt-differing users, different top-10 in E vs D: 84
among identical-prompt users, identical ranking in E and D: 43
mean E - D on prompt-differing users: -0.0007
cross-sample profile donors in E: 0

## 7. Labelled users
| Label | future purchases | in candidates | CBF | B | C | D | E |
|---|---|---|---|---|---|---|---:|
| U030 | 2 | 1 | 0.6131 | 0.6131 | 0.6131 | 0.6131 | 0.3066 |
| U031 | 1 | 1 | 0.5000 | 0.6309 | 0.6309 | 0.4307 | 0.6309 |
| U039 | 1 | 1 | 0.5000 | 0.6309 | 0.6309 | 0.5000 | 0.5000 |
| U045 | 6 | 1 | 0.1078 | 0.1078 | 0.1078 | 0.1513 | 0.1513 |
| U047 | 1 | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U048 | 1 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U049 | 1 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U056 | 1 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U069 | 1 | 1 | 0.2891 | 0.3010 | 0.5000 | 0.5000 | 0.5000 |
| U072 | 1 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U094 | 2 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U110 | 3 | 2 | 0.3172 | 0.2021 | 0.1564 | 0.1564 | 0.1564 |
| U117 | 1 | 1 | 0.3010 | 0.5000 | 0.3869 | 0.3010 | 0.3010 |
| U127 | 2 | 1 | 0.3066 | 0.3869 | 0.3869 | 0.3066 | 0.3066 |
| U135 | 5 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U140 | 2 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U145 | 1 | 1 | 0.6309 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U148 | 4 | 1 | 0.2463 | 0.3904 | 0.0000 | 0.0000 | 0.0000 |
| U164 | 6 | 2 | 0.2381 | 0.2684 | 0.2684 | 0.2684 | 0.2684 |
| U176 | 5 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U191 | 1 | 1 | 0.6309 | 0.6309 | 0.6309 | 0.6309 | 0.6309 |
| U194 | 4 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| U196 | 1 | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| U198 | 7 | 2 | 0.4123 | 0.4123 | 0.4123 | 0.4123 | 0.4123 |

## 8. Hand-worked nDCG@10
user U031, 1 future purchase(s)
ideal DCG terms: 1.0000 -> ideal DCG = 1.0000
cbf: rank 3 GRS419003009 0.5000 -> DCG = 0.5000, nDCG = 0.5000 (script 0.5000)
B: rank 2 GRS419003009 0.6309 -> DCG = 0.6309, nDCG = 0.6309 (script 0.6309)
C: rank 2 GRS419003009 0.6309 -> DCG = 0.6309, nDCG = 0.6309 (script 0.6309)
D: rank 4 GRS419003009 0.4307 -> DCG = 0.4307, nDCG = 0.4307 (script 0.4307)
E: rank 2 GRS419003009 0.6309 -> DCG = 0.6309, nDCG = 0.6309 (script 0.6309)

## 9. Where the purchased assets sit
| Label | future purchases | in eligible | repeat | candidate positions |
|---|---:|---:|---:|---|
| U030 | 2 | 2 | 2 | 1 |
| U031 | 1 | 1 | 1 | 3 |
| U039 | 1 | 1 | 1 | 3 |
| U045 | 6 | 6 | 6 | 6 |
| U047 | 1 | 1 | 0 | 39 |
| U048 | 1 | 1 | 0 | - |
| U049 | 1 | 1 | 0 | - |
| U056 | 1 | 1 | 0 | - |
| U069 | 1 | 1 | 1 | 10 |
| U072 | 1 | 1 | 0 | - |
| U094 | 2 | 2 | 1 | - |
| U110 | 3 | 3 | 2 | 5, 10 |
| U117 | 1 | 1 | 1 | 9 |
| U127 | 2 | 2 | 2 | 3 |
| U135 | 5 | 5 | 2 | - |
| U140 | 2 | 2 | 1 | - |
| U145 | 1 | 1 | 0 | 2 |
| U148 | 4 | 4 | 4 | 2 |
| U164 | 6 | 6 | 2 | 4, 6 |
| U176 | 5 | 5 | 5 | - |
| U191 | 1 | 1 | 1 | 2 |
| U194 | 4 | 4 | 3 | - |
| U196 | 1 | 1 | 1 | 1 |
| U198 | 7 | 7 | 2 | 1, 3 |

totals: future purchases 60, in eligible 60, repeat 38, among 50 candidates 18, of those in positions 1-10 17

## 10. Per-sample and pooled nDCG@10
| Method | sample 1 all | sample 1 labelled | sample 2 all | sample 2 labelled | pooled all | pooled labelled |
|---|---|---|---|---|---|---:|
| Popularity | 0.0286 | 0.2599 | 0.0399 | 0.3066 | 0.0342 | 0.2852 |
| Latest buy | 0.0277 | 0.2520 | 0.0670 | 0.5153 | 0.0474 | 0.3946 |
| Latest buy or sell | 0.0271 | 0.2464 | 0.0697 | 0.5361 | 0.0484 | 0.4033 |
| CBF (initial candidate order, matched control) | 0.0201 | 0.1827 | 0.0408 | 0.3141 | 0.0305 | 0.2539 |
| B (raw history, no summary) | 0.0228 | 0.2076 | 0.0379 | 0.2916 | 0.0304 | 0.2531 |
| C (summary only) | 0.0248 | 0.2257 | 0.0324 | 0.2494 | 0.0286 | 0.2385 |
| D (summary + risk level and capacity) | 0.0220 | 0.1996 | 0.0308 | 0.2366 | 0.0264 | 0.2196 |
| E (D with shuffled profiles) | 0.0209 | 0.1899 | 0.0308 | 0.2366 | 0.0258 | 0.2152 |

## 11. How the ranker changes the candidate order
| Method | mean avg candidate position | slots 1-10 | slots 11-20 | slots 21-50 | users with >=1 asset in 11-50 |
|---|---:|---:|---:|---:|---:|
| cbf | 5.50 | 2000 | 0 | 0 | 0 |
| B | 8.47 | 1447 | 426 | 127 | 106 |
| C | 9.61 | 1279 | 541 | 180 | 147 |
| D | 9.40 | 1281 | 552 | 167 | 139 |
| E | 9.82 | 1247 | 555 | 198 | 145 |

| Arm | improved | worsened | stayed same | remained outside |
|---|---:|---:|---:|---:|
| B | 9 | 2 | 6 | 1 |
| C | 8 | 3 | 6 | 1 |
| D | 5 | 4 | 8 | 1 |
| E | 6 | 4 | 7 | 1 |

## 12. By history size
Descriptive only; the groups are small.
### 1 to 5 assets
users 160, labelled 9
| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0210 | 0.3741 |
| Latest buy | 0.0252 | 0.4485 |
| Latest buy or sell | 0.0242 | 0.4299 |
| CBF (initial candidate order, matched control) | 0.0223 | 0.3960 |
| B (raw history, no summary) | 0.0189 | 0.3365 |
| C (summary only) | 0.0192 | 0.3410 |
| D (summary + risk level and capacity) | 0.0186 | 0.3314 |
| E (D with shuffled profiles) | 0.0167 | 0.2974 |
### 6 or more assets
users 40, labelled 15
| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0869 | 0.2319 |
| Latest buy | 0.1359 | 0.3623 |
| Latest buy or sell | 0.1453 | 0.3874 |
| CBF (initial candidate order, matched control) | 0.0632 | 0.1686 |
| B (raw history, no summary) | 0.0762 | 0.2031 |
| C (summary only) | 0.0664 | 0.1771 |
| D (summary + risk level and capacity) | 0.0572 | 0.1525 |
| E (D with shuffled profiles) | 0.0622 | 0.1659 |

## 13. Bootstrap intervals
Descriptive intervals only; no significance test is performed.
D - C, all: n=200 mean=-0.0023 2.5%=-0.0052 97.5%=0.0000 share<0=0.9706
D - C, labelled: n=24 mean=-0.0189 2.5%=-0.0421 97.5%=-0.0013 share<0=0.9772
E - D, all: n=200 mean=-0.0005 2.5%=-0.0046 97.5%=0.0030 share<0=0.5308
E - D, labelled: n=24 mean=-0.0044 2.5%=-0.0383 97.5%=0.0250 share<0=0.5352
C - B, all: n=200 mean=-0.0018 2.5%=-0.0069 97.5%=0.0020 share<0=0.7682
C - B, labelled: n=24 mean=-0.0146 2.5%=-0.0554 97.5%=0.0167 share<0=0.7684
B - cbf, all: n=200 mean=-0.0001 2.5%=-0.0081 97.5%=0.0058 share<0=0.4656
B - cbf, labelled: n=24 mean=-0.0008 2.5%=-0.0683 97.5%=0.0473 share<0=0.4659
