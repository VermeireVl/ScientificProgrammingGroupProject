import pygame as py
import math as m
import json
#pip install matplotlib
import matplotlib.pyplot as plt
#pip install numpy
import numpy as np
from scipy.stats import linregress
from datetime import datetime

class DataAnalysis:
    class Level:
        def __init__(self, levelId):
            self.levelId = levelId
            self.shots = 0
            self.misses = 0
            self.startTime = datetime.now()
            self.match_time = 0
    def __init__(self, width, height):
        self.currentLevels = []

    def StartNewLevel(self):
        self.currentLevels.append(self.Level(len(self.currentLevels)))

    def AddShot(self):
        self.currentLevels[len(self.currentLevels) - 1].shots += 1
        self.currentLevels[len(self.currentLevels) - 1].misses += 1

    def AddHit(self):
        self.currentLevels[len(self.currentLevels) - 1].misses -= 1

    def EndLevel(self):
        self.currentLevels[len(self.currentLevels) - 1].endTime = datetime.now()

    def EndGame(self):
        if len(self.currentLevels) > 1:
            self.finished_games[len(self.finished_games) - 1]['id']
            entries = []
            for index in range(len(self.currentLevels) -1 ):
                entries.append({"level": self.currentLevels[index].levelId, "shots": self.currentLevels[index].shots, "misses": self.currentLevels[index].misses, "match_time": (self.currentLevels[index].endTime - self.currentLevels[index].startTime).seconds})
            newGame = {
                "id": self.finished_games[len(self.finished_games) - 1]['id'] + 1,
                "finished": True,
                "levels":entries
                }
            with open(r"data.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                data["games"].append(newGame)
            with open(r"data.json", "w") as file:
                json.dump(data, file, indent=4)

    def dataget(self): 
        self.game_ids = []
        self.avg_accuracies = []

        with open(r"data.json", "r", encoding='utf-8') as file:
            data = json.load(file)
        self.finished_games = [game for game in data["games"] if game["finished"]] #so we have complete data

        for game in self.finished_games:
            levels = game["levels"]

            total_shots = sum(level["shots"] for level in levels)
            total_misses = sum(level["misses"] for level in levels)
            self.accuracy = (total_shots - total_misses) / total_shots if total_shots > 0 else 0 #shouldn't be 0 but just incase

            self.game_ids.append(game["id"])
            self.avg_accuracies.append(self.accuracy)

    def linreg(self, fig, ax): #linear regression of accuracy vs shots
        ax.clear() #clears plot
        Accuracy_percent = [a * 100 for a in self.avg_accuracies] #turning accuaracy into a percent
        ax.scatter(self.game_ids, Accuracy_percent, color='blue')

        slope, intercept, r_value, p_value, std_err = linregress(self.game_ids, self.avg_accuracies) #regression computation
        regression_line = [(slope * x + intercept) * 100 for x in self.game_ids] #regression line multiplied by 100 for accuracy stat
        slope, intercept = np.polyfit(self.game_ids, self.avg_accuracies, 1) #numpy polyfit

        ax.plot(self.game_ids, regression_line, color='red', label=f'Accuracy = {slope * 100:.2f} * GameID + {intercept * 100:.2f}\nR = {r_value:.2f}')

        ax.set_title("Game # vs Accuracy (%)")
        ax.set_xlabel("Game #")
        ax.set_ylabel("Accuracy (%)")
        ax.legend()
        ax.grid(True)
        fig.canvas.draw_idle()
    
    def scatter(self, fig, ax, scatter_index): #scatter plot of how many rounds per level there were.
        ax.clear() #clears plot
        game = self.finished_games[scatter_index[0]] #retrieve game ids at index
        levels = game["levels"]
        level_numbers = list(range(1, len(levels) + 1)) #x axis
        rounds_per_level = [level["shots"] for level in levels] #y axis

        ax.scatter(level_numbers, rounds_per_level, color='blue', s=80) #s is size of dots
        ax.set_xlabel("Level Number")
        ax.set_ylabel("Rounds Played ")
        ax.set_title(f"Game {game['id']} — Rounds per Level ({scatter_index[0]+1}/{len(self.finished_games)})")
        ax.grid(True) #adds grid
        fig.canvas.draw_idle()  # Refresh the plot

    def avg_attempts_plot(self, fig, ax):
        ax.clear()
        max_levels = max(len(game["levels"]) for game in self.finished_games) #find max level number
        avg_per_level = []
        for level_index in range(max_levels): #loop over levels
            attempts = []
            for game in self.finished_games: #getting attempt data
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

    def combined_stats(self):
        fig, ax = plt.subplots()
        current_index = [0]   # 0 = linreg, 1 = scatter, 2 = avg attempts
        scatter_index = [0]

        plot_functions = [self.linreg, self.scatter, self.avg_attempts_plot]

        plot_functions = [ #function wrappers, ready to use functions
            lambda: self.linreg(fig,ax),
            lambda: self.scatter(fig, ax, scatter_index),
            lambda: self.avg_attempts_plot(fig, ax)
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
                scatter_index[0] = (scatter_index[0] + 1) % len(self.finished_games)
                self.scatter(fig, ax, scatter_index)

            elif event.key == "down" and current_index[0] == 1:
                scatter_index[0] = (scatter_index[0] - 1) % len(self.finished_games)
                self.scatter(fig, ax, scatter_index)
    
        fig.canvas.mpl_connect("key_press_event", on_key) #maps key
        plot_functions[0]()
        plt.show()