import streamlit as st
import numpy_financial as npf


st.title("Home Buying vs. Renting Calculator")

# --- Buying Inputs ---
st.header("Buying Info")
home_price = st.number_input("Home price ($)", value=500000)
down_payment_pct = st.slider("Down payment (%)", 0, 100, 20)
interest_rate = st.slider("Loan interest rate (%)", 0.0, 10.0, 4.0)
loan_term = st.slider("Loan term (years)", 1, 40, 30)
property_tax_rate = st.slider("Property tax rate (%)", 0.0, 5.0, 1.2)
maintenance_pct = st.slider("Maintenance (% of home price/year)", 0.0, 10.0, 1.0)
closing_costs = st.number_input("One-time closing costs ($)", value=10000)
home_insurance = st.number_input("Annual home insurance ($)", value=1200)
appreciation_rate = st.slider("Home appreciation rate (%)", 0.0, 10.0, 0.0)

# --- Renting Inputs ---
st.header("Renting Info")
monthly_rent = st.number_input("Monthly rent ($)", value=2000)
rent_increase_rate = st.slider("Rent inflation per year (%)", 0.0, 10.0, 3.0)

# --- Other Inputs ---
st.header("Other Inputs")
years = st.slider("How many years will you stay?", 1, 40, 10)

if st.button("Compare"):

    # --- Calculations ---
    # Loan & mortgage setup
    loan_amount = home_price * (1 - down_payment_pct / 100)
    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12

    # Monthly payment (PMT formula)
    monthly_payment = npf.pmt(monthly_interest_rate, num_payments, -loan_amount)


    # Total payments over years
    total_mortgage_paid = monthly_payment * 12 * years

    # Approximate principal paid (simplified)
    equity = loan_amount * (years / loan_term)

    # Appreciation
    appreciated_value = home_price * ((1 + appreciation_rate / 100) ** years)

    # Annual costs
    property_tax_total = property_tax_rate / 100 * home_price * years
    maintenance_total = maintenance_pct / 100 * home_price * years
    insurance_total = home_insurance * years

    total_buying_cost = (
        total_mortgage_paid
        + closing_costs
        + property_tax_total
        + maintenance_total
        + insurance_total
    )

    net_cost_buying = total_buying_cost - equity

    # Rent cost with inflation
    total_renting = 0
    current_rent = monthly_rent
    for _ in range(years):
        total_renting += current_rent * 12
        current_rent *= (1 + rent_increase_rate / 100)

    # --- Results ---
    st.subheader("Results")
    st.write(f"**Net Cost of Buying:** ${net_cost_buying:,.2f}")
    st.write(f"**Total Cost of Renting:** ${total_renting:,.2f}")

    if net_cost_buying < total_renting:
        st.success("✅ Buying is financially better over this period.")
    else:
        st.warning("📉 Renting is cheaper over this time frame.")

    st.caption(f"Note: Appreciation considered, but not subtracted from cost (not a cash benefit unless sold).")
