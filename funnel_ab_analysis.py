import pandas as pd
import numpy as np

np.random.seed(42)

n = 5000

df = pd.DataFrame({
    "user_id": range(n),
    "visited_pricing": np.random.binomial(1, 0.7, n),
})

df["started_trial"] = df["visited_pricing"] * np.random.binomial(1, 0.5, n)
df["subscribed"] = df["started_trial"] * np.random.binomial(1, 0.4, n)

df["variant"] = np.random.choice(["A", "B"], n)
df["country"] = np.random.choice(["US", "UK", "IN"], n)
df["device"] = np.random.choice(["Mobile", "Desktop"], n)

df.head()


funnel = {
    "Visited Pricing": df["visited_pricing"].sum(),
    "Started Trial": df["started_trial"].sum(),
    "Subscribed": df["subscribed"].sum()
}

funnel_df = pd.DataFrame.from_dict(funnel, orient="index", columns=["Users"])
funnel_df

counts = funnel_df["Users"]

funnel_analysis = pd.DataFrame({
    "Users": counts,
    "Step Conversion": (counts / counts.shift(1) * 100).round(2),
})

funnel_analysis["Drop-off %"] = (100- funnel_analysis["Step Conversion"]).round(2)

funnel_analysis

import matplotlib.pyplot as plt

funnel_df.plot(kind="bar", legend=False)
plt.title("User Funnel")
plt.ylabel("Number of Users")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




plt.figure(figsize=(8, 5))
plt.bar(funnel_analysis.index, funnel_analysis["Users"], color=["#4C72B0", "#55A868", "#C44E52"])

# Add value labels on bars
for i, (val, idx) in enumerate(zip(funnel_analysis["Users"], funnel_analysis.index)):
    plt.text(i, val + 30, f'{int(val)}', ha='center', fontsize=11)

plt.title("Funnel Analysis", fontsize=14)
plt.xlabel("Funnel Step")
plt.ylabel("Number of Users")
plt.tight_layout()
plt.show()




fig, ax1 = plt.subplots(figsize=(8, 5))

bars = ax1.bar(funnel_analysis.index, funnel_analysis["Users"], color=["#4C72B0", "#55A868", "#C44E52"])
ax1.set_ylabel("Number of Users")
ax1.set_title("Funnel Analysis")

# Add user count labels
for i, val in enumerate(funnel_analysis["Users"]):
    ax1.text(i, val + 30, f'{int(val)}', ha='center', fontsize=11)

# Add conversion % labels
for i, val in enumerate(funnel_analysis["Step Conversion"]):
    if not np.isnan(val):
        ax1.text(i, funnel_analysis["Users"].iloc[i] / 2, f'Conv: {val}%', 
                 ha='center', color='white', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()


from scipy import stats

# Split into A and B groups
group_a = df[df["variant"] == "A"]
group_b = df[df["variant"] == "B"]

# Calculate conversion rates for each group
ab_summary = pd.DataFrame({
    "Total Users": [len(group_a), len(group_b)],
    "Subscribed": [group_a["subscribed"].sum(), group_b["subscribed"].sum()],
}, index=["A", "B"])

ab_summary["Conversion Rate %"] = (ab_summary["Subscribed"] / ab_summary["Total Users"] * 100).round(2)

print(ab_summary)

# Contingency table
subscribed_a = group_a["subscribed"].sum()
not_subscribed_a = len(group_a) - subscribed_a

subscribed_b = group_b["subscribed"].sum()
not_subscribed_b = len(group_b) - subscribed_b

contingency_table = [[subscribed_a, not_subscribed_a],
                     [subscribed_b, not_subscribed_b]]

chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

print(f"\nChi-Square Statistic: {chi2:.4f}")
print(f"P-Value: {p_value:.4f}")
print(f"Degrees of Freedom: {dof}")

if p_value < 0.05:
    print("\nResult: Statistically Significant ✅ (reject null hypothesis)")
else:
    print("\nResult: Not Statistically Significant ❌ (fail to reject null hypothesis)")


ab_summary["Conversion Rate %"].plot(kind="bar", color=["#4C72B0", "#C44E52"], figsize=(6, 4))
plt.title("A/B Test - Subscription Conversion Rate")
plt.ylabel("Conversion Rate %")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Segment Analysis
segments = ["country", "device", "variant"]

for seg in segments:
    print(f"\n--- Conversion by {seg.upper()} ---")
    segment_df = df.groupby(seg).agg(
        Total_Users=("user_id", "count"),
        Subscribed=("subscribed", "sum")
    )
    segment_df["Conversion Rate %"] = (segment_df["Subscribed"] / segment_df["Total_Users"] * 100).round(2)
    print(segment_df)


fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, seg in zip(axes, segments):
    segment_df = df.groupby(seg)["subscribed"].mean() * 100
    segment_df.plot(kind="bar", ax=ax, color=["#4C72B0", "#55A868", "#C44E52"])
    ax.set_title(f"Conversion Rate by {seg.capitalize()}")
    ax.set_ylabel("Conversion Rate %")
    ax.set_xlabel(seg.capitalize())
    ax.tick_params(axis='x', rotation=0)

plt.suptitle("Segment Analysis", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()

# Cohort: Variant x Country
cohort_country = df.groupby(["variant", "country"]).agg(
    Total_Users=("user_id", "count"),
    Subscribed=("subscribed", "sum")
)
cohort_country["Conversion Rate %"] = (cohort_country["Subscribed"] / cohort_country["Total_Users"] * 100).round(2)
print("\n--- Cohort: Variant x Country ---")
print(cohort_country)

# Cohort: Variant x Device
cohort_device = df.groupby(["variant", "device"]).agg(
    Total_Users=("user_id", "count"),
    Subscribed=("subscribed", "sum")
)
cohort_device["Conversion Rate %"] = (cohort_device["Subscribed"] / cohort_device["Total_Users"] * 100).round(2)
print("\n--- Cohort: Variant x Device ---")
print(cohort_device)

# Cohort: Variant x Country x Device
cohort_full = df.groupby(["variant", "country", "device"]).agg(
    Total_Users=("user_id", "count"),
    Subscribed=("subscribed", "sum")
)
cohort_full["Conversion Rate %"] = (cohort_full["Subscribed"] / cohort_full["Total_Users"] * 100).round(2)
print("\n--- Cohort: Variant x Country x Device ---")
print(cohort_full)

import seaborn as sns

# Heatmap: Variant x Country
pivot_country = cohort_country["Conversion Rate %"].unstack(level=0)

plt.figure(figsize=(8, 4))
sns.heatmap(pivot_country, annot=True, fmt=".1f", cmap="Blues", linewidths=0.5)
plt.title("Conversion Rate % — Variant x Country")
plt.tight_layout()
plt.show()

# Heatmap: Variant x Device
pivot_device = cohort_device["Conversion Rate %"].unstack(level=0)

plt.figure(figsize=(6, 3))
sns.heatmap(pivot_device, annot=True, fmt=".1f", cmap="Greens", linewidths=0.5)
plt.title("Conversion Rate % — Variant x Device")
plt.tight_layout()
plt.show()

# Heatmap: Country x Device (for each variant separately)
for variant in ["A", "B"]:
    pivot = df[df["variant"] == variant].groupby(["country", "device"])["subscribed"].mean() * 100
    pivot = pivot.unstack()
    plt.figure(figsize=(6, 4))
    sns.heatmap(pivot.round(2), annot=True, fmt=".1f", cmap="Oranges", linewidths=0.5)
    plt.title(f"Conversion Rate % — Variant {variant} (Country x Device)")
    plt.tight_layout()
    plt.show()
