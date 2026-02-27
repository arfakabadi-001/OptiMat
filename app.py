from flask import Flask, render_template, request, send_file
import csv
import os
from engine import filter_materials, rank_materials
from database import init_db, seed_materials, fetch_materials

app = Flask(__name__)

# Initialize database
init_db()
seed_materials()

# Path to save CSV results
CSV_FILE = "results.csv"

# --- Homepage ---
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# --- Main form page ---
@app.route("/run", methods=["GET", "POST"])
def index():
    materials = fetch_materials()
    ranked = []
    rejected = []

    if request.method == "POST":
        # --- Read constraints ---
        min_strength = float(request.form["min_strength"])
        max_density = float(request.form["max_density"])
        max_cost = float(request.form["max_cost"])
        required_temp = float(request.form["required_temp"])

        # --- Read weights ---
        ws = float(request.form["ws"])
        wc = float(request.form["wc"])
        wd = float(request.form["wd"])
        wcor = float(request.form["wcor"])
        wsus = float(request.form["wsus"])

        total = ws + wc + wd + wcor + wsus
        weights = {
            'ws': ws / total,
            'wc': wc / total,
            'wd': wd / total,
            'wcor': wcor / total,
            'wsus': wsus / total
        }

        # --- Run filtering & ranking ---
        shortlisted, rejected = filter_materials(
            materials, min_strength, max_density, max_cost, required_temp
        )
        ranked = rank_materials(
            shortlisted, weights, min_strength, max_density, max_cost, required_temp
        )

        # --- Save CSV to disk ---
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Material", "Score", "Status", "Reason"])
            for m, score in ranked:
                writer.writerow([m.name, round(score, 3), "Shortlisted", "-"])
            for m, reasons in rejected:
                writer.writerow([m.name, 0, "Rejected", "; ".join(reasons)])

        return render_template("result.html", ranked=ranked, rejected=rejected)

    return render_template("index.html")

# --- Download CSV ---
@app.route("/download_csv")
def download_csv():
    if os.path.exists(CSV_FILE):
        return send_file(
            CSV_FILE,
            mimetype="text/csv",
            as_attachment=True,
            download_name="OptiMat_results.csv"
        )
    else:
        return "CSV file not found. Run the optimization first.", 404


if __name__ == "__main__":
    app.run(debug=True)