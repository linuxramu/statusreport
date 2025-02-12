import os
import pandas as pd
from datetime import datetime

# Base directory (root of repo)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get all resource folders (excluding hidden/system files)
resources = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and not d.startswith('.')]

# HTML report
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Status Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid black; padding: 10px; text-align: left; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h2>Daily Status Report</h2>
"""

for resource in resources:
    resource_path = os.path.join(BASE_DIR, resource)
    csv_files = sorted([f for f in os.listdir(resource_path) if f.endswith('.csv')], reverse=True)

    html_content += f"<h3>{resource}</h3>"
    
    if csv_files:
        latest_csv = os.path.join(resource_path, csv_files[0])
        df = pd.read_csv(latest_csv)

        html_content += "<table><tr>"
        html_content += "".join([f"<th>{col}</th>" for col in df.columns])
        html_content += "</tr>"

        for _, row in df.iterrows():
            html_content += "<tr>"
            html_content += "".join([f"<td>{row[col]}</td>" for col in df.columns])
            html_content += "</tr>"

        html_content += "</table>"
    else:
        html_content += "<p>No reports available</p>"

html_content += "</body></html>"

# Write to index.html
with open(os.path.join(BASE_DIR, "index.html"), "w") as f:
    f.write(html_content)
