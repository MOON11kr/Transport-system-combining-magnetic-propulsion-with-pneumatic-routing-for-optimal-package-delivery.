import time
import tracemalloc
from magnetic_router import MagneticRouter
import matplotlib.pyplot as plt


def benchmark_package_routing():
    """Run benchmarks for different grid sizes and save GIFs and metrics."""
    sizes = [5, 10, 15, 20]  # Grid sizes to test
    results = {'time': [], 'memory': [], 'packages': []}

    for size in sizes:
        router = MagneticRouter(size=size)

        # Add packages in cross pattern (NS and EW directions)
        for i in range(size):
            router.add_package(f"P{i}_NS", (i, 0), (i, size - 1))
            router.add_package(f"P{i}_EW", (0, i), (size - 1, i))

        # File name for saving the animation
        gif_filename = f"grid_{size}x{size}.gif"

        # Start tracking memory and time
        tracemalloc.start()
        start_time = time.perf_counter()

        # Run simulation and save animation
        router.run(frames=100, save_as=gif_filename)

        # Stop tracking
        elapsed = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Record results
        results['time'].append(elapsed)
        results['memory'].append(peak / 10**6)  # Convert to MB
        results['packages'].append(2 * size)

        print(
           f"✔ Saved {gif_filename} "
           f"(Time: {elapsed:.2f}s, "
           f"Peak Memory: {peak / 10**6:.1f} MB)")

    # Save benchmark results to text file
    with open("benchmark_results.txt", "w") as f:
        f.write("Grid Size, Packages, Time (s), Memory (MB)\n")
        for i, size in enumerate(sizes):
            f.write(
                f"{size}x{size}, {results['packages'][i]}, "
                f"{results['time'][i]:.2f}, {results['memory'][i]:.1f}\n"
            )

    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(results['packages'], results['time'], 'o-')
    ax1.set_xlabel('Number of Packages')
    ax1.set_ylabel('Time (s)')
    ax1.set_title('Routing Time Scaling')

    ax2.plot(results['packages'], results['memory'], 'o-r')
    ax2.set_xlabel('Number of Packages')
    ax2.set_ylabel('Peak Memory (MB)')
    ax2.set_title('Memory Usage Scaling')

    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300)
    print("📊 Benchmark plot saved as benchmark_results.png")
    print("📄 Benchmark data saved as benchmark_results.txt")
    plt.tight_layout()


if __name__ == "__main__":
    benchmark_package_routing()
