import os,time,joblib
import numpy as np
import pandas as pd
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
import re

from application.utils.ingestion import fetch_ts

MODEL_DIR = "models"
MODEL_VERSION = 1.0
MODEL_VERSION_NOTE = "FB Prophet model"

def _model_train(df,country,test=False):
    """
    example funtion to train model
    
    The 'test' flag when set to 'True':
        (1) subsets the data
        (2) specifies that the use of the 'test' log file 

    """
    ## start timer for runtime
    time_start = time.time()

    ## Getting data in FB Prophet's format
    df = df[['date', 'revenue']].copy(deep=True)
    df.rename(columns={'date':'ds', 'revenue': 'y'},inplace=True)

    if test:
        n_samples = int(np.round(0.3 * df.shape[0]))
        df = df[-n_samples:]

    ## Perform a train-test split
    n_test = int(np.round(0.2 * df.shape[0]))
    
    df_train = df[:-n_test]
    df_test = df[-n_test:]

    # Train model
    m = Prophet(weekly_seasonality=True)  
    m.fit(df_train)
    
    y_pred = m.predict(df_test)

    eval_rmse =  round(np.sqrt(mean_squared_error(df_test.y.values,y_pred.yhat)))
    
    ## retrain using all data
    m = Prophet(weekly_seasonality=True)  
    m.fit(df)

    model_name = re.sub("\.","_",str(MODEL_VERSION))
    if test:
        saved_model = os.path.join(MODEL_DIR,
                                   "test-{}-{}.joblib".format(country,model_name))
        print("... saving test version of model: {}".format(saved_model))
    else:
        saved_model = os.path.join(MODEL_DIR,
                                   "prod-{}-{}.joblib".format(country,model_name))
        print("... saving model: {}".format(saved_model))
        
    joblib.dump(m,saved_model)

    m, s = divmod(time.time()-time_start, 60)
    h, m = divmod(m, 60)
    runtime = "%03d:%02d:%02d"%(h, m, s)

    ## update log
    print("UPDATE LOG")
    print(country)
    print(df.ds.min())
    print(df.ds.max())
    print(eval_rmse)
    update_train_log(tag,(str(df.ds.min()),str(df.ds.max())),{'rmse':eval_rmse},runtime,
                    MODEL_VERSION, MODEL_VERSION_NOTE,test=True)

def model_train(data_dir,test=False):
    """
    funtion to train model given a df
    """
    
    if not os.path.isdir(MODEL_DIR):
        os.mkdir(MODEL_DIR)

    if test:
        print("... test flag on")
        print("...... subsetting data")
        print("...... subsetting countries")
        
    ## fetch time-series formatted data
    ts_data = fetch_ts(data_dir)

    ## train a different model for each data sets
    for country,df in ts_data.items():
        
        if test and country not in ['all','united_kingdom']:
            continue
        
        _model_train(df,country,test=test)

if __name__ == "__main__":

    """
    basic test procedure for model.py
    """

    ## train the model
    print("TRAINING MODELS")
    data_dir = os.path.join("data","cs-train")
    model_train(data_dir,test=True)

    # ## load the model
    # print("LOADING MODELS")
    # all_data, all_models = model_load(prefix='test')
    # print("... models loaded: ",",".join(all_models.keys()))

    # print("PREDICTING")
    # ## test predict
    # country='all'
    # year='2018'
    # month='01'
    # day='05'
    # result = model_predict(country,year,month,day,test=True)
    # print(result)