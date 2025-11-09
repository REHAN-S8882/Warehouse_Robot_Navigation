import cv2
import numpy as np
import random
import math

W, H = 700, 500
ROBOT_R = 10          # robot radius (pixels)
SPEED = 2.5           # pixels per frame
FOV = math.radians(90)   # field of view to scan for free direction
RAY_DIST = 30            # how far ahead to check for collision (pixels)

# --- Build warehouse with random rectangular obstacles ---
canvas = np.ones((H, W, 3), dtype=np.uint8) * 255
rng = random.Random(42)
for _ in range(12):
    x1, y1 = rng.randint(30, W-160), rng.randint(30, H-120)
    x2, y2 = x1 + rng.randint(40, 120), y1 + rng.randint(40, 120)
    cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 0, 255), -1)

# Edges/contours for “vision”
gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
obstacle_mask = (edges > 0).astype(np.uint8)  # 1 where edge exists

# --- Robot state ---
pos = np.array([60.0, 60.0])                       # x, y
heading = math.radians(0)                          # facing angle
trail = []                                          # breadcrumb path

def in_bounds(p):
    x, y = int(p[0]), int(p[1])
    return 0 <= x < W and 0 <= y < H

def collides_at(p):
    """Check collision by sampling a small disk around p against obstacles or walls."""
    x, y = int(p[0]), int(p[1])
    if not in_bounds((x, y)): 
        return True
    # quick wall check by dilating edges to approximate obstacle thickness + robot radius
    return inflated_mask[y, x] > 0

def look_ahead_direction(angle):
    """Returns True if the robot has free space RAY_DIST ahead along 'angle'."""
    step = 2
    for d in range(ROBOT_R, RAY_DIST, step):
        lx = int(pos[0] + math.cos(angle) * d)
        ly = int(pos[1] + math.sin(angle) * d)
        if not in_bounds((lx, ly)) or inflated_mask[ly, lx] > 0:
            return False
    return True

# Inflate obstacles by robot radius so we treat edges as solid thickness
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ROBOT_R*2, ROBOT_R*2))
inflated_mask = cv2.dilate(obstacle_mask, kernel, iterations=1)

# --- Main loop ---
while True:
    frame = canvas.copy()

    # draw inflated obstacles as light gray overlay (for visualization)
    overlay = frame.copy()
    overlay[inflated_mask > 0] = (220, 220, 220)
    frame = cv2.addWeighted(overlay, 0.35, frame, 0.65, 0)

    # plan: if path blocked, search left/right within FOV for a free angle
    if not look_ahead_direction(heading):
        found_angle = None
        # try sweeping angles to left/right
        for delta in np.linspace(0, FOV/2, 20):
            for sign in (+1, -1):
                cand = (heading + sign*delta) % (2*math.pi)
                if look_ahead_direction(cand):
                    found_angle = cand
                    break
            if found_angle is not None:
                break
        if found_angle is None:
            # last resort: random nudge
            found_angle = (heading + rng.uniform(-math.pi, math.pi)) % (2*math.pi)
        heading = found_angle

    # move forward
    new_pos = pos + np.array([math.cos(heading), math.sin(heading)]) * SPEED

    # if new position collides, back up a bit and rotate
    if collides_at(new_pos):
        heading = (heading + rng.uniform(math.radians(20), math.radians(160))) % (2*math.pi)
    else:
        pos = new_pos

    # keep inside bounds
    pos[0] = np.clip(pos[0], ROBOT_R, W-ROBOT_R-1)
    pos[1] = np.clip(pos[1], ROBOT_R, H-ROBOT_R-1)

    # draw trail
    trail.append(tuple(pos.astype(int)))
    for i in range(1, len(trail)):
        cv2.line(frame, trail[i-1], trail[i], (100, 100, 255), 2)

    # draw robot
    cv2.circle(frame, (int(pos[0]), int(pos[1])), ROBOT_R, (50, 180, 60), -1)
    # draw heading line
    hx = int(pos[0] + math.cos(heading) * (ROBOT_R + 12))
    hy = int(pos[1] + math.sin(heading) * (ROBOT_R + 12))
    cv2.line(frame, (int(pos[0]), int(pos[1])), (hx, hy), (0, 0, 0), 2)

    # small look-ahead rays (visual)
    for ang in np.linspace(heading - FOV/2, heading + FOV/2, 9):
        rx = int(pos[0] + math.cos(ang) * RAY_DIST)
        ry = int(pos[1] + math.sin(ang) * RAY_DIST)
        color = (0, 200, 0) if look_ahead_direction(ang) else (0, 0, 200)
        cv2.line(frame, (int(pos[0]), int(pos[1])), (rx, ry), color, 1)

    cv2.putText(frame, "Auto-avoid: q to quit", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2, cv2.LINE_AA)

    cv2.imshow("Warehouse Robot - Auto Navigation (Sim)", frame)
    key = cv2.waitKey(15) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
