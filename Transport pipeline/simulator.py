import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from config import (
    GRID_SIZE,
    PIPE_RESISTANCE_RANGE,
    ENERGY_PER_UNIT,
    SIMULATION_TIME,
)


class MagneticTransportSystem:
    def __init__(self):
        """Initialize the magnetic transport network."""
        self.network = self._create_network()
        self.packages = {}
        self.occupied_edges = set()
        self.time = 0
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.pos = {(x, y): (x, y) for x, y in self.network.nodes()}
        self.colors = ['red', 'blue', 'green', 'purple', 'orange']

    def _create_network(self):
        """Create magnetic pipe network with random resistances."""
        G = nx.grid_2d_graph(*GRID_SIZE)
        for u, v in G.edges():
            G.edges[u, v]["weight"] = np.random.randint(*PIPE_RESISTANCE_RANGE)
            G.edges[u, v]["capacity"] = 1
        return G

    def add_package(self, package_id, start, end, delay=0):
        """Add a package with optional delay."""
        path = nx.dijkstra_path(self.network, start, end, weight="weight")
        self.packages[package_id] = {
            "path": path,
            "position": -delay,
            "start": start,
            "end": end,
            "energy": 0,
            "delivered": False,
        }

    def update_system(self):
        """Advance simulation by one time step."""
        self.time += 1
        self.occupied_edges.clear()

        for pkg in self.packages.values():
            if 0 <= pkg["position"] < len(pkg["path"]) - 1:
                current = pkg["path"][pkg["position"]]
                next_node = pkg["path"][pkg["position"] + 1]

                if (current, next_node) not in self.occupied_edges:
                    pkg["position"] += 1
                    edge = self.network.edges[current, next_node]
                    pkg["energy"] += edge["weight"] * ENERGY_PER_UNIT
                    self.occupied_edges.add((current, next_node))

                    if pkg["position"] == len(pkg["path"]) - 1:
                        pkg["delivered"] = True

            elif pkg["position"] < 0:
                pkg["position"] += 1

    def visualize(self):
        """Generate visualization of current state."""
        self.ax.clear()
        nx.draw(
            self.network,
            self.pos,
            ax=self.ax,
            node_color="lightgray",
            node_size=800,
            with_labels=True,
        )

        artists = []
        for i, pkg in enumerate(self.packages.values()):
            if pkg["position"] >= 0:
                color = self.colors[i % len(self.colors)]
                x, y = self.pos[pkg["path"][pkg["position"]]]
                dot, = self.ax.plot(x, y, 'o', color=color, markersize=15)

                if pkg["position"] > 0:
                    partial_path = pkg["path"][:pkg["position"] + 1]
                    coords = [self.pos[n] for n in partial_path]
                    xs, ys = zip(*coords)
                    line, = self.ax.plot(xs, ys, '-', color=color, linewidth=2)
                    artists.append(line)

                artists.append(dot)

        self.ax.set_title(f"Transport System (t={self.time})")
        return artists

    def run_simulation(self, filename="simulation.gif"):
        """Run complete simulation and save animation."""

        def update(frame):
            self.update_system()
            return self.visualize()

        ani = FuncAnimation(
            self.fig,
            update,
            frames=SIMULATION_TIME,
            interval=200,
            blit=True
        )
        ani.save(filename, writer="pillow", fps=5, dpi=100)
        plt.close()

    def get_stats(self):
        """Return simulation statistics."""
        stats = {
            "total_time": self.time,
            "packages": {},
            "total_energy": 0,
            "delivered": 0,
        }

        for pkg_id, pkg in self.packages.items():
            path_len = len(pkg["path"])
            progress = (
                min(100, pkg["position"] / path_len * 100)
                if path_len > 0 and pkg["position"] >= 0 else 0
            )

            stats["packages"][pkg_id] = {
                "path": pkg["path"],
                "energy": pkg["energy"],
                "delivered": pkg["delivered"],
                "progress": progress,
            }

            stats["total_energy"] += pkg["energy"]
            if pkg["delivered"]:
                stats["delivered"] += 1

        return stats
