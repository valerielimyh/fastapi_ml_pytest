from src.app.model_pred import process_data_for_model
import pandas as pd 
from io import StringIO
from databases import Database
import sqlite3
from config import get_settings

database = Database(f"sqlite:///{get_settings().DB_FOLDER_NAME}")

async def get_genre():
    query = "SELECT DISTINCT(predictions) FROM titles_and_genre"
    
    return await database.fetch_all(query=query)

async def get_titles_by_genre(genre: str):
    query = f"SELECT title FROM titles_and_genre WHERE predictions='{genre}'"
    return await database.fetch_all(query=query)

async def predict(file):
    contents = await file.read()
    s=str(contents,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)
    
    result_df = process_data_for_model(df)
    pending_list_id = result_df['trackID'].values.tolist()

    query = f"SELECT DISTINCT(trackID) FROM titles_and_genre"
    id_in_db_json = await database.fetch_all(query=query)
    list_id_in_db = [item['trackID'] for item in id_in_db_json]

    list_id_to_append = [trackID for trackID in pending_list_id if trackID not in list_id_in_db]
    list_id_to_overwrite = list(set(list_id_in_db).intersection(set(pending_list_id)))

    append_result_df = result_df.loc[result_df['trackID'].isin(list_id_to_append)]
    overwrite_result_df = result_df.loc[result_df['trackID'].isin(list_id_to_overwrite)]

    con = sqlite3.connect(f"{get_settings().DB_FOLDER_NAME}")
    if len(append_result_df) != 0 and len(overwrite_result_df) == 0:
        append_result_df.to_sql('titles_and_genre', con=con, if_exists='append',index=False)
        append_result_json = append_result_df.to_json(orient='records')
        return f'appended new rows to db {append_result_json}'
    elif len(overwrite_result_df) != 0 and len(append_result_df) == 0:
        overwrite_result_json = overwrite_result_df.to_json(orient='records')
        return f'could not append {overwrite_result_json} because data exists in db'
    elif len(append_result_df) != 0 and len(overwrite_result_df) != 0:
        append_result_df.to_sql('titles_and_genre', con=con, if_exists='append',index=False)
        append_result_json = append_result_df.to_json(orient='records')
        overwrite_result_json = overwrite_result_df.to_json(orient='records')
        return f'appended new rows to db \n {append_result_json} \n could not append {overwrite_result_json} because data exists in db'