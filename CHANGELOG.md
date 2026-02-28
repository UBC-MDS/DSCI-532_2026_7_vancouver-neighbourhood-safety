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

### Changed
- Updated the UI and Visual perception of the Dashboard App to follow design principles [#70](https://github.com/UBC-MDS/DSCI-532_2026_7_vancouver-neighbourhood-safety/pull/70)


### Known Issues
- The map section is rendering in a default wide view, and is not using the entire available space. Trobleshooting is active to solve for this situation.

### Reflection
- We had a full connection across our input and outputs, so creating a sub frame (PLOTS and KPIs) in our reactivity diagram provided clarity and refinement to our diagram.
