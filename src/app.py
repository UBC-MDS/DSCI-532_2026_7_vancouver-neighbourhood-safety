from shiny import App, ui, reactive, render
from shinywidgets import render_plotly, output_widget, render_widget
import pandas as pd
import altair as alt
alt.data_transformers.disable_max_rows()
import folium
from folium.plugins import HeatMap
import geopandas as gpd
from pyproj import Transformer


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
            ui.output_ui("crime_map"),
            style="height: 100%; width: 100%;",
            full_screen=True
            ),
        ui.layout_columns(
            ui.card(
                # ui.card_header(ui.strong("Count of Crime Type")),
                ui.card_header(ui.strong("Top Crime Types")),
                output_widget("top_crime_type_bar"),
                full_screen=True,
                # ui.card_body(output_widget("top_crime_type_bar", width="100%", height="100%"),
                # fill=True
                # ),
                #full_screen=True,
                #fill=True
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
    
    @reactive.calc
    def data_for_time_of_day_plot():
        nb = input.nb()
        crime_type = input.crime_type()
        month = input.month()
        df = crime_df.copy()
        if nb != "All":
            df = df[df["NEIGHBOURHOOD"] == nb]
        if crime_type != "All":
            df = df[df["TYPE"] == crime_type]
        if month != "All":
            df = df[df["MONTH_NAME"] == month]
        return df
        
    
    @render_plotly
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

    @reactive.calc
    def filtered_latlon():
        df = filtered_data()

        # Validate numeric values and drop missing coordinates
        xy = df[["X", "Y"]].copy()
        xy["X"] = pd.to_numeric(xy["X"], errors="coerce")
        xy["Y"] = pd.to_numeric(xy["Y"], errors="coerce")
        xy = xy.dropna()

        if xy.empty:
            return pd.DataFrame(columns=["lat", "lon"])
        
        # Source UTM Zone 10N WGS84 EPSG:32610 to WGS84 lat/lon EPSG:4326
        transformer = Transformer.from_crs("EPSG:32610", "EPSG:4326", always_xy=True)

        lons, lats = transformer.transform(xy["X"].to_numpy(), xy["Y"].to_numpy())
        out = pd.DataFrame({"lat": lats,
                            "lon": lons})
        
        # Metro Vancouver bounds
        out = out[
            out["lat"].between(49.0, 49.4) &
            out["lon"].between(-123.3, -122.9)
        ]

        return out
    
    @reactive.calc
    def selected_neigh_bounds():
        nb = input.nb()
        if nb == "All":
            return None
        
        neigh = neigh_gdf[neigh_gdf["Name"] == nb]
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
        df = crime_df.copy()
        nb = input.nb()
        month = input.month()
        daily_time = input.daily_time()

        if nb != "All":
            df = df[df["NEIGHBOURHOOD"] == nb]

        if month != "All":
            df = df[df["MONTH_NAME"] == month]

        if daily_time != "All":
            df = df[df["TIME_OF_DAY"] == daily_time]
        
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

        # Reverse for horizontal ordering (largest on top)
        #df_top = df_top.sort_values("Incidents")
        
        chart = (
            alt.Chart(df_top)
            .mark_bar()
            .encode(
                x=alt.X("Percent Share:Q", title="Percent of Incidents"),
                y=alt.Y(
                    "Crime Type:N",
                    sort=alt.SortField("Percent Share", order="descending"),
                    title="",
                    axis=alt.Axis(labelLimit=100)   # Restrict long labels
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
                # height=320,
                title=alt.TitleParams(
                    text="(All filters except Crime Type)",
                    # subtitle="(All filters except Crime Type)",
                ),
            )
            .configure_title(fontSize=12)
        )

        return chart


    @render.ui
    def crime_map():
        vancity_center = [49.2827, -123.1207]
        nb = input.nb()
        rates = neighbourhood_rates()
        
        # Map base
        m = folium.Map(
            location=vancity_center,
            zoom_start=12,
            tiles="CartoDB positron",
            width="100%",
            height="100%",
        )

        # Add neighbourhood polygons (default style)
        folium.GeoJson(
            neigh_gdf.__geo_interface__,
            name="Neighbourhoods",
            style_function=neigh_style_default,
        ).add_to(m)

        # Highlight selected neighbourhood
        if nb != "All":
            sel_neigh = neigh_gdf[neigh_gdf["Name"] == nb]
            if not sel_neigh.empty:
                folium.GeoJson(
                    sel_neigh.__geo_interface__,
                    name=f"Selected: {nb}",
                    style_function=neigh_style_selected,
                ).add_to(m)

        # Add crime Heatmap and Points layers based on X/Y (lat/lon)
        # Define toggleable layers
       
        # Heatmap layer (default on)
        heat_layer = folium.FeatureGroup(name="Heatmap", show=True)

        points = filtered_latlon()
        heat_data = points[["lat", "lon"]].values.tolist()

        if heat_data:
            HeatMap(
                heat_data,
                # name="Crime Heatmap",
                radius=14,
                blur=18,
                max_zoom=13,
            # ).add_to(m)
            ).add_to(heat_layer)
        
        heat_layer.add_to(m)
        
        # Points layer (optional)
        points_layer = folium.FeatureGroup(name="Points", show=False)

        max_points = 2000
        points_for_markers = points.head(max_points)

        for lat, lon in points_for_markers[["lat", "lon"]].values:
            folium.CircleMarker(
                location=[lat, lon],
                radius=3,
                weight=1,
                fill=True,
                fill_opacity=0.4,
            ).add_to(points_layer)
        
        points_layer.add_to(m)

        # Choropleth layer for crime rates by neighbourhood
        
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
            show=False
        ).add_to(m)

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


app = App(app_ui, server=server)
