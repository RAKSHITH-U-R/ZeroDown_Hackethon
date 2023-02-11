with open("D:\market_hotness.sql", "r") as f:
    sql = f.read()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Insert Complete")