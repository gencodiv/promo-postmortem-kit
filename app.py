from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Promo Postmortem Kit", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "promo_results.csv"


def load_results() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def pct_change(current: float, baseline: float) -> float:
    if baseline == 0:
        return 0.0
    return (current / baseline - 1) * 100


results = load_results()

campaign = st.sidebar.selectbox("Campaign", sorted(results["campaign"].unique()))
sku = st.sidebar.selectbox(
    "SKU",
    sorted(results.loc[results["campaign"] == campaign, "sku"].unique()),
)

view = results[(results["campaign"] == campaign) & (results["sku"] == sku)].copy()
period_order = ["pre", "promo", "post"]
view["period"] = pd.Categorical(view["period"], categories=period_order, ordered=True)
view = view.sort_values("period")
view["margin_rate"] = view["margin_value"] / view["revenue"]

pre = view.loc[view["period"] == "pre"].iloc[0]
promo = view.loc[view["period"] == "promo"].iloc[0]
post = view.loc[view["period"] == "post"].iloc[0]

sales_lift = pct_change(promo["revenue"], pre["revenue"])
volume_lift = pct_change(promo["units"], pre["units"])
margin_rate_delta = (promo["margin_rate"] - pre["margin_rate"]) * 100
post_fade = pct_change(post["revenue"], pre["revenue"])

st.title("Promo Postmortem Kit")
st.caption("A lightweight toolkit for reviewing what a promotion actually changed in sales, margin, and stock pressure.")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Promo sales lift vs pre", f"{sales_lift:.1f}%")
m2.metric("Promo volume lift vs pre", f"{volume_lift:.1f}%")
m3.metric("Margin rate delta", f"{margin_rate_delta:.1f} pts")
m4.metric("Post-promo revenue vs pre", f"{post_fade:.1f}%")

left, right = st.columns([1.15, 0.85])
with left:
    st.subheader("Period view")
    st.dataframe(
        view[["period", "units", "revenue", "margin_value", "margin_rate", "stockouts", "ending_stock"]].style.format(
            {"revenue": "$ {:,.0f}", "margin_value": "$ {:,.0f}", "margin_rate": "{:.1%}"}
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.bar_chart(view.set_index("period")[["revenue", "margin_value"]], use_container_width=True)

with right:
    st.subheader("Commercial interpretation")
    commentary = []
    if sales_lift > 20:
        commentary.append("The mechanic clearly moved demand during the promo window.")
    else:
        commentary.append("Demand moved, but not strongly enough to call the campaign a clean win.")

    if margin_rate_delta < -4:
        commentary.append("Margin deterioration is meaningful. The campaign likely bought volume too expensively.")
    else:
        commentary.append("Margin rate held within a manageable range for a short tactical push.")

    if promo["stockouts"] > pre["stockouts"]:
        commentary.append("Stock pressure increased during the campaign. Future runs should review inventory cover before repeating the mechanic.")

    if post_fade < -5:
        commentary.append("The post-promo dip suggests pull-forward risk or weak repeat demand after the offer ended.")
    else:
        commentary.append("Post-promo trade remained relatively healthy versus the pre-period baseline.")

    for item in commentary:
        st.markdown(f"- {item}")

st.subheader("Campaign scorecard")
scorecard = pd.DataFrame(
    [
        {"metric": "Sales lift vs pre", "value": f"{sales_lift:.1f}%"},
        {"metric": "Volume lift vs pre", "value": f"{volume_lift:.1f}%"},
        {"metric": "Margin rate delta", "value": f"{margin_rate_delta:.1f} pts"},
        {"metric": "Stockouts during promo", "value": int(promo['stockouts'])},
        {"metric": "Ending stock after promo", "value": int(post['ending_stock'])},
    ]
)
st.dataframe(scorecard, use_container_width=True, hide_index=True)
