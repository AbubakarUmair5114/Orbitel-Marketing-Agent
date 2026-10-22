# Power BI Executive Scorecard Specification
## Orbitel Automated Customer Sentiment & Churn Risk Intelligence Engine
**Target Canvas:** 16:9 Aspect Ratio (1920 × 1080 px Native Resolution)  
**Theme:** Orbitel Bento Grid Enterprise Theme (`theme_orbitel_executive.json`)  
**Target Audience:** Company Owner, VP Customer Operations, Chief Commercial Officer (CCO)

---

## 1. Canvas Geometry & Grid Blueprint (1920 × 1080)

```
+----------------------------------------------------------------------------------------------------+
| TOP HEADER & DROPDOWN SLICERS (Y: 20px - 105px | Height: 85px)                                     |
| [Orbitel Logo / Title]                              [Customer_type] [Urgency] [Service] [Timestamp]|
+----------------------------------------------------------------------------------------------------+
| KPI RIBBON (5 Uniform Cards | Y: 120px - 225px | Height: 105px)                                     |
| [1. Total: 21] [2. Sat Rate: 33.3%] [3. Dissat: 52.4%] [4. Churn Risk: 47.6%] [5. Quality: 0.89]   |
+----------------------------------------------------------------------------------------------------+
| MIDDLE GRID (Y: 240px - 625px | Height: 385px)                                                     |
| [Chart 1: 100% Stacked Bar]         | [Chart 2: Horizontal Bar]        | [Chart 3: Donut Chart]    |
| Churn by Value Segment (Excl. Unk) | Dept Escalations & Drivers       | Customer Sentiment Mix    |
| (Width: 590px)                      | (Width: 590px)                   | (Width: 640px)            |
+----------------------------------------------------------------------------------------------------+
| BOTTOM GRID (Y: 640px - 1055px | Height: 415px)                                                    |
| [Chart 4: Time-Series Line Chart]                    | [Visual 5: Executive Triage Table]          |
| Monthly Satisfaction vs. Dissatisfaction Trend       | High-Priority Escalations (Operational Log) |
| (Width: 890px)                                       | (Width: 940px)                              |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Component Coordinate Mapping & Configuration

### A. Top Header & Dropdown Slicers
- **Canvas Region:** `X: 30`, `Y: 20`, `Width: 1860`, `Height: 85`
- **Header Card Background:** Solid `#FFFFFF`, Border `#E2E8F0`, Corner Radius `8px`.
- **Title Block (`X: 55`, `Y: 35`, `Width: 600`, `Height: 55`):**
  - Primary Text: **Executive Customer Sentiment & Churn Risk** (Segoe UI Bold, 20pt, `#0F172A`).
  - Subtitle Text: `Orbitel Telecommunications • Real-Time AI Intelligence Engine` (Segoe UI Semibold, 10pt, `#64748B`).
- **Slicers (Horizontal Distribution in Top Right):**
  - All slicers configured as **Dropdown** mode (Style: Dropdown, single-select search enabled, select all enabled).
  - Background: `#F8FAFC`, Border: `#CBD5E1`, Text: 10pt Segoe UI `#1E293B`.
  1. **Customer Type Slicer (`X: 880`, `Y: 35`, `Width: 220`, `Height: 55`):**
     - Field: `'Sheet1'[Customer_type]`
     - Values: `All`, `corporate`, `enterprise`, `household`, `individual`, `sme`
  2. **Urgency Slicer (`X: 1120`, `Y: 35`, `Width: 200`, `Height: 55`):**
     - Field: `'Sheet1'[urgency]`
     - Values: `All`, `high`, `medium`, `low`
  3. **Service Type Slicer (`X: 1340`, `Y: 35`, `Width: 220`, `Height: 55`):**
     - Field: `'Sheet1'[service_type]`
     - Values: `All`, `broadband`, `fiber`, `postpaid`, `prepaid`
  4. **Time Stamp Slicer (`X: 1580`, `Y: 35`, `Width: 280`, `Height: 55`):**
     - Field: `'Sheet1'[timestamp]`
     - Control Type: Date Range Slider (`Between` date picker)

---

