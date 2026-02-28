# DSCI-532_2026_7_vancouver-neighbourhood-safety

The Vancouver Neighbourhood Safety dashboard was developed to provide an interactive overview of crime patterns across different neighbourhoods in Vancouver, Canada. The dashboard allows users to explore crime rates based on different breakdowns including neighbourhoods, crime types, and time patterns. Designed with home searchers in mind, it transforms crime data from the Vancouver Police Department (VPD) into clear visual comparisons, helping users better understand neighbourhood safety and make more informed housing decisions.

## Visualization

Both the *development* and the *stable* versions of this dashboard can be accessed via the following links:<br>
[Stable version](https://019c9287-0994-4ff7-4350-227e28a7e29e.share.connect.posit.cloud/)<br>
[Development version](https://019c928e-e698-6cad-eba8-b45208bebd6f.share.connect.posit.cloud/)

## Demo
![gif](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/blob/chore/demo-gif/img/vancouver-neighbourhood-safety.gif)

## Installation

To reproduce the environment, navigate to the root of the project dirctory and run:

``` bash
conda env create -f environment.yml
conda activate vc_safety2
```

## Render the app

To render the app, navigate to the root of the project directory and run:

``` bash
shiny run src/app.py
```

Open http://127.0.0.1:8000 in a web browser

## Data Attribution
This project uses dataset provided by the City of Vancouver and the Vancouver Police Department.

_Hence: **Contains information licensed under the Open Government License Vancouver**._


**Sources**
- [Vancouver Police Department GeoDASH Open Data Portal](https://geodash.vpd.ca/opendata/)
- [Official License Page](https://opendata.vancouver.ca/pages/licence/)