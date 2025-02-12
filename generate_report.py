import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Define the resources
resources = ["john", "vikram"]

# Define output files
output_csv = "consolidated_report.csv"
output_html = "index.html"
output_chart = "task_distribution.png"

# Read individual CSV reports and combine
data_frames = []
for resource in resources:
    folder = resource
    latest_file = None
    
    # Find the latest CSV file in the resource's folder
    if os.path.exists(folder):
        csv_files = sorted(
            [f for f in os.listdir(folder) if f.endswith(".csv")],
            reverse=True
        )
        if csv_files:
            latest_file = os.path.join(folder, csv_files[0])

    # If there's a latest file, read and process it
    if latest_file:
        df = pd.read_csv(latest_file)
        df["Resource"] = resource  # Add a column for resource name
        data_frames.append(df)

# Merge all reports
if data_frames:
    consolidated_df = pd.concat(data_frames, ignore_index=True)
    consolidated_df.to_csv(output_csv, index=False)
else:
    consolidated_df = pd.DataFrame(columns=["Resource", "Task", "Status", "Hours"])

# Generate a Pie Chart for Task Distribution
if not consolidated_df.empty and "Task" in consolidated_df.columns:
    task_counts = consolidated_df["Task"].value_counts()
    plt.figure(figsize=(8, 6))
    task_counts.plot.pie(autopct="%1.1f%%", startangle=90, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
    plt.title("Task Distribution Among Resources")
    plt.ylabel("")  # Hide y-axis label
    plt.savefig(output_chart)
    plt.close()
else:
    output_chart = None  # No chart if no data

# Generate HTML Report
with open(output_html, "w") as f:
    f.write("<html><head><title>Daily Status Report</title></head><body>")
    f.write("<h1>Daily Status Report</h1>")
    f.write(f"<h2>Date: {datetime.today().strftime('%d-%m-%Y')}</h2>")

    if output_chart:
        f.write(f'<img src="{output_chart}" alt="Task Distribution" width="500"><br><br>')

    if not consolidated_df.empty:
        f.write("<h2>Consolidated Report</h2>")
        f.write(consolidated_df.to_html(index=False))
    else:
        f.write("<p>No data available for today.</p>")

    f.write("</body></html>")

print("Report generated successfully!")
