from magnetic_router import MagneticRouter


def run_case_studies():
    """Runs case studies on the MagneticRouter simulation."""
    print("Running Case Study 1: Basic Movement")
    router = MagneticRouter(size=6)
    router.add_package("P1", (0, 0), (5, 5))
    router.run(frames=100, save_as="case_1_basic_movement.gif")

    print("Running Case Study 2: Destination Blocked")
    router = MagneticRouter(size=6)
    router.grid[5][5] = 1
    router.add_package("P2", (0, 0), (5, 5))
    router.run(frames=100, save_as="case_2_destination_blocked.gif")

    print("Running Case Study 3: Multiple Packages")
    router = MagneticRouter(size=6)
    router.add_package("P3", (0, 0), (5, 5))
    router.add_package("P4", (5, 5), (0, 0))
    router.add_package("P5", (0, 5), (5, 0))
    router.run(frames=120, save_as="case_3_multiple_packages.gif")

    print("Running Case Study 4: Reverse Direction")
    router = MagneticRouter(size=6)
    router.add_package("P6", (5, 5), (0, 0))
    router.run(frames=100, save_as="case_4_reverse_direction.gif")

    print("Running Case Study 5: Congestion in Same Direction")
    router = MagneticRouter(size=6)
    router.add_package("P7", (0, 0), (5, 5))
    router.add_package("P8", (1, 0), (5, 5))
    router.add_package("P9", (2, 0), (5, 5))
    router.run(frames=120, save_as="case_5_congestion_same_direction.gif")

    print("Running Case Study 6: Cross Paths (Potential Deadlock)")
    router = MagneticRouter(size=6)
    router.add_package("P10", (0, 0), (5, 5))
    router.add_package("P11", (5, 0), (0, 5))
    router.run(frames=120, save_as="case_6_cross_paths_deadlock.gif")

    print("Running Case Study 7: Bidirectional Transfer")
    router = MagneticRouter(size=6)
    router.add_package("P12", (0, 0), (5, 5))
    router.add_package("P13", (5, 5), (0, 0))
    router.run(frames=120, save_as="case_7_bidirectional_transfer.gif")

    print("Running Case Study 8: Node Sending & Receiving")
    router = MagneticRouter(size=6)
    router.add_package("P14", (0, 0), (3, 3))
    router.add_package("P15", (5, 5), (0, 0))
    router.run(frames=100, save_as="case_8_sending_receiving.gif")

    print("Running Case Study 9: Same Destination")
    router = MagneticRouter(size=6)
    router.add_package("P16", (0, 0), (5, 5))
    router.add_package("P17", (1, 0), (5, 5))
    router.run(frames=120, save_as="case_9_same_destination.gif")

    print("Running Case Study 10: Obstacle Navigation")
    router = MagneticRouter(size=6)
    router.grid[3][3] = 1
    router.add_package("P18", (0, 0), (5, 5))
    router.run(frames=120, save_as="case_10_obstacle_navigation.gif")

    print("Running Case Study 11: Circular Path Trap")
    router = MagneticRouter(size=6)
    router.add_package("P19", (0, 0), (1, 1))
    router.run(frames=60, save_as="case_11_circular_path_trap.gif")

    print("Running Case Study 12: Node Collision")
    router = MagneticRouter(size=6)
    router.add_package("P20", (0, 1), (3, 3))
    router.add_package("P21", (1, 0), (3, 3))
    router.run(frames=100, save_as="case_12_node_collision.gif")

    print("Running Case Study 13: QR Tampering")
    router = MagneticRouter(size=6)
    legit_sig = router.sign_package("P22")
    router.add_package("P22", (0, 0), (5, 5), qr_sig=legit_sig)
    router.run(frames=100, save_as="case_13_qr_tampering.gif")

    # Try verifying (this will succeed because we used a legit signature)
    verified = router.verify_package("P22")
    if not verified:
        print("Security: Tampered package detected!")
        router.eject_to_warehouse("P22")

    print("Running Case Study 14: OTP Fallback")
    router = MagneticRouter(size=6)
    router.add_package("P23", (0, 0), (5, 5), qr_sig=b"invalid")
    router.verify_package("P23")  # This triggers OTP fallback
    router.run(frames=100, save_as="case_14_otp_fallback.gif")

    print("Running Case Study 15: Warehouse Recovery")
    router = MagneticRouter(size=6)
    router.add_package("P24", (0, 0), (5, 5))
    router.eject_to_warehouse("P24")
    router.run(frames=50, save_as="case_15_warehouse.gif")


if __name__ == "__main__":
    run_case_studies()
