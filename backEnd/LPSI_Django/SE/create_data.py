import random
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="142857", db="sedatabase")
cursor = conn.cursor()

data = {
    1: "Plot",
    2: "Development",
    3: "Music",
    4: "Release",
    5: "Reception",
    6: "Legacy",
    7: "China",
    8: "Russia",
    9: "America",
    10: "France",
    11: "England"
}

n = 8
# 共生成100条数据
for i in range(100):
    keywords_index = list(set([int(random.gauss(7, 2) % 11 + 1) for _ in range(n)]))
    keywords = []  # 该条数据的关键词
    for index in keywords_index:
        keywords.append(data[index])
    print(keywords)
    length = len(keywords)  # 关键词的个数
    sql = "insert into se_keywordshistory(Keyword1, Keyword2, Keyword3, Keyword4, Keyword5, Keyword6, Keyword7, Keyword8) values("
    for kw in keywords:
        sql += "'" + kw + "'" + ", "
    for l in range(length, 8):
        sql += "NULL, "
    sql = sql.strip(", ") + ");"
    print(sql)
    cursor.execute(sql)
    conn.commit()

cursor.close()
conn.close()
