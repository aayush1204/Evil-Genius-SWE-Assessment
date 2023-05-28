# Evil-Genius-SWE-Assessment

## Documentation Report: ProcessGameState Class Methods

This documentation provides a detailed description of the methods available in the `ProcessGameState` class.

### 1: load_data(file_path)

This method loads the game state data from a given file path, performs file ingestion and Extract-Transform-Load (ETL) operations if necessary, and returns the processed data as a Pandas DataFrame.

### 2: get_data()

This method returns the loaded game state data as a Pandas DataFrame.

### 3: df_is_in_boundary(boundary_limits, df)

This method checks whether each row in a given DataFrame falls within a provided boundary defined by a quadrilateral shape. It takes the boundary limits as a list of coordinate points and the DataFrame to be checked. It iterates over the DataFrame rows, creates a Point object for each row's coordinates, and checks if the point is inside the quadrilateral using the Shapely library. It returns a boolean indicating whether all rows fall within the boundary or not.

### 4: extract_weapon_classes(row)

This method extracts the weapon classes from the inventory JSON column of a given row. It assumes the inventory column contains a list of dictionaries, each representing a weapon with a "weapon_class" key. It uses a Counter object to count the occurrences of each weapon class and returns the result as a Counter object.

### 5: row_is_in_boundary(boundary_limits, row)

This is a helper method used internally to determine whether a specific row falls within a provided boundary. It takes the boundary limits as a list of coordinate points and the row containing the coordinates to be checked. It uses a cache dictionary to store the results for efficient lookup and returns a boolean indicating whether the row falls within the boundary or not.

###  6: calculate_average_clock_timer()

This method calculates the average clock timer for rounds where Team2 on the T (terrorist) side enters "BombsiteB" with at least 2 rifles or SMGs. It iterates over the game state data, grouping it by rounds and filtering for the T side. For each round, it finds the first time each player from Team2 entered "BombsiteB" and counts the number of rifles and SMGs they had in their inventory. If at least two of these weapons are found, the clock timer for that entry is added to a list. Finally, it calculates the average time from the list of clock timers and returns it as a formatted string.

### 7: hiding_spot_identification()

This method identifies potential hiding spots for Team2 on the CT (counter-terrorist) side inside "BombsiteB". It analyzes the game state data by grouping it by rounds, filtering for the CT side, and further filtering for the "BombsiteB" area. It then groups the data by player and analyzes their movement within "BombsiteB" to identify potential hiding spots. It calculates the maximum time a player stayed at a location without moving and stores the coordinates and the corresponding waiting time in a DataFrame. Finally, it generates a heatmap plot using matplotlib to visualize the potential hiding spots.

### 8: create_plot(df)

This method generates a heatmap plot based on the provided DataFrame. It uses the seaborn library to create the heatmap plot with the waiting times at different locations.

### 9: calc_common_strategy(inner_lightblue_boundary, exit_edge)

This method determines whether entering via the light blue boundary is a common strategy used by Team2 on the T side. It calculates the percentage of rounds in which Team2 enters "BombsiteB" by crossing the light blue boundary and returns a formatted string indicating whether it is a common strategy or not. It uses the row_is_in_boundary() helper method to check if each entry falls within the boundary.

### 10: find_perpendicular_line(exit_edge)

This is a helper method used by calc_common_strategy() to calculate the outer boundary of the light blue boundary. It takes the start and end points of the boundary and the desired distance for the perpendicular line. It calculates the slope of the line, finds the midpoint, calculates the slope perpendicular to the original line, and calculates the coordinates for the perpendicular line at the specified distance from the midpoint.

---

This documentation report provides an overview of the methods available in the `ProcessGameState` class. The accurate implementation and usage of these methods will depend on the specific requirements and the quality of the underlying game state data.

