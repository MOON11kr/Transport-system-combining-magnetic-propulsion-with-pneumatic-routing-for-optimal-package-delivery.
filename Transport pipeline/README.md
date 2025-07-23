# Magneto-Pneumatic Autonomous Transport System (MPATS)

![System Diagram](docs/system_overview.png)

A novel hybrid transport system combining magnetic propulsion with pneumatic routing for optimal package delivery.

## Key Features
- **Dual-mode propulsion**: Magnetic acceleration + pneumatic assist
- **AI-driven routing**: Q-learning optimized pathfinding
- **Collision-free operation**: Priority-based scheduling
- **Energy monitoring**: Joule-level consumption tracking

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from magnetopneumatic import MPATS

# Initialize 5x5 network
network = MPATS(grid_size=(5,5))

# Add packages
network.add_package(
    pkg_id="urgent_1",
    start=(0,0),
    end=(4,4),
    priority=0.9  # 0-1 scale
)

# Run simulation
stats = network.simulate(
    duration=100,
    output="simulation.gif"
)
```

## Test Cases
1. **Unimodal Transport**: Single package baseline
2. **Concurrent Routing**: Multiple packages same path
3. **Cross-Network**: Divergent origin-destination pairs

## Research Applications
- Urban logistics automation
- Hospital specimen transport
- Industrial part delivery