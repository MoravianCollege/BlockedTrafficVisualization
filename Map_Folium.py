# import the library
import folium
import pandas as pd

# Make a data frame with dots to show on the map
data = pd.DataFrame({
    'lat': [-58, 2, 145, 30.32, -4.03, -73.57, 36.82, -38.5],
    'lon': [-34, 49, -38, 59.93, 5.33, 45.52, -1.29, -12.97],
    'name': ['Buenos Aires', 'Paris', 'melbourne', 'St Petersbourg', 'Abidjan', 'Montreal', 'Nairobi', 'Salvador'],
    'value': [10, 12, 40, 70, 23, 43, 100, 43]
})
data

# Make an empty map
m = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)

# I can add marker one by one on the map
for i in range(0, len(data)):
    folium.Circle(
        location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
        popup=data.iloc[i]['name'],
        radius=data.iloc[i]['value'] * 10000,
        color='crimson',
        fill=True,
        fill_color='crimson'
    ).add_to(m)

# Save it as html
m.save('mymap.html')
