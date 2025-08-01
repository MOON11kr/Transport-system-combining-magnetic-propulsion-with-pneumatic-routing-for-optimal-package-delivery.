"""
ENHANCED MAGNETIC ESCALATOR DEMO
Advanced visualization of FerroRoute's physical implementation.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from magnetic_router import MagneticRouter
import networkx as nx


class EnhancedEscalatorVisualizer:
    def __init__(self, size=6):
        self.router = MagneticRouter(size=size)
        self._setup_escalator_path()
        self.fig = plt.figure(figsize=(14, 6))
        self.ax_sim = self.fig.add_subplot(121)
        self.ax_phys = self.fig.add_subplot(122, projection='3d')
        self.ax_phys.set_box_aspect([1, 1, 0.3])
        self.occupied_destinations = set()
        self.warehouse_node = (0, 0)

    def _setup_escalator_path(self):
        """Create optimized escalator path with acceleration zones"""
        path = []
        size = self.router.size

        path.extend((0, col) for col in range(size))
        path.extend((row, size - 1) for row in range(1, size))
        path.extend((size - 1, col) for col in range(size - 2, -1, -1))
        path.extend((row, 0) for row in range(size - 2, 0, -1))

        self.loop_path = path
        self._optimize_escalator_physics()

    def _optimize_escalator_physics(self):
        """Simulate magnetic acceleration zones"""
        for i in range(len(self.loop_path) - 1):
            u, v = self.loop_path[i], self.loop_path[i + 1]
            if u[0] == v[0] or u[1] == v[1]:
                self.router.G.edges[u, v]['weight'] = 0.05
            else:
                self.router.G.edges[u, v]['weight'] = 0.2

    def add_package(self, pkg_id, destination=None, interval=5):
        """Add package with optional destination and interval"""
        start = self.loop_path[0]
        dest = destination or self.loop_path[-1]

        if dest in self.occupied_destinations:
            status = 'rejected'
            dest = self.warehouse_node
        else:
            status = 'accepted'
            self.occupied_destinations.add(dest)

        self.router.add_package(pkg_id, start, dest)
        self.router.packages[pkg_id]['status'] = status

        if hasattr(self, 'last_pkg_time'):
            self.router.time += interval

    def visualize(self):
        """Run enhanced visualization and save GIF"""
        def animate(i):
            self._update_views()
            self.router.update()

        anim = FuncAnimation(
            self.fig, animate, frames=150, interval=100
        )
        anim.save("enhanced_escalator.gif", writer='pillow', dpi=150, fps=10)
        plt.close()
        print("\u2714 Saved enhanced_escalator.gif")

    def _update_views(self):
        """Update both simulation and physical views"""
        self.ax_sim.clear()
        self.ax_phys.clear()

        pos = {n: (n[1], -n[0]) for n in self.router.G.nodes()}
        nx.draw(
            self.router.G, pos, ax=self.ax_sim,
            node_size=30, node_color='lightblue'
        )
        self.ax_sim.set_title(
            "Routing Simulation\n(Network Graph View)", pad=20
        )

        self._draw_3d_escalator()
        self.ax_phys.set_title("Magnetic Escalator Implementation", pad=20)
        self.ax_phys.set_axis_off()
        plt.tight_layout()

    def _draw_3d_escalator(self):
        """3D rendering of physical system"""
        x = [p[1] for p in self.loop_path]
        y = [-p[0] for p in self.loop_path]
        z = [0] * len(self.loop_path)
        self.ax_phys.plot(x, y, z, 'gray', linewidth=4, alpha=0.7)

        for node in self.loop_path:
            x, y = node[1], -node[0]
            self.ax_phys.plot([x], [y], [0], 'o',
                              markersize=10, color='blue', alpha=0.5)

        for pkg_id, pkg in self.router.packages.items():
            if pkg['pos'] < len(pkg['path']):
                x = pkg['path'][pkg['pos']][1]
                y = -pkg['path'][pkg['pos']][0]
                color = 'green' if pkg['status'] == 'accepted' else 'red'
                self.ax_phys.bar3d(
                    x - 0.3, y - 0.3, 0,
                    0.6, 0.6, 0.4,
                    color=color, alpha=0.8
                )
                for _ in range(3):
                    self.ax_phys.plot(
                        [x, x + np.random.normal(0, 0.2)],
                        [y, y + np.random.normal(0, 0.2)],
                        [0.4, 0],
                        'y-', linewidth=1, alpha=0.3
                    )


if __name__ == "__main__":
    print("Running Enhanced Escalator Visualization...")
    escalator = EnhancedEscalatorVisualizer(size=6)

    # Controlled test cases
    # Case 1: two packages with same destination (one accepted, one rerouted)
    common_dest = escalator.loop_path[-1]
    escalator.add_package("Pkg0", destination=common_dest, interval=5)
    escalator.add_package("Pkg1", destination=common_dest, interval=5)

    # Case 2: distinct destination
    if len(escalator.loop_path) > 5:
        escalator.add_package(
            "Pkg2",
            destination=escalator.loop_path[5],
            interval=5
        )

    # Case 3: forced rejection due to reused destination
    escalator.add_package("Pkg3", destination=common_dest, interval=5)

    escalator.visualize()
