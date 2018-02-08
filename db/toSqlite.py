import sqlite3

# 如果不存在diming.sqlite 则会自动在当前路径创建
conn = sqlite3.connect('diming.sqlite')
cursor = conn.cursor()

QUERY_CREATE_DIMING_TABLE = """
create table diming(name varchar(20) not null, df int not null);
"""

# 执行sql语句
cursor.execute(QUERY_CREATE_DIMING_TABLE)

QUERY_INSERT_DIMING = """
insert into diming(name, df) values ("{}", {});
"""

with open("./THUOCL_diming.txt", 'r', encoding="utf8") as f:
    while True:
        _s = f.readline().strip('\n')
        if _s:
            _s = _s.split('\t')
            print(QUERY_INSERT_DIMING.format(_s[0], _s[1]))
            cursor.execute(QUERY_INSERT_DIMING.format(_s[0], _s[1]))
            continue
        break

# 提交事务
conn.commit()

# 关闭连接
conn.close()