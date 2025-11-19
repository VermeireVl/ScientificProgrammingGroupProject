from logging import _levelToName
import math

class Cannonball:
    def __init__(self, levelGeometry, radius, screen, tankList):
        self.active = False
        self.levelGeometry = levelGeometry
        self.radius = radius
        self.screen = screen
        self.currentIndex = 0
        self.tankList = tankList
        self.start_x = self.tankList[self.currentIndex].x
        self.start_y = self.tankList[self.currentIndex].y

    def Shoot(self, angle: float, power: float, start_x: float = 0, start_y: float = 0):
        self.theta = math.radians(angle)
        self.power = power
        self.start_x = self.tankList[self.currentIndex].x
        self.start_y = self.tankList[self.currentIndex].y
        self.center = (self.start_x, self.start_y)
        self.time = 0
        self.active = True
        
    def GetRadius(self) -> float:
        return self.radius

    def GetActive(self) -> bool:
        return self.active

    def quadratic_bezier(self, p0, p1, p2, steps=10):
        self.points = []
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
            self.points.append((int(x), int(y)))
        return self.points

    def UpdateStart(self):
        self.start_x = self.tankList[self.currentIndex].x
        self.start_y = self.tankList[self.currentIndex].y

    def GetPointInArc(self, time: float, gravity: float = 9.81) -> list:
        time = 3 * (time /1000)
        x = self.start_x + self.power * math.cos(self.theta) * time
        y = self.start_y - (self.power * math.sin(self.theta) * time - 0.5 * gravity * time**2)
        return [x,y]

    def SetPower(self, power: float):
        if not self.active:
            self.power = power

    def SetAngle(self, angle: float):
        if not self.active:
            self.theta = math.radians(angle)

    def UpdatePointInArc(self, changedTime: float, gravity: float = 9.81) -> bool:
        # Calculate x and y positions
        self.time += 3*changedTime /1000
        x = self.start_x + self.power * math.cos(self.theta) * self.time
        y = self.start_y - (self.power * math.sin(self.theta) * self.time - 0.5 * gravity * self.time**2)
        self.center = (x, y)

        for index in range(len(self.tankList)):
            if index == self.currentIndex:
                continue
            else:
                tankPoints = [[self.tankList[index].x, self.tankList[index].y], [self.tankList[index].x + self.tankList[index].width, self.tankList[index].y],
                              [self.tankList[index].x + self.tankList[index].width, self.tankList[index].y + self.tankList[index].height],
                              [self.tankList[index].x, self.tankList[index].y + self.tankList[index].height]]
                if self.CircleEdgeCollision(tankPoints):
                    self.active = False
                    self.currentIndex += 1
                    print("hit index: " + str(index))
                    if self.currentIndex >= len(self.tankList):
                        self.currentIndex = 0
                    self.UpdateStart()
                    return True

        if self.PointInPolygon() or self.CircleEdgeCollision(self.levelGeometry) or self.InScreen():
            self.active = False
            self.currentIndex += 1
            if self.currentIndex >= len(self.tankList):
                self.currentIndex = 0
            self.UpdateStart()
            return False

        
        return False

    def GetCurrentPosition(self) -> tuple[float, float]:
        return self.center

    def PointInPolygon(self) -> bool:
        n = len(self.levelGeometry)
        inside = False
        for i in range(n):
            x1, y1 = self.levelGeometry[i]
            x2, y2 = self.levelGeometry[(i + 1) % n]
            if self.start_y > min(y1, y2):
                if self.start_y <= max(y1, y2):
                    if self.start_x <= max(x1, x2):
                        if y1 != y2:
                            x_intersect = (self.start_y - y1) * (x2 - x1) / (y2 - y1) + x1
                        if x1 == x2 or self.start_x <= x_intersect:
                            inside = not inside
        return inside

    def CircleEdgeCollision(self, collisionPoints) -> bool:
        collision = False
        
        for index in range(len(collisionPoints)):
            stopIndex = index + 1   
            if index == len(collisionPoints) - 1:
                stopIndex = 0
            # Vector from edge_start to edge_end
            edge_vector = (collisionPoints[stopIndex][0] - collisionPoints[index][0], collisionPoints[stopIndex][1] - collisionPoints[index][1])
            # Vector from edge_start to circle_center
            circle_vector = (self.center[0] - collisionPoints[index][0], self.center[1] - collisionPoints[index][1])

            # Length of the edge
            edge_length_squared = edge_vector[0]**2 + edge_vector[1]**2

            # Projection of circle_vector onto edge_vector
            if edge_length_squared == 0:
                # Edge is a point
                distance_squared = (self.center[0] - collisionPoints[index][0])**2 + (self.center[1] - collisionPoints[index][1])**2
                return distance_squared <= self.radius**2

            projection = (circle_vector[0] * edge_vector[0] + circle_vector[1] * edge_vector[1]) / edge_length_squared

            # Closest point on the edge to the circle's center
            if projection < 0:
                closest_point = collisionPoints[index]
            elif projection > 1:
                closest_point = collisionPoints[stopIndex]
            else:
                closest_point = (
                    collisionPoints[index][0] + projection * edge_vector[0],
                    collisionPoints[index][1] + projection * edge_vector[1]
                )

            # Distance from circle's center to closest point on the edge
            distance_squared = (self.center[0] - closest_point[0])**2 + (self.center[1] - closest_point[1])**2
            if distance_squared <= self.radius**2:
                collision = True
                break
            # Check if the distance is less than or equal to the circle's radius
        return collision

    def InScreen(self) -> bool:
        if self.center[0] < 0 or self.center[0] > self.screen[0] or self.center[1] < 0 or self.center[1] > self.screen[1]:
            return True
        return False