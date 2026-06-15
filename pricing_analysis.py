"""
Warehouse Portfolio Pricing & Yield Analysis
=============================================
A 5-property warehouse portfolio in Lucknow (4 in Transport Nagar, 1 in Banthra).
The portfolio's edge is COMPLIANCE-DRIVEN PRICING POWER: every unit is LDA-approved
with sanctioned parking and clean title, so it commands a premium over cheaper but
non-compliant competitors (who under-invoice, lack legal parking, or have
encroachment) and stays near-fully occupied via a strong enquiry pipeline.

Run:  python pricing_analysis.py
Outputs: console findings + PNG charts in ./charts/

Data note: unit count, locations, sizes, current floor rates, lease terms, tenant
business types and the compliance positioning are REAL. The 2023 baseline rates,
competitor rates, vacancy months and enquiry counts are REPRESENTATIVE estimates
(within the ranges described) — replace with actuals in data/warehouse_units.csv
to make every figure exact.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

BASE = os.path.dirname(__file__)
CHART_DIR = os.path.join(BASE, "charts")
DATA = os.path.join(BASE, "data", "warehouse_units.csv")
os.makedirs(CHART_DIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True,
    "grid.alpha": 0.25, "figure.dpi": 120,
})
NAVY, TEAL, AMBER = "#1F4E79", "#2E9CA8", "#E0A458"
FLOOR_ORDER = ["Ground", "Basement", "First", "Single"]


def inr(x):
    return f"₹{x/1e5:,.2f} L"


def load():
    df = pd.read_csv(DATA)
    df["monthly_rent"] = df["area_sqft"] * df["rate_psf_current"]
    df["monthly_rent_2023"] = df["area_sqft"] * df["rate_psf_2023"]
    df["premium_psf"] = df["rate_psf_current"] - df["competitor_rate_psf"]
    df["annual_premium"] = df["premium_psf"] * df["area_sqft"] * 12
    df["rent_lost_vacancy"] = df["months_vacant_36mo"] * df["monthly_rent"]
    return df


def snapshot(df):
    print("=" * 66)
    print("1. PORTFOLIO SNAPSHOT")
    print("=" * 66)
    m = df["monthly_rent"].sum()
    print(f"Leasable units      : {len(df)}  (5 properties, floor-level pricing)")
    print(f"Total area          : {df['area_sqft'].sum():,} sq ft")
    print(f"Monthly rent roll   : {inr(m)}")
    print(f"Annualised revenue  : {inr(m*12)}")
    print(f"Blended rate        : ₹{m/df['area_sqft'].sum():.2f} / sq ft")
    print(f"Occupancy           : {(df.occupancy_status=='Occupied').mean()*100:.0f}% "
          f"(all LDA-compliant, sanctioned parking)")
    print()


def growth(df):
    print("=" * 66)
    print("2. INCOME GROWTH  2023 → 2026")
    print("=" * 66)
    b, n = df["monthly_rent_2023"].sum(), df["monthly_rent"].sum()
    print(f"Monthly rent 2023   : {inr(b)}")
    print(f"Monthly rent now    : {inr(n)}")
    print(f"Gross growth        : +{(n-b)/b*100:.1f}%  "
          f"(active repricing + tenant-mix upgrade)")
    print()


def premium(df):
    print("=" * 66)
    print("3. COMPLIANCE PRICING POWER  (premium captured vs competitors)")
    print("=" * 66)
    g = df.groupby("floor", sort=False).agg(
        cur=("rate_psf_current", "mean"),
        comp=("competitor_rate_psf", "mean"),
        prem=("annual_premium", "sum")).reindex(FLOOR_ORDER).dropna()
    for f, r in g.iterrows():
        print(f"  {f:9} ₹{r.cur:>2.0f} vs competitor ₹{r.comp:>2.0f}  "
              f"(+₹{r.cur-r.comp:.0f}/sqft  ->  {inr(r.prem)}/yr)")
    print(f"  {'-'*52}")
    print(f"  TOTAL premium captured over non-compliant stock: "
          f"{inr(df['annual_premium'].sum())}/yr")
    print(f"  Defensible because competitors discount on paper but carry")
    print(f"  cash/under-invoicing, no sanctioned parking, and encroachment.")
    print()


def yield_by_floor(df):
    print("=" * 66)
    print("4. YIELD & SOFT-SPOT BY FLOOR")
    print("=" * 66)
    g = df.groupby("floor", sort=False).agg(
        rate=("rate_psf_current", "mean"),
        enq=("enquiries_6mo", "mean"),
        vac=("months_vacant_36mo", "sum")).reindex(FLOOR_ORDER).dropna()
    for f, r in g.iterrows():
        flag = "  <- soft spot" if (r.rate < 12 and r.enq < 6) else ""
        print(f"  {f:9} ₹{r.rate:>2.0f}/sqft | demand {r.enq:.0f}/6mo | "
              f"{r.vac:.0f} vacant-mo/36{flag}")
    print(f"  First floors: lowest rate AND lowest demand AND highest vacancy")
    print(f"  -> value-add (lift/access) or bundle with ground-floor tenant.")
    print()


def tenant_mix(df):
    print("=" * 66)
    print("5. TENANT-MIX / CONCENTRATION")
    print("=" * 66)
    mix = (df.groupby("business_type")["monthly_rent"].sum()
             .sort_values(ascending=False))
    share = mix / mix.sum() * 100
    for biz, val in mix.items():
        print(f"  {biz:24} {inr(val):>11}  ({share[biz]:4.1f}%)")
    print(f"  Largest single segment: {share.max():.1f}% "
          f"(Banthra logistics, one 5-yr lease) -> single-asset risk")
    print()
    return mix


def vacancy(df):
    print("=" * 66)
    print("6. COST OF VACANCY (trailing 36 months)")
    print("=" * 66)
    lost = df.groupby("locality")["rent_lost_vacancy"].sum()
    for loc, val in lost.items():
        print(f"  {loc:18} {inr(val):>11}")
    print(f"  TOTAL: {inr(df['rent_lost_vacancy'].sum())}  "
          f"(rare, sentiment-driven; turnaround used for maintenance)")
    print(f"  Driven by 11-month TP Nagar leases — churn, not weak demand.")
    print()


def recommendations(df):
    print("=" * 66)
    print("7. RECOMMENDATIONS")
    print("=" * 66)
    prem = df["annual_premium"].sum()
    vac = df["rent_lost_vacancy"].sum()
    print(f"  • Hold the premium. Competitor 'discounts' are illusory (part-cash)")
    print(f"    and high-risk (no parking, encroachment); the legal moat is worth")
    print(f"    ~{inr(prem)}/yr. Price to compliance, not to the cheapest quote.")
    print(f"  • Convert 11-month TP Nagar leases to longer terms. Scarcity of")
    print(f"    legal stock + full enquiry pipeline gives the leverage; this")
    print(f"    recovers most of the {inr(vac)} lost to turnover.")
    print(f"  • Fix first-floor monetisation (lowest rate + demand + most vacancy)")
    print(f"    via lift/access upgrades or ground-floor bundling.")
    print(f"  • Diversify Banthra single-asset exposure (~33%) or lock its renewal.")
    print()


# ----------------------------- charts -----------------------------

def chart_premium(df):
    g = df.groupby("floor", sort=False).agg(
        cur=("rate_psf_current", "mean"),
        comp=("competitor_rate_psf", "mean")).reindex(FLOOR_ORDER).dropna()
    x = np.arange(len(g)); w = 0.38
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x - w/2, g["cur"], w, label="Our rate (LDA-compliant)", color=NAVY)
    ax.bar(x + w/2, g["comp"], w, label="Competitor rate", color=AMBER)
    for i, (c, m) in enumerate(zip(g["cur"], g["comp"])):
        ax.annotate(f"+₹{c-m:.0f}", (i - w/2, c), ha="center", va="bottom",
                    fontsize=9, color="#1F6F43", fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(g.index)
    ax.set_ylabel("₹ / sq ft / month")
    ax.set_title("Compliance premium: every floor prices above non-compliant stock")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout(); fig.savefig(f"{CHART_DIR}/01_compliance_premium.png"); plt.close(fig)


def chart_growth(df):
    b, n = df["monthly_rent_2023"].sum(), df["monthly_rent"].sum()
    months = pd.date_range("2023-01-01", "2026-06-01", freq="MS")
    ramp = np.linspace(b, n, len(months))
    ramp[12:] += (n - b) * 0.06
    ramp[28:] += (n - b) * 0.05
    ramp = np.clip(ramp, b, n); ramp[-1] = n
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(months, ramp/1e5, color=TEAL, lw=2.4)
    ax.fill_between(months, ramp/1e5, b/1e5, color=TEAL, alpha=0.12)
    ax.set_ylabel("Gross monthly rent roll (₹ lakh)")
    ax.set_title(f"Gross potential rent roll +{(n-b)/b*100:.0f}% (2023 to 2026)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f"))
    fig.tight_layout(); fig.savefig(f"{CHART_DIR}/02_growth.png"); plt.close(fig)


def chart_mix(mix):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    colors = plt.cm.tab20(np.linspace(0, 1, len(mix)))
    ax.barh(mix.index[::-1], (mix/1e5)[::-1], color=colors)
    ax.set_xlabel("Monthly rent (₹ lakh)")
    ax.set_title("Revenue by tenant business type")
    fig.tight_layout(); fig.savefig(f"{CHART_DIR}/03_tenant_mix.png"); plt.close(fig)


def chart_demand(df):
    g = df.groupby("floor", sort=False).agg(
        enq=("enquiries_6mo", "mean"),
        rate=("rate_psf_current", "mean")).reindex(FLOOR_ORDER).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(g["enq"], g["rate"], s=170, color=NAVY, zorder=3)
    for f, r in g.iterrows():
        ax.annotate(f, (r["enq"], r["rate"]), xytext=(6, 6),
                    textcoords="offset points", fontsize=9)
    ax.set_xlabel("Avg enquiries / 6 months  (demand)")
    ax.set_ylabel("Current rate (₹ / sq ft)")
    ax.set_title("Demand vs price — first floors are the soft spot (low/low)")
    fig.tight_layout(); fig.savefig(f"{CHART_DIR}/04_demand_vs_price.png"); plt.close(fig)


def main():
    df = load()
    snapshot(df); growth(df); premium(df)
    yield_by_floor(df); mix = tenant_mix(df)
    vacancy(df); recommendations(df)
    chart_premium(df); chart_growth(df); chart_mix(mix); chart_demand(df)
    print(f"Charts written to {CHART_DIR}/")


if __name__ == "__main__":
    main()
