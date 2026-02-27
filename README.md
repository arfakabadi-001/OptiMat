# OptiMat – AI-Inspired Multi-Criteria Material Selection

**OptiMat** is an intelligent material selection system designed to help engineers choose the best materials for a given application based on multiple constraints and user-defined priorities. The system evaluates mechanical, economic, and environmental criteria, ranks the materials, and provides a comprehensive report.

---

## 🌟 Features

- Multi-criteria decision-making using weighted scoring
- Dynamic filtering of materials based on:
  - Strength
  - Density
  - Cost
  - Operating Temperature
  - Corrosion Resistance
  - Sustainability
- Interactive **Web UI** using Flask with:
  - Input form for constraints & weights
  - Result dashboard with table and pie chart
  - CSV export of results
- CLI version available for quick evaluation
- Database-driven material repository (SQLite)

---

## 🛠 Problem Statement / Motivation

Engineers often struggle to select the most suitable materials when multiple factors such as cost, strength, weight, and sustainability must be considered simultaneously. OptiMat addresses this by providing a **ranked list of materials** based on constraints and priorities, simplifying decision-making and saving design time.

---

## 🧰 Technology Stack

- **Python 3.11**
- **Flask** – Web framework for building the interactive UI
- **SQLite** – Database for storing materials
- **Pandas / NumPy** – For data handling and calculations
- **Matplotlib / Chart.js** – Visualization of results
- **HTML, CSS, JavaScript** – Front-end for a polished UI
