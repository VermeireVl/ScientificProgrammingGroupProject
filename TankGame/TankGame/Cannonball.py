import math

def calculatePointInArc(angle: float, power: float, time: float, 
                        start_x: float = 0, start_y: float = 0, gravity: float = 9.81) -> tuple[float, float]:
    theta = math.radians(angle)

    # Calculate x and y positions
    x = start_x + power * math.cos(theta) * time
    y = start_y - power * math.sin(theta) * time - 0.5 * gravity * time**2

    return (x, y)
