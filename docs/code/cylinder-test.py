from build123d import *
import math

# 1. Define Cylinder dimensions
cyl_radius = 50
cyl_height = 100
dome_radius = 4

# 2. Define your "2D Plane Grid" parameters
# Columns wrap around the circumference, Rows go up the height
num_columns = 12  # Number of domes around the cylinder
num_rows = 8      # Number of domes along the length

with BuildPart() as final_model:
    # Create the base cylinder
    Cylinder(radius=cyl_radius, height=cyl_height)

    # Calculate spacing
    angle_step = 360 / num_columns
    height_step = cyl_height / (num_rows + 1)

    # Loop through your 2D grid array mapping onto the cylinder
    for row in range(num_rows):
        # Calculate Z position (centered vertically)
        z_pos = -cyl_height / 2 + (row + 1) * height_step

        for col in range(num_columns):
            angle = col * angle_step

            # Position the dome precisely at the outer radius
            # Rotate around Z, then move outward along X
            dome_loc = Rotation(0, 0, angle) * Pos(cyl_radius, 0, z_pos)

            # Place the dome (Sphere) onto the location
            # Note: The sphere will inherently intersect halfway, creating a perfect dome
            with Locations(dome_loc):
                Sphere(radius=dome_radius)
