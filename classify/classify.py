#%%
from flashtext.keyword import KeywordProcessor
import sqlite3

keyword_processor = KeywordProcessor()

conn = sqlite3.connect('./diming.sqlite')
cursor = conn.cursor()

QUERY_DIMING = """
select name from diming;
"""

# 执行sql语句
cursor.execute(QUERY_DIMING)
v = cursor.fetchall()
print(v)


# 提交事务
conn.commit()

# 关闭连接
conn.close()