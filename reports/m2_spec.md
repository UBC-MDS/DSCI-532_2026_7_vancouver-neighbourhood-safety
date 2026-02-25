# Updated Job Stories



# Component Inventory



# Reactivity Diagram
```mermaid 
flowchart TD
    A[/input_nbhd/] --> F{{filtered_df}}
    B[/input_crime_type/] --> F
    C[/input_crime_month/] --> F
    D[/input_crime_day/] --> F
    F --> P1([plot_map])
    F --> P2([plot_bar])
    F --> P3([plot_pie])
    F --> K1[kpi_rep_incidents]
    F --> K2[kpi_crime_rate]
    F --> K3[kpi_avg_comparison]
    F --> K4[kpi_mom_change]
```


# Calculation Details