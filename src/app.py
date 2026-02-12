from shiny import App, ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("neighbourhood", "Neighbourhood",
            ["All", "Milestone 1", "Milestone 2"]),
        ui.input_select("crime_type", "Crime Type",
            ["All Crime Types", "Team 01", "Team 02"]),
        ui.input_select("month", "Month",
            ["All", "January", "February", "March", "April", "May", "June", "July", "August",
            "September", "October", "November", "Decemeber"]),
        ui.input_select("daily_time", "Time of Day",
            ["All", "Morning", "Afternoon", "Evening"]),
        full_screen=True
    ),
    ui.layout_columns(
        ui.value_box("Reported Incidents", "259"),
        ui.value_box("Crime Rate", "9%"),
        ui.value_box("Average Comparison", "2%"),
        ui.value_box("MoM Change", "4%"),
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
                ui.card_header(ui.strong("Crime by Time of Day")), 
                full_screen=True,
                ),
            col_widths=[12,12],
            fill=True
        ),
        col_widths=[7, 5],
        ),
    title=ui.tags.h2("Vancouver Neighbourhood Safety", style="font-weight: bold;"), fillable=True,
)


def server(input, output, session):
    pass


app = App(app_ui, server=server)



