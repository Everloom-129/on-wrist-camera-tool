import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def analyze_depth_log(file_path):
    with open(file_path, 'r') as file:
        file_content = file.readlines()

    image_names = []
    min_depths = []
    max_depths = []
    mean_depths = []

    for line in file_content:
        if line.startswith("Depth statistics for"):
            image_name = re.search(r'data\/(.*?)\:', line).group(1)
            image_names.append(image_name)
        elif line.startswith("Min depth"):
            min_depths.append(float(re.search(r"Min depth: (.*?)m", line).group(1)))
        elif line.startswith("Max depth"):
            max_depths.append(float(re.search(r"Max depth: (.*?)m", line).group(1)))
        elif line.startswith("Mean depth"):
            mean_depths.append(float(re.search(r"Mean depth: (.*?)m", line).group(1)))

    depth_data = pd.DataFrame({
        "Image Name": image_names,
        "Min Depth (mm)": min_depths,
        "Max Depth (mm)": max_depths,
        "Mean Depth (mm)": mean_depths
    })

    summary = (
        f"Summary of Depth Statistics:\n"
        f"- Minimum Depth Range: {min(depth_data['Min Depth (mm)'])}mm to {max(depth_data['Min Depth (mm)'])}mm\n"
        f"- Maximum Depth Range: {min(depth_data['Max Depth (mm)'])}mm to {max(depth_data['Max Depth (mm)'])}mm\n"
        f"- Mean Depth Range: {min(depth_data['Mean Depth (mm)'])}mm to {max(depth_data['Mean Depth (mm)'])}mm\n"
    )
    print(summary)
    with open(file_path, 'a') as file:
        file.write("\n" + summary)
    output_folder = os.path.dirname(file_path)

    # Create Bar Chart
    bar_chart_path = os.path.join(output_folder, 'BarChart.png')
    depth_data.set_index("Image Name")[["Min Depth (mm)", "Max Depth (mm)", "Mean Depth (mm)"]].plot(kind='bar', figsize=(12, 6))
    plt.title("Minimum, Maximum, and Mean Depths by Image")
    plt.xlabel("Image Name")
    plt.ylabel("Depth (mm)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(bar_chart_path)
    plt.close()

    # Create Line Chart
    line_chart_path = os.path.join(output_folder, 'LineChart.png')
    depth_data.set_index("Image Name")[["Min Depth (mm)", "Max Depth (mm)", "Mean Depth (mm)"]].plot(marker='o', figsize=(12, 6))
    plt.title("Trends in Depth Statistics Across Images")
    plt.xlabel("Image Name")
    plt.ylabel("Depth (mm)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(line_chart_path)
    plt.close()

    print(f"Analysis complete. Summary written to log, and visualizations saved to {output_folder}.")
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyze_depth.py <log_file_path>")
        print("Example: python analyze_depth.py phone_depth/depth_stats.log")
        sys.exit(1)
        
    log_file_path = sys.argv[1]
    analyze_depth_log(log_file_path)

