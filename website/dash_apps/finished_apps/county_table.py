import pandas as pd
import numpy as np
import plotly.graph_objs as go

df = pd.read_csv('data/counties/population/density.tsv', sep='\t')
df_health = pd.read_csv('data/counties/county_health_rankings/county_age.tsv', sep='\t')
df_beds = pd.read_csv('data/counties/hospital_capacity/beds.tsv', sep='\t')
df_ensured = pd.read_csv('data/counties/county_health_rankings/county_uninsured.tsv', sep='\t')
df_risk = pd.read_csv("data/counties/simulations/risk_index0.csv")


def table_fig(fips=1039):
    
    global df
    global df_health
    global df_beds
    global df_ensured

    
    county_data = df.loc[df.fips == fips]
    county_health_data = df_health.loc[df_health.fips == fips]
    county_uninsured = df_ensured.loc[df_ensured.fips == fips]
    population = county_data.population.item()
    county, state = county_data.location.item().split(', ')
    county_risk = df_risk.loc[df_risk.fips==fips]
    age = county_health_data["percent_65_and_over"].item()    
    
    county = county.split(" ")[0]

    risk1 = round(county_risk["Risk index"].item(),3)
    risk2 = round(county_risk["Peak ICU/ICU beds"].item(),3)
    risk3 = round(county_risk["Fatalities/population"].item(),3)
    risk4 = round(county_risk["Fatalities"].item(),3)

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
        columnwidth=[25, 30],
        header=dict(values=['<b>Property</b>', '<b>Value</b>'],
                    line_color='darkslategray',
                    fill_color='rgb(255, 109, 90)',
                    align='left',
                    font_size=20,
                    height=32,
                    font_color='white',),
        cells=dict(values=[["State","County","Population","Demographic", "ICU beds", "Pop. density","Uninsured","Risk: Combined","Risk: Intensive care","Risk: Mortality","Risk: Total fatalities"], # 1st column
                        [state, county, population, demographic,round(ICU_beds),density,str(round(ensured,2))+"%",risk1,risk2,risk3,risk4]], # 2nd column
                line_color='darkslategray',
                fill_color='white',
                align='left',
                font_size=18,
                height=30),)
        ],
        layout=go.Layout(
            margin=dict(t=0,r=0,l=0,b=0),
            ))
    return fig