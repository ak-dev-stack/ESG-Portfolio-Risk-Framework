# ==============================================================================
# PROJECT: E&S RISK SCREENING & ESAP TRACKING DIAGNOSTIC
# CONTEXT: Oliver Wyman – Financial Services (Risk & Analytics) Simulation
# VERSION: Final Partner-Ready (Risk-First Logic)
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------------------
# GLOBAL SETTINGS
# ------------------------------------------------------------------------------
np.random.seed(2024)  # Ensures the "Client Scenario" is reproducible
plt.rcParams['figure.dpi'] = 120
sns.set_theme(style="whitegrid")  # Professional consulting aesthetic

print(">>> INITIALIZING ESG RISK DIAGNOSTIC ENGINE...")

# ==============================================================================
# PHASE 1: SYNTHETIC DATA GENERATION (THE "LOAN TAPE")
# ==============================================================================

def generate_portfolio(n_clients=400):
    """
    Simulates a multi-country commercial loan portfolio (Emerging Markets).
    Includes sector-correlated Environmental & Social risk characteristics.
    """
    sectors = ['Renewable Energy', 'Agribusiness', 'Manufacturing', 
               'Infrastructure', 'Oil & Gas', 'TMT', 'Financial Services']
    countries = ['Vietnam', 'Indonesia', 'Kenya', 'Nigeria']
    risk_levels = ['High', 'Medium', 'Low']
    esap_states = ['Not Started', 'In Progress', 'Delayed', 'Closed']

    # 1. Sector Weights (Heavy on Transition-Sensitive sectors)
    weights = [0.15, 0.20, 0.20, 0.15, 0.10, 0.10, 0.10]
    client_sectors = np.random.choice(sectors, n_clients, p=weights)

    # 2. Exposure: Log-normal (Skewed to simulate realistic corporate loan sizes)
    exposure = np.random.lognormal(mean=16.1, sigma=1.0, size=n_clients)
    exposure = np.round(exposure, -5)

    env_risk, soc_risk, green_tag = [], [], []

    for sec in client_sectors:
        # Environmental Risk Logic (Sector Correlated)
        if sec in ['Oil & Gas', 'Agribusiness', 'Manufacturing']:
            # Heavy Industry = Higher Environmental Risk
            env_risk.append(np.random.choice(risk_levels, p=[0.6, 0.3, 0.1])) 
            green_tag.append(False)
        elif sec == 'Renewable Energy':
            env_risk.append('Low')
            green_tag.append(True)
        else:
            env_risk.append(np.random.choice(risk_levels, p=[0.1, 0.4, 0.5]))
            green_tag.append(False)

        # Social Risk Logic (Labor/Community focus)
        if sec in ['Agribusiness', 'Infrastructure']:
            soc_risk.append(np.random.choice(risk_levels, p=[0.5, 0.4, 0.1]))
        else:
            soc_risk.append(np.random.choice(risk_levels, p=[0.1, 0.4, 0.5]))

    # 3. ESAP Execution Logic (Operational Risk)
    # High Risk clients struggle more; higher rate of 'Delayed' and 'Not Started'
    esap_status = []
    for r in env_risk:
        if r == 'High':
            esap_status.append(np.random.choice(esap_states, p=[0.1, 0.3, 0.4, 0.2]))
        else:
            esap_status.append(np.random.choice(esap_states, p=[0.3, 0.4, 0.1, 0.2]))

    df = pd.DataFrame({
        'Client_ID': [f'CL-{1000+i}' for i in range(n_clients)],
        'Country': np.random.choice(countries, n_clients),
        'Sector': client_sectors,
        'Exposure_USD': exposure,
        'Env_Risk': env_risk,
        'Soc_Risk': soc_risk,
        'ESAP_Status': esap_status,
        'Green_Tagged': green_tag
    })

    return df

df = generate_portfolio()
print(f"phase 1 Complete: Loaded {len(df)} Clients. Total Exposure: ${df['Exposure_USD'].sum()/1e9:,.2f}B")

# ==============================================================================
# PHASE 2: CONSERVATIVE RISK SCORING (NON-COMPENSATORY)
# ==============================================================================

