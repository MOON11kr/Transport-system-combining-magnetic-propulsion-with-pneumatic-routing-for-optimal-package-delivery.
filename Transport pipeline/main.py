from simulator import MagneticTransportSystem
from config import GRID_SIZE


def run_case(case_num, description, packages):
    """Run a test case and print results."""
    print(f"\n{'=' * 50}")
    print(f"Case {case_num}: {description}")
    print(f"{'=' * 50}")

    system = MagneticTransportSystem()

    for pkg_id, (start, end, delay) in packages.items():
        system.add_package(pkg_id, start, end, delay)
        print(f"Added {pkg_id}: {start} → {end} (delay: {delay})")

    print("\n🚀 Running simulation...")
    system.run_simulation(f"case{case_num}.gif")

    stats = system.get_stats()
    print("\n✅ Simulation complete!")
    print(f"⏱️ Total time: {stats['total_time']}")
    print(f"⚡ Total energy: {stats['total_energy']:.2f}")
    print(f"📦 Packages delivered: {stats['delivered']}/{len(packages)}")

    for pkg_id, pkg_stats in stats["packages"].items():
        print(f"\nPackage {pkg_id}:")
        print(f"Path: {' → '.join(str(p) for p in pkg_stats['path'])}")
        print(f"Energy used: {pkg_stats['energy']:.2f}")
        print(f"Progress: {pkg_stats['progress']:.1f}%")
        status = 'Delivered' if pkg_stats['delivered'] else 'In transit'
        print(f"Status: {status}")


def main():
    """Run all test cases."""
    # Case 1: Single package
    run_case(
        1,
        "Single package transport",
        {"Package1": ((0, 0), (GRID_SIZE[0] - 1, GRID_SIZE[1] - 1), 0)},
    )

    # Case 2: Two packages same route (with delay)
    run_case(
        2,
        "Two packages same route",
        {
            "Package1": ((0, 0), (GRID_SIZE[0] - 1, GRID_SIZE[1] - 1), 0),
            "Package2": ((0, 0), (GRID_SIZE[0] - 1, GRID_SIZE[1] - 1), 3),
        },
    )

    # Case 3: Three packages different routes
    run_case(
        3,
        "Three packages different routes",
        {
            "North-South": ((2, 0), (2, GRID_SIZE[1] - 1), 0),
            "East-West": ((0, 2), (GRID_SIZE[0] - 1, 2), 1),
            "Diagonal": ((0, 0), (GRID_SIZE[0] - 1, GRID_SIZE[1] - 1), 2),
        },
    )


if __name__ == "__main__":
    print("Magnetic Transport System Simulation")
    print("===================================")
    main()
