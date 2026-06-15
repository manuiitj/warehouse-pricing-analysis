Warehouse Portfolio Pricing & Yield Analysis  —  SQL layer
SQLite-compatible.
Load:  sqlite3 portfolio.db
.mode csv
.import --skip 1 data/warehouse_units.csv warehouse_units

1. PORTFOLIO SNAPSHOT 
SELECT
    COUNT(*)                              AS leasable_units,
    SUM(area_sqft)                        AS total_sqft,
    SUM(area_sqft * rate_psf_current)     AS monthly_rent_inr,
    SUM(area_sqft * rate_psf_current)*12  AS annual_rent_inr,
    ROUND(SUM(area_sqft*rate_psf_current)*1.0/SUM(area_sqft),2) AS blended_rate_psf
FROM warehouse_units;

2. INCOME GROWTH 2023 -> NOW (the ~50% story) 
SELECT
    SUM(area_sqft*rate_psf_2023)          AS monthly_rent_2023,
    SUM(area_sqft*rate_psf_current)       AS monthly_rent_current,
    ROUND((SUM(area_sqft*rate_psf_current)-SUM(area_sqft*rate_psf_2023))
          *100.0/SUM(area_sqft*rate_psf_2023),1) AS growth_pct
FROM warehouse_units;

3. COMPLIANCE PRICING POWER (premium over competitors)
Every unit is LDA-compliant; competitors discount on paper
but carry cash deals / no parking / encroachment.
SELECT
    floor,
    ROUND(AVG(rate_psf_current),1)        AS our_rate_psf,
    ROUND(AVG(competitor_rate_psf),1)     AS competitor_rate_psf,
    ROUND(AVG(rate_psf_current-competitor_rate_psf),1) AS premium_psf,
    SUM((rate_psf_current-competitor_rate_psf)*area_sqft)*12 AS annual_premium_inr
FROM warehouse_units
GROUP BY floor
ORDER BY premium_psf DESC;

3b. TOTAL ANNUAL PREMIUM CAPTURED
SELECT SUM((rate_psf_current-competitor_rate_psf)*area_sqft)*12 AS annual_premium_inr
FROM warehouse_units;

4. YIELD & SOFT-SPOT BY FLOOR 
First floors: lowest rate, lowest demand, highest vacancy.
SELECT
    floor,
    ROUND(AVG(rate_psf_current),1)        AS avg_rate_psf,
    ROUND(AVG(enquiries_6mo),1)           AS avg_demand_6mo,
    SUM(months_vacant_36mo)               AS vacant_months_36
FROM warehouse_units
GROUP BY floor
ORDER BY avg_rate_psf DESC;

5. TENANT-MIX / CONCENTRATION
SELECT
    business_type,
    COUNT(*)                              AS units,
    SUM(area_sqft*rate_psf_current)       AS monthly_rent_inr,
    ROUND(SUM(area_sqft*rate_psf_current)*100.0/
        (SELECT SUM(area_sqft*rate_psf_current) FROM warehouse_units),1) AS revenue_share_pct
FROM warehouse_units
GROUP BY business_type
ORDER BY monthly_rent_inr DESC;

6. COST OF VACANCY (trailing 36 months)
Churn from 11-month TP Nagar leases, not weak demand.
SELECT
    locality,
    SUM(months_vacant_36mo)               AS vacant_months,
    SUM(months_vacant_36mo*area_sqft*rate_psf_current) AS rent_lost_inr
FROM warehouse_units
GROUP BY locality
ORDER BY rent_lost_inr DESC;
