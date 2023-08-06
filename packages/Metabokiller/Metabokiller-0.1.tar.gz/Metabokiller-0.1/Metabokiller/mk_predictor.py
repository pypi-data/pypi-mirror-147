from signaturizer import Signaturizer
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import joblib
from importlib import resources
import io
import warnings
warnings.filterwarnings('ignore', '.*X does not have valid feature names*', )
warnings.filterwarnings('ignore', '.*signatures are NaN*', )
warnings.filterwarnings('ignore', '.*tensorflow:6*', )

def Feature_Signaturizer(dat):
    sig_df=pd.DataFrame()
    desc=['A','B','C','D','E']
    for dsc in tqdm(desc):
        for i in range(1,6):
            sign = Signaturizer(dsc+str(i),)
            results = sign.predict(dat)
            df=pd.DataFrame(results.signature)
            for clm in list(df.columns):
                df=df.rename(columns={clm:dsc+str(i)+'_'+str(clm)})
            sig_df=pd.concat([sig_df,df],axis = 1)
    sig_df = handle_missing_values(sig_df)
    res = pd.DataFrame()
    res['smiles'] = dat
    res = pd.concat([res,sig_df],axis = 1)
    return res
def handle_missing_values(data):
    print('Handling missing values')
    data = data.replace([np.inf, -np.inf, "", " "], np.nan)
    data = data.replace(["", " "], np.nan)
    for i in data.columns:
        data[i] = data[i].fillna(data[i].mean())
    return data


class model_epigenetic:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Epigenetics_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Epigenetic_svm.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds


class model_apoptosis:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Apoptosis_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Apoptosis_KNN.sav') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        

class model_oxidative:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Oxidative_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Oxidative_mlp.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        

class model_ginstability:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Genomic_Instability_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Genomic_Instabilty_RF.sav') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        
class model_proliferation:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Proliferation_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Proliferation_RF.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        
class model_electrophile:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Electrophile_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Electrophile_MLP.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds

    
def Epigenetics(smi_list):
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m1 = model_epigenetic(Sig_Carcin)
    probs,preds = m1.test_model()
    Feature_data['Epigenetics_0'] = probs[:,0]
    Feature_data['Epigenetics_1'] = probs[:,1]
    Feature_data['Epigenetics_preds'] = preds 
    return Feature_data
def Oxidative(smi_list):
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m2 = model_oxidative(Sig_Carcin)
    probs,preds = m2.test_model()
    Feature_data['Oxidative_0'] = probs[:,0]
    Feature_data['Oxidative_1'] = probs[:,1]
    Feature_data['Oxidative_preds'] = preds
    return Feature_data
def GInstability(smi_list):
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m3 = model_ginstability(Sig_Carcin)
    probs,preds = m3.test_model()    
    Feature_data['GInstability_0'] = probs[:,0]
    Feature_data['GInstability_1'] = probs[:,1]
    Feature_data['GInstability_preds'] = preds
    return Feature_data
def Electrophile(smi_list):
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m4 = model_electrophile(Sig_Carcin)
    probs,preds = m4.test_model() 
    Feature_data['Electrophile_0'] = probs[:,0]
    Feature_data['Electrophile_1'] = probs[:,1]
    Feature_data['Electrophile_preds'] = preds
    return Feature_data
def Proliferation(smi_list):
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m5 = model_proliferation(Sig_Carcin)
    probs,preds = m5.test_model()    
    Feature_data['Proliferation_0'] = probs[:,0]
    Feature_data['Proliferation_1'] = probs[:,1]
    Feature_data['Proliferation_preds'] = preds
    return Feature_data
def Apoptosis(smi_list):
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m6 = model_apoptosis(Sig_Carcin)
    probs,preds = m6.test_model()
    Feature_data['Apoptosis_0'] = probs[:,0]
    Feature_data['Apoptosis_1'] = probs[:,1]
    Feature_data['Apoptosis_preds'] = preds
    return Feature_data