### B. Top KPI Ribbon (5 Uniform Cards)
- **Container Region:** `Y: 120`, `Height: 105`, `Spacing: 18px`
- **Card Geometry:** `Width: 357px`, `Height: 105px`, Background `#FFFFFF`, Border `#E2E8F0`, Radius `8px`.

| Card | Field / Measure | Callout Value | Format | Callout Color | Subtitle / Label | X-Coord |
|---|---|---|---|---|---|---|
| **1. Total Feedback** | `Total_Records = COUNTROWS('Sheet1')` | **21** | Integer | `#0F172A` | Total Ingested Telemetry | `30` |
| **2. Satisfaction Rate** | `Positive_Sentiment_Pct` | **33.3%** | 1 Decimal Pct | `#27ae60` (Green) | Positive Sentiment Ratio | `405` |
| **3. Dissatisfaction Rate** | `Negative_Sentiment_Pct` | **52.4%** | 1 Decimal Pct | `#0F172A` (Charcoal) | Friction & Complaint Ratio | `780` |
| **4. Churn Risk Rate** | `Churn_Rate_Pct` | **47.6%** | 1 Decimal Pct | `#c0392b` (Alert Red) | Critical Retention Threshold | `1155` |
| **5. Model Quality** | `Avg_Confidence_Score` | **0.89** | 2 Decimals | `#1E293B` (Slate) | GPT-4o-mini Confidence Mean | `1530` |

---

### C. Visual Charts (Middle Grid)

#### Visual 1: Churn Risk by Customer Value Segment (100% Stacked Bar Chart)
- **Coordinates:** `X: 30`, `Y: 240`, `Width: 590`, `Height: 385`
- **Chart Type:** 100% Stacked Bar Chart (Horizontal Orientation)
- **Field Mappings:**
  - **Y-Axis:** `'Sheet1'[customer_value_segment]` (Categories: `low`, `medium`, `high`, `premium`)
  - **X-Axis:** `Total_Records`
  - **Legend:** `'Sheet1'[Churn_Status]` (`High Risk` vs `Low Risk`)
- **Color Assignments:**
  - `High Risk`: Alert Red (`#c0392b`)
  - `Low Risk`: Slate Gray (`#64748B`)
- **Visual Filters (Filter on this Visual pane):**
  - Field: `'Sheet1'[customer_value_segment]`
  - Condition: **is not** `unknown` (Visual-level filter explicitly removes unsegmented or test telemetry).
- **Formatting:** Data labels enabled (Percentage display inside segments, white font 9pt), Y-axis title hidden.

#### Visual 2: Department Escalations & Churn Drivers (Horizontal Bar Chart)
- **Coordinates:** `X: 638`, `Y: 240`, `Width: 590`, `Height: 385`
- **Chart Type:** Clustered Horizontal Bar Chart
- **Field Mappings:**
  - **Y-Axis:** `'Sheet1'[target_department]` (Operations, Finance, Marketing, Sales, HR)
  - **X-Axis:** `High_Risk_Escalations_Count = CALCULATE(COUNTROWS('Sheet1'), 'Sheet1'[churn_risk] = TRUE())`
- **Data Insights:**
  - **Operations:** 5 escalations (Leading driver: Cell tower blackouts, fiber cutoffs, throughput degradation)
  - **Finance:** 3 escalations (Secondary driver: Roaming dispute billing, unauthorized VAS recurring charges)
  - **Marketing:** 2 escalations (Competitive retention: Jazz / Zong tariff matching)
- **Color Assignment:** Corporate Gradient / Accent Color (`#2980b9` or `#c0392b` alert gradient).
- **Formatting:** Data labels enabled (Values displayed outside bar end, 10pt Segoe UI Bold).

#### Visual 3: Overall Customer Sentiment Mix (Donut Chart)
- **Coordinates:** `X: 1246`, `Y: 240`, `Width: 644`, `Height: 385`
- **Chart Type:** Donut Chart
- **Field Mappings:**
  - **Legend:** `'Sheet1'[sentiment]`
  - **Values:** `Total_Records`
