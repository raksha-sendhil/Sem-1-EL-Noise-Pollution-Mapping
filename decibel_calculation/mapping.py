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
    [12.922551, 77.500018, 86, "Mingo's Canteen Area"],
    [12.922588, 77.500268, 45, "Library Block"],
    [12.922406, 77.499305, 55, "Gymnasium Construction Site"],
    [12.923075, 77.498496,70,"Mechanical Department Construction Site"],
    [12.9228892,77.4989644,55,"Biotech Quadrangle"],
    [12.9228118,77.4990046,66,"Inside Biotech Quadrangle"],
    [12.922635, 77.499198,45,"CCH"],
    [12.922729, 77.500094,55,"Nursery"],
    [12.923560, 77.499811,60,"MM Foods RVCE"],
    [12.923779, 77.500495,63,"ETE"],
    [12.923460, 77.500765,59,"Old Library"],
    [12.922923, 77.500480,61,"Main MM Foods"],
    [12.922732, 77.500219,61,"RVU Libary Entrance"],
    [12.923646, 77.499874,67,"ECE Department"],
    [12.923646, 77.499874,54,"Outside CSE"],
    [12.923179, 77.498660,55,"IEM Auditorium"],
    [12.923488, 77.497984,57,"In front of DTH"],
    [12.923324, 77.500835,54,"Inside ISE Department"],
    [12.9247933,77.5000059,60,"Civil"],
    [12.924348, 77.500108,59,"EEE"],
    [12.9243367,77.50109,55,"Cauvery"],
    [12.922921, 77.500819,65,"Aerospace"],
    [12.922766, 77.501578,65,"Academic Block"],
    [12.923967, 77.500873,72,"Mess"],
    [12.923241, 77.501287,57,"RVU Main Gate"],
    [12.922330, 77.502134,47,"Chamundi Hostel"],
    [12.922582, 77.498264,49,"Memorial"],
    [12.924982, 77.499903,49,"CSE Ground"],
    [12.924292, 77.498322,71,"Inside Metro Station"],
    [12.924703, 77.500448,50,"CSE New Labs"],
    [12.9224409,77.498848,49,"MCA Department"],
    [12.923835, 77.501509,62,"Mathematics Department"],
    [12.924322, 77.49907,55,"Kotak Lab"],
    [12.924513, 77.498888,55,"Kotak Bank"],
    [12.9245403,77.500595,56,"Health Centre"],
    [12.924632, 77.500938,54,"Temple"],
    [12.923392, 77.500993,59,"Outside ISE"],
    [12.922658, 77.501075,78,"Construction Near ISE"],
    [12.924037, 77.500602,63,"Krishna Hostel"],
    [12.923158, 77.503009,51,"DJ Hostel"],
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
    if db > 50:
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
