# HW3 analysis

## 1. nDCG@10
n = 11 labelled users out of 100.

| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0286 | 0.2599 |
| Latest buy | 0.0277 | 0.2520 |
| Latest buy or sell | 0.0271 | 0.2464 |
| CBF (initial candidate order, matched control) | 0.0201 | 0.1827 |
| B (raw history, no summary) | 0.0228 | 0.2076 |
| C (summary only) | 0.0248 | 0.2257 |
| D (summary + risk level and capacity) | 0.0220 | 0.1996 |
| E (D with shuffled profiles) | 0.0209 | 0.1899 |

## 2. Paired differences (first minus second)
No significance test is reported because of the small number of labelled users.
D - C: all -0.0029, labelled -0.0262, higher 1 lower 2 equal 97
E - D: all -0.0011, labelled -0.0097, higher 1 lower 1 equal 98
C - B: all 0.0020, labelled 0.0181, higher 1 lower 0 equal 99
B - cbf: all 0.0027, labelled 0.0249, higher 3 lower 0 equal 97

## 3. Top-10 list overlap
B vs cbf: identical 45 of 100, mean overlap 7.24
C vs cbf: identical 28 of 100, mean overlap 6.47
D vs cbf: identical 30 of 100, mean overlap 6.51
E vs cbf: identical 28 of 100, mean overlap 6.41
D vs C: identical 43 of 100, mean overlap 8.12
E vs D: identical 62 of 100, mean overlap 8.50
C vs B: identical 40 of 100, mean overlap 7.70

## 4. Candidate coverage
users with future purchases and none of their purchases among the 50 candidates: 5
oracle ceiling nDCG@10: all 0.0492, labelled 0.4469

## 5. LLM runs
| Arm | users | invalid_outputs | wall_seconds_whole_arm | resolved_commit | risk | capacity |
|---|---:|---:|---:|---|---:|---:|
| B | 100 | 0 | 5568.4 | 70d244cc86cc | 0 | 0 |
| C | 100 | 0 | 8367.7 | 70d244cc86cc | 0 | 0 |
| D | 100 | 0 | 11205.8 | 70d244cc86cc | 98 | 97 |
| E | 100 | 0 | 10194.0 | 70d244cc86cc | 100 | 100 |

## 6. Profile availability
users with a profile: 87, without: 13
D differs from C in the top-10: with profile 48, without 9
E vs D: prompt differs for 77 users, keeps own profile 0, identical prompt 23
among prompt-differing users, different top-10 in E vs D: 38
among identical-prompt users, identical ranking in E and D: 23
mean E - D on prompt-differing users: -0.0014

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

totals: future purchases 18, in eligible 18, repeat 12, among 50 candidates 6, of those in positions 1-10 5

## 11. How the ranker changes the candidate order
| Method | mean avg candidate position | slots 1-10 | slots 11-20 | slots 21-50 | users with >=1 asset in 11-50 |
|---|---:|---:|---:|---:|---:|
| cbf | 5.50 | 1000 | 0 | 0 | 0 |
| B | 8.24 | 724 | 224 | 52 | 55 |
| C | 9.39 | 647 | 271 | 82 | 71 |
| D | 9.35 | 651 | 266 | 83 | 66 |
| E | 9.76 | 641 | 261 | 98 | 68 |

| Arm | improved | worsened | stayed same | remained outside |
|---|---:|---:|---:|---:|
| B | 3 | 0 | 2 | 1 |
| C | 3 | 0 | 2 | 1 |
| D | 2 | 1 | 2 | 1 |
| E | 3 | 1 | 1 | 1 |

## 12. By history size
Descriptive only; the groups are small.
### 1 to 5 assets
users 78, labelled 4
| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0190 | 0.3710 |
| Latest buy | 0.0162 | 0.3160 |
| Latest buy or sell | 0.0155 | 0.3026 |
| CBF (initial candidate order, matched control) | 0.0116 | 0.2256 |
| B (raw history, no summary) | 0.0117 | 0.2285 |
| C (summary only) | 0.0143 | 0.2783 |
| D (summary + risk level and capacity) | 0.0143 | 0.2783 |
| E (D with shuffled profiles) | 0.0103 | 0.2016 |
### 6 or more assets
users 22, labelled 7
| Method | nDCG@10 (all) | nDCG@10 (labelled) |
|---|---:|---:|
| Popularity | 0.0625 | 0.1965 |
| Latest buy | 0.0686 | 0.2155 |
| Latest buy or sell | 0.0682 | 0.2143 |
| CBF (initial candidate order, matched control) | 0.0504 | 0.1583 |
| B (raw history, no summary) | 0.0623 | 0.1957 |
| C (summary only) | 0.0623 | 0.1957 |
| D (summary + risk level and capacity) | 0.0492 | 0.1546 |
| E (D with shuffled profiles) | 0.0583 | 0.1832 |

## 13. Bootstrap intervals
Descriptive intervals only; no significance test is performed.
D - C, all: n=100 mean=-0.0029 2.5%=-0.0082 97.5%=0.0009 share<0=0.8634
D - C, labelled: n=11 mean=-0.0262 2.5%=-0.0721 97.5%=0.0079 share<0=0.8890
E - D, all: n=100 mean=-0.0011 2.5%=-0.0092 97.5%=0.0060 share<0=0.5365
E - D, labelled: n=11 mean=-0.0097 2.5%=-0.0836 97.5%=0.0546 share<0=0.5518
C - B, all: n=100 mean=0.0020 2.5%=0.0000 97.5%=0.0060 share<0=0.0000
C - B, labelled: n=11 mean=0.0181 2.5%=0.0000 97.5%=0.0543 share<0=0.0000
B - cbf, all: n=100 mean=0.0027 2.5%=0.0000 97.5%=0.0067 share<0=0.0000
B - cbf, labelled: n=11 mean=0.0249 2.5%=0.0000 97.5%=0.0595 share<0=0.0000
