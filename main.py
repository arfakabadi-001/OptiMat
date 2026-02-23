from models import Material
from engine import filter_materials, rank_materials, display_results, export_to_csv
from colorama import init

init(autoreset=True)

from database import init_db, seed_materials, fetch_materials

init_db()
seed_materials()
materials = fetch_materials()

def main():

    while True:

        print("\n=== OptiMat Material Selection ===")
        print("1. Enter constraints and priorities")
        print("2. Run material selection")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":

            min_strength = float(input("Minimum required strength: "))
            max_density = float(input("Maximum allowed density: "))
            max_cost = float(input("Maximum cost per kg: "))
            required_temp = float(input("Required operating temperature: "))

            print("\nEnter priority weights (0 to 1):")

            ws = float(input("Weight for Strength: "))
            wc = float(input("Weight for Cost: "))
            wd = float(input("Weight for Density: "))
            wcor = float(input("Weight for Corrosion: "))
            wsus = float(input("Weight for Sustainability: "))

            total = ws + wc + wd + wcor + wsus

            weights = {
                'ws': ws / total,
                'wc': wc / total,
                'wd': wd / total,
                'wcor': wcor / total,
                'wsus': wsus / total
            }

            print("\nConstraints and weights saved.")

        elif choice == "2":

            try:
                shortlisted, rejected = filter_materials(
                    materials, min_strength, max_density,
                    max_cost, required_temp
                )

                scored_list = rank_materials(
                    shortlisted, weights,
                    min_strength, max_density,
                    max_cost, required_temp
                )

                display_results(scored_list, rejected)
                export_to_csv(scored_list, rejected)

                print("\nResults exported to results.csv")

            except NameError:
                print("Please set constraints first (Option 1).")

        elif choice == "3":
            print("Exiting OptiMat...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
