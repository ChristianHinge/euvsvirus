import pandas as pd
import numpy as np
import plotly.graph_objs as go


def table_fig(fips=1039):
    
    df = pd.read_csv('data/counties/population/density.tsv', sep='\t')
    df_health = pd.read_csv('data/counties/county_health_rankings/county_age.tsv', sep='\t')
    df_beds = pd.read_csv('data/counties/hospital_capacity/beds.tsv', sep='\t')
    df_ensured = pd.read_csv('data/counties/county_health_rankings/county_uninsured.tsv', sep='\t')
    
    
    county_data = df.loc[df.fips == fips]
    county_health_data = df_health.loc[df_health.fips == fips]
    county_uninsured = df_ensured.loc[df_ensured.fips == fips]
    population = county_data.population.item()
    county, state = county_data.location.item().split(', ')
    
    age = county_health_data["percent_65_and_over"].item()    
    
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
    ICU_beds = df_beds.loc[df_beds.fips == fips]["icu_beds"].item()
    ensured = county_uninsured["num_uninsured"].item()/population*100
    risk = 8
    
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Property', 'Value'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[["State","County","Population","Age demographic", "ICU beds", "Pop. density","Un-ensured","Risk"], # 1st column
                        [state, county, population, demographic,round(ICU_beds),density,str(round(ensured,2))+"%",2]], # 2nd column
                line_color='darkslategray',
                fill_color='white',
                align='left'))
        ])
    return fig