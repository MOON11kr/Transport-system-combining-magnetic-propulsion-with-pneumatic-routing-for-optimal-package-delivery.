from router_core import MagneticRouter
import time


def performance_test():
    router = MagneticRouter(size=10)

    for i in range(20):
        router.add_package(
            id=f"P{i}",
            start=(0, 0),
            end=(9, 9)
        )

    start_time = time.time()
    total_energy = 0

    for _ in range(50):
        energy = router.update()
        total_energy += energy

    elapsed_time = time.time() - start_time
    print(f"Simulation finished in {elapsed_time:.4f} seconds.")
    print(f"Total energy consumed: {total_energy:.2f} J")


if __name__ == "__main__":
    performance_test()
