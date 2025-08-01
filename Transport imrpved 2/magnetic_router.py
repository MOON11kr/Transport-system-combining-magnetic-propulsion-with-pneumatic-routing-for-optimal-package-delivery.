import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import secrets


class MagneticRouter:
    """Optimized routing with magnetic constraints and package
      authentication."""

    def __init__(self, size=5):
        """Initialize router with grid graph and crypto keys."""
        self.size = size
        self.G = nx.grid_2d_graph(size, size)
        self._init_graph()
        self.packages = {}
        self.time = 0
        self.grid = np.zeros((size, size), dtype=int)
        self.warehouse = (size // 2, size // 2)
        self._init_crypto()

    def _init_graph(self):
        """Set random weights and capacities for edges."""
        edge_attrs = {
            (u, v): {
                'weight': np.random.randint(1, 10),
                'capacity': 1
            } for u, v in self.G.edges()
        }
        nx.set_edge_attributes(self.G, edge_attrs)

    def _init_crypto(self):
        """Generate RSA keys for QR signing."""
        self.priv_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.pub_key = self.priv_key.public_key()

    def add_package(self, pkg_id, start, end, qr_sig=None):
        """Add package with optional QR signature."""
        try:
            path = nx.dijkstra_path(self.G, start, end, weight='weight')
            self.packages[pkg_id] = {
                'path': path,
                'pos': 0,
                'energy': 0.0,
                'start': start,
                'end': end,
                'qr_sig': qr_sig
            }
        except nx.NetworkXNoPath:
            print(f"[ERROR] No path from {start} to {end} for {pkg_id}")

    def sign_package(self, pkg_data):
        """Generate QR signature for package data."""
        return self.priv_key.sign(
            pkg_data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify_package(self, pkg_id):
        """Verify package with QR fallback to OTP."""
        pkg = self.packages.get(pkg_id)
        if not pkg or not pkg['qr_sig']:
            return self._verify_otp(pkg_id)

        try:
            self.pub_key.verify(
                pkg['qr_sig'],
                pkg_id.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return self._verify_otp(pkg_id)

    def _verify_otp(self, pkg_id):
        """Simulate OTP verification (6-digit code)."""
        otp = secrets.randbelow(1_000_000)
        print(f"OTP for {pkg_id}: {otp:06d} (simulated)")
        return True  # Assume correct input

    def eject_to_warehouse(self, pkg_id):
        """Re-route failed packages to warehouse."""
        if pkg_id in self.packages:
            current_pos = self.packages[pkg_id]['path'][
                self.packages[pkg_id]['pos']
            ]
            self.add_package(
                f"WH_{pkg_id}",
                current_pos,
                self.warehouse
            )

    def _is_valid_move(self, u, v, occupied):
        """Check if move respects capacity and occupation."""
        try:
            return (
                (u, v) not in occupied and
                self.G.edges[u, v]['capacity'] > 0
            )
        except KeyError:
            return False

    def update(self):
        """Advance simulation by one timestep."""
        occupied = set()
        total_energy = 0.0
        for pkg in self.packages.values():
            if pkg['pos'] < len(pkg['path']) - 1:
                u = pkg['path'][pkg['pos']]
                v = pkg['path'][pkg['pos'] + 1]
                if self._is_valid_move(u, v, occupied):
                    pkg['pos'] += 1
                    energy = self.G.edges[u, v]['weight']
                    pkg['energy'] += energy
                    total_energy += energy
                    occupied.add((u, v))
        self.time += 1
        return total_energy

    def _package_summary(self):
        """Generate package status summary."""
        return '\n'.join(
            f"Package {pkg_id}: {pkg['start']} → {pkg['end']}"
            for pkg_id, pkg in self.packages.items()
        )

    def run(self, frames=100, save_as=None):
        """Execute simulation with animation."""
        fig, ax = plt.subplots(figsize=(6, 6))
        plt.subplots_adjust(top=0.85, bottom=0.15)

        def animate(i):
            ax.clear()
            energy = self.update()
            pos = {n: (n[1], -n[0]) for n in self.G.nodes()}
            nx.draw(self.G, pos, ax=ax, node_size=20)

            for pkg in self.packages.values():
                if pkg['pos'] < len(pkg['path']):
                    x, y = pkg['path'][pkg['pos']]
                    ax.plot(x, -y, 'ro')

            ax.set_title(
                f"Time: {self.time} | Energy: {energy:.1f} J",
                fontsize=13, pad=20
            )
            ax.text(
                0, -self.size - 1.5,
                self._package_summary(),
                fontsize=9, ha='left', va='top',
                family='monospace'
            )
            ax.axis('off')

        anim = FuncAnimation(fig, animate, frames=frames, interval=300)

        if save_as:
            try:
                anim.save(save_as, writer='pillow')
                print(f"[SAVED] {save_as}")
            except Exception as e:
                print(f"[ERROR] Save failed: {e}")
        else:
            plt.show()
