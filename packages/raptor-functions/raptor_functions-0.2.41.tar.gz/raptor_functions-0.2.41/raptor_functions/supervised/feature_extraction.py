

import numpy as np
import xgboost as xgb
from boruta import BorutaPy
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import ComprehensiveFCParameters, settings, extract_features
from tsfresh import extract_features, extract_relevant_features, select_features




FEATURES = [ 'exp_unique_id', 'timesteps', 'sensor_1', 'sensor_2',
       'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6', 'sensor_7', 'sensor_8',
       'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12', 'sensor_13',
       'sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18',
       'sensor_19', 'sensor_20', 'sensor_21', 'sensor_22', 'sensor_23',
       'sensor_24', 'result']

TARGET_COL = 'result'

extraction_settings = ComprehensiveFCParameters()



def get_features(df, unique_id='exp_unique_id', label='result', timesteps='timesteps', features=FEATURES):


    df = df[features]

    X = df.drop(label, axis=1)
    y = df.groupby(unique_id).first()[label]

    X = extract_features(X, column_id=unique_id, column_sort=timesteps,
        default_fc_parameters=extraction_settings,
        
        # we impute = remove all NaN features automatically
        impute_function=impute)



    return df, X, y

xgb = xgb.XGBClassifier()

def get_relevant_features(X, y, tree_model=xgb):


    boruta = BorutaPy(
        estimator=tree_model, 
        n_estimators='auto',
        max_iter=100 # number of trials to perform
        )

    ### fit Boruta (it accepts np.array, not pd.DataFrame)
    boruta.fit(np.array(X), np.array(y))
    
    
    # green and blue area are the important features identified by boruta algorithm
    green_area = X.columns[boruta.support_].to_list()
    blue_area = X.columns[boruta.support_weak_].to_list()


    relevant_features = green_area + blue_area
    X = X[relevant_features]
    df = X.join(y)



    return df, X, y











