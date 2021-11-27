from traffic_model import *

CARS = 1
COLS = 26
ROWS = 26
MAX_STEPS = 1000

model = TrafficModel(MAX_STEPS)

if __name__ == '__main__':
    for i in range(10):
        print(f"Step {i}")
        model.step()