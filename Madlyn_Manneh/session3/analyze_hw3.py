#!/usr/bin/env python3
"""Read-only HW3 analysis.

Reads saved starter / llm_rerank outputs and the course data. Never calls a
model, and never prints or writes a customer ID: users are shown as labels
U001, U002, ... in the order of <baseline-dir>/contexts.jsonl.
"""
import argparse
import csv
import json
import math
import sys
from datetime import date
from pathlib import Path

import starter

BASELINE_ORDER = ['popularity', 'latest_buy', 'latest_buy_or_sell', 'cbf']
BASELINE_LABELS = {
    'popularity': 'Popularity',
    'latest_buy': 'Latest buy',
    'latest_buy_or_sell': 'Latest buy or sell',
    'cbf': 'CBF (initial candidate order, matched control)',
}
ARM_LABELS = {
    'B': 'B (raw history, no summary)',
    'C': 'C (summary only)',
    'D': 'D (summary + risk level and capacity)',
    'E': 'E (D with shuffled profiles)',
}
ARM_ORDER = ['B', 'C', 'D', 'E']


def read_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def read_predictions(path):
    out = {}
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            m, uid = row['method'], row['user_id']
            out.setdefault(m, {}).setdefault(uid, []).append((int(row['rank']), row['ISIN']))
    for m in out:
        for uid in out[m]:
            out[m][uid] = [isin for _, isin in sorted(out[m][uid])]
    return out


def read_per_user(path):
    out = {}
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            out[(row['user_id'], row['method'])] = {
                'relevant_count': int(row['relevant_count']),
                'ndcg_at_10': float(row['ndcg_at_10']),
            }
    return out


def mean(values):
    return sum(values) / len(values) if values else 0.0


