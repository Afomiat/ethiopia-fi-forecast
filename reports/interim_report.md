# Interim Submission Report: Financial Inclusion Forecasting in Ethiopia

**Challenge Wave:** 10 Academy Challengers  
**Analyst:** Antigravity (Data Scientist, Selam Analytics)  
**Date:** July 18, 2026  

---

## Executive Summary
This report summarizes the data setup, enrichment, and exploratory data analysis (EDA) for the financial inclusion forecasting system in Ethiopia. Our models track two key target indicators defined by the World Bank's Global Findex:
1. **Access** (Account Ownership Rate, `ACC_OWNERSHIP`)
2. **Usage** (Digital Payment Adoption Rate, `USG_DIGITAL_PAYMENT`)

Despite the massive expansion of mobile money platforms (such as *telebirr* and *M-Pesa*) between 2021 and 2024, our analysis reveals a deceleration in account ownership growth. We identify critical gender gaps and a persistent disconnect between account registration and active usage.

---

## 1. Data Enrichment Summary (Task 1)

To build a reliable forecasting model, we enriched the starter dataset with 17 new records (9 observations, 3 events, and 5 impact links) from official Findex, operator, and regulatory sources. These additions target specific data gaps in the historical timeline.

| Record ID | Type | Indicator / Event | Year / Date | Value / Status | Source / URL | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REC_0034** | Observation | Account Ownership Rate (`ACC_OWNERSHIP`) | 2011-12-31 | 14.0% | Global Findex 2011 | Establish absolute baseline for access |
| **REC_0035** | Observation | Digital Payment Adoption (`USG_DIGITAL_PAYMENT`) | 2014-12-31 | 1.2% | Global Findex 2014 | Historical baseline for usage |
| **REC_0036** | Observation | Digital Payment Adoption (`USG_DIGITAL_PAYMENT`) | 2017-12-31 | 12.0% | Global Findex 2017 | Usage trend prior to mobile money push |
| **REC_0037** | Observation | Digital Payment Adoption (`USG_DIGITAL_PAYMENT`) | 2021-12-31 | 21.0% | Global Findex 2021 | Usage baseline at start of Telebirr rollout |
| **REC_0038** | Observation | Digital Payment Adoption (`USG_DIGITAL_PAYMENT`) | 2024-11-29 | 35.0% | Global Findex 2024 | Current usage target point |
| **REC_0039** | Observation | Account Ownership (Male) | 2024-11-29 | 56.5% | Global Findex 2024 | Current gender access (Male) |
| **REC_0040** | Observation | Account Ownership (Female) | 2024-11-29 | 41.6% | Global Findex 2024 | Current gender access (Female) |
| **REC_0041** | Observation | Digital Payment Adoption (Male) | 2021-12-31 | 26.0% | Global Findex 2021 | Gender usage baseline (Male) |
| **REC_0042** | Observation | Digital Payment Adoption (Female) | 2021-12-31 | 16.0% | Global Findex 2021 | Gender usage baseline (Female) |
| **EVT_0011** | Event | NBE Directive ONPS/01/2020 | 2020-04-01 | Implemented | National Bank of Ethiopia | Landmark policy enabling non-bank mobile money |
| **EVT_0012** | Event | NBE Foreign Operator Liberalization | 2022-10-18 | Implemented | National Bank of Ethiopia | Regulatory change allowing Safaricom/M-Pesa |
| **EVT_0013** | Event | Telebirr & Dashen Bank Sanduq Launch | 2022-08-04 | Launched | Ethio Telecom | Micro-savings/micro-credit product launch |

**Impact Links Added:**
- **IMP_0015 & IMP_0016:** Link ONPS/01/2020 Directive and Foreign Operator Liberalization to Mobile Money Account Rate (`ACC_MM_ACCOUNT`) with 12 and 10 months lags respectively.
- **IMP_0017, IMP_0018 & IMP_0019:** Link Telebirr Sanduq, Telebirr Launch, and M-Pesa Launch to Digital Payment Adoption (`USG_DIGITAL_PAYMENT`) to capture product-driven usage.

---

## 2. Key Insights from Exploratory Data Analysis (Task 2)

