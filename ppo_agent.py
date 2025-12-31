import torch
import torch.nn as nn
import torch.optim as optim

class PPOAgent():
    def __init__(self, state_dim=16, action_dim=3):
        super(PPOAgent, self).__init__
        self.policy = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )

        self.value = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def act(self, state):
        probs = self.policy(state)
        action = torch.multinomial(probs, 1)
        return action.item(), probs
    
if __name__ == "__main__":
    mock_features = torch.randn(1, 16)
    agent = PPOAgent()
    
    action_code, probabilities = agent.act(mock_features)
    actions = ["HOLD", "BUY", "SELL"]
    
    print("=== PPO Agent Test ===")
    print(f"Fitur Masuk: {mock_features.shape}")
    print(f"Probabilitas Aksi: {probabilities.detach().numpy()}")
    print(f"Keputusan Agen: {actions[action_code]}")