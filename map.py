# imports
import pandas as pd
import folium
import folium.features
import folium.map
import geopandas

# read in the data
borders = geopandas.read_file('states.json')
csvFile = pd.read_csv("pincome.csv")
population = pd.read_csv("population.csv", thousands=',')

population['NAME'] = population['NAME'].str[1:]
population['Population'] = pd.to_numeric(population['Population'])

# renames the file's county_name into NAME, so it matches with borders
csvFile.rename(columns={"State": "NAME"}, inplace=True)
csvFile.rename(columns={"2023": "PIbS"}, inplace=True)

csvFile = csvFile.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# join csvfile and borders into combined
combined = borders.merge(population.merge(csvFile, on="NAME"), on="NAME")

# add new col with avg
combined['PIbS_avg'] = (combined['PIbS'] / combined['Population']) * 1000000

# creates the default map with zoom to US
m = folium.Map(location=[48, -102], zoom_start=3)

# EXPANSION
# creates bins out of the quantiles of the value
# this makes it proportional to the values instead of flat values
bins = list(combined["PIbS_avg"].quantile([0, 0.40, 0.80, 1]))

# FOLIUM CREATING VISUALIZATION
# creates the choropleth and names it cp
cp = folium.Choropleth(
    # both geojson data and data come from new_borders
    geo_data=combined,
    data=combined,
    # key is fips, value and color is cases
    columns=["NAME", "PIbS_avg"],
    # eliminated as many grey counties as I could
    # for some reason there are still some left
    key_on="feature.properties.NAME",
    # color from colorbrewer
    fill_color="BuPu",
    fill_opacity=0.7,
    line_opacity=0.2,
    # change legend name
    legend_name="Personal Income per Capita by State",
    name="choropleth",
    bins=bins,
).add_to(m) #add to map

# # EXPANSION
# # hover tooltip
folium.features.GeoJsonTooltip(
    # fields displayed and their aliases
        fields=['NAME',
                'Population',
                'PIbS',
                'PIbS_avg'],
        aliases=['State Name: ',
                 'Population: ',
                 'Total Personal Income by State (Millions): ',
                 'Average Personal Income per Person: ',],
        localize=True,
                ).add_to(cp.geojson) # add to cholopleth's geojson

# add a layercontrol
folium.LayerControl().add_to(m)

# save it as an html
m.save("PIbS.html")

print(combined)