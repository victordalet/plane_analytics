# plane_analytics


## Install dependencies

```bash
pip install -r requirements.txt
```

## Launch apps

```bash
streamlit run src/app/app.py
```

## Launch on docker

- create a folder `data` in `docker/` & put the flights.csv file in it

```bash
cd docker
docker compose up -d 
docker compose exec -it namenode bash
hdfs dfs -mkdir -p /user/data
hdfs dfs -put data/flights.csv /user/data
hdfs dfs -put data/airlines.csv /user/data
hdfs dfs -put data/airports.csv /user/data
```