# Project 9: Collective vs Individual Oversight Patterns

## Research Question

**How does group decision-making change the dynamics of AI oversight, and what are the optimal team structures?**

Comparing the effectiveness of individual human supervisors vs collaborative oversight teams across error detection, trust calibration, cognitive load distribution, and decision quality.

---

## 1. Theoretical Framework

### 1.1 Core Constructs

| Construct | Individual Oversight | Collective Oversight |
|-----------|---------------------|---------------------|
| Decision authority | Single supervisor | Distributed across team |
| Cognitive load | Concentrated | Shared (potentially amplified by coordination costs) |
| Error detection | Limited by single perspective | Multiple viewpoints, but subject to groupthink |
| Trust calibration | Personal calibration only | Social calibration + conformity pressures |
| Response latency | Fast (no coordination) | Slower (deliberation required) |
| Accountability | Clear | Diffused |

### 1.2 Relevant Theoretical Models

**Social Decision Scheme Theory (Davis, 1973)**: Predicts group decisions from individual preferences via combination rules (majority, unanimity, truth-wins). Applied here: How do teams combine individual oversight assessments into collective accept/reject decisions?

**Transactive Memory Systems (Wegner, 1987)**: Teams develop shared knowledge of "who knows what." In oversight teams, members may specialize in different AI failure modes, improving collective coverage.

**Process Gains vs Process Losses (Steiner, 1972)**:
- *Gains*: Error-checking, diverse perspectives, knowledge pooling
- *Losses*: Coordination costs, social loafing, conformity pressure, production blocking

**Signal Detection Theory (SDT) Extension**: Individual d' (sensitivity) and β (criterion) combine non-trivially in groups. Optimal aggregation depends on correlation structure of individual signals.

### 1.3 Hypotheses

