from shiny import App, ui, reactive, render
from shinywidgets import render_plotly, output_widget
import pandas as pd
import altair as alt
alt.data_transformers.disable_max_rows()

crime_df = pd.read_csv("data/processed/processed_vancouver_crime_data_2025.csv")
population_df = pd.read_csv("data/raw/van_pop_2016.csv")

# Input options for the dropdowns
neighbourhoods = ["All"] + sorted(crime_df["NEIGHBOURHOOD"].unique())
crime_types = ["All"] + sorted(crime_df["TYPE"].unique())
months = ["All", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
time_of_day = ["All", "Morning", "Afternoon", "Evening"]

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("nb", "Neighbourhood",
            neighbourhoods),
        ui.input_select("crime_type", "Crime Type",
            crime_types),
        ui.input_select("month", "Month",
            months),
        ui.input_select("daily_time", "Time of Day",
            time_of_day),
        full_screen=True
    ),
    ui.layout_columns(
        ui.value_box("Reported Incidents", ui.output_text("crime_count")),
        ui.value_box("Crime Rate", ui.output_text("crime_rate")),
        ui.value_box("Average Comparison", ui.output_ui("average_comparison")),
        ui.value_box("Neighbourhood Safety Rank", ui.output_text("neighbourhood_rank")),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header(ui.strong("Crime Map by Neigbourhood")), 
            full_screen=True
            ),
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.strong("Count of Crime Type")), 
                full_screen=True,
                ),
            ui.card(
                ui.card_header(ui.strong("Crime Occurrences By Time of Day")), 
                ui.card_body(output_widget("time_of_day_plot", width="100%", height="100%"),
                fill=True,
                ),
                full_screen=True,
                fill=True
                ),
            col_widths=[12,12],
            fill=True
        ),
        col_widths=[7, 5],
        ),
    title=ui.tags.h2("Vancouver Neighbourhood Safety", style="font-weight: bold;"), fillable=True,
)

def server(input, output, session):
    @reactive.calc
    def filtered_data():
        nb = input.nb()
        crime_type = input.crime_type()
        month = input.month()
        daily_time = input.daily_time()
        df = crime_df.copy()
        if nb != "All":
            df = df[df["NEIGHBOURHOOD"] == nb]
        if crime_type != "All":
            df = df[df["TYPE"] == crime_type]
        if month != "All":
            df = df[df["MONTH_NAME"] == month]
        if daily_time != "All":
            df = df[df["TIME_OF_DAY"] == daily_time]
        return df
    
    @reactive.calc
    def filtered_population():
        nb = input.nb()
        if nb == "All":
            return population_df["POPULATION"].sum()
        else:
            pop = population_df[population_df["NEIGHBOURHOOD"] == nb]["POPULATION"]
            return pop.iloc[0] if not pop.empty else 0
        
    @reactive.calc
    def neighbourhood_ranking():
        nb = input.nb()
        crime_type = input.crime_type()
        month = input.month()
        daily_time = input.daily_time()
        if nb == "All":
            return None
        df = crime_df.copy()
        if crime_type != "All":
            df = df[df["TYPE"] == crime_type]
        if month != "All":
            df = df[df["MONTH_NAME"] == month]
        if daily_time != "All":
            df = df[df["TIME_OF_DAY"] == daily_time]
        crime_counts = df.groupby("NEIGHBOURHOOD").size()
        rates = crime_counts / population_df.set_index("NEIGHBOURHOOD")["POPULATION"] * 100
        ranked = rates.sort_values(ascending=True).reset_index()
        if nb in ranked["NEIGHBOURHOOD"].values:
            rank = ranked[ranked["NEIGHBOURHOOD"] == nb].index[0] + 1
            total = len(ranked)
            return f"{rank} / {total}"
        return None
    
    @render.text
    def crime_count():
        return str(len(filtered_data()))
    
    @render.text
    def crime_rate():
        count = len(filtered_data())
        pop = filtered_population()
        if pop == 0:
            return "No population data"
        rate = (count / pop * 100) if not pd.isna(pop) else 0
        return f"{rate:.2f}%"
    
    @render.ui
    def average_comparison():
        nb = input.nb()
        city_avg = len(crime_df) / population_df["POPULATION"].sum() * 100
        if nb == "All":
            return ui.span(ui.span(f"{city_avg:.2f}%", style="color: black"))
        
        neighbourhood_rate = int(len(filtered_data())) / filtered_population() * 100 if filtered_population() > 0 else 0
        comparison_val = neighbourhood_rate - city_avg
        color = "green" if comparison_val < 0 else "red"
        return ui.span(f"{comparison_val:.2f}%", style=f"color: {color}")
    
    @render.text
    def neighbourhood_rank():
        rank = neighbourhood_ranking()
        return rank if rank else "N/A"
    
    @render_plotly
    def time_of_day_plot():
        df = filtered_data()
        
        custom_color = ["#fb8500", "#023047", "#669bbc"]

        base = alt.Chart(df).transform_aggregate(
            count='count()',
            groupby=['TIME_OF_DAY']
        ).transform_joinaggregate(
            total='sum(count)'
        ).transform_calculate(
            percent='datum.count / datum.total',
            full_label='datum.TIME_OF_DAY + ": " + format(datum.percent, ".0%")'

        ).encode(
            theta=alt.Theta('count:Q', stack=True),
            color=alt.Color('TIME_OF_DAY:N', scale=alt.Scale(range=custom_color), legend=None),
            tooltip=[alt.Tooltip('TIME_OF_DAY:N', title='Time of Day'), alt.Tooltip('percent:Q', format='.1%', title='Percentage'), alt.Tooltip('count:Q', format=',', title='Count')]
        )

        slices = base.mark_arc(innerRadius=60, outerRadius=120)


        text = base.mark_text(radius=160, size=12).encode(
            text='full_label:N'
        )

        pie_chart = (slices + text).properties(
            width=400,
            height=300
        ).configure_view(
            stroke=None 
        )

        return pie_chart

app = App(app_ui, server=server)
