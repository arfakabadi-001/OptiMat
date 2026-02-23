from tabulate import tabulate
from colorama import Fore, Style
import csv


def filter_materials(materials, min_strength, max_density,
                     max_cost, required_temp):

    shortlisted = []
    rejected = []

    for m in materials:
        reasons = []
        hard_reject = False

        # Extreme rejection rules
        if m.strength < min_strength * 0.5:
            hard_reject = True
            reasons.append("Strength extremely low")

        if m.density > max_density * 1.5:
            hard_reject = True
            reasons.append("Density extremely high")

        if m.cost > max_cost * 1.5:
            hard_reject = True
            reasons.append("Cost extremely high")

        if m.max_temp < required_temp * 0.5:
            hard_reject = True
            reasons.append("Temperature capacity extremely low")

        if hard_reject:
            rejected.append((m, reasons))
        else:
            shortlisted.append(m)

    return shortlisted, rejected


def rank_materials(shortlisted, weights,
                   min_strength, max_density,
                   max_cost, required_temp):

    scored_list = []

    for m in shortlisted:
        score = m.calculate_score(
            min_strength, max_density,
            max_cost, required_temp,
            weights
        )

        scored_list.append((m, score))

    scored_list.sort(key=lambda x: x[1], reverse=True)

    return scored_list


def display_results(scored_list, rejected):

    if scored_list:
        table = [
            [
                m.material_id,
                m.name,
                m.strength,
                m.density,
                m.cost,
                m.max_temp,
                m.corrosion,
                m.sustainability,
                round(score, 3)
            ]
            for m, score in scored_list
        ]

        headers = [
            "ID", "Name", "Strength", "Density", "Cost",
            "Max Temp", "Corrosion", "Sustainability", "Score"
        ]

        print(Fore.GREEN + "\nShortlisted & Ranked Materials:\n" + Style.RESET_ALL)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

        best = scored_list[0][0]

        print(Fore.CYAN + "\nBest Material Selected:\n" + Style.RESET_ALL)
        print(tabulate([[best.material_id, best.name, best.strength,
                         best.density, best.cost, best.max_temp,
                         best.corrosion, best.sustainability]],
                       headers=headers[:-1],
                       tablefmt="fancy_grid"))

    if rejected:
        reject_table = [
            [m.material_id, m.name, "; ".join(reasons)]
            for m, reasons in rejected
        ]

        print(Fore.RED + "\nRejected Materials:\n" + Style.RESET_ALL)
        print(tabulate(reject_table,
                       headers=["ID", "Name", "Reason"],
                       tablefmt="fancy_grid"))


def export_to_csv(scored_list, rejected):

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Material", "Score", "Status", "Reason"])

        for m, score in scored_list:
            writer.writerow([m.name, round(score, 3), "Shortlisted", "-"])

        for m, reasons in rejected:
            writer.writerow([m.name, 0, "Rejected", "; ".join(reasons)])
