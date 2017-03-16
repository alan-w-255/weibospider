#%%
import urllib
dir(urllib)
print("hello world")
for x in range(10):
    print("hello world")


#%%
from weibospider.db.db import DB as db

db = db()

db.closeDB()
