import math
import random
from typing import Optional, Tuple

import cv2
import gymnasium as gym
import numpy as np
from gymnasium import spaces


class WarehouseNavEnv(gym.Env):
    """
    A tiny continuous 2D warehouse nav env:
    - State (12 floats): [goal_dx, goal_dy, cos(h), sin(h), 8 lidar rays], all in [0,1] or [-1,1] range
    - Actions (Discrete 3): 0=forward, 1=turn_left, 2=turn_right
    - Rewards: + (prev_dist - new_dist)*5  , -10 on collision, +100 on goal, -0.01 step cost
    """
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, width: int = 700, height: int = 500, render_mode: Optional[str] = None):
        super().__init__()
        self.W, self.H = width, height
        self.render_mode = render_mode

        # --- action/observation spaces ---
        self.action_space = spaces.Discrete(3)  # 0=forward, 1=left, 2=right
        # obs = goal_dx_norm, goal_dy_norm, cos(h), sin(h), 8 lidar rays (normalized 0..1)
        self.num_rays = 8
        low = np.array([-1, -1, -1, -1] + [0.0] * self.num_rays, dtype=np.float32)
        high = np.array([+1, +1, +1, +1] + [1.0] * self.num_rays, dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # --- robot/physics params ---
        self.ROBOT_R = 10
        self.SPEED = 4.0
        self.TURN = math.radians(18)
        self.RAY_DIST = 80

        # will be filled in reset()
        self.canvas = None
        self.obstacle_mask = None
        self.inflated_mask = None
        self.pos = None
        self.heading = None
        self.goal = None
        self.prev_goal_dist = None
        self.steps = 0
        self.max_steps = 1000

    # --------- helper geometry ----------
    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.W and 0 <= y < self.H

    def _collides_xy(self, x: int, y: int) -> bool:
        if not self._in_bounds(x, y):
            return True
        return self.inflated_mask[y, x] > 0

    def _lidar_rays(self) -> np.ndarray:
        """Cast self.num_rays rays in a ±90° fan around heading; return normalized distances [0..1]."""
        rays = []
        start = self.heading - math.pi / 2
        end = self.heading + math.pi / 2
        for ang in np.linspace(start, end, self.num_rays):
            hit = self.RAY_DIST
            for d in range(self.ROBOT_R, self.RAY_DIST):
                x = int(self.pos[0] + math.cos(ang) * d)
                y = int(self.pos[1] + math.sin(ang) * d)
                if not self._in_bounds(x, y) or self.inflated_mask[y, x] > 0:
                    hit = d
                    break
            rays.append(hit / self.RAY_DIST)
        return np.array(rays, dtype=np.float32)

    def _observe(self) -> np.ndarray:
        dx = (self.goal[0] - self.pos[0]) / self.W
        dy = (self.goal[1] - self.pos[1]) / self.H
        obs = np.array([dx, dy, math.cos(self.heading), math.sin(self.heading)], dtype=np.float32)
        rays = self._lidar_rays()
        return np.concatenate([obs, rays]).astype(np.float32)

    def _goal_distance(self) -> float:
        return float(np.linalg.norm(self.goal - self.pos))

    # --------- Gym API ----------
    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        rng = random.Random(seed if seed is not None else 42)

        # canvas & obstacles
        self.canvas = np.ones((self.H, self.W, 3), dtype=np.uint8) * 255
        for _ in range(10):
            x1, y1 = rng.randint(30, self.W - 180), rng.randint(30, self.H - 140)
            x2, y2 = x1 + rng.randint(40, 160), y1 + rng.randint(40, 140)
            cv2.rectangle(self.canvas, (x1, y1), (x2, y2), (0, 0, 255), -1)

        # edge mask + inflate by robot radius
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        self.obstacle_mask = (edges > 0).astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.ROBOT_R * 2, self.ROBOT_R * 2))
        self.inflated_mask = cv2.dilate(self.obstacle_mask, kernel, iterations=1)

        # start & goal
        self.pos = np.array([40.0, 40.0], dtype=np.float32)
        self.heading = 0.0
        self.goal = np.array([self.W - 40.0, self.H - 40.0], dtype=np.float32)

        self.prev_goal_dist = self._goal_distance()
        self.steps = 0
        return self._observe(), {}

    def step(self, action: int):
        self.steps += 1

        # turn or move
        if action == 1:
            self.heading -= self.TURN
        elif action == 2:
            self.heading += self.TURN

        # propose new position (forward move each step)
        nx = int(self.pos[0] + math.cos(self.heading) * self.SPEED)
        ny = int(self.pos[1] + math.sin(self.heading) * self.SPEED)

        terminated = False
        reward = -0.01  # small step penalty

        if self._collides_xy(nx, ny):
            reward -= 10.0
            terminated = True
        else:
            self.pos = np.array([nx, ny], dtype=np.float32)
            # reward for getting closer to goal
            d = self._goal_distance()
            reward += (self.prev_goal_dist - d) * 5.0
            self.prev_goal_dist = d

        # success?
        if self._goal_distance() < 20.0:
            reward += 100.0
            terminated = True

        truncated = self.steps >= self.max_steps
        obs = self._observe()
        info = {}

        # optional render
        if self.render_mode == "human":
            self.render()

        return obs, reward, terminated, truncated, info

    def render(self):
        frame = self.canvas.copy()
        # draw inflated mask as gray
        overlay = frame.copy()
        overlay[self.inflated_mask > 0] = (220, 220, 220)
        frame = cv2.addWeighted(overlay, 0.35, frame, 0.65, 0)
        # goal & robot
        cv2.circle(frame, (int(self.goal[0]), int(self.goal[1])), 10, (0, 180, 255), -1)
        cv2.circle(frame, (int(self.pos[0]), int(self.pos[1])), self.ROBOT_R, (50, 180, 60), -1)
        hx = int(self.pos[0] + math.cos(self.heading) * (self.ROBOT_R + 12))
        hy = int(self.pos[1] + math.sin(self.heading) * (self.ROBOT_R + 12))
        cv2.line(frame, (int(self.pos[0]), int(self.pos[1])), (hx, hy), (0, 0, 0), 2)
        cv2.imshow("RL Env (preview)", frame)
        cv2.waitKey(1)

    def close(self):
        if self.render_mode == "human":
            cv2.destroyAllWindows()


# ---- quick smoke test ----
if __name__ == "__main__":
    env = WarehouseNavEnv(render_mode=None)  # change to "human" to visualize
    obs, info = env.reset(seed=0)
    total = 0.0
    for _ in range(50):
        action = env.action_space.sample()
        obs, r, term, trunc, info = env.step(action)
        total += r
        if term or trunc:
            break
    env.close()
    print("Smoke test OK. Steps run:", _ + 1, "Total reward:", round(total, 2))
