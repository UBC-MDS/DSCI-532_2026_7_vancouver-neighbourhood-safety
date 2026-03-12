from shiny import App, ui, reactive, render
from shinywidgets import render_plotly, output_widget, render_widget
import pandas as pd
import altair as alt
alt.data_transformers.disable_max_rows()
import folium
from folium.plugins import HeatMap
import geopandas as gpd
from pyproj import Transformer
import faicons as fa
import querychat
from chatlas import ChatGithub, ChatAnthropic
from dotenv import load_dotenv
import os
from utils import resolve_filter, get_filtered_data

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

crime_df = pd.read_csv("data/processed/processed_vancouver_crime_data_2025.csv")
population_df = pd.read_csv("data/raw/van_pop_2016.csv")

# Load neighbourhood polygons
neigh_gdf = gpd.read_file("data/processed/merged_vancity.gpkg",
                        layer="merged_vancity")

# Latitude and Longitude compatibility with Leaflet/Folium
neigh_gdf = neigh_gdf.to_crs(epsg=4326)


# Input options for the dropdowns
neighbourhoods = ["All"] + sorted(crime_df["NEIGHBOURHOOD"].unique())
crime_types = ["All"] + sorted(crime_df["TYPE"].unique())
months = ["All", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
time_of_day = ["All", "Morning", "Afternoon", "Evening/Night"]

def neigh_style(_feature):
    return {
        "fillOpacity": 0.05,
        "weight": 1,
    }

def neigh_style_default(_feature):
    return {
        "fillOpacity": 0.03, 
        "weight": 1
    }

def neigh_style_selected(_feature):
    return {
        "fillOpacity": 0.18, 
        "weight": 3
    }


header = ui.div(
    ui.h2(
        "🍁 Vancouver Neighbourhood Safety",
        style="margin-bottom:4px; font-weight:600;"
    ),
    ui.p(
        "Compare crime patterns across Vancouver neighbourhoods",
        style="margin-bottom:2px;"
    ),
    ui.p(
        "Explore where incidents cluster, which crime types are most common, and when they happen.",
        style="margin-bottom:0; color:rgba(255,255,255,0.85);"
    ),
    style="""
        background-color:#023047;
        color:white;
        padding:16px 20px;
        border-radius:8px;
        margin-bottom:14px;
        border-bottom:4px solid #fb8500;
    """
)

qc = querychat.QueryChat(
    crime_df.copy(),
    "VancouverNeighbourhoodSafety",
    greeting="""👋 Hi there! I am your friendly Vancouver neighbourhood crime bot. Ask me anything about the crimes in Vancouver.

1. Sorting the data <span class="suggestion">Show me all crime from newest to oldest by date it happened</span>
2. Filter the data <span class="suggestion">Show me all mischief crimes</span>
3. Answer questions about the data: <span class="suggestion">How does the crime rate of Kitsilano compare to the Vancouver average?</span>

You can also say <span class="suggestion">Reset</span> to clear the current filter/sort, or <span class="suggestion">Help</span> for more usage tips.
""",
    data_description="""
Vancouver Police Department crime incident dataset used to analyze neighbourhood safety and crime patterns in Vancouver.

Each row represents a single reported crime incident.

Columns:
- TYPE: Category of the crime (e.g., Mischief, Break and Enter Commercial, Theft from Vehicle).
- YEAR: Year when the incident occurred.
- MONTH: Month of the incident (1–12).
- DAY: Day of the month when the incident occurred.
- HOUR: Hour of the day when the incident occurred (0–23).
- MINUTE: Minute when the incident occurred.
- HUNDRED_BLOCK: Approximate street block where the crime occurred (e.g., "10XX HORNBY ST").
- NEIGHBOURHOOD: Vancouver neighbourhood where the incident took place (e.g., Downtown, West End, Sunset).
- X: UTM easting coordinate of the incident location (EPSG:32610).
- Y: UTM northing coordinate of the incident location (EPSG:32610).

The dataset can be used to analyze:
- crime frequency by type
- crime patterns by neighbourhood
- temporal trends by year, month, day, or hour
- spatial patterns of crime locations across Vancouver.
""",
    client=ChatAnthropic(model="claude-sonnet-4-0"),
)

app_ui = ui.page_navbar(
    ui.nav_panel(
        "LLM Chat",
        ui.layout_sidebar(
            qc.sidebar(),
            ui.card(
                ui.card_header(
                    ui.output_text("title"),
                    ui.download_button("download_filtered", 
                                       "Download data"),
                    class_="d-flex justify-content-between align-items-center"
                    ),
                ui.output_data_frame("data_table"),
                fill=True,
            ),
            ui.layout_columns(
                ui.card(
                    ui.div(
                        "Incidents Found",
                        style="font-size:0.9rem; color:#666; line-height:1; margin-bottom:0.2rem;"
                    ),
                    ui.div(
                        ui.output_text("chat_crime_count"),
                        style="font-size:1.4rem; font-weight:600; line-height:1;"
                    ),
                    class_="border border-dark shadow-sm",
                    style="height:100px; padding:0rem 0rem; overflow:hidden;"
                ),
                ui.card(
                    ui.div(
                        "Most Affected Neighbourhood",
                        style="font-size:0.9rem; color:#666; line-height:1; margin-bottom:0.2rem;"
                    ),
                    ui.div(
                        ui.output_text("chat_top_neighbourhood"),
                        style="font-size:1.4rem; font-weight:600; line-height:1;"
                    ),
                    class_="border border-dark shadow-sm",
                    style="height:100px; padding:0rem 0rem; overflow:hidden;"
                ),
                ui.card(
                    ui.div(
                        "Most Common Crime",
                        style="font-size:0.9rem; color:#666; line-height:1; margin-bottom:0.2rem;"
                    ),
                    ui.div(
                        ui.output_text("chat_top_crime"),
                        style="font-size:1.4rem; font-weight:600; line-height:1;"
                    ),
                    class_="border border-dark shadow-sm",
                    style="height:100px; padding:0rem 0rem; overflow:hidden;"
                ),
                fillable=False,
            ),
            fillable=True,

        ),
        value = "llm_chat",
    ),
    ui.nav_panel(
        "Main dashboard",
        header,
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_selectize("nb", "Neighbourhood",
                    choices=neighbourhoods,
                    multiple=True,
                    selected=["Downtown", "West End"]), 
                ui.input_selectize("crime_type", "Crime Type",
                    choices=crime_types,
                    multiple=True,
                    selected="Break and Enter Residential/Other"),
                ui.input_selectize("month", "Month",
                    choices=months, 
                    multiple=False,
                    selected="All"),
                ui.input_selectize("daily_time", "Time of Day",
                    choices=time_of_day,
                    multiple=False,
                    selected="All"),
                ui.input_action_button("clear_filters", "Clear All Filters", 
                    class_="btn btn-secondary btn-sm w-100 mt-2",
                    style="""
                    background-color:#023047;
                    color:white;
                    """),
                full_screen=True,
                width=250,
                bg="#f8f9fa",
            ),
            ####################################################################################################
            ###### KINDLY NOTE THAT: The styling for the value boxes Code block below  was customized with Gemini #####
            ####################################################################################################
            ui.layout_columns(
            ui.div(
                ui.div(fa.icon_svg("file-invoice", width="16px", height="16px"), " Reported Incidents", style="font-size: 14px; color: #444; margin-bottom: 4px;"),
                ui.div(ui.output_text("crime_count"), style="font-size: 26px; font-weight: bold; line-height: 1;"),
                class_="card border border-dark shadow-sm",
                style="padding: 15px; height: 90px; display: flex; flex-direction: column; justify-content: center;"
            ),
            
            ui.div(
                ui.div(fa.icon_svg("chart-line", width="16px", height="16px"), " Crime Rate", style="font-size: 14px; color: #444; margin-bottom: 4px;"),
                ui.div(ui.output_text("crime_rate"), style="font-size: 26px; font-weight: bold; line-height: 1;"),
                class_="card border border-dark shadow-sm",
                style="padding: 15px; height: 90px; display: flex; flex-direction: column; justify-content: center;"
            ),
            
            ui.div(
                ui.div(fa.icon_svg("scale-balanced", width="16px", height="16px"), " Average Comparison", style="font-size: 14px; color: #444; margin-bottom: 4px;"),
                ui.div(ui.output_ui("average_comparison"), style="font-size: 26px; font-weight: bold; line-height: 1;"),
                class_="card border border-dark shadow-sm",
                style="padding: 15px; height: 90px; display: flex; flex-direction: column; justify-content: center;"
            ),
            
            ui.div(
                ui.div(fa.icon_svg("shield-halved", width="16px", height="16px"), " Neighbourhood Safety Rank", style="font-size: 14px; color: #444; margin-bottom: 4px;"),
                ui.div(ui.output_text("neighbourhood_rank"), style="font-size: 26px; font-weight: bold; line-height: 1;"),
                class_="card border border-dark shadow-sm",
                style="padding: 15px; height: 90px; display: flex; flex-direction: column; justify-content: center;"
            ),
            fill=False,
            
            ),
            ui.layout_columns(
                ui.div(
                    ui.div(
                        ui.strong("Map layers"),
                        ui.input_switch("show_heatmap", "Heatmap", True),
                        ui.input_switch("show_points", "Points", False),
                        ui.input_switch("show_rates", "Rate per 1,000", False),
                        style="""
                            display:flex;
                            gap:1rem;
                            align-items:center;
                            padding:0.2rem 0.6rem;
                            background:#f8f9fa;
                            border-bottom:1px solid #ddd;
                            font-size:0.8rem;
                            #white-space:nowrap;
                            #vertical-align:middle;
                            position:relative; top:10px;
                        """
                    ),
                    ui.card(
                        ui.card_header(ui.strong("Crime Occurrences Across Neigbourhoods")),
                        ui.output_ui("crime_map"),
                        full_screen=True,
                        style="height: 600px;"
                    ),
                    style="display: flex; flex-direction: column; gap: 0.75rem;"
                ), 
                ui.div(
                    ui.card(
                        ui.card_header(ui.strong("Top Crime Types")),
                        output_widget("top_crime_type_bar"),
                        full_screen=True,
                        style="""
                            height: 320px;
                            flex-grow: 1 1 0;
                        """
                    ),
                    ui.card(
                        ui.card_header(ui.strong("Crime Occurrences By Time of Day")), 
                        output_widget("time_of_day_plot"),
                        padding=0,
                        full_screen=True,
                        style="""
                            height: 320px;
                            flex-grow: 1 1 0;
                        """
                    ),
                    style="""
                        display: flex;
                        flex-direction: column;
                        gap: 0.2rem;
                        height: 100%;
                    """
                ), 
                col_widths=[7, 5],
                fill=True
            ),
        ),
        value = "main_dashboard",
    )
)

