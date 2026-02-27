# Updated Job Stories

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | As a newcomer unfamiliar with Vancouver neighbourhoods, I want to view an interactive map that displays crime levels by neighbourhood so that I can visually compare areas and better understand where higher or lower crime concentrations are located. | ✅ Implemented |                               |
| 2   | As a parent with young children, I want to see when crimes most frequently occur (morning, afternoon, evening, night) so that I can assess whether incidents tend to happen during times when my children may be home. | ✅ Implemented |  |
| 3   | As someone comparing neighbourhoods of different sizes, I want to see crime rates normalized by population so that I can make fair comparisons between larger and smaller areas. | ✅ Implemented  |                               |
| 4   | As someone relocating to a new city and unfamiliar with its neighbourhoods, I want to see how a neighbourhood ranks in safety compared to other areas so that I can quickly understand whether it is relatively safer or riskier when making a housing decision. | ✅ Implemented  |                               |

# Component Inventory

| ID                        | Type      | Shiny widget / renderer | Depends on                                                | Job Story |
|---------------------------|-----------|--------------------------|-----------------------------------------------------------|-----------|
| `input_nb`                | Input     | `ui.input_select()`      | —                                                         | #1, #3, #4 |
| `input_crime_type`        | Input     | `ui.input_select()`      | —                                                         | #1, #2, #3 |
| `input_month`             | Input     | `ui.input_select()`      | —                                                         | #2        |
| `input_daily_time`        | Input     | `ui.input_select()`      | —                                                         | #2        |
| `crime_count`             | Output    | `@render.text`           | `filtered_data()`                                        | #1        |
| `crime_rate`              | Output    | `@render.text`           | `filtered_data()`, `filtered_population()`               | #3        |
| `average_comparison`      | Output    | `@render.ui`             | `filtered_data()`, `filtered_population()`               | #3        |
| `neighbourhood_rank`      | Output    | `@render.text`           | `neighbourhood_rank_calc()`                              | #4        |
| `filtered_data`           | Reactive  | `@reactive.calc`         | `input_nb`, `input_crime_type`, `input_month`, `input_daily_time` | #1, #2, #3 |
| `filtered_population`     | Reactive  | `@reactive.calc`         | `input_nb`                                               | #3        |
| `neighbourhood_rank_calc` | Reactive  | `@reactive.calc`         | `input_crime_type`, `input_month`, `input_daily_time`    | #4        |

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
    KPIS --> K4([kpi_neighbourhood_rank])
```


# Calculation Details

| Reactive Calculation      | Inputs it Depends On | Transformation Performed | Outputs Consuming Reactive Calculation |
|---------------------------|---------------------|--------------------------|----------------------------------------|
| `filtered_data()` | `input.nb`, `input.crime_type`, `input.month`, `input.daily_time` | Filters the crime dataset to match the selected neighbourhood, crime type, month, and time-of-day selections. | `crime_count`, `crime_rate`, `average_comparison` |
| `filtered_population()` | `input.nb` | Returns the population of the selected neighbourhood. | `crime_rate`, `average_comparison` |
| `neighbourhood_ranking()` | `input.nb`, `input.crime_type`, `input.month`, `input.daily_time` | Applies the selected filters, calculates crime counts per neighbourhood then converts them into population-adjusted crime rates. Returns the rank of the neighbourhoods sorted by crime rate. | `neighbourhood_rank` |
