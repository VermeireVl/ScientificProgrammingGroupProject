import math

class Cannonball:
    def __init__(self):
        self.active = False

    def Shoot(self, angle: float, power: float, start_x: float = 0, start_y: float = 0):
        self.theta = math.radians(angle)
        self.power = power
        self.start_x = start_x
        self.start_y = start_y
        self.time = 0
        self.active = True

    def GetActive(self) -> bool:
        return self.active

    def CalculatePointInArc(self, time: float, gravity: float = 9.81) -> tuple[float, float]:
        # Calculate x and y positions
        self.time += time /1000
        x = self.start_x + self.power * math.cos(self.theta) * time
        y = -(self.start_y - self.power * math.sin(self.theta) * time - 0.5 * gravity * time**2)

        return (x, y)
