import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter # Importing the formatter

def main():
    # ==========================================
    # 1. SETUP & RANDOM DATA GENERATION (SOUTH ASIA)
    # ==========================================
    print("--- [1/6] Generating synthetic South Asia portfolio data... ---")
    np.random.seed(42)
    n = 200

    data = {
        "Client_ID": [f"SA-{i:03d}" for i in range(1, n+1)],
        "Sector": np.random.choice(
            ["Agribusiness", "Manufacturing", "Textiles", "Renewable Energy", "Infrastructure", "Financial Services"],
            size=n
        ),
        "Country": np.random.choice(
            ["India", "Bangladesh", "Sri Lanka", "Pakistan", "Nepal", "Bhutan", "Maldives"],
            size=n,
            p=[0.4, 0.2, 0.1, 0.15, 0.05, 0.05, 0.05]
        ),
        # INCREASED LOAN AMOUNTS slightly so 'Billions' format looks better
        "Loan_Amount_USD": np.random.randint(5000000, 50000000, size=n),
        "Environmental_Risk": np.random.choice(["Low", "Medium", "High"], size=n, p=[0.3, 0.5, 0.2]),
        "Social_Risk": np.random.choice(["Low", "Medium", "High"], size=n, p=[0.4, 0.4, 0.2]),
        "HSE_Compliance": np.random.choice(["Yes", "No"], size=n, p=[0.70, 0.30]),
        "ESAP_Status": np.random.choice(
            ["Not Started", "In Progress", "Delayed", "Closed"],
            size=n,
            p=[0.25, 0.45, 0.10, 0.20]
        ),
        "Green_Finance_Tag": np.random.choice(["Yes", "No"], size=n, p=[0.20, 0.80])
    }

    df = pd.DataFrame(data)

    # ==========================================
    # 2. RISK SCORING & CALCULATION
    # ==========================================
    print("--- [2/6] Calculating ESG risk scores... ---")
    risk_map = {"Low": 1, "Medium": 2, "High": 3}

    df["E_Risk_Score"] = df["Environmental_Risk"].map(risk_map)
    df["S_Risk_Score"] = df["Social_Risk"].map(risk_map)
    
    # Total Score (Range 2 to 6)
    df["Total_ESG_Risk_Score"] = df["E_Risk_Score"] + df["S_Risk_Score"]

    # Flag High Risk Clients (Threshold >= 5)
    df["High_Risk_Flag"] = np.where(df["Total_ESG_Risk_Score"] >= 5, "Yes", "No")

    # ==========================================
    # 3. AGGREGATION & SUMMARY TABLES
    # ==========================================
    print("--- [3/6] Aggregating portfolio metrics... ---")
    
    # Portfolio Summary by Sector
    portfolio_summary = (
        df.groupby("Sector")
        .agg(
            Total_Loan_Amount=("Loan_Amount_USD", "sum"),
            Avg_ESG_Risk=("Total_ESG_Risk_Score", "mean"),
            High_Risk_Clients=("High_Risk_Flag", lambda x: (x == "Yes").sum())
        )
        .reset_index()
        .sort_values(by="Total_Loan_Amount", ascending=False)
    )

    # ESAP Status Count
    esap_status = (
        df.groupby("ESAP_Status")
        .size()
        .reset_index(name="Number_of_Clients")
    )

    # Green Finance Overview
    green_finance = (
        df.groupby("Green_Finance_Tag")
        .agg(
            Clients=("Client_ID", "count"),
            Loan_Book=("Loan_Amount_USD", "sum")
        )
        .reset_index()
    )

    # ==========================================
    # 4. EXPORT TO CSV
    # ==========================================
    print("--- [4/6] Exporting data to CSV... ---")
    try:
        df.to_csv("south_asia_loan_portfolio.csv", index=False)
        portfolio_summary.to_csv("south_asia_portfolio_summary.csv", index=False)
        print(" -> Files saved: 'south_asia_loan_portfolio.csv' and 'south_asia_portfolio_summary.csv'")
    except Exception as e:
        print(f" -> Error saving CSVs: {e}")

    # ==========================================
    # 5. EXECUTIVE MANAGEMENT REPORT (TERMINAL)
    # ==========================================
    print("\n" + "="*50)
    print("SOUTH ASIA REGION: ESG RISK MANAGEMENT REPORT")
    print("="*50)
    
    total_val = df['Loan_Amount_USD'].sum()
    high_risk_count = df[df['High_Risk_Flag']=='Yes'].shape[0]
    green_book = green_finance[green_finance['Green_Finance_Tag']=='Yes']['Loan_Book'].values[0] if 'Yes' in green_finance['Green_Finance_Tag'].values else 0

    print(f"Total Portfolio Value:   ${total_val:,.2f}")
    print(f"Total Clients:           {n}")
    print(f"High Risk Clients:       {high_risk_count} ({(high_risk_count/n)*100:.1f}%)")
    print(f"Green Finance Assets:    ${green_book:,.2f}")
    
    print("\n[A] Portfolio Sector Breakdown:")
    print("-" * 50)
    print(portfolio_summary.to_string(index=False))
    
    print("\n[B] Action Plan (ESAP) Status:")
    print("-" * 50)
    print(esap_status.to_string(index=False))
    print("="*50 + "\n")

    # ==========================================
    # 6. VISUALIZATION DASHBOARD
    # ==========================================
    print("--- [5/6] Generating Dashboard... ---")
    
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('South Asia Portfolio: ESG Risk Dashboard', fontsize=18, weight='bold')

    # Chart 1: High Risk Clients by Sector
    sns.countplot(ax=axes[0, 0], data=df, x='Sector', hue='High_Risk_Flag', palette='Reds')
    axes[0, 0].set_title("Count of High-Risk Clients by Sector", fontsize=14)
    axes[0, 0].legend(title='High Risk Flag')
    axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=45, ha='right')
    axes[0, 0].set_xlabel("Sector", fontsize=12)

    # --- Chart 2: Total Loan Exposure by Country (WITH BILLION FORMATTER) ---
    
    # 1. Define the formatting function
    def billions(x, pos):
        """Converts numbers to Billions (e.g., 1,500,000,000 -> 1.5B)"""
        return f'{x*1e-9:.1f}B'

    country_risk = df.groupby('Country')['Loan_Amount_USD'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(ax=axes[0, 1], data=country_risk, x='Loan_Amount_USD', y='Country', palette='viridis')
    axes[0, 1].set_title("Total Exposure by Country (USD)", fontsize=14)
    axes[0, 1].set_xlabel("Exposure (Billions $)")
    
    # 2. Apply the formatter to the X-axis
    axes[0, 1].xaxis.set_major_formatter(FuncFormatter(billions))

    # Chart 3: ESAP Status
    esap_counts = df['ESAP_Status'].value_counts()
    axes[1, 0].pie(esap_counts, labels=esap_counts.index, autopct='%1.1f%%', 
                   colors=sns.color_palette('pastel'), startangle=90)
    axes[1, 0].set_title("Portfolio ESAP Status Overview", fontsize=14)

    # Chart 4: Green vs Standard Risk Scores
    sns.boxplot(ax=axes[1, 1], data=df, x='Green_Finance_Tag', y='Total_ESG_Risk_Score', palette='Greens')
    axes[1, 1].set_title("ESG Risk Score Distribution: Green vs. Standard", fontsize=14)
    axes[1, 1].set_ylabel("Total ESG Risk Score (2-6)")

    # --- LAYOUT FIX ---
    plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=4.0, w_pad=2.0)
    
    print("--- [6/6] Dashboard launched. Close window to finish. ---")
    plt.show()

if __name__ == "__main__":
    main()