import pandas as pd

fips = 1017

df = pd.DataFrame.from_csv('data/counties/betas.tsv', sep='\t')
county,state = df.iloc[df.index == fips].location.item().split(", ")


population =3
p_65 = 4
ICU_beds = 5 
density = 6
ensured = 7
risk = 8



"""
fig = go.Figure(data=[go.Table(
    header=dict(values=['Property', 'Value'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[["State","County","Population","Fraction > 65 yr.", "ICU beds", "Density","Ensured","Risk"], # 1st column
                    [95, 85, 75, 95]], # 2nd column
            line_color='darkslategray',
            fill_color='lightcyan',
            align='left')))
"""