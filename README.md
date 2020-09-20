# CovClude

## Introduction:

With all the issues with testing being unreliable, lagged from actual number of cases, we can see that there is an evident issue. Tracking Covid is hard, and so we decided to investigate the correlation between Covid-19 confirmed cases and emergency phone calls with Covid-related symptoms.

## How it works:

We leverage Goldman Sachs' Marquee API for the NHS Phone Triage dataset, and cross-reference this with the government's own dataset for confirmed cases, we then split the data-set based on location, then we perform a lag-based autocorrelation to see whether the phone triage could be used as a good predictor for the confirmed cases.

## Use case:

Understand how the exponential spread of Covid could be potentially mitigated by some Early Warning System, if there is some correlation between the two series.

## Problems we encountered:

- Cross-API integration with location data wasn't an exact match, so we had to build a linker
- GS Quant's correlation function's statistical background

## TODO:

- Visualisation of data -- plotly doesn't support UK county
- Perform data smoothing as the data is quite noisy!

## Contributors

- Neel Dugar
- Samuel Adekunle
