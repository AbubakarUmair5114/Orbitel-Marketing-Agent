# Power BI Executive Scorecard Build & Deployment Guide
## Orbitel Automated Customer Sentiment & Churn Risk Intelligence Engine

This step-by-step implementation guide provides complete instructions for standing up the C-level Executive Bento Grid Scorecard in Power BI Desktop or Power BI Service.

---

## 1. Data Ingestion & Source Connection

### Option A: Direct Google Sheets Master Ledger (Live Cloud Sync)
1. Open **Power BI Desktop**.
2. Select **Get Data** -> **Web** (or **Google Sheets** connector).
3. Enter the authenticated URL of the Orbitel Master Sheet:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_ORBITEL_MASTER_SHEET_ID/edit#gid=0
   ```
4. Authenticate via Google OAuth / Organizational Account.
5. In Power Query, name the table **`Sheet1`**.

### Option B: Local Production Export (Offline Verification)
1. Select **Get Data** -> **Text/CSV**.
2. Select `data/orbitel_master_dataset_21_records.csv`.
3. In Power Query Editor:
   - Ensure `confidence_score` is formatted as **Decimal Number**.
   - Ensure `churn_risk` and `is_duplicate` are formatted as **True/False (Logical)**.
   - Ensure `timestamp` is formatted as **Date/Time/Timezone**.
4. Click **Close & Apply**.

---

## 2. Theme Installation & Canvas Configuration

1. In the Power BI ribbon, navigate to **View** -> **Themes dropdown** -> **Browse for themes**.
2. Select `powerbi/theme_orbitel_executive.json`.
   - Automatically initializes corporate palette: `#c0392b` (Alert Red), `#27ae60` (Positive Green), `#0F172A` (Dark Charcoal), `#1E293B` (Slate Dark), `#64748B` (Slate Gray).
3. Configure Canvas Settings:
   - Click blank canvas -> **Format page** -> **Canvas settings**.
   - Type: **Custom** -> Width: **1920 px**, Height: **1080 px** (16:9 ratio).
   - Canvas background: Color `#F8FAFC`, Transparency: `0%`.

---

## 3. DAX Measures & Calculated Columns Setup

Open **Modeling** -> **New Measure** or **New Column**, and load the measures from `powerbi/dax_measures_and_columns.dax`:

### A. Calculated Columns
```dax
Churn_Status = IF('Sheet1'[churn_risk] = TRUE(), "High Risk", "Low Risk")

Month_Year = FORMAT('Sheet1'[timestamp], "MMM YYYY")

YearMonth_Sort = YEAR('Sheet1'[timestamp]) * 100 + MONTH('Sheet1'[timestamp])

Location_Clean = IF(ISBLANK('Sheet1'[location_mentioned]), "Unknown", TRIM(LEFT('Sheet1'[location_mentioned], SEARCH(" ", 'Sheet1'[location_mentioned] & " ") - 1)))
```
*Note: Select `Month_Year` -> Click **Column Tools** -> **Sort by Column** -> Choose `YearMonth_Sort` to enforce chronological order (Aug 2026 -> Sep 2026 -> Oct 2026).*

### B. Core Executive Measures
```dax
// Volume
Total_Records = COUNTROWS('Sheet1')

// Customer Satisfaction Rate % (Callout Color: #27ae60, 1 Decimal)
Positive_Sentiment_Pct = 
DIVIDE(
    CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[sentiment] = "positive"),
    COUNTROWS('Sheet1'),
    0
)

// Customer Dissatisfaction Rate % (Callout Color: #0F172A, 1 Decimal)
Negative_Sentiment_Pct = 
DIVIDE(
    CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[sentiment] = "negative"),
    COUNTROWS('Sheet1'),
    0
)

// Churn Risk Rate % (Callout Color: #c0392b, 1 Decimal)
Churn_Rate_Pct = 
DIVIDE(
    CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[churn_risk] = TRUE()),
    COUNTROWS('Sheet1'),
    0
)

// Model Confidence Score (Callout Color: #1E293B, 2 Decimals)
Avg_Confidence_Score = AVERAGE('Sheet1'[confidence_score])

// High-Risk Escalations Count (for Department Bar Chart)
High_Risk_Escalations_Count = CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[churn_risk] = TRUE())
```

---

## 4. Visual Component Assembly

