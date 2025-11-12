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
    game_ids = []
    avg_accuracies = []

    with open(r"data.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    finished_games = [game for game in data["games"] if game["finished"]] #so we have complete data

    for game in finished_games:
        levels = game["levels"]

        total_shots = sum(level["shots"] for level in levels)
        total_misses = sum(level["misses"] for level in levels)
        accuracy = (total_shots - total_misses) / total_shots if total_shots > 0 else 0 #shouldn't be 0 but just incase

        game_ids.append(game["id"])
        avg_accuracies.append(accuracy)

    return game_ids, avg_accuracies, finished_games


dataget()

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
    color_cycle = plt.cm.get_cmap('tab10') #gets switching colors
    n_games = len(finished_games)
    for i, game in enumerate(finished_games):
        levels = game["levels"]
        level_numbers = list(range(1, len(levels) + 1))
        rounds_per_level = [level["shots"] for level in levels]

        color = color_cycle(i % n_games) #colors
        plt.scatter(level_numbers, rounds_per_level, color=color, s=80),# label=f'Game {game["id"]}')


    plt.xlabel("Level Number")
    plt.ylabel("Rounds Played (Shots)")
    plt.title("Rounds per Level for Each Game ID")
    #plt.xticks(range(1, max(len(game["levels"]) for game in finished_games) + 1))
    plt.legend()
    plt.grid(True)
    plt.show()

game_ids, avg_accuracies, finished_games = dataget()
linreg(game_ids, avg_accuracies)
scatter(finished_games)

for event in py.event.get():
    if event.type == py.QUIT:
        running = False