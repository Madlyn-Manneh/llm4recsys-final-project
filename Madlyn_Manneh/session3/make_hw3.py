#!/usr/bin/env python3
"""Create llm_rerank_hw3.py from llm_rerank.py by adding arm E (shuffled profiles).

Checks the source hash first. Every replacement must match exactly once.
Usage: python make_hw3.py llm_rerank.py llm_rerank_hw3.py
"""
import hashlib
import sys
from pathlib import Path

SRC_SHA256 = 'D7A34C1F9F715D7437CA5B2CC7989DBFF12348602495B8A427CF8E56FA7007BA'

EDITS = [
("""\"\"\"Shared pipeline for the team arms A, B, C, D (starter FAR-Trans, ranker seam).
""",
"""\"\"\"Shared pipeline for the team arms A, B, C, D, E (starter FAR-Trans, ranker seam).

HW3 copy of llm_rerank.py (SHA-256 D7A34C1F...). The only change is arm E.
"""),
("""                           investmentCapacity (flagged observed / estimated)
""",
"""                           investmentCapacity (flagged observed / estimated)
  E  ablation (HW3)        same as D, but each user whose profile is available at the
                           cutoff gets another user's profile (seeded cyclic shuffle)
"""),
("""choices=['A', 'B', 'C', 'D'], required=True)""",
 """choices=['A', 'B', 'C', 'D', 'E'], required=True)"""),
("""    if arm == 'D':
        parts.append(profile_block(ctx, questionnaire_ok))""",
 """    if arm in ('D', 'E'):
        parts.append(profile_block(ctx, questionnaire_ok))"""),
("""    q_dates = questionnaire_dates(args.data_dir, cutoff, {c['user_id'] for c in contexts})
""",
"""    q_dates = questionnaire_dates(args.data_dir, cutoff, {c['user_id'] for c in contexts})
    donor, by_uid, map_sha = {}, {c['user_id']: c for c in contexts}, None
    if args.arm == 'E':
        # Seeded cyclic shuffle over users whose profile is available at the cutoff:
        # nobody keeps their own profile; unavailable users are left unchanged.
        avail = sorted(u for u in by_uid if q_dates.get(u, '9999') < cutoff)
        assert len(avail) > 1, 'arm E needs at least two users with an available profile'
        random.Random(args.seed).shuffle(avail)
        donor = {u: avail[(i + 1) % len(avail)] for i, u in enumerate(avail)}
        assert all(u != d for u, d in donor.items())
"""),
("""    args.out_dir.mkdir(parents=True, exist_ok=True)
""",
"""    args.out_dir.mkdir(parents=True, exist_ok=True)
    if args.arm == 'E':
        map_text = json.dumps(donor, indent=1, sort_keys=True) + '\\n'
        (args.out_dir / 'profile_shuffle_map.json').write_text(
            map_text, encoding='utf-8', newline='\\n')
        map_sha = hashlib.sha256(map_text.encode('utf-8')).hexdigest()
"""),
("""        for ctx in contexts:
            assert_no_future(ctx)
""",
"""        for ctx in contexts:
            if args.arm == 'E' and ctx['user_id'] in donor:
                ctx = dict(ctx, profile=by_uid[donor[ctx['user_id']]]['profile'])
            assert_no_future(ctx)
"""),
("""            if args.arm == 'D' and not q_ok:""",
 """            if args.arm in ('D', 'E') and not q_ok:"""),
("""            raw.write(json.dumps({'user_id': uid, 'arm': args.arm,
                                  'questionnaire_before_cutoff': q_ok,
                                  'summary_prompt': s_user, 'summary': summary,
                                  'rank_prompt': r_user, 'rank_output': answer,
                                  'parsed_numbers': numbers, 'valid': valid},
                                 ensure_ascii=False) + '\\n')
""",
"""            record = {'user_id': uid, 'arm': args.arm,
                      'questionnaire_before_cutoff': q_ok,
                      'summary_prompt': s_user, 'summary': summary,
                      'rank_prompt': r_user, 'rank_output': answer,
                      'parsed_numbers': numbers, 'valid': valid}
            if args.arm == 'E':
                record['profile_donor'] = donor.get(uid)
            raw.write(json.dumps(record, ensure_ascii=False) + '\\n')
"""),
("""            'arm_D_profile_unavailable_users': n_unavailable if args.arm == 'D' else None,""",
 """            'arm_D_profile_unavailable_users': n_unavailable if args.arm in ('D', 'E') else None,"""),
("""            **backend.meta()}""",
 """            **({'profile_shuffle_map_sha256': map_sha} if args.arm == 'E' else {}),
            **backend.meta()}"""),
]


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    data = src.read_bytes()
    got = hashlib.sha256(data).hexdigest().upper()
    if got != SRC_SHA256:
        sys.exit(f'source hash mismatch: {got}')
    text = data.decode('utf-8')
    for i, (old, new) in enumerate(EDITS, 1):
        n = text.count(old)
        if n != 1:
            sys.exit(f'edit {i}: expected 1 match, found {n}')
        text = text.replace(old, new)
    dst.write_bytes(text.encode('utf-8'))
    print('wrote', dst, hashlib.sha256(text.encode('utf-8')).hexdigest().upper())


main()
