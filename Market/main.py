from typing import Union
import psycopg2
from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv


cur = None
conn = None
app = FastAPI()
# origins = [
#     "http://localhost:3000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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


@app.get("/details/")
def details():
    table_name = os.environ.get('MARKET')
    try:
        Hotness_Score = (Demand_Score * Demand_Weight) + \
            (Supply_Score * Supply_Weight)
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def hotness_calc(data):
    hot_list = []
    for row in data:
        sold_homes_count = row[1]
        new_listings_count = row[2]
        homes_sold_over_list_price_count = row[3]
        median_sale_to_list_ratio = row[4]
        days_to_sell = row[5]
        if new_listings_count != 0 and sold_homes_count != 0 and days_to_sell != 0:
            hotness_score = (sold_homes_count / new_listings_count) * (homes_sold_over_list_price_count /
                                                                       sold_homes_count) * (1 - (median_sale_to_list_ratio)) * (1 / days_to_sell)
            hot_list.append([row[0], hotness_score])
    return hot_list


@app.get("/hotness")
def hotness():
    table_name = os.environ.get('METRIC')
    try:
        cur.execute(
            f"SELECT market_id,sold_homes_count,new_listings_count,homes_sold_over_list_price_count,sold_homes_count,median_sale_to_list_ratio,days_to_sell FROM {table_name}")
        rows = cur.fetchall()
        data = hotness_calc(rows)
        print(sorted(data, key=lambda x: x[0]))
        return sorted(data, key=lambda x: x[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
