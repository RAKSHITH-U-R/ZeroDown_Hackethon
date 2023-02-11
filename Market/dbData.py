import urllib.parse as up
import psycopg2
import pandas as pd


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
                                                                       sold_homes_count) * (1 / days_to_sell) * 1000000

            score.append(hotness_score)
    score = sum(score)/len(score)

    return score


def hotness_calc(data):
    head = ['market_id', 'sold_homes_count', 'new_listings_count',
            'homes_sold_over_list_price_count', 'median_sale_to_list_ratio', 'days_to_sell']
    data = data_processing(data, head)

    hot_list = {}
    for row in data.index:

        sold_homes_count = data['sold_homes_count'][row]
        new_listings_count = data['new_listings_count'][row]
        homes_sold_over_list_price_count = data['homes_sold_over_list_price_count'][row]
        median_sale_to_list_ratio = data['median_sale_to_list_ratio'][row]
        days_to_sell = data['days_to_sell'][row]

        if new_listings_count != 0 and sold_homes_count != 0 and homes_sold_over_list_price_count != 0 and days_to_sell != 0:

            hotness_score = (sold_homes_count / new_listings_count) * (homes_sold_over_list_price_count /
                                                                       sold_homes_count) * (1 / days_to_sell)*1000000
            hot_list.setdefault(str(data['market_id'][row]),
                                []).append(hotness_score)
        else:
            hot_list.setdefault(str(data['market_id'][row]),
                                []).append(0)
    for key in hot_list:
        hot_list[key] = sum(hot_list[key]) / len(hot_list[key])
    # print(hot_list)
    return hot_list


up.uses_netloc.append("postgres")
url = up.urlparse(
    "postgres://xfelfohc:F-fp4eg_sXBTG8evRgiYoIyABFX8y1UY@tiny.db.elephantsql.com/xfelfohc")
conn = psycopg2.connect(database=url.path[1:],
                        user=url.username,
                        password=url.password,
                        host=url.hostname,
                        port=url.port
                        )

# with open("D:\data.txt", "w") as f:
#     # sql = f.read()
#     cur = conn.cursor()
#     # cur.execute(sql)
#     # conn.commit()
#     # print("Insert Complete")
#     cur.execute(
#         f"SELECT market_id,sold_homes_count,new_listings_count,homes_sold_over_list_price_count,median_sale_to_list_ratio,days_to_sell FROM market_metrics")
#     data = cur.fetchall()
#     print("fetch complete")
#     hot_list = hotness_calc(data)
#     print("hotness complete")
#     f.write("INSERT INTO market_hotness(market_id, market_hotness) VALUES")
#     for key in hot_list:
#         sql = f"({key}, {hot_list[key]}),"
#         f.write(sql)


with open("D:\market_hotness.sql", "r") as f:
    sql = f.read()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Insert Complete")
