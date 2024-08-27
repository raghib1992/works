# for parent in range(3):
#     print(f"Parent loop, iteration {parent}")
#     for child in range(3):
#         print(f"  Child loop, iteration {child}")
#         if child == 1:
#             print("  Child condition met, continuing parent loop")
#             continue  # Skips the rest of the child loop
#     print("End of parent loop iteration")


def run_loops():
    parent_index = 0
    while parent_index < 3:
        print(f"Parent loop, iteration {parent_index}")
        for child in range(3):
            print(f"  Child loop, iteration {child}")
            if child == 1:
                print("  Child condition met, restarting parent loop")
                parent_index -= 1  # Adjust the parent index to rerun
                break  # Break out of the child loop and rerun the parent
        parent_index += 1
        print("End of parent loop iteration")

run_loops()