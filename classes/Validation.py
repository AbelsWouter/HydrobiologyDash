import pandas as pd
import numpy as np

class Validations:
    
    # Validate the Collection numbers 
    def collection(collection_data):
        return collection_data.loc[collection_data['externalreference'].str.startswith('2021') == False]

    def taxonstatus(taxonstatus_data):
       return taxonstatus_data.loc[taxonstatus_data['statuscode'].isin([10, 80] ) == False] 
    
    # Oligochaeta count validation
    def oligochaeta(oligochaeta_data):
        externalreference = pd.unique(oligochaeta_data['externalreference'])
        oli_data = []
        for reference in externalreference:
            measuredvalue = oligochaeta_data.loc[(oligochaeta_data['externalreference'] == reference) & (oligochaeta_data['name_tg'] == 'Annelida/Platyhelminthes - Oligochaeta'), 'measuredvalue'].sum()
            calculatedvalue = oligochaeta_data.loc[(oligochaeta_data['externalreference'] == reference) & (oligochaeta_data['name_tg'] == 'Annelida/Platyhelminthes - Oligochaeta'), 'calculatedvalue'].sum()
            if (calculatedvalue > 100) & (measuredvalue < 100):
               oli_data = pd.concat([oligochaeta_data.loc[(oligochaeta_data['name_tg'] == 'Annelida/Platyhelminthes - Oligochaeta') & (oligochaeta_data['externalreference'] == reference)], pd.DataFrame(oli_data)])
            else:
                pass
        return oli_data

    # Chironomidae count validation 
    def chironomidae(chironomidae_data):
        externalreference = pd.unique(chironomidae_data['externalreference'])
        chiro_data = []
        for reference in externalreference:
            measuredvalue = chironomidae_data.loc[(chironomidae_data['externalreference'] == reference) & (chironomidae_data['name_tg'] == 'Insecta (Diptera) - Chironomidae'), 'measuredvalue'].sum()
            calculatedvalue = chironomidae_data.loc[(chironomidae_data['externalreference'] == reference) & (chironomidae_data['name_tg'] == 'Insecta (Diptera) - Chironomidae'), 'calculatedvalue'].sum()
            if (calculatedvalue > 100) & (measuredvalue < 100):
                chiro_data = pd.concat([chironomidae_data.loc[(chironomidae_data['name_tg'] == 'Insecta (Diptera) - Chironomidae') & (chironomidae_data['externalreference'] == reference)], pd.DataFrame(chiro_data)])
            else:
                pass
        return chiro_data

    # Other taxongroups count validation
    def taxongroup(taxongroup_data):
        externalreference = pd.unique(taxongroup_data['externalreference'])
        taxongroup = pd.unique(taxongroup_data['name_tg'])
        group_data = []
        for reference in externalreference:
            for group in taxongroup:
                measuredvalue = taxongroup_data.loc[(taxongroup_data['externalreference'] == reference) & (taxongroup_data['name_tg'] == group), 'measuredvalue'].sum()
                calculatedvalue = taxongroup_data.loc[(taxongroup_data['externalreference'] == reference) & (taxongroup_data['name_tg'] == group), 'calculatedvalue'].sum()
                if (calculatedvalue > 50) & (measuredvalue < 50):
                    group_data = pd.concat([taxongroup_data.loc[(taxongroup_data['name_tg'] == group) & (taxongroup_data['externalreference'] == reference)], pd.DataFrame(group_data)])
                else:
                    pass
        return group_data

    def factor(factor_data):
        externalreference = pd.unique(factor_data['externalreference'])
        factor = factor_data.groupby('externalreference')
        limit_data=[]
        for reference in externalreference:
            factorgroups = factor.get_group(reference)
            calculated = sum(factorgroups['calculatedvalue'])
            measured = sum(factorgroups['measuredvalue'])
            values = calculated / measured
            if factorgroups['limitsymbol'].str.contains('>').any():
                continue
            elif values > 1:
                limit_data = pd.concat([factor_data.loc[(factor_data['externalreference'] == reference)], pd.DataFrame(limit_data)])
        return limit_data

    def missing(missing_current_data, missing_historic_data):
        diff_old = pd.DataFrame(data = np.setdiff1d(np.sort(pd.unique(missing_historic_data['parameter'])), np.sort(pd.unique(missing_current_data['parameter']))), columns = ['parameter'])
        parameters = pd.unique(diff_old['parameter']) 
        old_data = []
        for parameter in parameters:
            old_data = pd.concat([missing_current_data.loc[(missing_current_data['parameter'] == parameter)], pd.DataFrame(old_data)])

        return old_data
            
    def new(new_current_data, new_historic_data):
        diff_new = pd.DataFrame(data = np.setdiff1d(np.sort(pd.unique(new_current_data['parameter'])), np.sort(pd.unique(new_historic_data['parameter']))), columns = ['parameter'])
        parameters = pd.unique(diff_new['parameter'])
        new_data =[]
        for parameter in parameters:
            new_data = pd.concat([new_current_data.loc[(new_current_data['parameter'] == parameter)], pd.DataFrame(new_data)])
        return new_data