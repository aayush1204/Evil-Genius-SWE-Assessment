from inspect import BoundArguments
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon
from collections import Counter
import matplotlib.pyplot as plt

class ProcessGameState:

    def __init__(self, file_path):
        self.data = self.load_data(file_path)
        self.cache = {}

    def load_data(self, file_path):
      # Perform file ingestion and ETL if necessary
        data = pd.read_parquet(file_path)
        return data

    def get_data(self):
        return self.data

    # Function to Return whether or not each row falls within a provided boundary
    def df_is_in_boundary(self,boundary_limits, df):

        quadrilateral = Polygon(boundary_limits)
        for index, row in df.iterrows():
            point_coords = (row['x'],row['y'])
            # Create a Point object from the point coordinates
            point = Point(point_coords)
            # Check if the point is inside the quadrilateral
            is_inside = quadrilateral.contains(point)
            # Print the result
            if not is_inside:
                return False
        return True
    
    # Extract the weapon classes from the inventory json column
    def extract_weapon_classes(self, row):
        return Counter([weapon_info['weapon_class'] for weapon_info in row['inventory']])
 
    ####         My helper classes 
  
    # Return is a given row is in the boundary or not
    def row_is_in_boundary(self, boundary_limits, row):
        quadrilateral = Polygon(boundary_limits)
        self.cache[(tuple(boundary_limits),row['x'],row['y'])] = quadrilateral.contains(Point((row['x'],row['y'])))
        is_inside = self.cache[(tuple(boundary_limits),row['x'],row['y'])]
        return is_inside

    # Q2b What is the average timer that Team2 on T (terrorist) side enters
    # “BombsiteB” with least 2 rifles or SMGs?
    def calculate_average_clock_timer(self):

        # This list stores all the clock timers for each round of game Team2 on T (terrorist) 
        # side enters “BombsiteB” with least 2 rifles or SMGs
        clock_time_list = []
        data = self.data

        # Group the data based on rounds
        grouped_data = data.groupby('round_num')

        for category, group in grouped_data:
            # Sort in ascending value of tick
            sorted_data_group = group.sort_values(by='tick')
            # Filter only data of the side which is Terrorist in that round
            sorted_data_group_T = sorted_data_group[sorted_data_group['side']=='T']

            # check if the Terrorist side is Team2 or not
            if sorted_data_group_T['team'].iloc[0] == 'Team1':
                continue
      
            # Create a dataframe of all players from Team2 which contains 
            # the clock timer of the first time they entered BombSiteB
            unique_players_group = sorted_data_group_T[sorted_data_group_T['area_name']=='BombsiteB'].drop_duplicates(subset='player', keep='first')
      
            # check if any player in this round entered the BombSiteB or not
            if unique_players_group.shape[0] == 0:
                continue
      
            count_rifle = 0
            count_smg = 0
      
            # For loop which finds the first timestamp when 
            # almost all players in BombSiteB have atleast 2 count_rifle or SMG
            for index, row in unique_players_group.iterrows():
                
                if count_rifle >= 2 or count_smg >= 2:
                    clock_time_list.append(row['clock_time'])
                    break

                counter = self.extract_weapon_classes(row)
                count_rifle+=counter['Rifle']
                count_smg+=counter['SMG']

        # Convert time strings to datetime objects
        time_objects = pd.to_datetime(clock_time_list, format='%M:%S')

        # Calculate average time
        average_time = pd.to_datetime(str(time_objects.mean().time()), format='%H:%M:%S.%f').strftime('%M:%S')

        # return average time
        return average_time

    # Q2c Now that we’ve gathered data on Team2 T side, let's examine their CT
    # (counter-terrorist) Side. Using the same data set, tell our coaching
    # staff where you suspect them to be waiting inside “BombsiteB”
    def hiding_spot_identification(self):
   
        ls_coordinates_with_max_waiting_time = []

        grouped_data = self.data.groupby('round_num')

        for category, group in grouped_data:
      
            # Sort in ascending value of tick and then 
            # Filter only data of the side which is Counter Terrorist in that round
            sorted_data_group = group.sort_values(by='tick')
            sorted_data_group_T = sorted_data_group[sorted_data_group['side']=='CT']

            # check if the Terrorist side is Team2 or not
            if sorted_data_group_T['team'].iloc[0] == 'Team1':
                continue
      
            # Filter out data regarding only bombsiteB
            players_group_bombsite = sorted_data_group_T[sorted_data_group_T['area_name']=='BombsiteB']

            # Group now player wise and analyse individual player movement
            new_grouped_data = players_group_bombsite.groupby('player')

            for new_cat ,new_group in new_grouped_data:

                # Group By based on the coordinates where this player visited
                for coordinates, new_group_coordinate in new_group.groupby(['x','y']):
          
                    # We can ignore the data after the player is dead
                    new_group_coordinate = new_group_coordinate[new_group_coordinate['is_alive']==True] 
          
                    if len(new_group_coordinate) > 2:
                        first_row = new_group_coordinate.iloc[0]
                        prev = first_row['seconds']
                        count_waiting = 0
                        max_waiting = 0

                        # For loop to find the maximum 
                        # time the player was waiting at a location in this round
                        for index, row in new_group_coordinate.iterrows():

                            if prev == row['seconds']:
                                continue
                            if prev == row['seconds']-1:
                                prev = row['seconds']
                                count_waiting +=1
                            elif row['seconds'] == 0 and row['bomb_planted'] == True:
                                count_waiting +=1
                                prev = 0
                            else:
                                max_waiting = max(max_waiting, count_waiting)
                                count_waiting = 0

                        max_waiting = max(max_waiting, count_waiting)
          
                        if max_waiting > 1:
                            ls_coordinates_with_max_waiting_time.append([coordinates[0],coordinates[1],max_waiting])
                            continue

          
        df_set = pd.DataFrame(ls_coordinates_with_max_waiting_time, columns=['x', 'y','waiting'])
        self.create_plot(df_set)

    # Function to generate a Heatmap
    def create_plot(self,df):

        plt.hist2d(df['x'], df['y'], bins=20, cmap='hot', weights=df['waiting'])
        # Add colorbar for reference
        plt.colorbar()
        #   Set plot labels and title
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('HeatMap showing the locations in BombsiteB where players might be hiding')
        plt.savefig('images/hiding_spot.png')
        plt.close()

    # Q2a Is entering via the light blue boundary a common strategy used by
    # Team2 on T (terrorist) side?
    def calc_common_strategy(self, inner_lightblue_boundary, exit_edge):

        # inner_lightblue_boundary = [(-1735, 250), (-2024, 398), (-2806, 742), (-2472, 1233), (-1565, 580)]
        # create a new boundary with an offset of 30 just near exit
        outer_lightblue_boundary = inner_lightblue_boundary
        new_points = self.find_outer_boundary_coordinates(exit_edge)

        # If any of the new points already are inside the boundary, ignore them
        for i in new_points:
            x_point, y_point = i
            if self.row_is_in_boundary(inner_lightblue_boundary,{'x':x_point,'y':y_point}):
                outer_lightblue_boundary.append((x_point,y_point))

        print(outer_lightblue_boundary)

        x_coordinates, y_coordinates = zip(*outer_lightblue_boundary)

        # Find the maximum and minimum x and y coordinates
        max_x = max(x_coordinates)
        min_x = min(x_coordinates)
        max_y = max(y_coordinates)
        min_y = min(y_coordinates)
        
        data = self.data
        grouped_data = data.groupby('round_num')
        outcomes_list = []

        for category, group in grouped_data:

            # Sort in ascending value of tick and then 
            # Filter only data of the side which is Terrorist in that round
            count_people_following_strategy = 0
            sorted_data_group = group.sort_values(by='tick')
            sorted_data_group_T = sorted_data_group[sorted_data_group['side']=='T']

            # check if the Terrorist side is Team2 or not
            if sorted_data_group_T['team'].iloc[0] == 'Team1':
                continue

            ### Filtering out data about locations away from our boundary since they are of no use to us
            sorted_data_group_T = sorted_data_group_T[sorted_data_group_T['x'] >= min_x]
            sorted_data_group_T = sorted_data_group_T[sorted_data_group_T['x'] <= max_x]
            sorted_data_group_T = sorted_data_group_T[sorted_data_group_T['y'] >= min_y]
            sorted_data_group_T = sorted_data_group_T[sorted_data_group_T['y'] <= max_y]
            
            group_players = sorted_data_group_T.groupby('player')
            # Analysing data player wise
            for category_playername, group_player in group_players:
                sorted_data_player_group = group_player.sort_values(by='tick')

                prev_inner = False
                prev_outer = False
                
                if count_people_following_strategy > 1:
                    break

                # Main logic to find out if the player followed this strategy
                for index, row in sorted_data_player_group.iterrows():    
          
                    if (tuple(inner_lightblue_boundary),row['x'],row['y']) in self.cache:
                        curr_inner = self.cache[(tuple(inner_lightblue_boundary),row['x'],row['y'])]
                    else:  
                        curr_inner = self.row_is_in_boundary(inner_lightblue_boundary,row)
          
                    if (tuple(outer_lightblue_boundary),row['x'],row['y']) in self.cache:
                        curr_outer = self.cache[(tuple(outer_lightblue_boundary),row['x'],row['y'])]
                    else:
                        curr_outer = self.row_is_in_boundary(outer_lightblue_boundary,row)
           
                    if prev_inner == False and prev_outer == False and curr_inner == True and curr_outer == True:
                        count_people_following_strategy+=1
                        break
                    if prev_inner == False and prev_outer == False and curr_inner == False and curr_outer == True:
                        break

                    prev_inner = curr_inner
                    prev_outer = curr_outer
            # According to me, if atleast 1 person follows this 
            # strategy in this round, I would consider this round.
            if count_people_following_strategy > 0:
                outcomes_list.append(1)
            else:
                outcomes_list.append(0)

        # Constant of checking - 0.5
        percent_of_attempts = sum(outcomes_list)/len(outcomes_list)

        if percent_of_attempts < 0.5:
            return str("No, it is not a common stratergy as only " + str(percent_of_attempts*100) + "% times it is attempted, which is less than our threshold of 50% times")
        else:
            return str("It is a common strategy since " + str(percent_of_attempts*100) + "% times the team attempted to enter from the tunnel")

    # Helper function to calculate the outer Boundary which will be used to solve Q2a later
    def find_outer_boundary_coordinates(self,exit_edge):
    # Extract coordinates from the input points
        x1, y1 = exit_edge[0]
        x2, y2 = exit_edge[1]

        # Calculate the slope of the given line
        original_slope = (y2 - y1) / (x2 - x1)

        # Calculate the slope of the perpendicular line
        perpendicular_slope = -1 / original_slope

        ans = []
        x = x1
        y = y1

        # Calculate the y-intercept of the perpendicular line
        y_intercept = y - perpendicular_slope * x

        # Finding Offset at 30 distance from both points
        ans.append((x + 30, perpendicular_slope * (x+30) + y_intercept))
        ans.append((x - 30, perpendicular_slope * (x-30) + y_intercept))

        x = x2
        y = y2

        # Calculate the y-intercept of the perpendicular line
        y_intercept = y - perpendicular_slope * x

        # Finding Offset at 30 distance from both points
        ans.append((x + 30, perpendicular_slope * (x+30) + y_intercept))
        ans.append((x - 30, perpendicular_slope * (x-30) + y_intercept))

        return ans