### Top Header & Dropdown Slicers (`Y: 20px - 105px`)
1. Insert **Shape** (Rounded Rectangle, Radius 8px) at `X: 30`, `Y: 20`, `W: 1860`, `H: 85`. Fill `#FFFFFF`, Border `#E2E8F0`.
2. Add Title Text Box at `X: 55`, `Y: 35`:
   - Title: `Executive Customer Sentiment & Churn Risk` (Segoe UI Bold, 20pt, `#0F172A`).
   - Subtitle: `Orbitel Telecommunications • Real-Time AI Intelligence Engine` (Segoe UI, 10pt, `#64748B`).
3. Add 4 Slicers in Top Right (Format: **Dropdown**):
   - **Customer Type:** `'Sheet1'[Customer_type]` (`X: 880`, `W: 220`)
   - **Urgency:** `'Sheet1'[urgency]` (`X: 1120`, `W: 200`)
   - **Service Type:** `'Sheet1'[service_type]` (`X: 1340`, `W: 220`)
   - **Timestamp:** `'Sheet1'[timestamp]` as Date Range Slider (`X: 1580`, `W: 280`)

### Top KPI Ribbon (`Y: 120px - 225px`)
Insert 5 **Card** visuals (`W: 357`, `H: 105`, Spacing `18px`):
1. **Total Feedback (`X: 30`):** Measure `[Total_Records]` -> Value: `21`.
2. **Satisfaction Rate (`X: 405`):** Measure `[Positive_Sentiment_Pct]` -> Value: `33.3%`. Callout color `#27ae60`.
3. **Dissatisfaction Rate (`X: 780`):** Measure `[Negative_Sentiment_Pct]` -> Value: `52.4%`. Callout color `#0F172A`.
4. **Churn Risk (`X: 1155`):** Measure `[Churn_Rate_Pct]` -> Value: `47.6%`. Callout color `#c0392b`.
5. **Model Quality (`X: 1530`):** Measure `[Avg_Confidence_Score]` -> Value: `0.89`. Callout color `#1E293B`.

### Middle Grid Charts (`Y: 240px - 625px`)
1. **Visual 1 (Left - `W: 590`): 100% Stacked Bar Chart**
   - Y-Axis: `'Sheet1'[customer_value_segment]`
   - X-Axis: `[Total_Records]`
   - Legend: `'Sheet1'[Churn_Status]` (`High Risk` = `#c0392b`, `Low Risk` = `#64748B`)
   - Visual Filter: `'Sheet1'[customer_value_segment]` is not `unknown`.
2. **Visual 2 (Center - `W: 590`): Clustered Horizontal Bar Chart**
   - Y-Axis: `'Sheet1'[target_department]` (Operations, Finance, Marketing, Sales, HR)
   - X-Axis: `[High_Risk_Escalations_Count]`
   - Bars: Solid Corporate Blue `#2980b9` with bold data labels.
3. **Visual 3 (Right - `W: 640`): Donut Chart**
   - Legend: `'Sheet1'[sentiment]`
   - Values: `[Total_Records]`
   - Slices: Negative (52.38% - `#c0392b`), Positive (33.33% - `#27ae60`), Neutral (14.29% - `#94A3B8`).

### Bottom Grid Trend & Operational Triage (`Y: 640px - 1055px`)
1. **Visual 4 (Bottom Left - `W: 890`): Monthly Line Chart**
   - X-Axis: `'Sheet1'[Month_Year]`
   - Y-Axis: `[Positive_Sentiment_Pct]` (Green `#27ae60`), `[Negative_Sentiment_Pct]` (Red `#c0392b`)
   - Format: **Markers ON** (Shape: Circle, Size: 6), Data labels ON, Percentage axis (0% - 100%).
2. **Visual 5 (Bottom Right - `W: 952`): Executive Triage Table**
   - Visual Filter: `'Sheet1'[churn_risk] = TRUE` **OR** `'Sheet1'[urgency] = "high"`.
   - Columns:
     1. `'Sheet1'[customer_id]`
     2. `'Sheet1'[location_mentioned]`
     3. `'Sheet1'[issue_categories]`
     4. `'Sheet1'[urgency]`
     5. `'Sheet1'[root_cause_summary]`
   - Table Style: Header `#1E293B` bold white, zebra striping `#FFFFFF` & `#F8FAFC`, horizontal gridlines `#E2E8F0`, no vertical lines, auto-fit columns.

---

## 5. Automated Refresh Scheduling

1. Publish report to Power BI Workspace (e.g., `Orbitel Executive Scorecards`).
2. Navigate to Dataset Settings -> **Scheduled Refresh**.
3. Set refresh cadence:
   - **Frequency:** Daily or Hourly (aligns with n8n real-time write speed).
   - **Gateway Connection:** Cloud direct OAuth2 for Google Sheets API.

