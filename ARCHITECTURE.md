LILA Player Journey Visualization Tool Architecture

1. Technology Stack

Component — Technology — Purpose

UI Framework — Streamlit — Interactive dashboard interface
Data Processing — Pandas — Data filtering and transformation
Data Format — Parquet — Efficient telemetry storage
File Reader — PyArrow — Reading parquet files
Visualization — Plotly — Map rendering and event plotting
Image Handling — Base64 — Background map rendering
Deployment — Streamlit Cloud — Application hosting

Stack rationale

The stack was selected to enable rapid development of an interactive visualization tool while keeping the system simple, readable, and easy to extend. Streamlit and Plotly allowed focusing on insight generation rather than frontend infrastructure.

2. System Data Flow
High level flow

Parquet Files
↓
PyArrow Loader
↓
Pandas DataFrames
↓
Filtering Layer
↓
Coordinate Transformation
↓
Visualization Layer
↓
Streamlit UI

Processing steps

Data Loading

All parquet files for a selected day are merged into a single dataframe to ensure complete match visibility.

Data Cleaning

Event values stored as bytes are converted into strings to enable correct filtering.

Filtering

Data is filtered by:

• Day
• Map
• Match

This ensures only relevant data is visualized and improves performance.

Coordinate Transformation

Game world coordinates are normalized and converted into minimap pixel positions.

Visualization

Plotly renders:

• Map background
• Event markers
• Event categories
• Density visualization
• Match progression view

UI Layer

Streamlit provides:

• Map visualization
• Filters
• Event legend
• Match summary metrics
• Event distribution tables

3. Coordinate Mapping Approach
Problem

Game telemetry uses world coordinates while minimaps use pixel coordinates. A transformation was required to correctly align events.

Solution

Each map uses calibration values:

• origin_x
• origin_z
• scale

Coordinates are normalized:

u = (x − origin_x) / scale
v = (z − origin_z) / scale

Converted to pixel space:

px = u × 1024
py = (1 − v) × 1024

Y-axis inversion was required because image coordinate systems grow downward while world coordinates grow upward.

Result

Events correctly align with minimap locations enabling spatial analysis.

4. Key Features Implemented
Core visualization

• Player position visualization
• Loot event visualization
• Bot kill events
• Storm damage events
• Event categorization

Interaction features

• Day filtering
• Map filtering
• Match filtering
• Event legend

Match exploration

• Event progression slider
• Density visualization (heatmap)
• Match statistics summary

Analytics support

• Event counts
• Player counts
• Event distribution tables

5. Engineering Challenges Solved
Coordinate alignment issue

Problem:

Events initially rendered incorrectly due to Y axis inversion conflict.

Cause:

Axis inversion was applied both during coordinate conversion and plot rendering.

Fix:

Corrected axis range configuration.

Result:

Markers aligned correctly with the minimap.

Background map rendering

Problem:

Map images did not render consistently.

Solution:

Used Plotly layout image rendering with background layering.

Fragmented parquet datasets

Problem:

Match data spread across multiple files.

Solution:

Merged files into a single dataframe before filtering.

Event data inconsistencies

Problem:

Events stored as byte format.

Solution:

Normalized event values into strings before processing.

6. Assumptions Made

Issue — Assumption

Missing world bounds — Manual scale calibration used
No player type flag — Bot classification inferred from events
Map resolution undefined — Minimap dimensions used
Incomplete files possible — Failed reads skipped safely

7. Tradeoffs

Decision — Alternative — Reason

Streamlit — Custom frontend — Faster development
Plotly — Custom rendering — Built-in interactivity
Manual calibration — Automated scaling — Predictability
Pandas — Distributed processing — Dataset manageable
Simple transforms — Complex spatial math — Easier debugging

The architecture prioritizes clarity and reliability over complexity.

8. Performance Considerations

Optimizations implemented:

• Data caching to prevent repeated file reads
• Early filtering to reduce rendering load
• Event grouping to improve plotting performance
• Progressive event display through slider
• Fault tolerance for corrupt files

These decisions ensure smooth interaction despite multiple event datasets.

9. Current Limitations

Current constraints include:

• Bot detection based on heuristics
• No player journey path rendering
• No advanced clustering algorithms
• Manual map calibration required
• No cross-match player tracking

10. Future Improvements

Possible extensions include:

• Player path visualization
• Improved bot classification
• Movement clustering analysis
• Match comparison tools
• Automated coordinate calibration
• Player behavior segmentation

11. Summary

The system transforms gameplay telemetry into spatial insights using a simple visualization pipeline:

Telemetry Data
↓
Structured Events
↓
Filtered Match Data
↓
Spatial Transformation
↓
Interactive Visualization

The architecture focuses on correctness, clarity, and extensibility while enabling fast gameplay analysis for level design decisions.
