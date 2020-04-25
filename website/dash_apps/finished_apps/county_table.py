import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objs as go

fips = 1017

df = pd.DataFrame.from_csv('data/counties/population/density.tsv', sep='\t')
df_health = pd.DataFrame.from_csv('data/counties/county_health_rankings/county_age.tsv', sep='\t')



county_data = df.loc[df.fips == fips]
county_health_data = df_health.loc[df_health.index == fips]

population = county_data.population.item()
county, state = county_data.location.item().split(', ')

age = county_health_data["percent_65_and_over"].item()
plt.hist(np.log(df["density"].to_numpy()))


demographic = ""
if age < 16.2:
    demographic = "Young"
elif age < 18.8:
    demographic = "Normal"
elif age < 21.7:
    demographic = "Old"
else:
    demographic = "Very old"

logdens = np.log(county_data["density"].item())

if logdens < 2:
    density = "Low"
elif logdens < 6:
    density = "Normal"
else:
    density = "High"


p_65 = demographic
ICU_beds = 5 
ensured = 7
risk = 8


fig = go.Figure(data=[go.Table(
    header=dict(values=['Property', 'Value'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[["State","County","Population","Age demographic", "ICU beds", "Pop. density","Ensured","Risk"], # 1st column
                    [state, county, population, demographic,2,density,2,2]], # 2nd column
            line_color='darkslategray',
            fill_color='lightcyan',
            align='left'))
    ])
fig.show()