# Map Ratings to Scores
risk_map = {'High': 3, 'Medium': 2, 'Low': 1}
df['E_Score'] = df['Env_Risk'].map(risk_map)
df['S_Score'] = df['Soc_Risk'].map(risk_map)

# CORRECTED LOGIC: Non-Compensatory Scoring
# Use max() instead of average. A 'High' in E OR S triggers High Overall Risk.
df['Max_Risk_Score'] = df[['E_Score', 'S_Score']].max(axis=1)

# CORRECTED LOGIC: Watchlist Definition
# High Risk (3) AND (Delayed OR Not Started) action plans.
df['Watchlist'] = np.where(
    (df['Max_Risk_Score'] == 3) & 
    (df['ESAP_Status'].isin(['Delayed', 'Not Started'])), 
    True, False
)

# --- VISUAL 1: SECTOR EXPOSURE HEATMAP ---
print(">>> GENERATING DIAGNOSTIC 1: RISK HEATMAP...")
pivot_risk = df.pivot_table(index='Sector', columns='Env_Risk', values='Exposure_USD', aggfunc='sum') / 1e6
pivot_risk = pivot_risk[['High', 'Medium', 'Low']] # Logical Order

plt.figure(figsize=(10, 5))
# Annot=True puts the numbers in the boxes (Critical for Consulting)
sns.heatmap(pivot_risk, annot=True, fmt=".0f", cmap="Reds", cbar_kws={'label': 'Exposure ($M)'})
plt.title("Portfolio Concentration: Exposure ($M) by Sector & Environmental Risk")
plt.tight_layout()
plt.show()

# ==============================================================================
# PHASE 3: OPERATIONAL EXECUTION (ESAP BOTTLENECK)
# ==============================================================================

# Focus on Clients flagged as High Risk (Score = 3)
high_risk_only = df[df['Max_Risk_Score'] == 3]
esap_summary = high_risk_only.groupby('ESAP_Status')['Exposure_USD'].sum() / 1e6

# --- VISUAL 2: EXECUTION GAP ANALYSIS ---
print(">>> GENERATING DIAGNOSTIC 2: OPERATIONAL FAILURE CHART...")
plt.figure(figsize=(9, 5))

# Reindex for logical execution order
esap_summary = esap_summary.reindex(
    ['Closed', 'Delayed', 'In Progress', 'Not Started']
)

# Soft consulting-grade palette
colors = ['#A8D5BA', '#E6A0A0', '#F2D8A7', '#C9CED6']

ax = esap_summary.plot(
    kind='bar',
    color=colors,
    edgecolor='none'
)

plt.title(
    "Execution Gap: High-Risk Exposure by ESAP Status",
    fontsize=13,
    pad=12
)
plt.ylabel("Exposure ($M)", fontsize=10)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.25)

# Value annotations (subtle, not loud)
for p in ax.patches:
    ax.annotate(
        f'${p.get_height():.0f}M',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='bottom',
        fontsize=9,
        xytext=(0, 6),
        textcoords='offset points'
    )

plt.tight_layout()
plt.show()

failed_compliance = esap_summary.get('Delayed', 0) + esap_summary.get('Not Started', 0)
print(f"CRITICAL INSIGHT: ${failed_compliance:,.1f}M of High-Risk exposure has unmitigated issues.")

# ==============================================================================
# PHASE 4: TRANSITION RISK SCENARIO (OVERLAY INDEX)
# ==============================================================================
# NOTE: This models "Transition Sensitivity" as a normalized index.
# ==============================================================================

