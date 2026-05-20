import pandas as pd
import streamlit as st

st.set_page_config(page_title="Promo Postmortem Kit", layout="wide")
st.title("Promo Postmortem Kit")
st.caption("A small toolkit for reviewing promotion outcomes")

sample = pd.DataFrame([
    {"period": "pre", "sales": 1000, "margin": 420, "stockouts": 1},
    {"period": "promo", "sales": 1450, "margin": 390, "stockouts": 5},
    {"period": "post", "sales": 920, "margin": 405, "stockouts": 0},
])

st.dataframe(sample, use_container_width=True)
st.metric("Sales lift vs pre", f"{(sample.loc[1, 'sales'] / sample.loc[0, 'sales'] - 1) * 100:.1f}%")
st.metric("Margin change vs pre", f"{(sample.loc[1, 'margin'] / sample.loc[0, 'margin'] - 1) * 100:.1f}%")
