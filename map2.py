# imports
import pandas as pd
import folium
import folium.features
import folium.map
import geopandas

# read in the data
borders = geopandas.read_file('states.json')
csvFile = pd.read_csv("tax.csv", thousands=',')
population = pd.read_csv("population.csv", thousands=',')

population['NAME'] = population['NAME'].str[1:]
population['Population'] = pd.to_numeric(population['Population'])

csvFile['Tax'] = csvFile['Tax'].astype('int')

csvFile = csvFile.map(lambda x: x.strip() if isinstance(x, str) else x)

# join csvfile and borders into combined
combined = borders.merge(population.merge(csvFile, on="NAME"), on="NAME")

# creates the default map with zoom to US
m = folium.Map(location=[48, -102], zoom_start=3)

# FOLIUM CREATING VISUALIZATION
# creates the choropleth and names it cp
cp = folium.Choropleth(
    # both geojson data and data come from new_borders
    geo_data=combined,
    data=combined,
    # key is fips, value and color is cases
    columns=["NAME", "Percent"],
    # eliminated as many grey counties as I could
    # for some reason there are still some left
    key_on="feature.properties.NAME",
    # color from colorbrewer
    fill_color="BuPu",
    fill_opacity=0.7,
    line_opacity=0.2,
    # change legend name
    legend_name="Percent of Personal Income Collected as Tax (%)",
    name="choropleth",
).add_to(m) #add to map

# # EXPANSION
# # hover tooltip
folium.features.GeoJsonTooltip(
    # fields displayed and their aliases
        fields=['NAME',
                'Population',
                'TotalTax',
                'Tax',
                'Percent'],
        aliases=['State Name: ',
                 'Population: ',
                 'Total Tax Revenue by State: $',
                 'Average Tax Revenue per Capita: $',
                 'Percent of Personal Income Collected as Tax: ',],
        localize=True,
                ).add_to(cp.geojson) # add to cholopleth's geojson

# add a layercontrol
folium.LayerControl().add_to(m)

# save it as an html
m.save("Tax.html")

print(combined)