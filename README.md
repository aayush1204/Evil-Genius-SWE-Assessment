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


### 1) Using REST API endpoints

This project provides a REST API for displaying a Matplotlib plot based on the game state data. It includes several endpoints to perform different operations and retrieve specific information from the game state.

Follow these steps:

1. Install the project dependencies by running the following command:

    ```terminal
    pip install -r requirements.txt
    ```

2. Start the server by running the following command:

    ```terminal
    python3 main.py
    ```

3. Access the API endpoints using a web browser or API testing tool.

#### Endpoints

- `/`: Home endpoint that displays a short description of all the available endpoints and how to access them.
- `/Average-Timer`: Endpoint that calculates and returns the average clock timer for rounds where specific conditions are met.
- `/Hiding-Spot-Identification`: Endpoint that generates an image showcasing potential hiding spots based on game state data.
- `/Common-Strategy`: Endpoint that determines if a specific strategy is commonly used by analyzing the game state data.

#### Example Usage

1. To calculate the average clock timer:
- Send a GET request to the `/Average-Timer` endpoint.
- The response will contain the average time calculated.

2. To generate a hiding spot identification image:
- Send a GET request to the `/Hiding-Spot-Identification` endpoint.
- The response will indicate that the image has been created.

3. To check if a common strategy is used:
- Send a GET request to the `/Common-Strategy` endpoint.
- The response will indicate whether the strategy is common or not.


### 2) Using the ProcessGameState Class

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


