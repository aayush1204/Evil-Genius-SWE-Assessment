from flask import Flask, request, jsonify
from ProcessGameState import ProcessGameState
app = Flask(__name__)

obj1 = ProcessGameState('./data/game_state_frame_data.parquet')

@app.route("/")
def home():
    return "Home"

@app.route("/Average-Timer")
def get_average_timer():
    ans = obj1.calculate_average_clock_timer()
    return "Average time is - " + str(ans)

@app.route("/Hiding-Spot-Identification")
def get_hiding_spot():

    obj1.hiding_spot_identification()
    return "Image created"

@app.route("/Common-Strategy")
def get_is_common_strategy():

    inner_lightblue_boundary = [(-1735, 250), (-2024, 398), (-2806, 742), (-2472, 1233), (-1565, 580)]

    ans = obj1.calc_common_strategy(inner_lightblue_boundary)

    return ans



if __name__ == "__main__":
    app.run(port=8000, debug=True)



