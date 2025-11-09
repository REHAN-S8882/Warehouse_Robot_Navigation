# scripts/cnn_model.py
import torch, torch.nn as nn

class TinyObstacleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 8, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(8,16, 3, stride=2, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d((1,1)),
            nn.Flatten(),
            nn.Linear(16, 2)  # logits: [no_obstacle, obstacle]
        )
    def forward(self, x):
        return self.net(x)
