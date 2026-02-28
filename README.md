# DSCI-532_2026_7_vancouver-neighbourhood-safety

The Vancouver Neighbourhood Safety dashboard was developed to provide an interactive overview of crime patterns across different neighbourhoods in Vancouver, Canada. The dashboard allows users to explore crime rates based on different breakdowns including neighbourhoods, crime types, and time patterns. Designed with home searchers in mind, it transforms crime data from the Vancouver Police Department (VPD) into clear visual comparisons, helping users better understand neighbourhood safety and make more informed housing decisions.

## Visualization

Both the *development* and the *stable* versions of this dashboard can be accessed via the following links:<br>
[Stable version](https://019c9287-0994-4ff7-4350-227e28a7e29e.share.connect.posit.cloud/)<br>
[Development version](https://019c928e-e698-6cad-eba8-b45208bebd6f.share.connect.posit.cloud/)

## Demo
![gif](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/blob/chore/demo-gif/img/vancouver-neighbourhood-safety.gif)

## User Guide

The Vancouver Neighbourhood Safety dashboard is organized into a sidebar for filters and a main panel for key metrics and visual summaries.

Use the sidebar to choose a Neighbourhood, Crime Type, Month or Time of day to filter the dashboard. Selecting All shows all results for that filter, while selecting specific values narrows the data to your chosen subset.

In the main panel, the dashboard displays multiple KPI metrics for crime numbers across the city that updates based on your filter selections. Below the metrics, visual panels are provided for:

- Map of crimes across the City of Vancouver with multiple layers:
  - Heat map of the number of incidents
  - Points of reported incidents
  - Heat map of the rate per 1000 Residents
- Bar chart of the top 5 crime yypes by % share
- Donut chart of crime by time of day

These views are designed to help users quickly explore where incidents are happening, which crime types are most common, and when incidents tend to occur.

## Contributing

Interested in contributing? Check out the [contributing guidelines](./CONTRIBUTING.md) before you start to contribute. Please note that this project is released with a [Code of Conduct](./CODE_OF_CONDUCT.md). By contributing to this project, you agree to abide by its terms.

Follow the steps below to set up the project and start contributing:

1. Clone the repository

Run the following commands in your terminal to clone the repository to your local machine:

```bash
git clone <https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety.git>
cd <DSCI-532_2026_7_vancouver-neighbourhood-safety>
```

2. Install the project environment

Navigate to the root of the project dirctory and run:

``` bash
conda env create -f environment.yml
conda activate vc_safety2
```

3. Render the app

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