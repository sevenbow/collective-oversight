#!/usr/bin/env python3
"""Analysis for HIM-22: Collective vs Individual Oversight Patterns"""
import os, numpy as np, pandas as pd, warnings
from scipy import stats
from itertools import combinations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for d in ['results/figures','results/tables','results/statistical-output']:
    os.makedirs(os.path.join(BASE, d), exist_ok=True)

print("HIM-22 Analysis Pipeline")
df = pd.read_csv(os.path.join(BASE, 'data', 'raw', 'collective_oversight_data.csv'))

# Processed summary
summary = df.groupby(['oversight_structure','task_complexity']).agg({
    'detection_rate':['mean','std','sem'],
    'false_alarm_rate':['mean','std'],
    'trust_calibration':['mean','std'],
    'response_time_ms':['mean','std'],
    'subject_id':'count'
}).round(4)
summary.to_csv(os.path.join(BASE, 'data', 'processed', 'structure_summary.csv'))

structures = ['Individual','Dyad','Quad']
complexities = ['Low','Medium','High']

s = ["STATISTICAL ANALYSIS: HIM-22 Collective vs Individual Oversight\n" + "="*60]
s.append(f"N = {len(df)}")

# ANOVA by complexity level
for comp in complexities:
    sub = df[df['task_complexity']==comp]
    groups = [grp['detection_rate'].values for _, grp in sub.groupby('oversight_structure')]
    fv, pv = stats.f_oneway(*groups)
    s.append(f"\n{comp.upper()} complexity: F({len(groups)-1},{sum(len(g) for g in groups)-len(groups)}) = {fv:.2f}, p < .001" if pv<0.001 else f"\n{comp.upper()}: F = {fv:.2f}, p = {pv:.4f}")
    for struct in structures:
        m = sub[sub['oversight_structure']==struct]['detection_rate'].mean()
        s.append(f"  {struct}: M={m:.4f}")

# Trust vs team size correlation
trust_corr = np.corrcoef(df['team_size'], df['trust_calibration'])[0,1]
s.append(f"\nTrust × Team Size: r = {trust_corr:.4f}")

# False alarm comparison
for comp in complexities:
    groups_fa = [grp['false_alarm_rate'].values for _, grp in df[df['task_complexity']==comp].groupby('oversight_structure')]
    f_fa, p_fa = stats.f_oneway(*groups_fa)
    s.append(f"\nFA Rate at {comp} complexity: F = {f_fa:.2f}, p = {p_fa:.4f}")

# Efficiency: detection rate per unit response time
df['efficiency'] = df['detection_rate'] / (df['response_time_ms']/1000)
for struct in structures:
    eff = df[df['oversight_structure']==struct]['efficiency'].mean()
    s.append(f"\n{struct} efficiency (det/sec): {eff:.4f}")

# Pairwise comparisons at high complexity
high_comp = df[df['task_complexity']=='High']
s.append("\nHigh-complexity pairwise comparisons (Bonferroni):")
groups_hc = [grp['detection_rate'].values for _, grp in high_comp.groupby('oversight_structure')]
for (i,a),(j,b) in combinations(enumerate(structures), 2):
    t, p = stats.ttest_ind(groups_hc[i], groups_hc[j])
    padj = min(p*3, 1.0)
    d = (np.mean(groups_hc[j])-np.mean(groups_hc[i]))/np.sqrt((np.var(groups_hc[i])+np.var(groups_hc[j]))/2)
    sig = "***" if padj<0.001 else "ns"
    s.append(f"  {a} vs {b}: d={d:.3f}, p_adj={padj:.4f} {sig}")

with open(os.path.join(BASE, 'results', 'statistical-output', 'complete_stats.txt'), 'w') as f:
    f.write('\n'.join(s))

# Table
table = []
for struct in structures:
    for comp in complexities:
        sub = df[(df['oversight_structure']==struct)&(df['task_complexity']==comp)]
        table.append({
            'Structure': struct, 'Complexity': comp, 'N': len(sub),
            'Detection (M±SD)': f"{sub['detection_rate'].mean():.3f}±{sub['detection_rate'].std():.3f}",
            'FA Rate': f"{sub['false_alarm_rate'].mean():.3f}",
            'Trust': f"{sub['trust_calibration'].mean():.2f}",
            'RT (ms)': f"{sub['response_time_ms'].mean():.0f}"
        })
pd.DataFrame(table).to_csv(os.path.join(BASE, 'results', 'tables', 'structure_comparison.csv'), index=False)
print("✓ HIM-22 analysis complete")