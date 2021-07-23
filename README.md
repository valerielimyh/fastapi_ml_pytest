# Quickstart


### Clone this repo
```
git clone https://github.com/valerielimyh/fastapi_ml_pytest.git
```
### Navigate to the directory
```
cd fastapi_ml_pytest
```

### Build the images and run the containers:
```
$ docker-compose up -d --build
```
You should see:

```
[+] Building 247.4s (12/12) FINISHED                                                          
 => [internal] load build definition from Dockerfile                                     0.0s
 => => transferring dockerfile: 32B                                                      0.0s
 => [internal] load .dockerignore                                                        0.0s
 => => transferring context: 2B                                                          0.0s
 => [internal] load metadata for docker.io/tiangolo/uvicorn-gunicorn:python3.8           2.9s
 => [auth] tiangolo/uvicorn-gunicorn:pull token for registry-1.docker.io                 0.0s
 => [1/6] FROM docker.io/tiangolo/uvicorn-gunicorn:python3.8@sha256:5d427e4d76d0e3ec57e  0.0s
 => [internal] load build context                                                        0.0s
 => => transferring context: 141.05kB                                                    0.0s
 => CACHED [2/6] WORKDIR /fastapi_ml_pytest                                              0.0s
 => CACHED [3/6] RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/m  0.0s
 => [4/6] COPY ./pyproject.toml ./poetry.lock /fastapi_ml_pytest/                        0.0s
 => [5/6] RUN poetry install --no-root --no-dev                                        242.2s
 => [6/6] COPY . .                                                                       0.2s 
 => exporting to image                                                                   2.0s 
 => => exporting layers                                                                  1.9s 
 => => writing image sha256:a6bb8cd88597181c73daed371039a98d0f6c202f631f55cbaec8419b493  0.0s 
 => => naming to docker.io/library/fastapi_ml_pytest_web                                 0.0s 
                                                                                              
Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 2/2
 ⠿ Container fastapi_ml_pytest_db_1   Started                                            1.9s
 ⠿ Container fastapi_ml_pytest_web_1  Started                                            1.9s
```
Test out the APIs at 
[http://localhost:8080/docs](http://localhost:8080/docs)

You should see:
![fastapi_ml_pytest_docs_landing_page](https://raw.githubusercontent.com/valerielimyh/fastapi_ml_pytest/master/fastapi_ml_pytest_docs_landing_page.jpg)

1. To retrieve a list of titles to a provided genre.
![fastapi_ml_pytest_docs_landing_page.jpg](https://raw.githubusercontent.com/valerielimyh/fastapi_ml_pytest/master/fastapi_ml_pytest_docs_landing_page.jpg)

2. To retrieve a list of classified genres in the database
![fastapi_ml_pytest_docs_get_titles](https://raw.githubusercontent.com/valerielimyh/fastapi_ml_pytest/master/fastapi_ml_pytest_docs_get_titles.jpg)

3. To upload input data (see [test.csv](https://github.com/valerielimyh/multi_features_multiclass_text_classification/blob/master/data/test.csv) as a sample) persist the results and titles into an embedded database (sqlite)
![fastapi_ml_pytest_docs_get_predictions](https://raw.githubusercontent.com/valerielimyh/fastapi_ml_pytest/master/fastapi_ml_pytest_docs_get_predictions.jpg)

	if data doesn't exist in db, new titles and predictions will be appended.
	else, they won't be appended 

### to run the test after building the container
```
$ docker-compose exec web pytest . -p no:warnings
```

You should see:

```
============================ test session starts ============================
platform linux -- Python 3.8.6, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /fastapi_ml_pytest
collected 1 item                                                            

src/tests/test_get_genre.py .                                         [100%]

============================= 1 passed in 4.46s =============================
```

### maintainability and extendibility

1. The current containerized ML web service is a dev env, and is linked to an SQLite DB. To run the web service on a productionized DB, simply change `DB_FOLDER_NAME` in `.env` file with the appropriate `DATABASE_URL` 
2. To add new models, save the model objects in `models` folder and import the file as such, and changing the name and filename of the model. E.g. `lgbm_cv_model_1 = pkl.load(open(f"{get_settings().MODEL_FOLDER_NAME}/lgbm_cv_model_1.pkl",'rb'))`


### To update the image after making changes:
```
$ docker-compose up -d --build
```