| ID | Hypothesis | Theoretical Basis |
|----|-----------|-------------------|
| H1 | Teams detect more AI errors than individuals (higher sensitivity d') | Pooled signal diversity |
| H2 | Teams have higher false alarm rates than individuals | Lower collective criterion β |
| H3 | Optimal team size follows inverted-U: peaks at 3-4 members | Steiner's process loss model |
| H4 | Diverse-expertise teams outperform homogeneous teams | Transactive memory theory |
| H5 | Teams show better trust calibration than individuals | Social correction of miscalibration |
| H6 | Individual oversight is faster per-decision | Coordination cost elimination |
| H7 | Team oversight quality degrades under time pressure more than individual | Coordination overhead becomes bottleneck |
| H8 | Teams resist automation bias more effectively than individuals | Social accountability reduces complacency |

---

## 2. Experimental Design

### 2.1 Study Architecture

**Design**: 2 × 3 × 2 mixed factorial

| Factor | Levels | Type |
|--------|--------|------|
| Oversight structure | Individual, Dyad, Quad (4-person team) | Between-subjects |
| Task complexity | Low, Medium, High | Within-subjects |
| Time pressure | Normal, Constrained (50% time) | Within-subjects |

**Power Analysis**:
```
Effect of interest: Medium effect (Cohen's f = 0.25)
α = 0.05, Power = 0.80
Groups = 3 (individual, dyad, quad)
Repeated measures = 6 (3 complexity × 2 time pressure)
Correlation among measures = 0.5

Required: ~42 decision units per condition
→ 42 individuals + 42 dyads (84 people) + 42 quads (168 people)
→ Total N = 294 participants
```

### 2.2 Task Environment

**AI System Under Oversight**: Simulated medical image classification AI with controlled error injection.

**Error Types** (crossed with complexity):
| Error Type | Detection Difficulty | Base Rate |
|------------|---------------------|-----------|
| Gross misclassification | Easy | 5% |
| Boundary case error | Medium | 8% |
| Subtle systematic bias | Hard | 3% |
| Correct but low-confidence | Ambiguous | 10% |

**Decision Options**: Accept AI recommendation, Override (with justification), Defer to specialist, Request re-analysis

### 2.3 Team Structure Conditions

**Individual**: Single supervisor reviews AI outputs alone.

**Dyad**: Two supervisors with structured deliberation protocol:
- Phase 1: Independent review (2 min)
- Phase 2: Share assessments, discuss disagreements (3 min)
- Phase 3: Joint decision (1 min)

**Quad (4-person team)**: Structured roles:
- Lead reviewer: Primary assessment
- Devil's advocate: Challenge AI and team assumptions
- Domain specialist: Deep technical evaluation
- Process monitor: Track decision quality and time

### 2.4 Measurements

**Primary Outcomes**:

| Metric | Operationalization | Scale |
|--------|-------------------|-------|
| Detection sensitivity (d') | SDT analysis of hits/false alarms | Continuous |
| Decision accuracy | % correct accept/reject decisions | 0-100% |
| Calibration score | Brier score on confidence-accuracy alignment | 0-1 |
| Decision latency | Time from presentation to final decision | Seconds |
| Appropriate reliance | Ratio of correct automation use to total | 0-1 |

**Process Measures**:

| Metric | Operationalization | Source |
|--------|-------------------|--------|
| Cognitive load | NASA-TLX (6 subscales) | Self-report, post-block |
| Participation equity | Gini coefficient of speaking time | Audio/video analysis |
| Conflict type | Task vs relationship conflict scale | Self-report |
| Information sharing | Unique vs shared information discussed | Coded transcripts |
| Conformity pressure | Pre-discussion to post-discussion opinion change | Behavioral |

---

## 3. Statistical Analysis Plan

### 3.1 Primary Analysis: Mixed-Effects Models

**Model 1: Detection Sensitivity**

```
d'_ij = β₀ + β₁(Structure) + β₂(Complexity) + β₃(TimePressure)
       + β₄(Structure × Complexity) + β₅(Structure × TimePressure)
       + β₆(Complexity × TimePressure)
       + β₇(Structure × Complexity × TimePressure)
       + u_j + ε_ij

Where:
  i = trial, j = decision unit (individual or team)
  Structure: dummy-coded (Individual = reference)
  u_j ~ N(0, σ²_u) — random intercept for decision unit
```

**Model 2: Decision Accuracy (Logistic Mixed-Effects)**

```
logit(P(correct)_ij) = β₀ + β₁(Structure) + β₂(Complexity)
                      + β₃(TimePressure) + β₄(ErrorType)
                      + β₅(Structure × Complexity)
                      + β₆(Structure × ErrorType)
                      + u_j + v_j(Complexity) + ε_ij

Random effects: intercept + complexity slope per decision unit
```

**Model 3: Response Time (Log-Normal Mixed-Effects)**

```
log(RT_ij) = β₀ + β₁(Structure) + β₂(Complexity) + β₃(TimePressure)
            + β₄(Structure × TimePressure) + u_j + ε_ij

Key contrast: Structure × TimePressure interaction tests H7
```

### 3.2 Signal Detection Analysis

**Individual-Level SDT**:
```
d'_individual = z(Hit Rate) - z(False Alarm Rate)
β_individual = -0.5 × [z(Hit Rate) + z(False Alarm Rate)]
```

**Team-Level SDT Aggregation Models**:

| Model | Rule | Prediction |
|-------|------|-----------|
| Optimal (Bayes) | Weighted average by individual d' | Upper bound on team d' |
| Majority rule | Accept if >50% members accept | d'_team ≈ √n × d'_individual (for independent signals) |
| Best member | Team d' = max(d'_members) | Lower bound for well-functioning teams |
| Most confident | Decision by highest-confidence member | Depends on metacognitive accuracy |

**Comparison**: Fit observed team d' against predictions from each aggregation model to identify actual decision strategy.

### 3.3 Optimal Team Size Analysis

**Parametric Model**:
```
Performance(n) = α × log(n) - γ × n + δ

Where:
  α = information gain coefficient (diminishing returns)
  γ = coordination cost coefficient (linear increase)
  n = team size
  Optimal n* = α / γ
```

**Non-Parametric Approach**: Compare performance across team sizes (1, 2, 4) with planned contrasts:
- Linear trend: Does performance increase with size?
- Quadratic trend: Is there diminishing returns / inverted-U?

### 3.4 Team Process Analysis

**Participation Equity → Performance Path Model**:
```
Gini(participation) → Information Sharing → Decision Quality
                    → Conformity Pressure → Decision Quality
```

Mediation analysis using structural equation modeling (SEM) to test whether balanced participation improves decisions via information pooling, while controlling for conformity effects.

**Conflict Analysis**:
```
Task Conflict → Improved error detection (positive path)
Relationship Conflict → Degraded performance (negative path)
```

Test moderation by team size: larger teams may amplify both effects.

### 3.5 Trust Calibration Comparison

**Calibration Metric**: Extended Brier Score decomposition

```
Brier Score = Reliability - Resolution + Uncertainty

Where:
  Reliability = calibration error (lower = better calibrated)
  Resolution = discrimination ability (higher = better)
  Uncertainty = base rate entropy (constant)
```

Compare reliability component across conditions:
- H5 predicts: Reliability_team < Reliability_individual (teams better calibrated)

**Dynamic Trust Analysis**: Fit Bayesian updating model to confidence sequences:
```
Confidence_t = w × Prior_t-1 + (1-w) × Evidence_t

Compare learning rate w across conditions:
  w_team vs w_individual — teams should update more optimally
```

---

## 4. Advanced Analyses

### 4.1 Social Network Analysis of Team Dynamics

For quad teams, model communication patterns:

**Metrics**:
| Network Metric | Interpretation |
|---------------|---------------|
| Centralization | How hierarchical is communication? |
| Density | How connected are team members? |
| Reciprocity | Is communication bidirectional? |
| Betweenness | Who bridges information gaps? |

**Prediction**: Teams with moderate centralization (clear leader but open communication) outperform both highly centralized (leader dominance) and fully distributed (no coordination) structures.

### 4.2 Groupthink Detection

**Operationalized Indicators**:
1. **Opinion convergence rate**: How quickly do individual assessments align?
2. **Dissent expression**: Frequency of devil's advocate behavior
3. **Information search**: Do teams seek confirming vs disconfirming evidence?
4. **Overconfidence**: Team confidence exceeds accuracy more than individual confidence exceeds accuracy?

**Statistical Test**: Compare pre-deliberation opinion variance to post-deliberation variance. Excessive convergence (beyond what evidence warrants) indicates groupthink.

```
Groupthink Index = 1 - (Post_variance / Expected_post_variance)

Where Expected_post_variance is derived from Bayesian updating
given the information actually shared.

Groupthink Index > 0.5 → Potential groupthink
```

### 4.3 Expertise Diversity Analysis

**Shannon Diversity Index for Team Composition**:
```
H = -Σ p_i × log(p_i)

Where p_i = proportion of team members from expertise category i
```

Test: H → Decision Quality, moderated by task complexity
- H4 predicts: Higher diversity → better performance, especially for complex/novel AI errors

### 4.4 Speed-Accuracy Tradeoff (SAT) Analysis

Fit diffusion model to individual and team decisions:

```
Individual: drift rate v, boundary a, non-decision time t₀
Team: drift rate v_team, boundary a_team, non-decision time t₀_team

Predictions:
  v_team > v_individual (better evidence accumulation from pooled info)
  a_team > a_individual (more cautious criterion)
  t₀_team > t₀_individual (coordination overhead in non-decision time)
```

### 4.5 Longitudinal Team Development

Over multiple sessions, track:
- Transactive memory development (who-knows-what accuracy)
- Role specialization emergence
- Communication efficiency (same quality, less discussion)
- Shared mental model convergence

**Growth Curve Model**:
```
Performance_it = β₀ + β₁(Session_t) + β₂(Session_t²) + β₃(Structure)
               + β₄(Structure × Session_t) + u_i + v_i(Session_t) + ε_it
```

Key test: β₄ — do teams improve faster than individuals over time?

---

## 5. Expected Results & Interpretation Framework

### 5.1 Predicted Effect Sizes

| Comparison | Metric | Expected Effect | Cohen's d |
|-----------|--------|----------------|-----------|
| Team vs Individual | Detection d' | Team advantage | 0.4-0.6 |
| Team vs Individual | False alarm rate | Team higher | 0.3-0.5 |
| Team vs Individual | Decision latency | Team slower | 0.8-1.2 |
| Team vs Individual | Calibration | Team better | 0.3-0.5 |
| Dyad vs Quad | Overall accuracy | Small quad advantage | 0.1-0.3 |
| Dyad vs Quad | Efficiency (accuracy/time) | Dyad advantage | 0.4-0.6 |
| High vs Low time pressure | Team performance drop | Larger for teams | 0.5-0.7 |

### 5.2 Optimal Structure Recommendations

Based on predicted results, recommendations will follow this decision matrix:

| Scenario | Recommended Structure | Rationale |
|----------|----------------------|-----------|
| High-stakes, no time pressure | Quad with structured roles | Maximum error detection |
| High-stakes, time-constrained | Dyad with pre-assigned specialties | Balance of coverage and speed |
| Routine monitoring | Individual with escalation protocol | Efficiency, teams for escalated cases |
| Novel/unprecedented situations | Diverse quad + external review | Maximum perspective diversity |
| High-volume decisions | Individual + spot-check by dyad | Throughput with quality sampling |

### 5.3 Cost-Effectiveness Analysis

```
Cost_individual = Salary_supervisor × Time_per_decision × N_decisions
Cost_team(n) = n × Salary_supervisor × Time_per_decision(n) × N_decisions + Coordination_overhead(n)

Effectiveness = Errors_detected / Total_errors

Cost-Effectiveness Ratio = Cost / Effectiveness

Break-even analysis: At what error cost does team oversight become cost-effective?
```

---

## 6. Methodological Considerations

### 6.1 Threats to Validity

| Threat | Mitigation |
|--------|-----------|
| Social desirability in teams | Behavioral measures > self-report; anonymous pre-discussion ratings |
| Free-riding in larger teams | Individual accountability (pre-discussion independent assessment recorded) |
| Hawthorne effect | All conditions observed equally; extended study duration for habituation |
| Self-selection into team roles | Random role assignment within quads |
| Practice effects | Counterbalanced task order; equivalent parallel forms |
| Experimenter demand | Double-blind to hypothesis; standardized protocols |

### 6.2 Ecological Validity

Real-world mapping of experimental conditions:

| Experimental | Real-World Analog |
|-------------|-------------------|
| Individual | Solo AI operator (e.g., single radiologist + AI) |
| Dyad | Paired review (e.g., pilot + co-pilot with AI) |
| Quad | Oversight committee (e.g., loan approval board with AI) |
| Time pressure | Operational urgency (emergency response, trading) |
| High complexity | Rare/novel cases (edge cases, distribution shift) |

### 6.3 Multiple Comparison Corrections

- Primary hypotheses (H1-H8): Bonferroni-Holm correction (α = 0.05/8 for most significant, adjusted sequentially)
- Exploratory analyses: False Discovery Rate (Benjamini-Hochberg, q = 0.10)
- Planned contrasts: No correction needed (a priori, orthogonal)

### 6.4 Sensitivity Analyses

1. **Exclude outlier teams** (performance > 3 SD from mean) — check robustness
2. **Alternative random effects structure** — compare AIC/BIC for model selection
3. **Non-parametric alternatives** (permutation tests) for small-sample contrasts
4. **Bayesian analysis** with weakly informative priors — assess evidence strength via Bayes factors

---

## 7. Practical Implications

### 7.1 Design Guidelines for Oversight Systems

1. **Default to dyads for critical AI oversight** — best efficiency/accuracy tradeoff
2. **Require independent pre-assessment** before team deliberation — prevents anchoring
3. **Assign devil's advocate role** — structured dissent prevents groupthink
4. **Monitor participation equity** — Gini > 0.4 signals potential domination
5. **Escalation from individual to team** for flagged cases — combines throughput with depth
6. **Time buffer for team decisions** — coordination overhead requires 40-80% more time than individual assessment
7. **Rotate team composition** periodically — prevents entrenched groupthink while maintaining some transactive memory

### 7.2 Key Performance Indicators for Oversight Teams

| KPI | Target | Measurement Frequency |
|-----|--------|----------------------|
| Team detection sensitivity d' | > 2.5 | Weekly batch analysis |
| False positive rate | < 15% | Per session |
| Calibration reliability | < 0.05 | Monthly |
| Decision latency (median) | < 2× individual baseline | Per decision |
| Participation Gini | < 0.3 | Per session |
| Disagreement resolution rate | > 90% within session | Per session |

---

## 8. Connections to Other Research Projects

| Project | Connection to This Study |
|---------|------------------------|
| HIM-14: Cognitive Load Thresholds | Cognitive load distribution in teams vs individuals |
| HIM-15: Trust Calibration Dynamics | Social calibration effects in team settings |
| HIM-16: Attention Allocation | Attention distribution and specialization in teams |
| HIM-17: Learning Curves | Team learning vs individual learning trajectories |
| HIM-19: Optimal Deferral | Team deferral strategies vs individual deferral |
| HIM-20: Temporal Dynamics | How team oversight effectiveness varies over time |
| HIM-23: Metacognitive Awareness | Collective metacognition vs individual metacognition |

---

## 9. Summary

This study addresses a critical gap in human-AI oversight research: whether teams or individuals provide more effective AI supervision. The 2×3×2 factorial design (structure × complexity × time pressure) with N=294 allows detection of medium effects across conditions.

**Key contributions**:
1. First systematic comparison of individual vs team AI oversight using SDT framework
2. Identification of optimal team size and structure for AI oversight contexts
3. Process-level analysis of how teams aggregate oversight signals
4. Practical design guidelines for deploying oversight teams

**Primary statistical methods**: Mixed-effects models, signal detection theory, social network analysis, structural equation modeling, and diffusion modeling for speed-accuracy tradeoffs.
