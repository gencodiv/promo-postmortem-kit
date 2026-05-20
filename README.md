# Promo Postmortem Kit

A lightweight toolkit for understanding what a retail promotion actually changed.

## Why this exists
Post-promo review is often shallow. Teams notice sales movement but miss the full commercial picture:
- volume lift
- revenue lift
- margin-rate damage
- stock pressure
- post-promo fade

This project is designed as a small but useful postmortem starter.

## What the demo now includes
- sample campaign results in `data/promo_results.csv`
- campaign and SKU selector
- period comparison across pre / promo / post
- sales-lift and volume-lift metrics
- margin-rate delta read-out
- simple stock-pressure and post-promo commentary
- scorecard table for fast workshop review

## Why this matters
It turns a vague “the promo worked” conversation into a more decision-ready one:
- did revenue grow enough?
- what did margin give up?
- did we create stock stress?
- did the business fade after the campaign?

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Good use cases
- post-campaign reviews
- commercial steering discussions
- merchandising and planning retrospectives
- lightweight public demos of retailer-legible analysis

## Next steps
- compare multiple campaigns together
- add baseline forecast vs actual uplift
- track store / channel mix
- export postmortem packs
