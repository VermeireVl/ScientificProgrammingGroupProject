import pygame as py
import math as m
import json
#pip install matplotlib
import matplotlib.pyplot as plt
#pip install numpy
import numpy as np
#pip install scipy
from scipy.stats import linregress
from datetime import datetime

#import os
#os.chdir(r"C:\Users\timei\Downloads\VScode\GitHub\ScientificProgrammingGroupProject\TankGame\TankGame")
class DataAnalysis:
    def __init__(self, width, height):
        self.currentLevels = []
        #self.dpi = plt.gcf().get_dpi()
        #self.width_inches = width / self.dpi
        #self.height_inches = height / self.dpi
        #plt.figure(figsize=(self.width_inches, self.height_inches), dpi=self.dpi)

    class Level:
        def __init__(self, levelId):
            self.levelId = levelId
            self.shots = 0
            self.misses = 0
            self.startTime = datetime.now()
            self.match_time = 0


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


    def linreg(self): #linear regression of accuracy vs shots
        Accuracy_percent = [a * 100 for a in self.avg_accuracies]
        #plt.figure(figsize=(self.width_inches, self.height_inches), dpi=self.dpi)
        plt.scatter(self.game_ids, Accuracy_percent, color='blue')

        slope, intercept, r_value, p_value, std_err = linregress(self.game_ids, self.avg_accuracies)
        regression_line = [(slope * x + intercept) * 100 for x in self.game_ids]
        slope, intercept = np.polyfit(self.game_ids, self.avg_accuracies, 1)

        plt.plot(self.game_ids, regression_line, color='red', label=f'Accuracy = {slope * 100:.2f} * GameID + {intercept * 100:.2f}\nR = {r_value:.2f}')

        plt.title("Game # vs Accuracy (%)")
        plt.xlabel("Game #")
        plt.ylabel("Accuracy (%)")
        plt.legend()
        plt.grid(True)
        plt.show()


    def scatter(self): #scatter plot of how many rounds per level there were. use different colors per game id
        #plt.figure(figsize=(self.width_inches, self.height_inches), dpi=self.dpi)
        color_cycle = plt.cm.get_cmap('tab10') #gets switching colors
        n_games = len(self.finished_games)
        for i, game in enumerate(self.finished_games):
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