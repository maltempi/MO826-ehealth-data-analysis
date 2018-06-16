import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

CSV_KEYS_PRENATAL = {
    'percentageKey': 'Percentual de gestantes com sete ou mais consultas de pré-natal / ano',
    'yearKey': 'Ano',
    'cityCode': 'Código município IBGE',
}

CSV_KEYS_DEATHS = {
    'deathYear': 'ano_obito: Descending',
    'numberOfDeaths': 'Óbitos',
    'cityCode': 'res_codmun_adotado: Descending',
}

CSV_KEYS_BIRTHS = {
    'birthYear': 'ano_nasc: Descending',
    'numberOfBirths': 'Total',
    'cityCode': 'res_codmun_adotado: Descending',
}

CSV_PATHS = {
    'birth': '../fiocruz/birth_grouped_by_year_city/data.csv',
    'deaths': '../fiocruz/deaths_between_0_5_years_grouped_by_age_city_year/data.csv',
    'prenatal': '../dados.gov/prenatal/prenatal_city_year.csv'
}

# Raw data
birthData = pd.read_csv(CSV_PATHS['birth'])
deathsData = pd.read_csv(CSV_PATHS['deaths'])
prenatalData = pd.read_csv(CSV_PATHS['prenatal'])

# filtering by percentage > 0 and year = 2014.
prenatalData = prenatalData.loc[(
    prenatalData[CSV_KEYS_PRENATAL['percentageKey']] > 0.00)]

# filtering Sao Paulo city only
#prenatalData = prenatalData.loc[(
#    prenatalData[CSV_KEYS_PRENATAL['cityCode']] == 355030)]
    
prenatalData = prenatalData.loc[(
    prenatalData[CSV_KEYS_PRENATAL['yearKey']] == 2014)]

birthData[CSV_KEYS_BIRTHS['numberOfBirths']] = pd.to_numeric(birthData[CSV_KEYS_BIRTHS['numberOfBirths']].str.replace(',', ''))
birthData[CSV_KEYS_BIRTHS['birthYear']] = pd.to_numeric(birthData[CSV_KEYS_BIRTHS['birthYear']].str.replace(',', ''))
birthData = birthData.loc[(birthData[CSV_KEYS_BIRTHS['birthYear']] == 2014)]
#birthData = birthData.loc[(birthData[CSV_KEYS_BIRTHS['cityCode']] == 355030)]
    
deathsData[CSV_KEYS_DEATHS['deathYear']] = pd.to_numeric(deathsData[CSV_KEYS_DEATHS['deathYear']].str.replace(',', ''))
deathsData[CSV_KEYS_DEATHS['numberOfDeaths']] = pd.to_numeric(deathsData[CSV_KEYS_DEATHS['numberOfDeaths']].str.replace(',', ''))
deathsData = deathsData.loc[(deathsData[CSV_KEYS_DEATHS['deathYear']] == 2014)]
#deathsData = deathsData.loc[(deathsData[CSV_KEYS_DEATHS['cityCode']] == 355030)]


# Retrieve the IBGE codes to use
#ibgeCodesToUse = prenatalData[CSV_KEYS_PRENATAL['cityCode']].unique()
#ibgeCodesToUse = random.sample(list(ibgeCodesToUse), 100)
ibgeCodesToUse = [355030,330455,530010,292740,230440,310620,130260,410690,261160,431490,520870,150140,351880,350950,211130,330490,270430,330170,240810,500270,221100,354870,250750,330350,354780,354990,353440,260790,354340,317020,355220,311860,280030,291080,510340,420910,313670,411370,520140,110020,150080,320500,330330,330045,330100,320520,420540,430510,160030,352940]

# print(ibgeCodesToUse)

# prenatalData.loc[df['A'] == 'foo']

def getMortalityRate(birthData, prenatalData, deathsData, ibgeCodesToUse):
    tabelao = []
    ## A ideia aqui é gerar um tabelão com dados de morte, dados de prenatal
    ## dados de nascimento por cidade no ano de 2014. 
    ## deathAge: deathSet.iloc[0]['idade_obito: Descending']
    for ibgeCode in ibgeCodesToUse:
        birthsSet = birthData.loc[(
            birthData[CSV_KEYS_BIRTHS['cityCode']] == ibgeCode)]

        deathsSet = deathsData.loc[(
            deathsData[CSV_KEYS_DEATHS['cityCode']] == ibgeCode)]

        prenatalSet = prenatalData.loc[(
            prenatalData[CSV_KEYS_PRENATAL['cityCode']] == ibgeCode)]

        if (birthsSet.empty or deathsSet.empty or prenatalSet.empty):
            print('no good data.. birth:', birthsSet.empty, 'deaths: ', deathsSet.empty, 'prenatal: ', prenatalSet.empty)
            continue

        try:
            numberOfDeaths = int(deathsSet['Óbitos'].sum())
            numberOfBirths = int(birthsSet['Total'].sum())
        except:
            continue

        if (numberOfBirths == 0):
            print('no good data... number of births is zero')
            continue

        tabelao.append({
            'year': 2014,
            'numberOfBirths': numberOfBirths,
            'numberOfDeaths': numberOfDeaths,
            'cityCode': ibgeCode,
            'mortalityRate': (numberOfDeaths * 1000) / numberOfBirths,
            'cityName': deathsSet['Município de residência'].unique()[0],
            'percentagePrenatal': prenatalSet[CSV_KEYS_PRENATAL['percentageKey']].unique()[0]
        })
    
    return tabelao


x = getMortalityRate(birthData, prenatalData, deathsData, ibgeCodesToUse)

#print(x)

#percentagePrenatal = [3, 40, 50, 40, 50, 50, 60, 70,
#                      80, 90, 10, 1, 11, 11, 12, 50,
#                      51, 52, 50, 50]

#mortalityRate = [90, 30, 30, 10, 11, 15, 9, 5,
#                 5, 1, 50, 70, 50, 30, 30, 10,
#                 10, 9, 90, 10]


mortalityRate = [d['mortalityRate'] for d in x]
percentagePrenatal = [d['percentagePrenatal'] for d in x]
cityNames = [d['cityName'] for d in x]

def scatterplot(x_data, y_data, x_label, y_label, title):

    # Create the plot object
    _, ax = plt.subplots()

    # Plot the data, set the size (s), color and transparency (alpha)
    # of the points
    ax.scatter(x_data, y_data, s=30, color='#539caf', alpha=0.75)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    for cityName, x, y in zip(cityNames, x_data, y_data): 
        if (x < 40 and y > 15):
            plt.annotate(
                cityName,
                xy=(x, y), xytext=(-15, -15),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
        
        if (x > 80 and y < 10):
            plt.annotate(
                cityName,
                xy=(x, y), xytext=(20, 20),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))            
            
    plt.show()

# # Call the function to create plot
scatterplot(x_data=percentagePrenatal,
            y_data=mortalityRate,
            x_label='Porcentagem de grávidas que fizeram ao menos 7 pre natal',
            y_label='Taxa mortalidade infantil',
            title='Taxa de Mortalidade infantil x Acesso ao prenatal')
