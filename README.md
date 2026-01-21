# Quantitative ESG Risk Framework: E&S Screening & ESAP Tracking

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Executive Summary
This project establishes a computational framework for **Environmental and Social Risk Management (ESRM)** within a multi-country commercial loan portfolio. By transitioning from qualitative assessments to a quantitative scoring model, the analysis enables the bank to statistically measure sustainability risks, track compliance gaps (ESAPs), and validate Green Finance asset performance.

The workflow simulates a live banking environment using a synthetic dataset of **200 corporate clients** across the South Asia region (India, Bangladesh, Sri Lanka, Pakistan, Nepal), aggregating a total exposure of **~$1.1 Billion USD**.

---

## ❓ The Problem Statement
Commercial banks and Development Finance Institutions (DFIs) face a critical data challenge in managing non-financial risks:

*   **Quantification Gap:** E&S risks are traditionally recorded as qualitative labels (e.g., "High," "Medium"), making it mathematically impossible to calculate "Portfolio Value at Risk" or aggregated exposure without data transformation.
*   **Compliance Blind Spots:** Manual tracking of **Environmental and Social Action Plans (ESAPs)** leads to operational opacity. Banks often lack a real-time statistical view of how many clients are "In Progress" versus "Delayed" on critical compliance mandates.
*   **Greenwashing Risk:** Without rigorous tagging and statistical validation of "Green" assets against risk scores, banks struggle to substantiate their sustainable finance disclosures to regulators.
*   **Sectoral Concentration:** Lenders often unknowingly accumulate systemic E&S risks in specific high-impact sectors (e.g., Agribusiness, Manufacturing) due to a lack of consolidated visualization.

---

## ⚙️ The Analytical Solution (Methodology)
To address these challenges, this project utilizes **Python (Pandas, NumPy, Seaborn)** to engineer a data-driven ESRM pipeline. The solution follows a four-phase statistical approach:

### Phase A: Algorithmic Risk Scoring
*   **Technique:** Ordinal Encoding & Weighted Summation.
*   **Process:** Transformed categorical risk ratings (Environmental, Social) into numerical vectors (`1=Low`, `2=Medium`, `3=High`).
*   **Metric:** Calculated a composite **Total ESG Risk Score (Range: 2–6)** for every facility to stratify the portfolio based on risk intensity.
*   **Outcome:** Automated flagging of "High-Risk" clients (Score ≥ 5) requiring Enhanced Due Diligence (EDD).

### Phase B: Exposure Aggregation & Stratification
*   **Technique:** Groupby Aggregation & Descriptive Statistics.
*   **Process:** Calculated total financial exposure ($ USD) segmented by **Sector** and **Geography**.
*   **Outcome:** Identification of risk hotspots. For example, identifying that while *Services* has high volume, *Manufacturing* holds the highest concentration of weighted ESG risk.

### Phase C: Compliance & ESAP Tracking
*   **Technique:** Frequency Distribution Analysis.
*   **Process:** Quantified the distribution of ESAP statuses (Not Started, In Progress, Delayed, Closed).
*   **Outcome:** A clear operational metric identifying the % of the portfolio with outstanding compliance issues, enabling targeted intervention by Relationship Managers.

### Phase D: Green Finance Validation
*   **Technique:** Comparative Statistical Analysis (Boxplots).
*   **Process:** Analyzed the variance in Total ESG Risk Scores between "Green-Tagged" and "Standard" loans.
*   **Outcome:** Statistical validation that Green assets possess a lower median risk profile, confirming the integrity of the bank’s green taxonomy.

---

## 📊 Key Statistical Insights (Simulation Results)
*   **Portfolio Composition:** Analysis of 200 unique facilities with a total loan book of **$1.1 Billion**.
*   **Risk Concentration:** The **Agribusiness** sector exhibited the highest frequency of "High-Risk" flags, necessitating stricter credit covenants.
*   **Compliance Lag:** Analysis revealed that **~35%** of the portfolio has "Not Started" or is "Delayed" on ESAP implementation, representing a material compliance risk.
*   **Green Performance:** Green-tagged assets demonstrated a median Risk Score of **2.0 (Low)**, compared to a median of **4.0 (Medium-High)** for the standard portfolio, validating the correlation between sustainable lending and lower E&S risk.

---

## 🛠 Tools & Technologies
*   **Data Processing:** Python (Pandas for manipulation, NumPy for vectorization).
*   **Data Visualization:** Matplotlib & Seaborn (Bar charts, Pie charts, and Box-and-Whisker plots for distribution analysis).
*   **Formatting:** `FuncFormatter` for financial notation (Billions/Millions).

---

## 🚀 How to Run the Project

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/ESG-Portfolio-Risk-Framework.git
    ```
2.  **Install required libraries**
    ```bash
    pip install pandas numpy matplotlib seaborn
    ```
3.  **Run the simulation script**
    ```bash
    python esg_south_asia_simulation.py
    ```
4.  **View Outputs**
    *   The script will generate a **Management Report** in the terminal.
    *   It will create two CSV files: `south_asia_loan_portfolio.csv` and `south_asia_portfolio_summary.csv`.
    *   It will launch an interactive **Dashboard window** containing the 4 key charts.

---

## ⚖️ Disclaimer
This project is an independent analytical simulation designed for learning and portfolio demonstration purposes. It utilizes synthetic data structures to replicate banking compliance workflows and does not represent proprietary data or internal models of any specific financial institution.ation designed for portfolio demonstration. It utilizes synthetic data structures to replicate banking compliance workflows and does not represent proprietary data or internal models of any specific financial institution.
