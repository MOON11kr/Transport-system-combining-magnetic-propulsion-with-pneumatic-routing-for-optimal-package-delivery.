import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class MagneticRouter:
    """Optimal parallel routing with magnetic constraints."""

    def __init__(self, size=5):
        self.size = size
        self.G = nx.grid_2d_graph(size, size)
        edge_attrs = {}
        for u, v in self.G.edges():
            edge_attrs[(u, v)] = {
                'weight': np.random.randint(1, 10),
                'capacity': 1
            }
        nx.set_edge_attributes(self.G, edge_attrs)
        self.packages = {}
        self.time = 0
        self.grid = np.zeros((size, size), dtype=int)

    def add_package(self, pkg_id, start, end):
        """Add a package and precompute its path using Dijkstra's algorithm."""
        try:
            path = nx.dijkstra_path(self.G, start, end, weight='weight')
            self.packages[pkg_id] = {
                'path': path,
                'pos': 0,
                'energy': 0.0,
                'start': start,
                'end': end
            }
        except nx.NetworkXNoPath:
            print(
                f"[ERROR] No path found for package {pkg_id} "
                f"from {start} to {end}."
            )

    def _is_valid_move(self, u, v, occupied):
        """Check if move is valid based on capacity and current occupation."""
        try:
            return (
                (u, v) not in occupied
                and self.G.edges[u, v]['capacity'] > 0
            )
        except KeyError:
            return False

    def update(self):
        """Update package positions and return total energy consumed step."""
        occupied = set()
        total_energy = 0.0
        for pkg in self.packages.values():
            if pkg['pos'] < len(pkg['path']) - 1:
                u = pkg['path'][pkg['pos']]
                v = pkg['path'][pkg['pos'] + 1]
                if self._is_valid_move(u, v, occupied):
                    pkg['pos'] += 1
                    energy_used = self.G.edges[u, v]['weight']
                    pkg['energy'] += energy_used
                    total_energy += energy_used
                    occupied.add((u, v))
        self.time += 1
        return total_energy

    def _package_summary(self):
        """Generate a string summary of all packages and their routes."""
        lines = []
        for pkg_id, pkg in self.packages.items():
            lines.append(
                f"Package {pkg_id}: {pkg['start']} → {pkg['end']}"
            )
        return '\n'.join(lines)

    def run(self, frames=100, save_as=None):
        """Run the simulation and optionally save as a GIF."""
        fig, ax = plt.subplots(figsize=(6, 6))
        plt.subplots_adjust(top=0.85, bottom=0.15)  # ✅ more room

        def animate(i):
            ax.clear()
            energy = self.update()
            pos = {n: (n[1], -n[0]) for n in self.G.nodes()}
            nx.draw(
                self.G, pos=pos, ax=ax, node_size=20, with_labels=False
            )

            # Draw current package locations
            for pkg in self.packages.values():
                if pkg['pos'] < len(pkg['path']):
                    x, y = pkg['path'][pkg['pos']]
                    ax.plot(x, -y, 'ro')

            # Title + description
            ax.set_title(
                f"Time: {self.time} | Step Energy: {energy:.1f} J",
                fontsize=13, pad=20  # ✅ More padding
            )
            ax.text(
                0, -self.size - 1.5,
                self._package_summary(),
                fontsize=9, ha='left', va='top',
                family='monospace'
            )
            ax.axis('off')

        anim = FuncAnimation(
            fig, animate, frames=frames, interval=300
        )

        if save_as:
            try:
                anim.save(save_as, writer='pillow')
                print(f"[SAVED] Animation saved as: {save_as}")
            except Exception as e:
                print(f"[ERROR] Failed to save animation: {e}")
        else:
            plt.show()
