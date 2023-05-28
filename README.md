# Evil-Genius-SWE-Assessment

## Dependencies

The ProcessGameState class requires the following dependencies:

- numpy: A library for efficient numerical operations in Python.
- pandas: A library for data manipulation and analysis.
- shapely.geometry: A library for geometric operations and calculations.
- collections.Counter: A class that provides a simple way to count elements in a list or other iterable.
- matplotlib.pyplot: A library for creating data visualizations in Python.

Make sure to install these dependencies before using the ProcessGameState class.

## Usage

To use the ProcessGameState class, follow these steps:

1. Instantiate an object of the class, providing the file path to the game data as an argument.

    ```python
    game_state = ProcessGameState(file_path)
    ```

2. Call the desired methods of the class to perform specific calculations and analyses on the game data.

    ```python
    data = game_state.load_data()
    average_timer = game_state.calculate_average_clock_timer()
    hiding_spots = game_state.hiding_spot_identification()
    common_strategy = game_state.calc_common_strategy()
    ```


