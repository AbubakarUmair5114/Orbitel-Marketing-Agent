# Orbitel Automated Customer Sentiment & Churn Risk Intelligence Engine
> **Enterprise AI Automation & Executive Business Intelligence Flagship Portfolio**  
> **Role Targeted:** AI Automation & Analytics Specialist (Reporting Directly to Company Owner)  
> **Author:** AI Automation & Analytics Specialist  
> **Live Production Artifacts:** [n8n Workflow](file:///c:/Users/ABC/Orbitel-marketing_agent/workflows/orbitel_feedback_intelligence_engine.json) • [Power BI Scorecard Mockup](file:///c:/Users/ABC/Orbitel-marketing_agent/powerbi/orbitel_executive_scorecard_mockup.html) • [Master Dataset](file:///c:/Users/ABC/Orbitel-marketing_agent/data/orbitel_master_dataset_21_records.csv) • [DAX Measures](file:///c:/Users/ABC/Orbitel-marketing_agent/powerbi/dax_measures_and_columns.dax)

---

## Executive Summary

The **Orbitel Automated Customer Sentiment & Churn Risk Intelligence Engine** is an enterprise-grade, closed-loop AI automation and business intelligence platform designed for telecommunications operators. It autonomously transforms high-volume, unstructured customer feedback into real-time operational escalations and C-Suite executive intelligence.

Operating at the intersection of **AI workflow automation (n8n)**, **cognitive language modeling (OpenAI GPT-4o-mini)**, **cloud data persistence (Google Sheets / GCP Service Accounts)**, and **executive data analytics (Power BI Bento Grid)**, this system eliminates manual ticket lag, prevents B2B subscriber churn, and surfaces mission-critical operational bottlenecks within seconds.

```
+----------------------------------------------------------------------------------------------------+
|                                    END-TO-END PIPELINE OVERVIEW                                    |
|                                                                                                    |
|  [Inbound Feedback]                                                                                |
|          │                                                                                         |
|          ▼                                                                                         |
|  [Webhook Ingestion] ────► [Schema Validation] ────► (Invalid <10 chars? ──► HTTP 400 Bad Request)|
|                                    │                                                               |
|                                    ▼                                                               |
|                       [Client-Side PII Masking]                                                    |
|                                    │                                                               |
|                                    ▼                                                               |
|                       [GPT-4o-mini AI Agent] ──► (Multi-Variable Extraction: 33 Attributes)        |
|                                    │                                                               |
|                                    ▼                                                               |
|                       [Historical Dedup Engine] ──► (Signal Lookback Window: 48h to 90d)           |
|                                    │                                                               |
|                                    ▼                                                               |
|                       [Google Cloud Master Ledger] ──► [HTTP 200 OK Response]                      |
|                                    │                                                               |
|            ┌───────────────────────┴───────────────────────┐                                       |
|            ▼                                               ▼                                       |
|  [Real-Time Escalations]                         [Power BI Executive Scorecard]                    |
|  - Operations (Coverage Blackouts)               - 1920x1080 Single-Page Bento Grid                |
|  - Finance (Billing Disputes)                    - 5 Uniform KPI Cards                             |
|  - Marketing (Retention / Pricing)               - 100% Stacked Bar (Excl. Unknown)                |
|  - Sales (B2B Upsell Leads)                      - Sentiment Mix Donut & Monthly Trend Line        |
|  - HR (Frontline Conduct Review)                 - Operational High-Priority Triage Table          |
+----------------------------------------------------------------------------------------------------+
```

---

## 1. System Architecture & Engineering Components

### Component 1: Real-Time Webhook Ingestion & Strict Validation
- **Ingestion Endpoint:** Asynchronous webhook listener listening for incoming customer feedback payloads (`POST /webhook/receive-feedback`).
- **Strict Schema Enforcement:** Deterministic validation validating `text`, `customer_id`, `customer_type`, `service_type`, and `source`.
  - Enforces minimum `text` length of >= 10 characters after whitespace collapse.
  - Automatically rejects malformed payloads with structured **HTTP 400 Bad Request** responses (`{ status: 'error', error: '...', field: '...' }`).

### Component 2: Client-Side PII Masking & Heuristic Urgency Overrides
- **Zero PII Leakage:** Deterministic regex pre-processor that strips customer emails and Pakistani mobile phone formats (`+92 3XX XXXXXXX`, `03XX-XXXXXXX`, `923XXXXXXXXX`), substituting them with `[EMAIL_REMOVED]` and `[PHONE_REMOVED]` *prior* to external LLM exposure.
- **Urgency Heuristic Override:** RegEx rules intercepting critical telecom trigger phrases (e.g., `outage`, `sue`, `switch`, `MNP`, `PTA`, `fraud`, as well as Roman Urdu triggers like `band karo`, `dobara nahi chahiye`, `chorna`) automatically forcing `urgency = "high"`.

### Component 3: Cognitive Extraction Agent (OpenAI GPT-4o-mini)
- **Multi-Variable Entity Extraction:** Transforms raw, unstructured customer statements into **33 discrete attributes**, including:
  - Sentiment (`positive`, `negative`, `neutral`) & Confidence Score (`0.00` to `1.00`)
  - Issue Categories (`network`, `billing`, `pricing`, `coverage`, `customer_service`, `roaming`, `service_delay`)
  - Urgency (`high`, `medium`, `low`) & Churn Risk (`TRUE`/`FALSE`)
  - Root Cause Summary & Actionable Recommendations
  - Department Routing (`operations`, `finance`, `marketing`, `sales`, `hr`)
  - Customer & Value Segmentation (`low`, `medium`, `high`, `premium`)
  - Tailored Retention Incentives (Discount, Bonus Data, Service Credit) & Pre-Drafted Customer Outreach Messages
- **Fail-Safe Robust Parsing:** Recursive brace-matching parser with 3 retries and automatic fallback to a human supervisor review state upon API error.

### Component 4: Multi-Window Deduplication & Anti-Flood Shield
Prevents department heads from being bombarded when a customer logs duplicate complaints across channels within a short interval:
- **Coverage Expansion:** 7-Day Window (168h)
- **Billing Issues:** 30-Day Window (720h)
- **Service Recovery:** 48-Hour Window (48h)
- **HR Misconduct:** 7-Day Window (168h)
- **Upsell Inquiries:** 30-Day Window (720h)
- **Product Feedback:** 90-Day Window (2160h)
- Duplicate records are stamped with `is_duplicate = TRUE` and linked to `duplicate_of = parent_record_id`, suppressing email alerts while maintaining ledger auditability.

### Component 5: Enterprise Master Ledger Persistence
- **Cloud Data Lake:** Synchronous write to Orbitel's enterprise master ledger authenticated through an asymmetric RSA private key via a **Google Cloud Service Account**.
- **Idempotency:** Uses `record_id` as primary match key to ensure zero duplicated row creation during retry execution.

### Component 6: Real-Time Department Escalations (Gmail OAuth2)
- **Trigger Condition:** Instant email routing when `churn_risk = TRUE` or `urgency = "high"` and `is_duplicate = FALSE`.
- **Department Routing Matrix:**
  1. **Operations Desk:** Cell tower blackouts, fiber cuts, high latency, signal dead-zones.
  2. **Finance Desk:** Unauthorized roaming charges, billing disputes, double-rentals, mystery VAS.
  3. **Marketing Desk:** Competitor pricing matching (Jazz/Zong/Telenor), tariff churn mitigation.
  4. **Sales Desk:** Roaming passes, SME corporate fleet expansions, static IP requests.
  5. **HR / QA Desk:** Call center agent misconduct, rude branch franchise staff.
- **Security:** Strict HTML entity escaping neutralizing potential email injection / stored XSS vulnerabilities.

---

## 2. Power BI Executive Scorecard Specifications

The Power BI scorecard is an executive single-page **Bento Grid** designed for 16:9 widescreen monitoring (**1920 × 1080 native resolution**).

```
+----------------------------------------------------------------------------------------------------+
|  EXECUTIVE CUSTOMER SENTIMENT & CHURN RISK             [Customer_Type] [Urgency] [Service] [Dates] |
+----------------------------------------------------------------------------------------------------+
| [ 21 ] Total     [ 33.3% ] Sat Rate    [ 52.4% ] Dissat    [ 47.6% ] Churn Risk   [ 0.89 ] Quality |
+----------------------------------------------------------------------------------------------------+
| [100% Stacked Bar Chart]             [Horizontal Bar Chart]            [Donut Chart]               |
| Churn Risk by Value Segment          Dept Escalations & Drivers        Overall Customer Sentiment  |
| - Low: 50% High Risk                 - Operations: 5 High Risk         - Negative: 52.38% (11)     |
| - Medium: 40% High Risk              - Finance: 3 High Risk            - Positive: 33.33% (7)      |
| - High: 16.7% High Risk              - Marketing: 2 High Risk          - Neutral: 14.29% (3)       |
| - Premium: 85.7% High Risk           - Sales: 0 / HR: 0                (Total: 21 Records)         |
| (Visual Filter: Excludes 'unknown')  (X-Axis: Count of High Risk)                                  |
+----------------------------------------------------------------------------------------------------+
| [Time-Series Line Chart with Markers]                [High-Priority Operational Triage Table]      |
| Monthly Satisfaction vs. Dissatisfaction Trend       churn_risk = TRUE OR urgency = "high"         |
| - Aug 2026: Sat 28.6% | Dissat 57.1%                Columns: Customer ID, Location, Issues,       |
| - Sep 2026: Sat 28.6% | Dissat 57.1%                         Urgency, Root Cause Summary           |
| - Oct 2026: Sat 42.9% | Dissat 42.9%                Header: #1E293B bold white, Zebra striping,    |
| (Markers: Size 6 Circle | Percentage Y-Axis)         Horizontal lines only, Auto-fitted widths     |
+----------------------------------------------------------------------------------------------------+
```

### A. Top Header & Dropdown Slicers
- **Slicers:** Positioned horizontally in the top-right header as compact **Dropdowns** (not tiles or checkboxes):
  - `Customer_type` (`All`, `corporate`, `enterprise`, `household`, `individual`, `sme`)
  - `urgency` (`All`, `high`, `medium`, `low`)
  - `service_type` (`All`, `broadband`, `fiber`, `postpaid`, `prepaid`)
  - `Time Stamp` (`Between` date slider / dropdown)

### B. Top KPI Ribbon (5 Uniform Cards with Horizontal Distribution)
1. **Total Feedback:** `21` (Field: `Total_Records = COUNTROWS('Sheet1')`)
2. **Satisfaction Rate:** `33.3%` (Field: `Positive_Sentiment_Pct`, green callout `#27ae60`, 1 decimal place)
3. **Dissatisfaction Rate:** `52.4%` (Field: `Negative_Sentiment_Pct`, dark charcoal `#0F172A`, 1 decimal place)
4. **Churn Risk:** `47.6%` (Field: `Churn_Rate_Pct`, alert red callout `#c0392b`, formatted as percentage with 1 decimal place)
5. **Model Quality:** `0.89` (Field: `Avg_Confidence_Score = AVERAGE('Sheet1'[confidence_score])`, 2 decimal places)

### C. Visual Charts (Middle & Bottom Grid)
1. **Churn Risk by Customer Value Segment (100% Stacked Bar Chart):**
   - Y-Axis: `customer_value_segment` (`low`, `medium`, `high`, `premium`). **Excludes `unknown`** via visual filter.
   - X-Axis: `Total_Records`.
   - Legend: `Churn_Status` (`High Risk` in red `#c0392b`, `Low Risk` in slate gray `#64748B`).
2. **Department Escalations & Churn Drivers (Horizontal Bar Chart):**
   - Y-Axis: `target_department` (Operations leading with network issues, Finance with billing, Marketing with pricing).
   - X-Axis: Count of high-risk records.
3. **Overall Customer Sentiment Mix (Donut Chart):**
   - Legend: `sentiment` (Negative 52.38% `#c0392b`, Positive 33.33% `#27ae60`, Neutral 14.29% `#94A3B8`).
   - Values: `Total_Records`.
4. **Monthly Satisfaction vs. Dissatisfaction Trend (Time-Series Line Chart):**
   - X-Axis: `Month_Year` (Aug 2026, Sep 2026, Oct 2026) with labels explicitly enabled.
   - Y-Axis: `Positive_Sentiment_Pct` (green) and `Negative_Sentiment_Pct` (red), formatted on percentage axis.
   - Markers enabled on data points (size 6 circle) to clearly convey trajectory.
5. **High-Priority Customer Escalations (Executive Triage Table):**
   - Placed in the bottom-right quadrant to ground the dashboard with operational transparency.
   - Columns: `customer_id`, `location_mentioned`, `issue_categories`, `urgency`, `root_cause_summary`.
   - Filter on visual: `churn_risk = TRUE` or `urgency = "high"`.
   - Styling: Header `#1E293B` with bold white text, subtle alternating row zebra-striping (`#FFFFFF` and `#F8FAFC`), horizontal gridlines only (`#E2E8F0`), no vertical bars, column widths auto-fitted so text displays without horizontal scrolling.

### D. Production DAX Formulations
```dax
// Volume
Total_Records = COUNTROWS('Sheet1')

// Churn Risk Rate %
Churn_Rate_Pct = 
DIVIDE(
    CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[churn_risk] = TRUE()),
    COUNTROWS('Sheet1'),
    0
)

// Customer Satisfaction Rate %
Positive_Sentiment_Pct = 
DIVIDE(
    CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[sentiment] = "positive"),
    COUNTROWS('Sheet1'),
    0
)

// Customer Dissatisfaction Rate %
Negative_Sentiment_Pct = 
DIVIDE(
    CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[sentiment] = "negative"),
    COUNTROWS('Sheet1'),
    0
)

// Average Confidence Score
Avg_Confidence_Score = AVERAGE('Sheet1'[confidence_score])

// Calculated Columns
Churn_Status = IF('Sheet1'[churn_risk] = TRUE(), "High Risk", "Low Risk")
Month_Year = FORMAT('Sheet1'[timestamp], "MMM YYYY")
YearMonth_Sort = YEAR('Sheet1'[timestamp]) * 100 + MONTH('Sheet1'[timestamp])
Location_Clean = IF(ISBLANK('Sheet1'[location_mentioned]), "Unknown", TRIM(LEFT('Sheet1'[location_mentioned], SEARCH(" ", 'Sheet1'[location_mentioned] & " ") - 1)))
```

---

## 3. Repository File Structure

```
Orbitel-marketing_agent/
│
├── README.md                                # Flagship project documentation & system blueprint
├── ARCHITECTURE.md                          # Technical architecture, Mermaid diagrams & threat model
├── PORTFOLIO_EXECUTIVE_SUMMARY.md           # Business impact, ROI & owner-facing pitch memo
│
├── workflows/
│   └── orbitel_feedback_intelligence_engine.json  # Complete production n8n workflow export
│
├── data/
│   ├── orbitel_master_dataset_21_records.csv      # Certified 21-row master ledger dataset
│   └── orbitel_master_dataset_21_records.json     # JSON mirror with all 33 discrete attributes
│
├── powerbi/
│   ├── dax_measures_and_columns.dax         # Production DAX measures & calculated columns
│   ├── theme_orbitel_executive.json         # Custom Power BI Bento Grid theme file
│   ├── powerbi_layout_specification.md      # Pixel-perfect 1920x1080 layout coordinates & guide
│   ├── scorecard_build_guide.md             # Step-by-step build & deployment manual
│   └── orbitel_executive_scorecard_mockup.html # Interactive HTML mockup with live slicers & charts
│
├── scripts/
│   ├── generate_dataset.py                  # Dataset generation script with mathematical assertions
│   └── test_webhook_payloads.py             # Validation, security & deduplication test suite
│
└── templates/                               # Responsive HTML email escalation templates
    ├── email_operations.html                # Operations cell tower / coverage escalation
    ├── email_finance.html                   # Finance billing dispute & refund escalation
    ├── email_sales.html                     # Commercial B2B upsell lead dispatch
    ├── email_marketing.html                 # Competitor churn & pricing retention alert
    └── email_hr.html                        # Frontline customer care conduct alert
```

---

## 4. Verification & Testing Instructions

### 1. Run the Dataset Generator & Validator
To re-generate or verify the certified 21-record master dataset matching the exact numbers:
```bash
python scripts/generate_dataset.py
```
*Output validates:* Total = 21, Positive = 33.3%, Negative = 52.4%, Neutral = 14.3%, Churn = 47.6%, Avg Confidence = 0.89.

### 2. Execute the Security & Webhook Test Suite
To verify strict schema validation, HTTP 400 rejections, PII redaction, and time-window deduplication:
```bash
python scripts/test_webhook_payloads.py
```
*Output validates:* 6 / 6 test suites passed with 100% success.

### 3. Launch the Interactive Executive Scorecard Mockup
Open [powerbi/orbitel_executive_scorecard_mockup.html](file:///c:/Users/ABC/Orbitel-marketing_agent/powerbi/orbitel_executive_scorecard_mockup.html) in any web browser to interact with the responsive 1920x1080 Bento Grid dashboard, test the dropdown slicers, inspect the 100% stacked bar chart, and review the live operational triage log.

---

## 5. Strategic Value for the Role

This production project directly substantiates readiness for the **AI Automation & Analytics Specialist** role:
- **Direct Owner Alignment:** High-impact executive scorecards focused on EBITDA protection, churn mitigation, and top-line expansion.
- **Autonomous Systems Thinking:** Closed-loop architecture that detects, routes, persists, and visualizes customer telemetry without requiring human data entry.
- **Production-Grade Rigor:** Hardened with client-side privacy controls, schema validation, rate-limiting anti-flood shields, and resilient fallback states.

