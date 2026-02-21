# 📊 SaaS Funnel & A/B Test Analysis

A Python-based analytics project that simulates and analyzes a SaaS user conversion funnel — from pricing page visits to trial starts to subscriptions — with A/B testing, segment analysis, and cohort-style breakdowns.

---

## 🚀 Features

- **Funnel Analysis** — Track user drop-off across each stage of the conversion funnel
- **A/B Testing** — Compare subscription conversion rates between variants using Chi-Square statistical testing
- **Segment Analysis** — Break down conversion rates by country, device, and variant
- **Cohort Analysis** — Cross-tabulate variant performance across country and device dimensions
- **Visualizations** — Bar charts, funnel charts, and heatmaps for all analyses

---

## 🛠️ Tech Stack

- Python 3.x
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy

---

## 📁 Project Structure

```
├── funnel_ab_analysis.py   # Main analysis script
└── README.md
```

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/saas-funnel-ab-analysis.git
cd saas-funnel-ab-analysis

# Install dependencies
pip install pandas numpy matplotlib seaborn scipy
```

---

## ▶️ Usage

```bash
python funnel_ab_analysis.py
```

---

## 📈 Analysis Breakdown

### Funnel Analysis
Tracks how users move through three stages:
- Visited Pricing Page
- Started Trial
- Subscribed

Calculates step-by-step conversion rates and drop-off percentages.

### A/B Testing
- Splits users into Variant A and Variant B
- Computes subscription conversion rate for each group
- Runs a **Chi-Square test** to determine statistical significance (p < 0.05)

### Segment Analysis
Conversion rates broken down independently by:
- **Country** — US, UK, IN
- **Device** — Mobile, Desktop
- **Variant** — A, B

### Cohort Analysis
Cross-dimensional conversion analysis:
- Variant × Country
- Variant × Device
- Variant × Country × Device (full granularity)

Visualized as **heatmaps** for easy pattern identification.

---

## 📊 Sample Output

```
--- A/B Test Results ---
   Total Users  Subscribed  Conversion Rate %
A         2512         175               6.97
B         2488         173               6.95

Chi-Square Statistic: 0.0023
P-Value: 0.9618
Result: Not Statistically Significant ❌
```

> **Note:** Since data is randomly generated with equal probabilities for both variants, results will show no significant difference — as expected. Replace with real data to uncover meaningful insights.

---

## 🌱 Future Improvements

- Add time-based cohort analysis (weekly/monthly retention)
- Integrate real data sources via CSV upload
- Build an interactive dashboard with Plotly or Streamlit
- Add confidence intervals and effect size reporting

---

## 📄 License

MIT License
