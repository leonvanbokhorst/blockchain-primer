# Milestone 5: USDC Transfer Streaming & GNN Anomaly Detection

## Overview

Now that you've mastered hashing, headers, wallets, and contracts, you'll plug into the live network: stream real USDC `Transfer` events from Ethereum mainnet, fold them into a graph structure with PyTorch Geometric, and train a simple Graph Autoencoder to spot anomalous transfers in near real‑time.

## Objectives

- Connect to an Ethereum provider (Infura/Alchemy) via Ape/Web3.
- Subscribe to the USDC contract's `Transfer` events and buffer incoming data.
- Build a dynamic graph where nodes are addresses and edge weights represent aggregate transfer volume.
- Use PyTorch Geometric to construct a Graph Autoencoder (GAE) that learns normal transfer patterns.
- Flag edges with high reconstruction error as potential anomalies (fraud, spikes, outliers).

## Prerequisites

1. Virtual environment with dependencies in `requirements.txt`:
   ```bash
   pip install eth-ape web3 torch torch_geometric pandas
   ```
2. An Ethereum mainnet API key (set `ALCHEMY_API_KEY` or `INFURA_API_KEY` as env var).
3. USDC contract address: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`.
4. Basic familiarity with PyTorch Geometric (GAE, Data objects).

## Steps

1. **Configure Provider**

   ```bash
   export ALCHEMY_API_KEY="your_key_here"
   ```

   In Python:

   ```python
   from ape import networks
   networks.default.set_provider("mainnet", "alchemy", api_key=os.getenv("ALCHEMY_API_KEY"))
   ```

2. **Stream USDC Events**

   - Write `stream_usdc.py`:

     ```python
     from web3 import Web3
     import os

     w3 = Web3(Web3.HTTPProvider(f"https://eth-mainnet.alchemyapi.io/v2/{os.getenv('ALCHEMY_API_KEY')}"))
     usdc = w3.eth.contract(address=USDC_ADDRESS, abi=USDC_ABI)
     filter = usdc.events.Transfer.createFilter(fromBlock='latest')
     while True:
         for event in filter.get_new_entries():
             yield (event.args.from, event.args.to, event.args.value)
     ```

3. **Build Graph Batches**

   - Accumulate events in pandas, map addresses to indices, and create a PyG `Data` object:

     ```python
     import pandas as pd
     from torch_geometric.data import Data

     df = pd.DataFrame(events, columns=["src","dst","amt"]).groupby(["src","dst"]).sum().reset_index()
     node_map = {addr:i for i, addr in enumerate(set(df.src) | set(df.dst))}
     edge_index = torch.tensor([[node_map[src] for src in df.src], [node_map[dst] for dst in df.dst]])
     edge_weight = torch.tensor(df.amt.values, dtype=torch.float)
     data = Data(x=torch.eye(len(node_map)), edge_index=edge_index, edge_weight=edge_weight)
     ```

4. **Define & Train GAE**

   ```python
   from torch_geometric.nn import GAE, GCNConv
   import torch

   class Encoder(torch.nn.Module):
       def __init__(self, in_channels, out_channels):
           super().__init__()
           self.conv1 = GCNConv(in_channels, 64)
           self.conv2 = GCNConv(64, out_channels)
       def forward(self, x, edge_index):
           x = self.conv1(x, edge_index).relu()
           return self.conv2(x, edge_index)

   model = GAE(Encoder(len(node_map), 32))
   optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

   for epoch in range(100):
       optimizer.zero_grad()
       z = model.encode(data.x, data.edge_index)
       loss = model.recon_loss(z, data.edge_index, data.edge_weight)
       loss.backward()
       optimizer.step()
       print(f"Epoch {epoch}: {loss.item():.4f}")
   ```

5. **Detect Anomalies**

   ```python
   with torch.no_grad():
       z = model.encode(data.x, data.edge_index)
       recon = model.decoder(z, data.edge_index)
       error = (recon - data.edge_weight).abs()
       anomalies = data.edge_index[:, error > threshold]
   ```

   - Edges flagged in `anomalies` are candidates for manual review.

6. **Run & Monitor**

   ```bash
   python stream_usdc.py | python gnn_train.py
   ```

   Watch console logs for high‐error edges lighting up.

7. **Commit Your Work**
   ```bash
   git add stream_usdc.py gnn_train.py docs/milestone5_usdc_graph_gnn.md
   git commit -m "Milestone 5: Stream USDC and detect anomalies with GNN"
   ```

## Expected Output

A terminal session where after training you see lines like:

```
Epoch 99: 0.0021
Anomalous edge detected: (node 123 -> node 456) error 0.029
```

Nodes with unusually high reconstruction error are your anomaly candidates.

## Next Steps

- Explore temporal‐graph contrastive learning to incorporate time dynamics.
- Integrate a dashboard (e.g. Streamlit) to visualize live anomaly streams.
- Reflect on what these patterns mean for on‑chain trust and risk. 🎷📈
