# Warehouse Portfolio Pricing & Yield Analysis

A pricing-analytics case study on a **5-property, ~102,000 sq ft warehouse portfolio**
in Lucknow (4 multi-floor units in Transport Nagar, 1 single-floor unit in Banthra).
The analysis quantifies the portfolio's pricing power, decomposes its ~50% revenue
growth, and surfaces concrete optimisation levers — using SQL for the metric layer
and pandas/matplotlib for analysis and visuals.

> **Role context:** built from a portfolio I priced and managed as Pricing & Yield
> Analyst. It reproduces the actual decision logic I used — competitor benchmarking,
> floor-level rate setting, tenant-mix and vacancy analysis.

## The thesis: compliance-driven pricing power

Competitors quote **₹2–5/sq ft cheaper**, but that discount is illusory and risky:
they under-invoice (part rent taken in cash to dodge tax), lack **LDA-sanctioned
parking**, and some carry **illegal encroachment**. As a result they sit vacant more
often and major brands avoid them. This portfolio is fully legal — clean title,
sanctioned parking, fully invoiced — and legal stock is **scarce**, so it commands a
premium *and* stays effectively fully occupied through a strong enquiry pipeline.

The job of the analysis is to **put a number on that moat** and find where the
portfolio still leaves money on the table.

## Key findings

| Metric | Result |
| Monthly rent roll | ₹16.20 L (₹194 L/yr) |
| Revenue growth 2023→2026 | **+50% gross potential rent** (repricing + tenant-mix upgrade) |
| Premium captured vs non-compliant stock | **~₹46 L/yr** |
| Largest single-asset exposure | Banthra logistics, **33%** of revenue |
| Rent lost to turnover (36 mo) | ₹20.4 L, all from 11-month TP Nagar leases |

**Soft spot:** first floors carry the lowest rate (₹10), the weakest demand, and the
most vacancy — a monetisation gap, not a market-wide one.

## Recommendations

1. **Hold the premium** — price to compliance, not to the cheapest quote; the legal
   moat is worth ~₹46 L/yr.
2. **Lengthen TP Nagar leases** — scarcity + full pipeline give the leverage to move
   off 11-month terms and recover most of the ₹20.4 L turnover loss.
3. **Fix first-floor monetisation** — lift/access upgrades or ground-floor bundling.
4. **De-risk Banthra concentration** — diversify or lock the 5-year renewal early.

## Repo structure

```
warehouse-pricing-analysis/
├── data/warehouse_units.csv   # unit-level dataset (one row per leasable floor)
├── analysis.sql               # SQLite metric layer (snapshot, premium, mix, vacancy)
├── pricing_analysis.py        # pandas analysis + charts + printed findings
├── charts/                    # generated PNGs
└── README.md
```

## Run it

```bash
pip install pandas numpy matplotlib
python pricing_analysis.py          # findings + charts/

# SQL layer (optional)
sqlite3 portfolio.db
.mode csv
.import --skip 1 data/warehouse_units.csv warehouse_units
.read analysis.sql
```

## Data provenance

**Real:** unit count, locations, floor areas, current floor rates, **2023 baseline
rates**, lease terms and escalations, tenant business types, full occupancy, and the
compliance positioning. **Representative estimates** (within the ranges I described,
editable in the CSV): exact competitor rates, vacancy months, and enquiry counts.

> **Gross vs realized:** the +50% figure is growth in *gross potential rent* (posted
> rates × area). Realized/collected income growth is lower once vacancy, free-rent
> periods and discounts are netted out — which is why headline collected-income
> growth may be quoted more conservatively.
