import pygame as py
import math as m
import json
import matplotlib.pyplot as plt #pip install matplotlib
import numpy as np #pip install numpy
from scipy.stats import linregress #pip install scipy

# Initialize Pygame
py.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Data Analysis")

import os
os.chdir(r"C:\Users\timei\Downloads\VScode\GitHub\ScientificProgrammingGroupProject\TankGame\TankGame")

def dataget():

    with open(r"data.json", "r", encoding='utf-8') as file: #json data
        data = json.load(file)
    finished_games = [game for game in data["games"] if game["finished"]] #so we have only complete data
    avg_accuracies = []
    avg_attempts =[]
    game_ids = []

    for game in finished_games: #game progress

        levels = game["levels"]

        total_shots = sum(level["shots"] for level in levels)
        total_misses = sum(level["misses"] for level in levels)
        accuracy = (total_shots - total_misses) / total_shots if total_shots > 0 else 0 #shouldn't be 0 but just incase
        average_attempts = total_shots / len(levels) if len(levels) > 0 else 0

        #stores game info
        game_ids.append(game["id"])
        avg_accuracies.append(accuracy)
        avg_attempts.append(average_attempts)

    return game_ids, avg_accuracies, avg_attempts, finished_games 


def combined_stats(game_ids, avg_accuracies, finished_games):
    fig, ax = plt.subplots()
    current_index = [0]   # 0 = linreg, 1 = scatter, 2 = avg attempts
    scatter_index = [0]

    def linreg(game_ids, avg_accuracies): #linear regression of accuracy vs shots
        ax.clear() #clears plot
        Accuracy_percent = [a * 100 for a in avg_accuracies] #turning accuaracy into a percent
        ax.scatter(game_ids, Accuracy_percent, color='blue')

        slope, intercept, r_value, p_value, std_err = linregress(game_ids, avg_accuracies) #regression computation
        regression_line = [(slope * x + intercept) * 100 for x in game_ids] #regression line multiplied by 100 for accuracy stat
        slope, intercept = np.polyfit(game_ids, avg_accuracies, 1) #numpy polyfit

        ax.plot(game_ids, regression_line, color='red', label=f'Accuracy = {slope * 100:.2f} * GameID + {intercept * 100:.2f}\nR = {r_value:.2f}')

        ax.set_title("Game # vs Accuracy (%)")
        ax.set_xlabel("Game #")
        ax.set_ylabel("Accuracy (%)")
        ax.legend()
        ax.grid(True)
        fig.canvas.draw_idle()


    def scatter(): #scatter plot of how many rounds per level there were.
        ax.clear() #clears plot
        game = finished_games[scatter_index[0]] #retrieve game ids at index
        levels = game["levels"]
        level_numbers = list(range(1, len(levels) + 1)) #x axis
        rounds_per_level = [level["shots"] for level in levels] #y axis

        ax.scatter(level_numbers, rounds_per_level, color='blue', s=80) #s is size of dots
        ax.set_xlabel("Level Number")
        ax.set_ylabel("Rounds Played ")
        ax.set_title(f"Game {game['id']} — Rounds per Level ({scatter_index[0]+1}/{len(finished_games)})")
        ax.grid(True) #adds grid
        fig.canvas.draw_idle()  # Refresh the plot

    def avg_attempts_plot(finished_games):
        ax.clear()
        max_levels = max(len(game["levels"]) for game in finished_games) #find max level number
        avg_per_level = []
        for level_index in range(max_levels): #loop over levels
            attempts = []
            for game in finished_games: #getting attempt data
                if level_index < len(game["levels"]):
                    attempts.append(game["levels"][level_index]["shots"]) #only adds attempts to levels that have been reached. 

            avg_per_level.append(sum(attempts) / len(attempts)) #add average per this level

        level_numbers = list(range(1, max_levels + 1))
        ax.bar(level_numbers, avg_per_level, color='orange')
        ax.set_title("Average Attempts per Level (across all games)")
        ax.set_xlabel("Level Number")
        ax.set_ylabel("Average Attempts")
        ax.grid(True, axis='y')
        fig.canvas.draw_idle()

    plot_functions = [linreg, scatter, avg_attempts_plot]

    plot_functions = [ #function wrappers, ready to use functions
        lambda: linreg(game_ids, avg_accuracies),
        lambda: scatter(),
        lambda: avg_attempts_plot(finished_games)
]


    def on_key(event):
        if event.key == "right":
            current_index[0] = (current_index[0] + 1) % len(plot_functions) #ensures it wraps around at end
            plot_functions[current_index[0]]()
        elif event.key == "left":
            current_index[0] = (current_index[0] - 1) % len(plot_functions)
            plot_functions[current_index[0]]()
        #scatter arguments
        elif event.key == "up" and current_index[0] == 1:
            scatter_index[0] = (scatter_index[0] + 1) % len(finished_games)
            scatter()

        elif event.key == "down" and current_index[0] == 1:
            scatter_index[0] = (scatter_index[0] - 1) % len(finished_games)
            scatter()
    
    fig.canvas.mpl_connect("key_press_event", on_key) #maps key
    plot_functions[0]()
    plt.show()

game_ids, avg_accuracies, avg_attempts, finished_games = dataget()
combined_stats(game_ids, avg_accuracies, finished_games) 
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
py.quit()