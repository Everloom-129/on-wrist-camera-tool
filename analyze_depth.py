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
        "Min Depth (m)": min_depths,
        "Max Depth (m)": max_depths,
        "Mean Depth (m)": mean_depths
    })

    summary = (
        f"Summary of Depth Statistics:\n"
        f"- Minimum Depth Range: {min(depth_data['Min Depth (m)'])}m to {max(depth_data['Min Depth (m)'])}m\n"
        f"- Maximum Depth Range: {min(depth_data['Max Depth (m)'])}m to {max(depth_data['Max Depth (m)'])}m\n"
        f"- Mean Depth Range: {min(depth_data['Mean Depth (m)'])}m to {max(depth_data['Mean Depth (m)'])}m\n"
    )

    with open(file_path, 'a') as file:
        file.write("\n" + summary)
    output_folder = os.path.dirname(file_path)

    # Create Bar Chart
    bar_chart_path = os.path.join(output_folder, 'depth_statistics_bar_chart.png')
    depth_data.set_index("Image Name")[["Min Depth (m)", "Max Depth (m)", "Mean Depth (m)"]].plot(kind='bar', figsize=(12, 6))
    plt.title("Minimum, Maximum, and Mean Depths by Image")
    plt.xlabel("Image Name")
    plt.ylabel("Depth (m)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(bar_chart_path)
    plt.close()

    # Create Line Chart
    line_chart_path = os.path.join(output_folder, 'depth_statistics_line_chart.png')
    depth_data.set_index("Image Name")[["Min Depth (m)", "Max Depth (m)", "Mean Depth (m)"]].plot(marker='o', figsize=(12, 6))
    plt.title("Trends in Depth Statistics Across Images")
    plt.xlabel("Image Name")
    plt.ylabel("Depth (m)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(line_chart_path)
    plt.close()

    print(f"Analysis complete. Summary written to log, and visualizations saved to {output_folder}.")

if __name__ == "__main__":
    analyze_depth_log("phone_depth/depth_stats.log")