We generated 6 primary visualizations (saved in [reports/figures/](file:///c:/Users/acer/Downloads/10%20Acadamy/projects/Week_11/reports/figures/)) to analyze the data.

### Insight 1: Deceleration in Account Ownership Growth (2021-2024)
*   **Evidence:** Account ownership grew by **+13pp** (2014-2017) and **+11pp** (2017-2021), but decelerated to just **+3pp** between 2021 and 2024, despite the launch of Telebirr (which grew to over 54M registered accounts).
*   **Interpretation:** The growth curve is flattening. The massive user acquisition by mobile money operators primarily onboarded existing bank account holders (multi-homing) rather than pulling the unbanked population into the financial sector. 
*   *Supporting Figure:* `reports/figures/account_ownership_trajectory.png`

### Insight 2: The "Registered vs. Active" Mobile Money Usage Gap
*   **Evidence:** By 2024/2025, mobile money registrations exceeded **65 million** (54.8M Telebirr + 10.8M M-Pesa), representing roughly **93% of the adult population**. Yet, the 2024 Findex survey reports that only **9.45% of adults** have a dedicated mobile money account, and **35% of adults** made or received digital payments.
*   **Interpretation:** A vast majority of registered mobile money accounts are either dormant or bank-linked. In Ethiopia, bank accounts are highly accessible and trusted; mobile money functions primarily as a digital wallet channel for people who *already* have bank accounts, rather than a standalone banking alternative.
*   *Supporting Figure:* `reports/figures/digital_payments_vs_mobile_money.png`

### Insight 3: Persistent and Evolving Gender Gap
*   **Evidence:** The account ownership gender gap in 2021 was **20pp** (56% male, 36% female). By 2024, the gap stood at **15pp** (56.5% male, 41.6% female). Women hold only **14% of mobile money accounts** (NBE/Shega 2024).
*   **Interpretation:** Although the overall access gap narrowed slightly (from 20pp to 15pp), women are severely underrepresented in the mobile money space. The digital usage gender gap is reinforced by a **24% gender gap in mobile phone ownership** (GSMA 2024).
*   *Supporting Figure:* `reports/figures/account_ownership_trajectory.png`

### Insight 4: P2P Dominance and Cash Crossover
*   **Evidence:** For the first time in Ethiopian history, P2P digital transaction volumes surpassed ATM cash withdrawals in FY2024/25, reaching a crossover ratio of **1.08** (128.3M P2P transactions vs 119.3M ATM transactions). P2P transactions grew **+158% YoY**, while cash ATM transactions grew only **+26%**.
*   **Interpretation:** Ethiopia's digital usage is experiencing structural change. P2P rails are used not only for transfers, but extensively for merchant commerce (P2P-as-Merchant pay). This shifts the digital payment ecosystem from a cash-out model to a digital circulation model.
*   *Supporting Figure:* `reports/figures/event_timeline_overlay.png`

### Insight 5: High Infrastructure and Policy Elasticity
*   **Evidence:** Linear correlation on interpolated data shows a strong correlation (**0.89**) between 4G population coverage (which grew from 37.5% to 70.8% by 2025) and P2P transaction count, and a **0.94** correlation between account ownership and digital payment adoption.
*   **Interpretation:** Infrastructure expansion (4G, mobile penetration) and structural enablers (Fayda Digital ID, reaching 15M registrations in 2025) are leading indicators. They act as supply-side triggers that directly forecast jumps in demand-side survey outcomes.
*   *Supporting Figure:* `reports/figures/correlation_matrix.png` and `infrastructure_enablers.png`

---

## 3. Preliminary Observations on Event-Indicator Relationships

By overlaying key product and policy milestones on the indicator trend lines, we observe clear trigger-response patterns:
1.  **Telebirr Launch (May 2021):** Preceded by the NBE ONPS/01/2020 Directive. This regulation triggered a transition from bank-only access to rapid mobile wallet adoption. Mobile money account ownership doubled (from 4.7% to 9.45%) in the three years following.
2.  **Safaricom Market Entry (Aug 2022) & M-Pesa Launch (Aug 2023):** Ended the state telecom monopoly and stimulated competitive investments in infrastructure (doubling 4G population coverage to 70.8%).
3.  **Fayda Digital ID Rollout (Jan 2024):** Coincides with the acceleration of P2P transaction value (reaching ETB 577.7 billion in 2025) by simplifying remote e-KYC compliance for operators.

---

## 4. Data Limitations Identified

The primary constraints to establishing a traditional forecasting model are:
1.  **Sparse Survey Points:** The target indicators (`ACC_OWNERSHIP` and `USG_DIGITAL_PAYMENT`) are demand-side survey metrics from the Global Findex. We have only 4-5 survey waves (2011, 2014, 2017, 2021, 2024), meaning there are large data gaps in intermediate years.
2.  **Short Trajectory for Enablers:** High-frequency enabler indicators (like Fayda registrations, 4G coverage, and transaction volume) only have continuous data starting from 2023/24, making long-term regression models sensitive to short-term trends.
3.  **Multi-Homing Ambiguity:** We lack administrative data to count how many users possess both a bank account and a mobile money account, which makes it difficult to model the exact overlap.