- **Color Mapping & Proportions:**
  - `negative`: **52.38%** (11 Records) -> `#c0392b` (Alert Red)
  - `positive`: **33.33%** (7 Records) -> `#27ae60` (Positive Green)
  - `neutral`: **14.29%** (3 Records) -> `#94A3B8` (Slate Muted)
- **Formatting:** Center label shows "21 Feedback", Detail Labels set to "Category, percent of total".

---

### D. Visual Charts & Operational Triage (Bottom Grid)

#### Visual 4: Monthly Satisfaction vs. Dissatisfaction Trend (Time-Series Line Chart)
- **Coordinates:** `X: 30`, `Y: 640`, `Width: 890`, `Height: 415`
- **Chart Type:** Line Chart with Continuous / Categorical Timeline
- **Field Mappings:**
  - **X-Axis:** `'Sheet1'[Month_Year]` (Aug 2026, Sep 2026, Oct 2026) sorted chronologically by `'Sheet1'[YearMonth_Sort]`.
  - **Y-Axis:**
    1. `Positive_Sentiment_Pct` (Line Color: Positive Green `#27ae60`, Stroke Width: 3px)
    2. `Negative_Sentiment_Pct` (Line Color: Alert Red `#c0392b`, Stroke Width: 3px)
- **Point Markers:**
  - Markers explicitly enabled on all data points.
  - Shape: Circle, Size: 6, Fill: Solid matching line color, Border: `#FFFFFF` 1.5px.
- **Labels & Axes:**
  - Data labels enabled on all vertices.
  - Y-Axis formatted strictly on percentage scale (0% to 100%).
  - Trajectory reflects actionable business recovery: Dissatisfaction drops from 57.1% (Aug/Sep) to 42.9% (Oct), while satisfaction surges from 28.6% to 42.9% as automated escalations remediate core operational bottlenecks.

#### Visual 5: High-Priority Customer Escalations (Executive Triage Table)
- **Coordinates:** `X: 938`, `Y: 640`, `Width: 952`, `Height: 415`
- **Chart Type:** Table Visual (`tableEx`)
- **Visual Filters (Filter on this Visual pane):**
  - Condition: `'Sheet1'[churn_risk] = TRUE` **OR** `'Sheet1'[urgency] = "high"`
  - Shows the 11 critical escalation cases requiring C-Level / VP oversight.
- **Columns & Auto-Fitted Width Allocations:**
  1. `customer_id` (Width: ~110px) - e.g., `ORB-10821`
  2. `location_mentioned` (Width: ~150px) - e.g., `DHA Phase 6, Lahore`
  3. `issue_categories` (Width: ~140px) - e.g., `network, coverage`
  4. `urgency` (Width: ~90px) - `high` (Conditional formatting: bold red text `#c0392b`)
  5. `root_cause_summary` (Width: ~420px) - Formatted with auto-wrap, no horizontal scroll.
- **Styling & Theme Enforcement:**
  - **Header Row:** Background `#1E293B`, Bold White Text (`#FFFFFF`), Height: 32px.
  - **Data Rows:** Alternating row zebra-striping:
    - Primary Row: `#FFFFFF`
    - Secondary Row: `#F8FAFC`
  - **Gridlines:** Horizontal gridlines only (`#E2E8F0`, 1px), **Zero vertical gridlines**.
  - **Row Height:** 28px with generous cell padding (6px top/bottom).
  - **Auto-Fit:** Column widths configured to consume full 952px without triggering horizontal scrollbars.

---

## 3. Executive Review Sign-Off Criteria
- [x] Canvas ratio exactly 16:9 (1920 × 1080).
- [x] All 5 top-ribbon KPIs match exact arithmetic (`21`, `33.3%`, `52.4%`, `47.6%`, `0.89`).
- [x] Slicers formatted as compact dropdowns in the top header.
- [x] `customer_value_segment` excludes `unknown` via visual-level filter.
- [x] Department horizontal bar chart led by Operations (5), Finance (3), Marketing (2).
- [x] Sentiment mix donut chart proportions match exact decimal targets (52.38%, 33.33%, 14.29%).
- [x] Monthly time-series chart displays markers on all 3 points (Aug 2026, Sep 2026, Oct 2026).
- [x] Operational triage table displays full issue context without truncation or horizontal clipping.