def fmt4(x):
    return '%.4f' % x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline-dir', required=True)
    ap.add_argument('--data-dir', default='data/FAR-Trans')
    ap.add_argument('--arm', action='append', default=[], metavar='NAME=EVAL_DIR')
    ap.add_argument('--run', action='append', default=[], metavar='NAME=RUN_DIR')
    ap.add_argument('--out-dir', default='outputs/hw3_analysis')
    ap.add_argument('--hand-check')
    args = ap.parse_args()

    base = Path(args.baseline_dir)
    protocol = read_json(base / 'protocol.json')
    cutoff = protocol['cutoff']
    end_exclusive = protocol['end_exclusive']
    base_hash = protocol['protocol_hash']
    horizon = (date.fromisoformat(end_exclusive) - date.fromisoformat(cutoff)).days

    truth = starter.load_data(Path(args.data_dir), cutoff, horizon)[3]

    contexts = read_jsonl(base / 'contexts.jsonl')
    user_ids = [c['user_id'] for c in contexts]
    labels = {uid: 'U%03d' % (i + 1) for i, uid in enumerate(user_ids)}
    uid_to_ctx = {c['user_id']: c for c in contexts}

    base_pred = read_predictions(base / 'predictions.csv')
    base_pu = read_per_user(base / 'per_user.csv')

    arms = {}
    for item in args.arm:
        name, d = item.split('=', 1)
        arms[name] = Path(d)
    runs = {}
    for item in args.run:
        name, d = item.split('=', 1)
        runs[name] = Path(d)

    rankings = {m: base_pred.get(m, {}) for m in BASELINE_ORDER}
    arm_pu = {}
    for name, d in arms.items():
        ap_ = read_json(d / 'protocol.json')
        if ap_.get('protocol_hash') != base_hash:
            sys.exit('arm %s: protocol_hash differs from baseline' % name)
        pu = read_per_user(d / 'per_user.csv')
        arm_pu[name] = pu
        arm_users = {uid for (uid, m) in pu if m == 'custom'}
        if arm_users != set(user_ids):
            sys.exit('arm %s: user set differs from baseline' % name)
        rankings[name] = read_predictions(d / 'predictions.csv').get('custom', {})

    method_names = list(BASELINE_ORDER) + [n for n in ARM_ORDER if n in arms]
    scores = {m: {} for m in method_names}
    rel = {}
    for uid in user_ids:
        relevant = truth.get(uid, set()) & set(uid_to_ctx[uid]['eligible_asset_ids'])
        rel[uid] = len(relevant)
        for m in BASELINE_ORDER:
            v = starter.ndcg10(rankings[m].get(uid), relevant)
            scores[m][uid] = v
            row = base_pu.get((uid, m))
            if row is None:
                sys.exit('baseline per_user.csv missing %s %s' % (m, labels[uid]))
            if abs(v - row['ndcg_at_10']) > 1e-9 or rel[uid] != row['relevant_count']:
                sys.exit('baseline %s %s recompute mismatch' % (m, labels[uid]))
        for name in arms:
            v = starter.ndcg10(rankings[name].get(uid), relevant)
            scores[name][uid] = v
            row = arm_pu[name].get((uid, 'custom'))
            if row is None:
                sys.exit('arm %s per_user.csv missing %s' % (name, labels[uid]))
            if abs(v - row['ndcg_at_10']) > 1e-9 or rel[uid] != row['relevant_count']:
                sys.exit('arm %s %s recompute mismatch' % (name, labels[uid]))

    labelled = [uid for uid in user_ids if rel[uid] > 0]
    n_labelled = len(labelled)
    n_users = len(user_ids)

    md = ['# HW3 analysis']
    result = {
        'protocol_hash': base_hash,
        'cutoff': cutoff,
        'end_exclusive': end_exclusive,
        'users': n_users,
        'labelled_users': n_labelled,
        'sections': {},
    }

    # ---- section 1
    md.append('')
    md.append('## 1. nDCG@10')
    md.append('n = %d labelled users out of %d.' % (n_labelled, n_users))
    md.append('')
    md.append('| Method | nDCG@10 (all) | nDCG@10 (labelled) |')
    md.append('|---|---:|---:|')
    sec1 = []
    for m in method_names:
        all_mean = mean([scores[m][u] for u in user_ids])
        lab_mean = mean([scores[m][u] for u in labelled])
        label = BASELINE_LABELS.get(m, ARM_LABELS.get(m, m))
        md.append('| %s | %s | %s |' % (label, fmt4(all_mean), fmt4(lab_mean)))
        sec1.append({'method': m, 'label': label,
                     'nDCG_all': round(all_mean, 4), 'nDCG_labelled': round(lab_mean, 4)})
    result['sections']['1_nDCG'] = sec1

    # ---- section 2
    md.append('')
    md.append('## 2. Paired differences (first minus second)')
    md.append('No significance test is reported because of the small number of labelled users.')
    sec2 = []
    pairs = [('D', 'C'), ('E', 'D'), ('C', 'B'), ('B', 'cbf')]
    for a, b in pairs:
        if a not in scores or b not in scores:
            continue
        diffs = [scores[a][u] - scores[b][u] for u in user_ids]
        lab_diffs = [scores[a][u] - scores[b][u] for u in labelled]
        higher = sum(1 for d in diffs if d > 1e-12)
        lower = sum(1 for d in diffs if d < -1e-12)
        equal = len(diffs) - higher - lower
        md.append('%s - %s: all %s, labelled %s, higher %d lower %d equal %d'
                  % (a, b, fmt4(mean(diffs)), fmt4(mean(lab_diffs)), higher, lower, equal))
        sec2.append({'pair': '%s-%s' % (a, b),
                     'all': round(mean(diffs), 4),
                     'labelled': round(mean(lab_diffs), 4),
                     'higher': higher, 'lower': lower, 'equal': equal})
    result['sections']['2_paired_differences'] = sec2

    # ---- section 3
    md.append('')
    md.append('## 3. Top-10 list overlap')
    sec3 = []
    arm_pairs = [(n, 'cbf') for n in ARM_ORDER if n in scores]
    arm_pairs += [('D', 'C'), ('E', 'D'), ('C', 'B')]
    for a, b in arm_pairs:
        if a not in scores or b not in scores:
            continue
        identical = sum(1 for u in user_ids if rankings[a].get(u) == rankings[b].get(u))
        overlaps = [len(set(rankings[a].get(u, [])) & set(rankings[b].get(u, [])))
                    for u in user_ids]
        md.append('%s vs %s: identical %d of %d, mean overlap %.2f'
                  % (a, b, identical, n_users, mean(overlaps)))
        sec3.append({'pair': '%s-%s' % (a, b), 'identical': identical,
                     'mean_overlap': round(mean(overlaps), 2)})
    result['sections']['3_top10_overlap'] = sec3

    # ---- section 4
    md.append('')
    md.append('## 4. Candidate coverage')
    no_candidate_purchase = 0
    oracle_all = []
    oracle_lab = []
    for uid in user_ids:
        cand = [a['id'] for a in uid_to_ctx[uid]['candidate_assets']]
        cand_set = set(cand)
        relevant = truth.get(uid, set()) & set(uid_to_ctx[uid]['eligible_asset_ids'])
        bought = relevant & cand_set
        if rel[uid] > 0 and not bought:
            no_candidate_purchase += 1
        oracle_ranking = sorted(bought) + [c for c in cand if c not in bought]
        o = starter.ndcg10(oracle_ranking[:10], relevant)
        oracle_all.append(o)
        if rel[uid] > 0:
            oracle_lab.append(o)
    md.append('users with future purchases and none of their purchases among the 50 '
              'candidates: %d' % no_candidate_purchase)
    md.append('oracle ceiling nDCG@10: all %s, labelled %s'
              % (fmt4(mean(oracle_all)), fmt4(mean(oracle_lab))))
    result['sections']['4_candidate_coverage'] = {
        'labelled_with_no_candidate_purchase': no_candidate_purchase,
        'oracle_all': round(mean(oracle_all), 4),
        'oracle_labelled': round(mean(oracle_lab), 4),
    }

    # ---- section 5
    md.append('')
    md.append('## 5. LLM runs')
    md.append('| Arm | users | invalid_outputs | wall_seconds_whole_arm | resolved_commit | risk | capacity |')
    md.append('|---|---:|---:|---:|---|---:|---:|')
    sec5 = []
    for name in ARM_ORDER:
        if name not in runs:
            continue
        meta = read_json(runs[name] / 'run_meta.json')
        raw = read_jsonl(runs[name] / 'raw_log.jsonl')
        commit = meta.get('resolved_commit')
        commit_short = (commit[:12] if commit else 'n/a')
        risk = sum(1 for r in raw if 'risk' in (r.get('summary') or '').lower())
        cap = sum(1 for r in raw if 'capacity' in (r.get('summary') or '').lower())
        md.append('| %s | %s | %s | %s | %s | %d | %d |'
                  % (name, meta.get('users'), meta.get('invalid_outputs'),
                     meta.get('wall_seconds_whole_arm'), commit_short, risk, cap))
        sec5.append({'arm': name, 'users': meta.get('users'),
                     'invalid_outputs': meta.get('invalid_outputs'),
                     'wall_seconds_whole_arm': meta.get('wall_seconds_whole_arm'),
                     'resolved_commit': commit_short, 'risk': risk, 'capacity': cap})
    result['sections']['5_llm_runs'] = sec5

    # ---- section 6
    md.append('')
    md.append('## 6. Profile availability')
    sec6 = {}
    if 'D' in runs:
        rawD = {r['user_id']: r for r in read_jsonl(runs['D'] / 'raw_log.jsonl')}
        with_prof = sum(1 for u in user_ids if rawD[u].get('questionnaire_before_cutoff'))
        without_prof = n_users - with_prof
        md.append('users with a profile: %d, without: %d' % (with_prof, without_prof))
        sec6['with_profile'] = with_prof
        sec6['without_profile'] = without_prof
        if 'C' in rankings:
            d_diff_w = sum(1 for u in user_ids if rawD[u].get('questionnaire_before_cutoff')
                           and rankings['D'].get(u) != rankings['C'].get(u))
            d_diff_wo = sum(1 for u in user_ids if not rawD[u].get('questionnaire_before_cutoff')
                            and rankings['D'].get(u) != rankings['C'].get(u))
            md.append('D differs from C in the top-10: with profile %d, without %d'
                      % (d_diff_w, d_diff_wo))
            sec6['D_vs_C_top10_differs_with_profile'] = d_diff_w
            sec6['D_vs_C_top10_differs_without_profile'] = d_diff_wo
    if 'E' in runs and 'D' in runs and 'E' in rankings and 'D' in rankings:
        rawE = {r['user_id']: r for r in read_jsonl(runs['E'] / 'raw_log.jsonl')}
        prompt_diff = [u for u in user_ids
                       if rawE[u].get('summary_prompt') != rawD[u].get('summary_prompt')]
        prompt_same = [u for u in user_ids
                       if rawE[u].get('summary_prompt') == rawD[u].get('summary_prompt')]
        keep_own = sum(1 for u in user_ids if rawE[u].get('profile_donor') == u)
        diff_rank = sum(1 for u in prompt_diff
                        if rankings['E'].get(u) != rankings['D'].get(u))
        same_rank = sum(1 for u in prompt_same
                        if rankings['E'].get(u) == rankings['D'].get(u))
        mean_ed = mean([scores['E'][u] - scores['D'][u] for u in prompt_diff])
        md.append('E vs D: prompt differs for %d users, keeps own profile %d, '
                  'identical prompt %d' % (len(prompt_diff), keep_own, len(prompt_same)))
        md.append('among prompt-differing users, different top-10 in E vs D: %d'
                  % diff_rank)
        md.append('among identical-prompt users, identical ranking in E and D: %d'
                  % same_rank)
        md.append('mean E - D on prompt-differing users: %s' % fmt4(mean_ed))
        sec6['E_prompt_differs'] = len(prompt_diff)
        sec6['E_keeps_own_profile'] = keep_own
        sec6['E_prompt_identical'] = len(prompt_same)
        sec6['E_diff_top10_among_prompt_diff'] = diff_rank
        sec6['E_identical_ranking_among_prompt_same'] = same_rank
        sec6['E_minus_D_mean_prompt_diff'] = round(mean_ed, 4)
    result['sections']['6_profile_availability'] = sec6

    # ---- section 7
    md.append('')
    md.append('## 7. Labelled users')
    header = ['Label', 'future purchases', 'in candidates', 'CBF']
    header += [n for n in ARM_ORDER if n in scores]
    md.append('| ' + ' | '.join(header) + ' |')
    md.append('|' + '---|' * (len(header) - 1) + '---:|')
    sec7 = []
    for uid in labelled:
        cand = set(a['id'] for a in uid_to_ctx[uid]['candidate_assets'])
        relevant = truth.get(uid, set()) & set(uid_to_ctx[uid]['eligible_asset_ids'])
        in_cand = len(relevant & cand)
        row = [labels[uid], str(rel[uid]), str(in_cand), fmt4(scores['cbf'][uid])]
        row += [fmt4(scores[n][uid]) for n in ARM_ORDER if n in scores]
        md.append('| ' + ' | '.join(row) + ' |')
        sec7.append({'label': labels[uid], 'future_purchases': rel[uid],
                     'in_candidates': in_cand,
                     'nDCG': {('cbf' if m == 'cbf' else m): round(scores[m][uid], 4)
                              for m in (['cbf'] + [n for n in ARM_ORDER if n in scores])}})
    result['sections']['7_labelled_users'] = sec7

    # ---- section 8
    md.append('')
    md.append('## 8. Hand-worked nDCG@10')
    if args.hand_check:
        hc_uid = next((u for u in user_ids if labels[u] == args.hand_check), None)
        if hc_uid is None:
            sys.exit('hand-check label not found: %s' % args.hand_check)
    else:
        if 'D' in scores and 'C' in scores:
            hc_uid = max(labelled, key=lambda u: abs(scores['D'][u] - scores['C'][u]))
        else:
            hc_uid = labelled[0]
    relevant = truth.get(hc_uid, set()) & set(uid_to_ctx[hc_uid]['eligible_asset_ids'])
    ideal_terms = [1.0 / math.log2(i + 2) for i in range(min(10, len(relevant)))]
    ideal_dcg = sum(ideal_terms)
    md.append('user %s, %d future purchase(s)' % (labels[hc_uid], len(relevant)))
    md.append('ideal DCG terms: %s -> ideal DCG = %s'
              % (', '.join(fmt4(t) for t in ideal_terms), fmt4(ideal_dcg)))
    sec8 = {'label': labels[hc_uid], 'ideal_dcg': round(ideal_dcg, 4),
            'methods': {}}
    hand_order = ['cbf'] + [n for n in ARM_ORDER if n in scores]
    for m in hand_order:
        r = rankings[m][hc_uid]
        hits = []
        for pos, isin in enumerate(r[:10], 1):
            if isin in relevant:
                hits.append((pos, isin, 1.0 / math.log2(pos + 1)))
        dcg = sum(h[2] for h in hits)
        ndcg_val = dcg / ideal_dcg if ideal_dcg else 0.0
        md.append('%s: %s -> DCG = %s, nDCG = %s (script %s)'
                  % (m,
                     ', '.join('rank %d %s %s' % (p, i, fmt4(t)) for p, i, t in hits)
                     if hits else 'no purchase in top 10',
                     fmt4(dcg), fmt4(ndcg_val), fmt4(scores[m][hc_uid])))
        sec8['methods'][m] = {'positions': [{'rank': p, 'isin': i, 'term': round(t, 4)}
                                            for p, i, t in hits],
                              'dcg': round(dcg, 4), 'nDCG': round(ndcg_val, 4),
                              'script_nDCG': round(scores[m][hc_uid], 4)}
    result['sections']['8_hand_check'] = sec8

    # ---- section 9
    md.append('')
    md.append('## 9. Where the purchased assets sit')
    for uid in user_ids:
        if rankings['cbf'].get(uid) != [a['id'] for a in uid_to_ctx[uid]['candidate_assets'][:10]]:
            sys.exit('self-check: CBF top-10 differs from first 10 candidates for %s' % labels[uid])
    md.append('| Label | future purchases | in eligible | repeat | candidate positions |')
    md.append('|---|---:|---:|---:|---|')
    sec9 = {'users': [], 'totals': {}}
    t_future = t_eligible = t_repeat = t_cand = t_top10 = 0
    for uid in labelled:
        tset = truth.get(uid, set())
        eligible_set = set(uid_to_ctx[uid]['eligible_asset_ids'])
        hist_ids = {a['id'] for a in uid_to_ctx[uid]['history']}
        cand_ids = [a['id'] for a in uid_to_ctx[uid]['candidate_assets']]
        positions = sorted(i + 1 for i, c in enumerate(cand_ids) if c in tset)
        n_future = len(tset)
        n_eligible = len(tset & eligible_set)
        n_repeat = len(tset & hist_ids)
        n_cand = len(positions)
        n_top10 = sum(1 for p in positions if p <= 10)
        t_future += n_future
        t_eligible += n_eligible
        t_repeat += n_repeat
        t_cand += n_cand
        t_top10 += n_top10
        md.append('| %s | %d | %d | %d | %s |'
                  % (labels[uid], n_future, n_eligible, n_repeat,
                     ', '.join(str(p) for p in positions) if positions else '-'))
        sec9['users'].append({'label': labels[uid], 'future_purchases': n_future,
                              'in_eligible': n_eligible, 'repeat': n_repeat,
                              'candidate_positions': positions})
    md.append('')
    md.append('totals: future purchases %d, in eligible %d, repeat %d, '
              'among 50 candidates %d, of those in positions 1-10 %d'
              % (t_future, t_eligible, t_repeat, t_cand, t_top10))
    sec9['totals'] = {'future_purchases': t_future, 'in_eligible': t_eligible,
                      'repeat': t_repeat, 'among_candidates': t_cand,
                      'candidate_positions_1_10': t_top10}
    result['sections']['9_purchased_assets'] = sec9

    body = '\n'.join(md) + '\n'
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'hw3_results.md').write_text(body, encoding='utf-8')
    (out_dir / 'hw3_results.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')

    print(body)
    print('wrote', out_dir / 'hw3_results.md')
    print('wrote', out_dir / 'hw3_results.json')


if __name__ == '__main__':
    main()
