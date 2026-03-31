**LILA Black Player Journey Visualization Tool**

**Overview**

This project is a web-based visualization tool built to help Level Designers understand how players interact with maps in LILA Black. The tool converts raw telemetry parquet data into an interactive visualization showing player movement, combat activity, loot interactions, and bot encounters.

The objective is to transform raw gameplay telemetry into an intuitive browser-based tool that designers can use to analyze player behavior and spatial gameplay patterns rather than relying on raw event logs.


**Live Demo**

Tool available at: https://lila-player-journey-tool.streamlit.app


**Features Implemented**

**Core Requirements**

✔ Load and parse parquet gameplay data
✔ Map world coordinates correctly to minimap
✔ Distinguish human players vs bots visually (when present in match data)
✔ Show Position, Loot, BotKilled, Storm events
✔ Filter by day, map, and match
✔ Match progression exploration via event slider
✔ Heatmap showing player activity zones
✔ Interactive visualization with hover details
✔ Map-based gameplay behavior analysis for level design insights


**Visualization Features**

**Player Movement** - Position events show player movement points across the map to help designers understand traversal patterns and frequently visited areas.


**Event Markers**

Color indicates event type:

Blue → Position
Yellow → Loot
Red → BotKilled
Purple → Storm deaths

Marker type:

Circle → Human player
X → Bot

(Note: Some matches may not contain bot entities, so only human markers may appear.)


**Match Progression Control** - Users can filter gameplay events using the progression slider to analyze how matches evolve over time.

**Event Progression** - The slider allows stepping through match events sequentially to observe how player behavior develops during the match.

**Heatmap** - Optional heatmap shows high-traffic areas and potential combat zones to support level design balancing decisions.



**Tech Stack**

Frontend: Streamlit
Visualization: Plotly
Data Processing: Pandas, PyArrow
Language: Python
Deployment: Streamlit Community Cloud


Project Structure

lila-player-journey-tool/

app.py
requirements.txt

README.md
ARCHITECTURE.md
INSIGHTS.md

February_10/
February_11/
February_12/
February_13/
February_14/

minimaps/
AmbroseValley_Minimap.png
GrandRift_Minimap.png
Lockdown_Minimap.jpg

Setup Instructions
Install dependencies

pip install -r requirements.txt

Run locally

streamlit run app.py

App opens at:

http://localhost:8501



Data Processing Approach

Steps:

1 Load parquet files for selected day
2 Decode event column
3 Filter by map and match
4 Convert world coordinates to normalized minimap coordinates
5 Apply match progression filtering
6 Render visualization layers
7 Apply optional heatmap visualization


Bot Detection Logic

The dataset does not explicitly label bots.



Assumption used:

Players that only appear in BotKilled events are treated as bots.

Players with Position or Loot activity are treated as humans.

This reflects typical gameplay telemetry behavior where bots often appear only in combat interactions while human players generate richer event patterns.

Note: Some selected matches may not contain bots, which is why only human markers may appear in certain visualizations.



Coordinate Mapping Logic

World coordinates converted using normalization:

px_norm = (x - origin_x) / scale
py_norm = (z - origin_z) / scale


Converted to minimap coordinates:

px = px_norm * 1024
py = (1 - py_norm) * 1024

The Y-axis inversion ensures alignment between game world coordinates and the minimap image coordinate system.


Assumptions

• Bot identification inferred from activity patterns
• Coordinate scaling derived from provided map configuration
• Missing events treated as non-critical
• Event progression based on event ordering
• Matches may not always contain bot entities


Known Limitations

• Bot detection is inferred (no explicit label available)
• Match progression assumes event ordering is correct
• Heatmap uses density approximation rather than exact clustering
• Player path lines intentionally excluded to avoid visual clutter
• Multi-player interaction analysis not included in current scope


Future Improvements

Potential enhancements:

• Player movement path visualization
• Separate combat vs exploration heatmaps
• Zone clustering analysis
• Player interaction graphs
• Match comparison dashboard
• Advanced bot vs human behavior comparison
