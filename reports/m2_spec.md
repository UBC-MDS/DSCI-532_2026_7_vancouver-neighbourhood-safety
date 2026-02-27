# Updated Job Stories

| # | Job Story | Status | Notes |
|---|-----------|--------|-------|
| 1 | As a newcomer unfamiliar with Vancouver neighbourhoods, I want to view an interactive map that displays crime levels by neighbourhood so that I can visually compare areas and better understand where higher or lower crime concentrations are located. |  |  |
| 2 | As a parent with young children, I want to see when crimes most frequently occur (morning, afternoon, evening, night) so that I can assess whether incidents tend to happen during times when my children may be home. |  |  |
| 3 | As someone comparing neighbourhoods of different sizes, I want to see crime rates normalized by population so that I can make fair comparisons between larger and smaller areas. |  |  |
| 4 | As someone making a housing decision, I want to see how crime rates change month by month throughout the year so that I can identify seasonal patterns or periods with higher levels of crime in a neighbourhood. |  |  |


# Component Inventory

| ID                 | Type           | Shiny widget / renderer | Depends on                                   | Job story         |
|--------------------|---------------|--------------------------|-----------------------------------------------|-------------------|
| input_nb           | input         | ui.page_sidebar()        |                                               | #1                |
| input_crime_type   | input         | ui.page_sidebar()        |                                               |                   |
| input_month        | input         | ui.page_sidebar()        |                                               |                   |
| input_daily_time   | input         | ui.page_sidebar()        |                                               | #2                |
| filtered_data      | Reactive Calc | @reactive.calc           | input_nb, input_crime_type, input_month, input_daily_time | #1, #2, #3, #4 |
| plot_map           | Output        | @render.plot             | filtered_df                                  |                   |
| plot_bar           | Output        | @render.plot             | filtered_df                                  |                   |
| plot_pie           | Output        | @render.plot             | filtered_df                                  |                   |
| kpi_rep_incidents  | Output        | @ui.value_box            | filtered_df                                  |                   |
| kpi_crime_rate     | Output        | @ui.value_box            | filtered_df                                  |                   |
| kpi_avg_comparison | Output        | @ui.value_box            | filtered_df                                  |                   |
| kpi_mom_change     | Output        | @ui.value_box            | filtered_df                                  |                   |


# Reactivity Diagram
```mermaid 
flowchart TD
    A[/input_nbhd/] --> F[filtered_df]
    B[/input_crime_type/] --> F
    C[/input_crime_month/] --> F
    D[/input_crime_day/] --> F
    
    F --> PLOTS[PLOTS]
    F --> KPIS[KPIs]

    PLOTS --> P1([plot_map])
    PLOTS --> P2([plot_bar])
    PLOTS --> P3([plot_pie])
    KPIS --> K1([kpi_rep_incidents])
    KPIS --> K2([kpi_crime_rate])
    KPIS --> K3([kpi_avg_comparison])
    KPIS --> K4([kpi_mom_change])
```


# Calculation Details