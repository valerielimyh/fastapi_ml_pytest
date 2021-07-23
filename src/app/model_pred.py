import pickle as pkl
import pandas as pd
import numpy as np
from config import get_settings
from src.utils.helpers import *

# load saved objects 
vect_pca = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/vect_pca.pkl",'rb'))
tfidf_pca = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/tfidf_pca.pkl",'rb'))
scaler = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/scaler.pkl",'rb'))
TFidf = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/TFidf.pkl",'rb'))

trained_vect_cols = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/vect_cols.pkl",'rb'))
trained_tfidf_cols = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/tfidf_cols.pkl",'rb'))
lgbm_cv_model_1 = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/lgbm_cv_model_1.pkl",'rb'))
labelencoder = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/labelencoder.pkl",'rb'))

def process_data_for_model(df):
    df1 = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    df1['tokenized_title'] = df1['title'].apply(lambda x:utils_preprocess_text(x))
    title_and_tags_cols = ['tokenized_title', 'tags']
    for col in title_and_tags_cols:
        df1.loc[df1[col].isnull(), col] = ''
    df1['title_and_tags'] = df1['tokenized_title'] + ', ' + df1['tags']
    corpus = df1['title_and_tags'].astype(str)
    dtm_TFidf = TFidf.transform(corpus)
    
    # convert document-term matrix into a df so that we can combine with original df
    # add `d_` prefix as an identifier for easier filtering later 
    title_and_tags_label = [e[:30]+"..." for e in corpus]
    dtm_TFidf_df = pd.DataFrame(dtm_TFidf.toarray(), index=title_and_tags_label, columns=["d_" + str(i) for i in TFidf.get_feature_names()])
    # quantize values
    dtm_TFidf_df = dtm_TFidf_df.astype(np.float16)
    dtm_TFidf_df['trackID'] = df1['trackID'].values
    numeric_feat = df1.select_dtypes(include = ['float64']).columns
    int_feat = df1.select_dtypes(include = ['int64']).columns
    numeric_feat_and_id = list(int_feat) + list(numeric_feat)
    # combine dtm_TFidf_df with original df
    df2 = df1[numeric_feat_and_id].merge(dtm_TFidf_df, on = 'trackID')
    
    test_vect_cols = [col for col in df2.columns if col.startswith('vect')]
    test_tfidf_cols = [col for col in df2.columns if col.startswith('d_')]
    absent_tfidf_cols = [col for col in trained_tfidf_cols if col not in test_tfidf_cols]
    absent_vect_cols = [col for col in trained_vect_cols if col not in test_vect_cols]
    if len(absent_tfidf_cols) != 0:
        for col in absent_tfidf_cols:
            df2[col] = 0
    else:
        pass

    if len(absent_vect_cols) != 0:
        for col in absent_vect_cols:
            df2[col] = 0
    else:
        pass

    features_to_scale = trained_tfidf_cols + trained_vect_cols
    # apply feature scaling
    X_scaled_cols_df = pd.DataFrame(scaler.transform(df2[features_to_scale].to_numpy().astype(np.float64)), columns=[str(i) + "_scaled" for i in features_to_scale])
    vect_scaled_cols = [str(i) + "_scaled" for i in trained_vect_cols]
    tfidf_scaled_cols = [str(i) + "_scaled" for i in trained_tfidf_cols]

    # apply pca to vect and tfidf cols
    X_test_vect_pca = vect_pca.transform(X_scaled_cols_df[vect_scaled_cols])
    X_test_tfidf_pca = tfidf_pca.transform(X_scaled_cols_df[tfidf_scaled_cols])

    vect_pca_n_components = 10
    tfidf_pca_n_components = 500

    # convert np array to df so as to combine with master_df with non scaled cols
    X_test_vect_pca_df = pd.DataFrame(X_test_vect_pca, columns=["vect_pca_" + str(i) for i in range(vect_pca_n_components)])
    X_test_tfidf_pca_df = pd.DataFrame(X_test_tfidf_pca, columns=["tfidf_pca_" + str(i) for i in range(tfidf_pca_n_components)])

    model_features = [col for col in df2.columns if col not in ('trackID')]
    non_scaled_cols = [col for col in model_features if col not in trained_vect_cols if col not in trained_tfidf_cols if col not in test_vect_cols if col not in test_tfidf_cols]
    
    # # combine our pca df with original df that i didn't scale
    X_test = pd.concat([df2[non_scaled_cols], X_test_vect_pca_df, X_test_tfidf_pca_df], axis=1)
    y_gbm_test_preds = lgbm_cv_model_1.predict(X_test).round(1)
    y_gbm_test_labels = labelencoder.inverse_transform(y_gbm_test_preds)
    results_df =pd.DataFrame({"trackID": df1['trackID'], "title": df1['title'], "predictions": y_gbm_test_labels})
    return results_df