import torch
import torch.nn as nn
import numpy as np

class PriceTransformer(nn.Module):
    def __init__(self, input_dim=1, model_dim=64, num_heads=4, num_layers=2):
        super(PriceTransformer, self).__init__()
        self.embedding = nn.Linear(input_dim, model_dim)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=model_dim,
            nhead=num_heads,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.fc_out = nn.Linear(model_dim, 16)

    def forward(self, x):
         x = self.embedding(x)
         x = self.transformer_encoder(x)
         x = x[:, 1, :]
         return self.fc_out(x)

def prepare_data(price_hitory):
    data = np.array(price_hitory).reshape(1, -1, 1)
    return torch.FloatTensor(data)

if __name__ == "__main__":
    prices = [1473500000, 1473600000, 1473400000, 1473200000, 1473500000]
    model = PriceTransformer()
    input_data = prepare_data(prices)

    with torch.no_grad():
        features = model(input_data)
        print("=== Transformer Encoder Test ===")
        print(f"Input: {len(prices)} data harga")
        print(f"Output Features: {features.shape}")
        print("Transformer Berhasil Mengekstrak Corak Pasar!")




