import math

class Cannonball:
    def __init__(self, levelGeometry, radius):
        self.active = False
        self.levelGeometry = levelGeometry
        self.radius = radius

    def Shoot(self, angle: float, power: float, start_x: float = 0, start_y: float = 0):
        self.theta = math.radians(angle)
        self.power = power
        self.start_x = start_x
        self.start_y = start_y
        self.time = 0
        self.active = True
        
    def GetRadius(self) -> float:
        return self.radius

    def GetActive(self) -> bool:
        return self.active

    def CalculatePointInArc(self, changedTime: float, gravity: float = 9.81) -> tuple[float, float]:
        # Calculate x and y positions
        self.time += 3*changedTime /1000
        x = self.start_x + self.power * math.cos(self.theta) * self.time
        y = self.start_y - (self.power * math.sin(self.theta) * self.time - 0.5 * gravity * self.time**2)

        return (x, y)

    def point_in_polygon(self):
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

    def circle_edge_collision(self, circle_center, circle_radius, edge_start, edge_end):
        """
        Check if a circle intersects a line segment (edge).

        Args:
            circle_center: (x, y) coordinates of the circle's center.
            circle_radius: Radius of the circle.
            edge_start: (x, y) coordinates of the edge's start point.
            edge_end: (x, y) coordinates of the edge's end point.

        Returns:
            bool: True if the circle intersects the edge, False otherwise.
        """
        # Vector from edge_start to edge_end
        edge_vector = (edge_end[0] - edge_start[0], edge_end[1] - edge_start[1])
        # Vector from edge_start to circle_center
        circle_vector = (circle_center[0] - edge_start[0], circle_center[1] - edge_start[1])

        # Length of the edge
        edge_length_squared = edge_vector[0]**2 + edge_vector[1]**2

        # Projection of circle_vector onto edge_vector
        if edge_length_squared == 0:
            # Edge is a point
            distance_squared = (circle_center[0] - edge_start[0])**2 + (circle_center[1] - edge_start[1])**2
            return distance_squared <= circle_radius**2

        projection = (circle_vector[0] * edge_vector[0] + circle_vector[1] * edge_vector[1]) / edge_length_squared

        # Closest point on the edge to the circle's center
        if projection < 0:
            closest_point = edge_start
        elif projection > 1:
            closest_point = edge_end
        else:
            closest_point = (
                edge_start[0] + projection * edge_vector[0],
                edge_start[1] + projection * edge_vector[1]
            )

        # Distance from circle's center to closest point on the edge
        distance_squared = (circle_center[0] - closest_point[0])**2 + (circle_center[1] - closest_point[1])**2

        # Check if the distance is less than or equal to the circle's radius
        return distance_squared <= circle_radius**2