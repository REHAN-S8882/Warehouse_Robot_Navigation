import cv2
import numpy as np
import random

# Create a blank warehouse floor (500x500 pixels)
warehouse = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Randomly generate obstacles (rectangles)
for _ in range(10):
    x1, y1 = random.randint(20, 400), random.randint(20, 400)
    x2, y2 = x1 + random.randint(30, 80), y1 + random.randint(30, 80)
    cv2.rectangle(warehouse, (x1, y1), (x2, y2), (0, 0, 255), -1)

# Convert to grayscale
gray = cv2.cvtColor(warehouse, cv2.COLOR_BGR2GRAY)

# Detect edges (simulate obstacle detection)
edges = cv2.Canny(gray, 50, 150)

# Find contours (outlines of obstacles)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(warehouse, contours, -1, (0, 255, 0), 2)

# Display result
cv2.imshow("Warehouse Simulation - Obstacle Detection", warehouse)
cv2.waitKey(0)
cv2.destroyAllWindows()
