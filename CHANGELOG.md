## [0.4.0]

### Added

### Changed

### Fixed

### Known Issues

### Release Highlight

### Collaboration

### Reflection

# Testing Plan

# Testing Plan

| Test function | Test type | Description | What could break |
|--------------|----------|-------------|------------------|
| test_sidebar_filters | UI test | Verifies that filters update correctly when selections are changed | Renaming input IDs, changing filter UI components or defaults, or altering dashboard navigation |
| test_clear_filters_button | UI test | Checks that clicking the "Clear All Filters" button resets sidebar filters to an empty state | Changing button ID, modifying reset logic, or altering reactive update behaviour |
| test_map_layer_switches | UI test | Ensures that map layer toggle switches change state correctly when interacted with | Renaming switch inputs, changing default states, or redesigning map layer controls |
| test_download_button | UI test | Verifies that the download button is visible in the LLM Chat tab with the correct label | Changing button ID or label, moving/removing the button, or restructuring the chat layout |
| test_filter_neighbourhood | Unit test | Ensures filtering by neighbourhood returns only matching rows | Changing filtering logic, dataframe column names, or how empty filters are handled |
| test_filter_multiple_conditions | Unit test | Ensures multiple filters are applied simultaneously to return the correct subset | Changing filter interaction logic (e.g., union vs intersection) or altering category values |


## [0.3.0]

### Added
- Enabled the map to keep a persistent state of the selected visual layers across changes in the filters. [#97](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/97)
- Implemented hover-over tooltips to the points in the map Points layer. Displaying further details about the incident. [99](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/99)
- Added three querychat reactive UI Cards ("Reported Incidents" and "Crime Rate") in the LLM Chat tab.[#100](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/100)
- Included default context for filtering, to provide context and opinion directions for prospective users of the vancouver neighborhood safety dashboard. [#104](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/104)
- Added new tab in the dashboard with QueryChat interface [#77](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/issues/77)
- Implemented QueryChat interface and default prompts [#88](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/issues/88)
- Implemented dataframe output to show filtered QueryChat dataframe [#89](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/issues/89)
- Implemented dataframe download button to download filtered QueryChat dataframe as csv file [#90](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/issues/90)



### Changed
- Adjusted the layout of the Map and the two graphics to use a "div" section. [#97](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/97)
- Adjusted the title bar to include a more comprehensive summary of the primary purpose of the dashboard. [#98](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/98)
- Optimized all code blocks associated with filtering data, Modified the filter pane to include a multi-select option alongside a clear all filters button. [101](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/101)
- Customized the Dashboard icons and KPIS to fit the a one-screen frame. [107](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/107)


### Known Issues
- Altair has some formatting constraints with a donut chart because the labels keep mixing with the chart even when the plot size is modifies, for the time of day plot, we would recommend changing or updating this workflow in the next milestone.

### Reflection
- Using card with shiny is absolutely tricky, because when we make changes to a plot, it extends and leaves extra un-used spaces at the bottom. A remedy for the next milestone would involve researching on other methods to optimize this.


<br>


## [0.2.0]

### Added
-  Added the processed data to the project-data folder. [#54](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/54#issue-3988254014)
- Added the reactivity diagram to provide clarity on the flow of calculations and filtering.[#55](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/55)
- Added donut plot to provide answer the question "what time of the day do crimes occur across the neighbourhoods of vancouver". [#63](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/63#issue-4001534511)
- Added the source Vancouver population by neighbourhood (2016) dataset. [#57](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/57)
- Added the processed dataset merged_vancity.gpkg containing the Vancouver neighbourhood polygons data, merged with the polygon for Stanley Park. [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Added interactive Leaflet-based map visualizing Vancouver crime incidents with neighbourhood boundary overlays to support visual comparison of crime distribution across areas. (User Story #1) [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Implemented dynamic neighbourhood highlighting and auto-zoom functionality when a specific neighbourhood is selected from the filter panel. (User Story #1) [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Added heatmap layer to display spatial concentration of crime incidents across Vancouver with toggle control. (User Story #1) [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Added optional point marker layer for individual crime incidents to allow granular spatial inspection (up to 2000 points). (User Story #1) [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Implemented choropleth layer displaying crime rate per 1,000 residents by neighbourhood to enable normalized comparison across differently sized areas. (User Story #3) [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Implemented reactive filtering across map layers (neighbourhood, crime type, month, time of day) to ensure consistent cross-component interaction. (User Stories #1, #2, #4) [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Added “Top 5 Crime Types” bar chart displaying percentage share of incidents based on selected filters (excluding crime type) to provide contextual breakdown of crime composition. [#61](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/61)
- Implemented functionality for KPI metrics for crime count, crime rate, crime rate, average crime rate comparison and neighbourhood safety ranking. [#59](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/59)
- Implemented reactive calculation functionality to filter the data based on the user's selection in the dashboard. [#53](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/53)
- Included the Demo-GIF for the Vancouver Neighbourhood Safety App to provide clarity to users on APP functionality.[#72](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/72)
- Enabled the map to keep a persistent state of the selected visual layers across changes in the filters. [#97](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/97)
- Implemented hover-over tooltips to the points in the map Points layer. Displaying further details about the incident. [99](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/99)
- Added three querychat reactive UI Cards ("Reported Incidents" and "Crime Rate") in the LLM Chat tab.[#100](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/100)

### Changed
- Updated the UI and Visual perception of the Dashboard App to follow design principles [#70](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/70)
- Adjusted the layout of the Map and the two graphics to use a "div" section. [#97](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/97)

- Adjusted the title bar to include a more comprehensive summary of the primary purpose of the dashboard. [#98](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/98)


### Known Issues
- The map section is rendering in a default wide view, and is not using the entire available space. Trobleshooting is active to solve for this situation.

### Reflection
- We had a full connection across our input and outputs, so creating a sub frame (PLOTS and KPIs) in our reactivity diagram provided clarity and refinement to our diagram.