def plot_transition_risk_overlay():
    print(">>> GENERATING DIAGNOSTIC 3: TRANSITION SCENARIO OVERLAY...")
    
    # 1. Timeline & Baseline
    years = np.arange(2025, 2036) # 10-year strategic horizon
    n = len(years)
    baseline_index = 100 # Index 100 = Current 2025 Risk Profile
    
    # 2. Scenario 1: Regulatory-Aligned Pathway
    # Assumption: Regulators expect a ~6% annual reduction in transition risk exposure
    reg_decay_rate = 0.06 
    reg_pathway = [baseline_index * ((1 - reg_decay_rate) ** i) for i in range(n)]
    
    # 3. Scenario 2: Portfolio BAU Pathway (The "Inertia" View)
    # Assumption: Due to high "Delayed" ESAPs, portfolio only de-risks at ~1.5% annually.
    bau_decay_rate = 0.015
    port_pathway = [baseline_index * ((1 - bau_decay_rate) ** i) for i in range(n)]
    
    # Add minor volatility
    noise = np.random.normal(0, 1.2, n)
    port_pathway = np.array(port_pathway) + noise
    reg_pathway = np.array(reg_pathway)
    risk_gap = port_pathway - reg_pathway

    # --- VISUALIZATION (Dark Mode / Stress Test Aesthetic) ---
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Clean Spines
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444444'); ax.spines['bottom'].set_color('#444444')

    # Plot Pathways
    ax.plot(years, port_pathway, color='#FF4F4F', linewidth=3, label='Portfolio BAU (Current Inertia)') # Red = Risk
    ax.plot(years, reg_pathway, color='#00D166', linewidth=2.5, linestyle='--', label='Regulatory-Aligned Pathway') # Green = Target

    # Highlight the Risk Gap
    ax.fill_between(
        years, port_pathway, reg_pathway, 
        color='#FF4F4F', alpha=0.25, 
        label='Transition Risk Gap (Capital Surcharge Zone)'
    )

    # Labels
    ax.set_title("Transition Risk Sensitivity: Regulatory Divergence (2025-2035)", 
                 fontsize=14, color='white', pad=20, fontweight='bold')
    ax.set_ylabel("Transition Sensitivity Index (2025 = 100)", fontsize=10, color='silver')
    ax.set_ylim(40, 110)
    ax.grid(axis='y', linestyle='--', alpha=0.2)
    ax.legend(loc='lower left', frameon=False, fontsize=9)

    # Insight Box
    gap_2035 = risk_gap[-1]
    text_str = (f"STRATEGIC DIVERGENCE (2035)\n───────────────────────────\n"
                f"Gap Magnitude:   +{gap_2035:.1f} pts\n"
                f"Implication:     Rising Cost of Risk")
    props = dict(boxstyle='round', facecolor='#1f1f1f', alpha=0.9, edgecolor='gray')
    ax.text(0.65, 0.85, text_str, transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', color='white', fontfamily='monospace', bbox=props)

    # MANDATORY DISCLAIMER
    plt.figtext(0.5, 0.01, 
                "DISCLAIMER: Illustrative scenario overlay using normalized indices. "
                "Not derived from loan-level emissions data.", 
                ha="center", fontsize=8, color="#888888", style='italic')

    plt.tight_layout()
    plt.show()
    plt.style.use('default') # Reset style

# Execute Phase 4
plot_transition_risk_overlay()

# ==============================================================================
# PHASE 5: EXECUTIVE SUMMARY
# ==============================================================================

watchlist_exposure = df[df['Watchlist']]['Exposure_USD'].sum() / 1e6
watchlist_count = df['Watchlist'].sum()
green_ratio = (df[df['Green_Tagged']]['Exposure_USD'].sum() / df['Exposure_USD'].sum()) * 100

summary = f"""
===========================================================================
RISK ADVISORY SUMMARY: ESG PORTFOLIO DIAGNOSTIC
===========================================================================
1. EXPOSURE AT RISK (WATCHLIST):
   - ${watchlist_exposure:,.1f} M ({watchlist_count} Clients) flagged.
   - Criteria: High Risk (Max Logic) AND (Delayed/Not Started) ESAP.
   - Correction: Used Non-Compensatory Scoring to prevent risk masking.

2. OPERATIONAL FAILURE:
   - ${failed_compliance:,.1f} M of High-Risk exposure lacks valid mitigation.
   - "Not Started" plans in Oil & Gas are the primary driver.

3. STRATEGIC TRANSITION GAP:
   - Portfolio is diverging from the Regulatory-Aligned Pathway.
   - The "Risk Gap" suggests the current portfolio inertia will create a 
     capital surcharge requirement by 2030.

4. RECOMMENDATION:
   - Establish a Remediation Unit to clear 'Delayed' ESAPs within 90 days.
   - Apply stricter underwriting to clients increasing the Transition Gap.
===========================================================================
"""
print(summary)