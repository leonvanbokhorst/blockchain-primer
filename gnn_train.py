#!/usr/bin/env python3
"""gnn_train.py: Consume USDC transfer stream, build graph, train GAE, detect anomalies."""

import sys
import json
import time
import pandas as pd
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GAE, GCNConv


# GAE Model Definition with Learnable Embeddings
class Encoder(torch.nn.Module):
    def __init__(self, num_nodes, embedding_dim, out_channels):
        super().__init__()
        self.embedding = torch.nn.Embedding(num_nodes, embedding_dim)
        self.conv1 = GCNConv(embedding_dim, 64)  # Input channels = embedding dim
        self.conv2 = GCNConv(64, out_channels)

    def forward(self, x, edge_index):
        # x input are node indices
        x = self.embedding(x)  # Look up embeddings
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)


def build_graph_data(events, usdc_decimals=6):
    """Build a PyG Data object from a list of (src, dst, value) events."""
    if not events:
        return None, None

    # Convert values from wei to USDC units and aggregate
    df = pd.DataFrame(events, columns=["src", "dst", "value"])
    df["amount_usdc"] = df["value"] / (10**usdc_decimals)
    df = df.groupby(["src", "dst"])["amount_usdc"].sum().reset_index()

    nodes = set(df.src) | set(df.dst)
    node_map = {addr: i for i, addr in enumerate(nodes)}
    rev_node_map = {i: addr for addr, i in node_map.items()}

    edge_index = torch.tensor(
        [[node_map[src] for src in df.src], [node_map[dst] for dst in df.dst]],
        dtype=torch.long,  # Ensure it's long type right from creation
    )
    edge_weight = torch.tensor(df.amount_usdc.values, dtype=torch.float)

    # Use node indices as features for embedding lookup
    num_nodes = len(node_map)
    node_indices = torch.arange(num_nodes, dtype=torch.long)
    data = Data(x=node_indices, edge_index=edge_index, edge_weight=edge_weight)
    return data, rev_node_map


def train_gae(model, data, optimizer, epochs=100):
    """Train the GAE model."""
    print(
        f"Debug: train_gae - data.x dtype={data.x.dtype}, data.edge_index dtype={data.edge_index.dtype}",
        file=sys.stderr,
    )
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        z = model.encode(data.x, data.edge_index)
        # Use default recon_loss which handles negative sampling
        loss = model.recon_loss(z, data.edge_index)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"  Epoch {epoch}: Loss {loss.item():.4f}", file=sys.stderr)
    return model


def detect_anomalies(model, data, rev_node_map, threshold=0.1):
    """Use trained GAE to detect anomalies and print recon scores."""
    # Ensure edge_index is of type LongTensor for PyG operations
    # data.edge_index = data.edge_index.long() # Already ensured in build_graph_data
    print(
        f"Debug: detect_anomalies - data.x dtype={data.x.dtype}, data.edge_index dtype={data.edge_index.dtype}",
        file=sys.stderr,
    )
    model.eval()
    with torch.no_grad():
        z = model.encode(data.x, data.edge_index)
        recon_weight = model.decoder(z, data.edge_index)
        error = (recon_weight - data.edge_weight).abs()

        print("\nEdge Reconstruction Analysis:", file=sys.stderr)
        for idx in range(data.num_edges):
            src_idx = data.edge_index[0, idx].item()
            dst_idx = data.edge_index[1, idx].item()
            orig_weight = data.edge_weight[idx].item()
            recon_w = recon_weight[idx].item()
            err = error[idx].item()
            # Print details for all edges, not just anomalies
            print(
                f"  - {rev_node_map[src_idx]} -> {rev_node_map[dst_idx]}: "
                f"Orig: {orig_weight:.2f}, Recon Score: {recon_w:.4f}, Error: {err:.4f}",
                file=sys.stderr,
            )

        # Keep anomaly detection logic for reference, but maybe comment out/adjust threshold later
        anomalous_indices = torch.where(error > threshold)[0]
        if anomalous_indices.numel() > 0:
            print(f"\nAnomalies Detected (Error > {threshold}):", file=sys.stderr)
            for idx in anomalous_indices.tolist():
                src_idx = data.edge_index[0, idx].item()
                dst_idx = data.edge_index[1, idx].item()
                orig_weight = data.edge_weight[idx].item()
                recon_w = recon_weight[idx].item()
                err = error[idx].item()
                print(
                    f"  - {rev_node_map[src_idx]} -> {rev_node_map[dst_idx]}: "
                    f"Orig: {orig_weight:.2f}, Recon Score: {recon_w:.4f}, Error: {err:.4f}",
                    file=sys.stderr,
                )


def main(
    batch_interval_secs=60, train_epochs=100, anomaly_threshold=0.1, embedding_dim=16
):
    """Main loop: consume events, build graph, train, detect."""
    current_batch = []
    last_batch_time = time.time()
    model = None
    optimizer = None

    print("Starting GNN anomaly detection loop...", file=sys.stderr)
    for line in sys.stdin:
        try:
            event_data = json.loads(line)
            current_batch.append(
                (event_data["src"], event_data["dst"], event_data["value"])
            )
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON: {line.strip()}", file=sys.stderr)
            continue

        # Process batch periodically
        if time.time() - last_batch_time >= batch_interval_secs:
            print(
                f"\nProcessing batch with {len(current_batch)} events...",
                file=sys.stderr,
            )
            if not current_batch:
                last_batch_time = time.time()
                continue

            data, rev_node_map = build_graph_data(current_batch)
            if data is None:
                print("No valid graph data in batch.", file=sys.stderr)
                current_batch = []
                last_batch_time = time.time()
                continue

            print(
                f"Graph built: {data.num_nodes} nodes, {data.num_edges} edges.",
                file=sys.stderr,
            )

            # Initialize or update model
            if model is None:
                print(
                    f"Initializing GAE model with {data.num_nodes} nodes, embedding_dim={embedding_dim}",
                    file=sys.stderr,
                )
                encoder = Encoder(
                    data.num_nodes, embedding_dim, 32
                )  # Output embedding size 32
                model = GAE(encoder)
                optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
            else:
                # Simple approach: Re-initialize for new node set
                # Check if number of nodes changed, requiring model re-initialization
                if data.num_nodes != model.encoder.embedding.num_embeddings:
                    print(
                        f"Node set changed ({model.encoder.embedding.num_embeddings} -> {data.num_nodes}), re-initializing model.",
                        file=sys.stderr,
                    )
                    encoder = Encoder(data.num_nodes, embedding_dim, 32)
                    model = GAE(encoder)
                    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

            print("Training GAE model...", file=sys.stderr)
            model = train_gae(model, data, optimizer, epochs=train_epochs)
            detect_anomalies(model, data, rev_node_map, threshold=anomaly_threshold)

            # Reset for next batch
            current_batch = []
            last_batch_time = time.time()
            print("\nWaiting for next batch...", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGNN training interrupted. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error in GNN main loop: {e}", file=sys.stderr)
        sys.exit(1)
