import pandas as pd
import numpy as np


class Question1:
    energy = {}
    GDP = {}
    ScimEn = {}

    def __init__(self):
        energy = {}
        GDP = {}
        ScimEn = {}
    def petajoulToGigajoulConversion(self, data):
        data['Energy Supply'] *= 1000000
        return data


    def load_energy_data(self):
        energy = pd.read_excel("Energy Indicators.xls", header=None, skip_footer=2)
        energy = (energy.drop([0, 1], axis=1).dropna().rename(columns={2: 'Country', 3: 'Energy Supply', 4: 'Energy Supply per Capita', 5: '% Renewable'}).replace(to_replace=["...", "Republic of Korea", "United States of America", "United Kingdom of Great Britain and Northern Ireland","China, Hong Kong Special Administrative Region"], value=[np.NaN, "South Korea", "United States", "United Kingdom", "Hong Kong"]).apply(self.petajoulToGigajoulConversion, axis=1,)).replace(regex=True, to_replace=[r'\d', r' \(([^)]+)\)'], value=r'')
        self.energy = energy


    def load_gdp_data(self):
        gdp = pd.read_csv("worldbank.csv", header=None, skiprows=4)
        gdp = gdp.drop(0).rename(columns=gdp.iloc[0]).replace(to_replace=["Korea, Rep.", "Iran, Islamic Rep.", "Hong Kong SAR, China"], value=["South Korea", "Iran", "Hong Kong"]).rename(columns = {2006.0: '2006', 2007.0: '2007', 2008.0: '2008', 2009.0: '2009', 2010.0:'2010',2011.0: '2011', 2012.0: '2012', 2013.0: '2013', 2014.0: '2014', 2015.0: '2015', 2016.0: '2016', 2017.0: '2017', 2018.0: '2018'})
        self.GDP = gdp

    def load_scimagojr(self):
        self.ScimEn = pd.read_excel('scimagojr.xlsx')

    def join_data(self):
        self.load_gdp_data()
        self.load_energy_data()
        self.load_scimagojr()
        gdp_columns = ['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
        self.GDP = self.GDP[gdp_columns]
        self.ScimEn = self.ScimEn[:15]
        merged = pd.merge(self.energy, self.GDP, how = 'inner', left_on = 'Country', right_on = 'Country Name').drop(['Country Name'],  axis = 1)
        merged = pd.merge(merged, self.ScimEn, how = 'inner', left_on = 'Country', right_on = 'Country').set_index('Country')
        result_columns = ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
        merged = merged[result_columns]
        
if __name__ == "__main__":
    # load_energy_data()
    question = Question1()
    question.join_data()
    

