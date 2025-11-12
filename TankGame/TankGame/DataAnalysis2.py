import pygame as py
import math as m
import json
#pip install matplotlib
import matplotlib.pyplot as plt
#pip install numpy
import numpy as np
#pip install scipy
from scipy.stats import linregress

# Initialize Pygame
py.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Data Analysis")

import os
os.chdir(r"C:\Users\timei\Downloads\VScode\GitHub\ScientificProgrammingGroupProject\TankGame\TankGame")

def dataget():

    with open(r"data.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    finished_games = [game for game in data["games"] if game["finished"]] #so we have complete data
    avg_accuracies = []
    avg_attempts =[]
    game_ids = []

    for game in finished_games:

        levels = game["levels"]

        total_shots = sum(level["shots"] for level in levels)
        total_misses = sum(level["misses"] for level in levels)
        accuracy = (total_shots - total_misses) / total_shots if total_shots > 0 else 0 #shouldn't be 0 but just incase
        average_attempts = total_shots / len(levels) if len(levels) > 0 else 0

        game_ids.append(game["id"])
        avg_accuracies.append(accuracy)
        avg_attempts.append(average_attempts)

    return game_ids, avg_accuracies, avg_attempts, finished_games 

def linreg(game_ids, avg_accuracies): #linear regression of accuracy vs shots
    Accuracy_percent = [a * 100 for a in avg_accuracies]
    plt.scatter(game_ids, Accuracy_percent, color='blue')

    slope, intercept, r_value, p_value, std_err = linregress(game_ids, avg_accuracies)
    regression_line = [(slope * x + intercept) * 100 for x in game_ids]
    slope, intercept = np.polyfit(game_ids, avg_accuracies, 1)

    plt.plot(game_ids, regression_line, color='red', label=f'Accuracy = {slope * 100:.2f} * GameID + {intercept * 100:.2f}\nR = {r_value:.2f}')

    plt.title("Game # vs Accuracy (%)")
    plt.xlabel("Game #")
    plt.ylabel("Accuracy (%)")
    plt.legend()
    plt.grid(True)
    plt.show()


def scatter(finished_games): #scatter plot of how many rounds per level there were. use different colors per game id
    fig, ax = plt.subplots() #creates figure and axis
    current_index = [0] #game were currently looking at

    def plot_game(index):
        ax.clear() #clears plot
        game = finished_games[index]
        levels = game["levels"]
        level_numbers = list(range(1, len(levels) + 1))
        rounds_per_level = [level["shots"] for level in levels]

        ax.scatter(level_numbers, rounds_per_level, color='blue', s=80) #s is size of dots
        ax.set_xlabel("Level Number")
        ax.set_ylabel("Rounds Played ")
        ax.set_title(f"Game {game['id']} — Rounds per Level ({index + 1}/{len(finished_games)})")
        ax.grid(True)
        fig.canvas.draw_idle()  # Refresh the plot
    
    def on_key(event):
        if event.key == "right":
            current_index[0] = (current_index[0] + 1) % len(finished_games) #ensures it wraps around at end
            plot_game(current_index[0])
        elif event.key == "left":
            current_index[0] = (current_index[0] - 1) % len(finished_games)
            plot_game(current_index[0])
    
    fig.canvas.mpl_connect("key_press_event", on_key) #maps key
    plot_game(current_index[0]) #starts at first plot
    plt.show()

def avg_attempts_plot(finished_games):
    max_levels = max(len(game["levels"]) for game in finished_games) #find max level number

    avg_per_level = []
    for level_index in range(max_levels):
        attempts = []
        for game in finished_games:
            if level_index < len(game["levels"]):
                attempts.append(game["levels"][level_index]["shots"])

        avg_per_level.append(sum(attempts) / len(attempts)) #add average per this level

    level_numbers = list(range(1, max_levels + 1))
    plt.bar(level_numbers, avg_per_level, color='orange')
    plt.title("Average Attempts per Level (across all games)")
    plt.xlabel("Level Number")
    plt.ylabel("Average Attempts")
    plt.grid(True, axis='y')
    plt.show()


game_ids, avg_accuracies, avg_attempts, finished_games = dataget()
linreg(game_ids, avg_accuracies)
scatter(finished_games)
avg_attempts_plot(finished_games)

running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
py.quit()