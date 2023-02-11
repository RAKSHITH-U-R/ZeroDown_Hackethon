from typing import Union
import psycopg2
from fastapi import FastAPI, HTTPException
import json
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd

cur = None
conn = None
app = FastAPI()
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    load_dotenv()
    global conn
    conn = psycopg2.connect(
        database=os.environ.get('DBNAME'),  # database name
        user=os.environ.get('USER'),  # user name
        password=os.environ.get('PASSWORD'),  # password
        host=os.environ.get('HOST'),  # host
        port=os.environ.get('PORT')  # port number enabled by you
    )
    global cur
    cur = conn.cursor()


@app.on_event("shutdown")
async def shutdown():
    await conn.commit()
    await conn.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def data_processing(data, head):
    data = pd.DataFrame.from_records(data)
    data.columns = head
    column_medians = data.median()
    data = data.fillna(column_medians)
    return data


def score_calc(data):
    head = ['market_id', 'sold_homes_count', 'new_listings_count',
            'homes_sold_over_list_price_count', 'median_sale_to_list_ratio', 'days_to_sell']
    data = data_processing(data, head)
    score = []
    for row in data.index:

        sold_homes_count = data['sold_homes_count'][row]
        new_listings_count = data['new_listings_count'][row]
        homes_sold_over_list_price_count = data['homes_sold_over_list_price_count'][row]
        median_sale_to_list_ratio = data['median_sale_to_list_ratio'][row]
        days_to_sell = data['days_to_sell'][row]

        if new_listings_count != 0 and sold_homes_count != 0 and homes_sold_over_list_price_count != 0 and days_to_sell != 0:

            hotness_score = (sold_homes_count / new_listings_count) * (homes_sold_over_list_price_count /
                                                                       sold_homes_count) * (1 - (median_sale_to_list_ratio)) * (1 / days_to_sell)

            score.append(hotness_score)
    score = sum(score)/len(score)
    return score
# def hotness_calc(data):
#     head = ['market_id', 'sold_homes_count', 'new_listings_count',
#             'homes_sold_over_list_price_count', 'median_sale_to_list_ratio', 'days_to_sell']
#     data = data_processing(data, head)

#     hot_list = {}
#     for row in data.index:

#         sold_homes_count = data['sold_homes_count'][row]
#         new_listings_count = data['new_listings_count'][row]
#         homes_sold_over_list_price_count = data['homes_sold_over_list_price_count'][row]
#         median_sale_to_list_ratio = data['median_sale_to_list_ratio'][row]
#         days_to_sell = data['days_to_sell'][row]

#         if new_listings_count != 0 and sold_homes_count != 0 and homes_sold_over_list_price_count != 0 and days_to_sell != 0:

#             hotness_score = (sold_homes_count / new_listings_count) * (homes_sold_over_list_price_count /
#                                                                        sold_homes_count) * (1 - (median_sale_to_list_ratio)) * (1 / days_to_sell)
#             hot_list.setdefault(int(data['market_id'][row]),
#                                 []).append(hotness_score)
#     for key in hot_list:
#         hot_list[key] = sum(hot_list[key]) / len(hot_list[key])
#     return hot_list


# @app.get("/hotness")
# def hotness():
#     table_name = os.environ.get('METRIC')
#     try:
#         cur.execute(
#             f"SELECT market_id,sold_homes_count,new_listings_count,homes_sold_over_list_price_count,median_sale_to_list_ratio,days_to_sell FROM {table_name}")
#         rows = cur.fetchall()
#         data = hotness_calc(rows)
#         return json.dumps(data)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.get('/market/')
def get_score(market_id: int):
    table_name = os.environ.get('METRIC')
    try:
        cur.execute(
            f"SELECT market_id,sold_homes_count,new_listings_count,homes_sold_over_list_price_count,median_sale_to_list_ratio,days_to_sell FROM {table_name} WHERE market_id = {market_id}")
        rows = cur.fetchall()
        data = score_calc(rows)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
