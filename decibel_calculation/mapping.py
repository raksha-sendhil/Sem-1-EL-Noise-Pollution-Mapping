import folium
from folium.plugins import HeatMap

# ==========================================
# 1. CONFIGURATION
# ==========================================

# Center of your college (replace with RVCE center coordinates)
COLLEGE_CENTER = [12.9241995,77.4994166]

# Noise sensor data
# Format: [Latitude, Longitude, dB_Level, "Location Name"]
sensor_data = [
    [12.924575, 77.499037, 85, "Main Gate (Traffic)"],
    [12.922551, 77.500018, 65, "Canteen Area"],
    [12.922588, 77.500268, 45, "Library Block"],
    [12.922406, 77.499305, 55, "Gymnasium Construction Site"],
]

# ==========================================
# 2. CREATE BASE MAP
# ==========================================

m = folium.Map(
    location=COLLEGE_CENTER,
    zoom_start=18,
    tiles=None
)

# Satellite view
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satellite View",
    overlay=False,
    control=True
).add_to(m)

# Street view
folium.TileLayer(
    "OpenStreetMap",
    name="Street View",
    overlay=False,
    control=True
).add_to(m)

# ==========================================
# 3. ADD HEATMAP LAYER
# ==========================================

heat_data = [[lat, lon, db] for lat, lon, db, _ in sensor_data]

HeatMap(
    heat_data,
    name="Noise Intensity Heatmap",
    min_opacity=0.4,
    radius=25,
    blur=15,
    max_zoom=18,
).add_to(m)

# ==========================================
# 4. ADD MARKERS
# ==========================================

for lat, lon, db, name in sensor_data:
    color = "green"
    if db > 60:
        color = "orange"
    if db > 80:
        color = "red"

    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>Noise Level: {db} dB",
        icon=folium.Icon(color=color, icon="volume-up", prefix="fa"),
    ).add_to(m)

folium.LayerControl().add_to(m)

# ==========================================
# 5. ADD LEGEND
# ==========================================

legend_html = """
<div style="
    position: fixed;
    bottom: 40px;
    left: 40px;
    width: 220px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 14px;
    padding: 10px;
">
<b>Noise Level (dB)</b><br><br>
<i style="background: green; width: 12px; height: 12px; float: left; margin-right: 8px; opacity: 0.7;"></i>
Quiet (≤ 60 dB)<br>
<i style="background: orange; width: 12px; height: 12px; float: left; margin-right: 8px; opacity: 0.7;"></i>
Moderate (61–80 dB)<br>
<i style="background: red; width: 12px; height: 12px; float: left; margin-right: 8px; opacity: 0.7;"></i>
Loud (> 80 dB)
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# ==========================================
# 6. SAVE MAP
# ==========================================

output_file = "rvce_noise_pollution_map.html"
m.save(output_file)

print(f"Map successfully generated: {output_file}")
print("Open this file in a browser to view the interactive map.")
