import math

# Values
delta_y = 597.60 - 541  # Vertical distance
delta_x = 4  # Horizontal distance in minutes

# Slope
slope = delta_y / delta_x

# Calculate angle in degrees
angle_degrees = math.atan(slope) * (180 / math.pi)

print(f"The angle of price movement is approximately {angle_degrees:.2f} degrees.")
