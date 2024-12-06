import os
import glob
import geopandas as gpd
import rasterio
import pandas as pd
from pathlib import Path
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def Changeintogpkg(input_path, output_dir, layer_name):
    input_path = str(input_path)
    # Check if the file is already in GPKG format
    if input_path.endswith(".gpkg"):
        return input_path
    else:
        # Convert to GPKG format if it's not
        gdf = gpd.read_file(input_path)
        output_gpkg = os.path.join(output_dir, f"{layer_name}.gpkg")
        gdf.to_file(output_gpkg, driver="GPKG")
        return output_gpkg


# Get the Flooded Building Count
def GetFloodedBuildingCountInfo(
    building_fp_path,
    study_area_path,
    raster1_path,
    raster2_path,
    contingency_map,
    save_dir,
    basename,
):
    output_dir = os.path.dirname(building_fp_path)

    # Convert files to GPKG if necessary
    building_fp_gpkg = Changeintogpkg(
        building_fp_path, output_dir, "building_footprint"
    )

    # Load the building footprint
    building_gdf = gpd.read_file(building_fp_gpkg)
    study_area_gdf = gpd.read_file(study_area_path)

    # Reproject both layers to the same CRS
    if building_gdf.crs != study_area_gdf.crs:
        building_gdf = building_gdf.to_crs(study_area_gdf.crs)

    # Clip the building footprint to the study area
    clipped_buildings = gpd.overlay(building_gdf, study_area_gdf, how="intersection")
    clipped_buildings["centroid"] = clipped_buildings.geometry.centroid

    # Initialize a dictionary to store the counts
    centroid_counts = {
        "Benchmark": 0,
        "Candidate": 0,
        "False Positive": 0,
        "False Negative": 0,
        "True Positive": 0,
    }

    def count_centroids_in_raster(raster_path, label):
        with rasterio.open(raster_path) as src:
            raster_data = src.read(1)
            transform = src.transform

            for centroid in clipped_buildings["centroid"]:
                # Get row, col of centroid in raster space
                row, col = src.index(centroid.x, centroid.y)

                # Check if the value at that location matches the expected pixel values
                if 0 <= row < raster_data.shape[0] and 0 <= col < raster_data.shape[1]:
                    pixel_value = raster_data[row, col]
                    if label in ["Benchmark", "Candidate"]:
                        if pixel_value == 2:  # False Positive
                            centroid_counts[label] += 1
                    else:
                        if pixel_value == 2:
                            centroid_counts["False Positive"] += 1
                        elif pixel_value == 3:
                            centroid_counts["False Negative"] += 1
                        elif pixel_value == 4:
                            centroid_counts["True Positive"] += 1

    # Identify Benchmark and Candidate rasters based on file name
    if "benchmark" in str(raster1_path).lower():
        count_centroids_in_raster(raster1_path, "Benchmark")
        count_centroids_in_raster(raster2_path, "Candidate")
    elif "candidate" in str(raster2_path).lower():
        count_centroids_in_raster(raster1_path, "Candidate")
        count_centroids_in_raster(raster2_path, "Benchmark")

    # Count for the third raster (contingency map)
    if "contingency" in str(contingency_map).lower():
        count_centroids_in_raster(contingency_map, "Contingency")

    # Percentage calculation
    total_buildings = len(clipped_buildings)
    percentages = {
        key: (count / total_buildings) * 100 for key, count in centroid_counts.items()
    }

    # Prepare data for the second plot (third raster counts)
    third_raster_labels = ["False Positive", "False Negative", "True Positive"]
    third_raster_counts = [
        centroid_counts["False Positive"],
        centroid_counts["False Negative"],
        centroid_counts["True Positive"],
    ]

    # Plotting the result using Plotly
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Building Counts on Different FIMs",
            "Contingency Flooded Building Counts",
        ),
    )

    # Add Candidate bar for the first plot
    fig.add_trace(
        go.Bar(
            x=["Candidate"],
            y=[centroid_counts["Candidate"]],
            text=[f"{centroid_counts['Candidate']}"],
            textposition="auto",
            marker_color="#1c83eb",
            marker_line_color="black",
            marker_line_width=1,
            name=f"Candidate ({percentages['Candidate']:.2f}%)",
        ),
        row=1,
        col=1,
    )

    # Add Benchmark bar for the first plot
    fig.add_trace(
        go.Bar(
            x=["Benchmark"],
            y=[centroid_counts["Benchmark"]],
            text=[f"{centroid_counts['Benchmark']}"],
            textposition="auto",
            marker_color="#a4490e",
            marker_line_color="black",
            marker_line_width=1,
            name=f"Benchmark ({percentages['Benchmark']:.2f}%)",
        ),
        row=1,
        col=1,
    )

    # Add bars for the second plot (third raster counts)
    for i in range(len(third_raster_labels)):
        fig.add_trace(
            go.Bar(
                x=[third_raster_labels[i]],
                y=[third_raster_counts[i]],
                text=[f"{third_raster_counts[i]}"],
                textposition="auto",
                marker_color=["#ff5733", "#ffc300", "#28a745"][i],
                marker_line_color="black",
                marker_line_width=1,
                name=f"{third_raster_labels[i]} ({percentages[third_raster_labels[i]]:.2f}%)",
            ),
            row=1,
            col=2,
        )

    # Customizing layout
    fig.update_layout(
        title="Flooded Building Counts",
        xaxis_title="Inundation Surface",
        yaxis_title="Flooded Building Counts",
        width=1100,
        height=400,
        xaxis=dict(showline=True, linewidth=2, linecolor="black"),
        yaxis=dict(showline=True, linewidth=2, linecolor="black"),
        xaxis2=dict(showline=True, linewidth=2, linecolor="black"),
        yaxis2=dict(showline=True, linewidth=2, linecolor="black"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=True,
        title_font=dict(family="Arial", size=24, color="black"),  # Removed weight
        xaxis_title_font=dict(family="Arial", size=20, color="black"),  # Removed weight
        yaxis_title_font=dict(family="Arial", size=20, color="black"),  # Removed weight
        font=dict(family="Arial", size=18, color="black"),
    )

    # Save counts to CSV
    counts_data = {
        "Category": [
            "Candidate",
            "Benchmark",
            "False Positive",
            "False Negative",
            "True Positive",
        ],
        "Building Count": [
            centroid_counts["Candidate"],
            centroid_counts["Benchmark"],
            centroid_counts["False Positive"],
            centroid_counts["False Negative"],
            centroid_counts["True Positive"],
        ],
    }
    counts_df = pd.DataFrame(counts_data)
    csv_file_path = os.path.join(
        save_dir, "EvaluationMetrics", f"BuildingCounts_{basename}.csv"
    )
    counts_df.to_csv(csv_file_path, index=False)

    # Save the plot as PNG
    plot_dir = os.path.join(save_dir, "FinalPlots")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    output_path = os.path.join(plot_dir, f"BuildingCounts_{basename}.png")
    fig.write_image(output_path, scale=500 / 96, engine="kaleido")
    print(f"Performance metrics chart is saved as PNG at {output_path}")
    fig.show()


def process_TIFF(
    tif_files, contingency_files, building_footprint, boundary, method_path
):
    benchmark_path = None
    candidate_path = []

    if len(tif_files) == 2:
        for tif_file in tif_files:
            if "benchmark" in tif_file.name:
                benchmark_path = tif_file
            else:
                candidate_path.append(tif_file)

    elif len(tif_files) > 2:
        for tif_file in tif_files:
            if "benchmark" in tif_file.name:
                benchmark_path = tif_file
                print(f"---Benchmark: {tif_file.name}---")
            else:
                candidate_path.append(tif_file)

    if benchmark_path and candidate_path:
        for candidate in candidate_path:

            # Matching contingency map for the candidate
            matching_contingency_map = None
            candidate_base_name = candidate.stem.replace("_clipped", "")

            for contingency_file in contingency_files:
                if candidate_base_name in contingency_file.name:
                    matching_contingency_map = contingency_file
                    print(
                        f"Found matching contingency map for candidate {candidate.name}: {contingency_file.name}"
                    )
                    break

            if matching_contingency_map:
                print(
                    f"---FIM evaluation with Building Footprint starts for {candidate.name}---"
                )
                GetFloodedBuildingCountInfo(
                    building_footprint,
                    boundary,
                    benchmark_path,
                    candidate,
                    matching_contingency_map,
                    method_path,
                    candidate_base_name,
                )
            else:
                print(
                    f"No matching contingency map found for candidate {candidate.name}. Skipping..."
                )


def EvaluationWithBuildingFootprint(main_dir, building_footprint, method_name):
    method_path = os.path.join(main_dir, method_name)
    if not os.path.exists(method_path):
        for root, dirs, files in os.walk(main_dir):
            if method_name in dirs:
                method_path = os.path.join(root, method_name)
                break
        else:
            raise FileNotFoundError(
                f"The folder '{method_name}' was not found in '{main_dir}' or its subdirectories."
            )

    # Traverse subfolders within the method directory
    for root, dirs, files in os.walk(method_path):
        for folder_name in dirs:
            if folder_name == "MaskedFIMwithBoundary":
                contingency_path = os.path.join(root, "ContingencyMaps")
                tif_files = list(Path(os.path.join(root, folder_name)).glob("*.tif"))
                contingency_files = list(Path(contingency_path).glob("*.tif"))
                boundary = os.path.join(
                    root, "BoundaryforEvaluation", "FIMEvaluatedExtent.shp"
                )
                process_TIFF(
                    tif_files,
                    contingency_files,
                    building_footprint,
                    boundary,
                    method_path,
                )