def server(input, output, session):
    
    @reactive.effect
    @reactive.event(input.clear_filters)
    def clear_all_filters():
        ui.update_selectize("nb", selected=[])
        ui.update_selectize("crime_type", selected=[])
        ui.update_selectize("month", selected=[])
        ui.update_selectize("daily_time", selected=[])
    
    @reactive.calc
    def filtered_data():
        return get_filtered_data(crime_df, resolve_filter(input.nb()), resolve_filter(input.crime_type()), resolve_filter(input.month()), resolve_filter(input.daily_time()))
    
    @reactive.calc
    def filtered_population():
        nb_values = resolve_filter(input.nb())
        if nb_values is None:
            return population_df["POPULATION"].sum()
        else:
            pop = population_df[population_df["NEIGHBOURHOOD"].isin(nb_values)]["POPULATION"]
            return pop.sum() if not pop.empty else 0
    
    @reactive.calc
    def neighbourhood_ranking():
        nb_values = resolve_filter(input.nb())
        
        if nb_values is None or len(nb_values) > 1:
            return None
            
        df = get_filtered_data(crime_df, resolve_filter(input.crime_type()), resolve_filter(input.month()), resolve_filter(input.daily_time()))
        nb = nb_values[0]
        
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
        nb_values = resolve_filter(input.nb())
        city_avg = len(crime_df) / population_df["POPULATION"].sum() * 100
        
        if nb_values is None:
            return ui.span(ui.span(f"{city_avg:.2f}%", style="color: black"))
        
        neighbourhood_rate = int(len(filtered_data())) / filtered_population() * 100 if filtered_population() > 0 else 0
        comparison_val = neighbourhood_rate - city_avg
        color = "green" if comparison_val < 0 else "red"
        return ui.span(f"{comparison_val:.2f}%", style=f"color: {color}")
    
    @render.text
    def neighbourhood_rank():
        rank = neighbourhood_ranking()
        return rank if rank else "N/A"
    
    @reactive.calc
    def data_for_time_of_day_plot():
        df = get_filtered_data(crime_df, resolve_filter(input.nb()), resolve_filter(input.crime_type()), resolve_filter(input.month()))
        return df
        
        
    @render_widget
    def time_of_day_plot():
        df = data_for_time_of_day_plot()
        
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

        slices = base.mark_arc(innerRadius=30, outerRadius=60)


        text = base.mark_text(radius=100, size=11, align='center', baseline='bottom').encode(
            text='full_label:N'
        )
        
        pie_chart = (text + slices).configure_view(
            stroke=None 
        ).properties(
            height="container",
            width="container",
        )

        return pie_chart

    @reactive.calc
    def filtered_latlon():
        df = filtered_data().copy()
        df["X"] = pd.to_numeric(df["X"], errors="coerce")
        df["Y"] = pd.to_numeric(df["Y"], errors="coerce")
        df = df.dropna(subset=["X", "Y"])

        if df.empty:
            return pd.DataFrame(columns=["lat", "lon"])
        
        # Source UTM Zone 10N WGS84 EPSG:32610 to WGS84 lat/lon EPSG:4326
        transformer = Transformer.from_crs("EPSG:32610", "EPSG:4326", always_xy=True)

        lons, lats = transformer.transform(df["X"].to_numpy(), df["Y"].to_numpy())
        df["lat"] = lats
        df["lon"] = lons

        return df
    
    @reactive.calc
    def selected_neigh_bounds():
        nb_values = resolve_filter(input.nb())
        if nb_values is None:
            return None
        
        neigh = neigh_gdf[neigh_gdf["Name"].isin(nb_values)]
        if neigh.empty:
            return None
        
        minx, miny, maxx, maxy = neigh.total_bounds
        return [[miny, minx], [maxy, maxx]]

    @reactive.calc
    def neighbourhood_rates():
        df = filtered_data()

        # Get crime counts by neighbourhood
        counts = (
            df.groupby("NEIGHBOURHOOD")
            .size()
            .reset_index(name="incident_count")
        )

        # Join incident counts with population data
        merged = counts.merge(
            population_df[["NEIGHBOURHOOD", "POPULATION"]],
            on="NEIGHBOURHOOD",
            how="left"
        )

        # Division by zero or missing values
        merged = merged.dropna(subset=["POPULATION"])
        merged = merged[merged["POPULATION"] > 0]

        merged["rate_per_1000"] = (
            merged["incident_count"] / merged["POPULATION"]
        ) * 1000

        return merged
    
    @reactive.calc
    def filetered_data_no_crime_type():
        df = get_filtered_data(crime_df, resolve_filter(input.nb()), resolve_filter(input.month()), resolve_filter(input.daily_time()))
        return df

    @reactive.calc
    def top_crime_types():
        df = filetered_data_no_crime_type()

        top = (
            df.groupby("TYPE")
            .size()
            .sort_values(ascending=False)
            .head(5)
        )

        return top

    # @render.ui
    @render_widget
    def top_crime_type_bar():
        top = top_crime_types()

        if top.empty:
            return alt.Chart(pd.DataFrame({"msg": ["No data for current filters"]})).mark_text(size=14).encode(text="msg:N")

        # Convert Series to DataFrame
        df_top = top.reset_index()
        df_top.columns = ["Crime Type", "Incidents"]

        # Compute percent share
        total_incidents = df_top["Incidents"].sum()
        df_top["Percent Share"] = (df_top["Incidents"] / total_incidents) * 100
        
        chart = (
            alt.Chart(df_top)
            .mark_bar(size=25)
            .encode(
                x=alt.X("Percent Share:Q", title="Percent of Incidents"),
                y=alt.Y(
                    "Crime Type:N",
                    sort=alt.SortField("Percent Share", order="descending"),
                    title="",
                    axis=alt.Axis(labelLimit=100),   # Restrict long labels
                    scale=alt.Scale(paddingInner=0)
                ),
                color=alt.Color(
                    "Percent Share:Q",
                    scale=alt.Scale(scheme="tealblues"),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip("Crime Type:N"),
                    alt.Tooltip("Incidents:Q"),
                    alt.Tooltip("Percent Share:Q", format=".1f"),
                ],
            )
            .properties(
                height="container",
                width="container",
                title=alt.TitleParams(
                    text="(All filters except Crime Type)",
                ),
            )
            .configure_title(fontSize=12)
        )

        return chart


    @render.ui
    def crime_map():
        vancity_center = [49.2827, -123.1207]
        nb_values = resolve_filter(input.nb())
        rates = neighbourhood_rates()
        
        # Map base
        m = folium.Map(
            location=vancity_center,
            zoom_start=12,
            tiles="CartoDB positron",
            width="100%",
            height="100%",
        )

        # Add neighbourhood polygons (default-persistent style)
        folium.GeoJson(
            neigh_gdf.__geo_interface__,
            name="Neighbourhoods",
            style_function=neigh_style_default,
        ).add_to(m)

        # Highlight selected neighbourhood
        if nb_values is not None:
            sel_neigh = neigh_gdf[neigh_gdf["Name"].isin(nb_values)]
            
            if not sel_neigh.empty:
                if len(nb_values) == 1:
                    layer_name = f"Selected: {nb_values[0]}"
                elif len(nb_values) <= 3:
                    layer_name = f"Selected: {', '.join(nb_values)}"
                else:
                    layer_name = f"Selected Neighbourhoods ({len(nb_values)})"
                    
                folium.GeoJson(
                    sel_neigh.__geo_interface__,
                    name=layer_name,
                    style_function=neigh_style_selected,
                ).add_to(m)

        # Add crime Heatmap and Points layers based on X/Y (lat/lon)
        
        # Map layers persistent state
        # Show them if selected
        points = filtered_latlon()

        # Heatmap layer
        if input.show_heatmap():
            heat_layer = folium.FeatureGroup(name="Heatmap", show=True)
            heat_data = points[["lat", "lon"]].values.tolist()

            if heat_data:
                HeatMap(
                    heat_data,
                    radius=14,
                    blur=18,
                    max_zoom=13,
                ).add_to(heat_layer)
            
            heat_layer.add_to(m)

        # Choropleth layer for crime rates by neighbourhood
        if input.show_rates():
            # Merge rates into polygons
            gdf_rate = neigh_gdf.merge(
                rates,
                left_on="Name",
                right_on="NEIGHBOURHOOD",
                how="left"
            )

            gdf_rate["incident_count"] = gdf_rate["incident_count"].fillna(0)
            gdf_rate["rate_per_1000"] = gdf_rate["rate_per_1000"].fillna(0)

            folium.Choropleth(
                geo_data=gdf_rate.__geo_interface__,
                data=gdf_rate[["Name", "rate_per_1000"]],
                columns=["Name", "rate_per_1000"],
                key_on="feature.properties.Name",
                name="Rate per 1,000 residents",
                fill_color="YlOrRd",
                fill_opacity=0.6,
                line_opacity=0.3,
                legend_name="Incidents per 1,000 residents",
                show=True  #False
            ).add_to(m)

        # Points layer
        if input.show_points():
            points_layer = folium.FeatureGroup(name="Points", show=True)
            max_points = 2000
            points_for_markers = points.head(max_points)

            for _, row in points_for_markers.iterrows():
                # Tooltip content
                tooltip_text = (
                    f"<b>{row['TYPE']}</b><br>"
                    f"{row['HUNDRED_BLOCK']}<br>"
                    f"{row['NEIGHBOURHOOD']}<br>"
                    f"{row['MONTH_NAME']} {row['DAY']} at {row['HOUR']:02}:{row['MINUTE']:02}"
                )
                
                folium.CircleMarker(
                    location=[row["lat"], row["lon"]],
                    radius=3,
                    weight=1,
                    fill=True,
                    fill_opacity=0.4,
                    tooltip=tooltip_text
                ).add_to(points_layer)
            
            points_layer.add_to(m)

        # Zoom map to selected neighbourhood
        bounds = selected_neigh_bounds()
        if bounds is not None:
            m.fit_bounds(bounds)

        folium.LayerControl(collapsed=True).add_to(m)
        
        # Note: This JS function was generated with ChatGPT 5.0 to solve for 
        # removing the always visible Choropleth scale in the map and to show
        # it only when the "Rate per 1000 residents" layer is toggled on.
        toggle_legend_js = """
        <script>
        (function() {
        function syncLegend() {
            // Choropleth legend is usually a branca legend with class "legend"
            const legend = document.querySelector('.legend');
            if (!legend) return false;

            // Find the overlay checkbox by its label text
            const labels = Array.from(document.querySelectorAll('.leaflet-control-layers-overlays label'));
            const target = labels.find(l => l.textContent.trim() === 'Rate per 1,000 residents');
            if (!target) return false;

            const cb = target.querySelector('input[type="checkbox"]');
            if (!cb) return false;

            // Set initial state + bind updates
            legend.style.display = cb.checked ? 'block' : 'none';
            cb.addEventListener('change', () => {
            legend.style.display = cb.checked ? 'block' : 'none';
            });

            return true;
        }

        // Try a few times because Leaflet controls/legend load after map HTML inserts
        let tries = 0;
        const timer = setInterval(() => {
            tries += 1;
            if (syncLegend() || tries > 25) clearInterval(timer);
        }, 200);
        })();
        </script>
        """
        m.get_root().html.add_child(folium.Element(toggle_legend_js))

        return ui.HTML(m._repr_html_())
    
    qc_vals = qc.server()

    @reactive.calc
    def query_df():
        return qc_vals.df()

    @render.text
    def title():
        return qc_vals.title() or "Vancouver Neighbourhood Crimes"

    @render.data_frame
    def data_table():
        return query_df()
    
    @render.download(filename="vancouver_neighbourhood_crimes.csv")
    def download_filtered():
        df = query_df()
        yield df.to_csv(index=False)

    @render.text
    def chat_crime_count():
        df = query_df()
        if df.empty:
            return "N/A"
        return str(len(df))
    
    @render.text
    def chat_top_neighbourhood():
        df = query_df()
        if df.empty:
            return "N/A"
        top = (
            df.groupby("NEIGHBOURHOOD")
            .size()
            .sort_values(ascending=False)
            .index[0]
        )
        return str(top)
    
    @render.text
    def chat_top_crime():
        df = query_df()
        if df.empty:
            return "N/A"
        top = (
            df.groupby("TYPE")
            .size()
            .sort_values(ascending=False)
            .index[0]
        )
        return str(top)
    

app = App(app_ui, server=server)
