import pandas as pd
import database

time1 = pd.Timestamp.now()
# database.update_database(reset_data=True)
print(database.database_info().to_markdown(colalign=("left", "right")))
# print(search_company("petro"))
delta = round((pd.Timestamp.now() - time1).total_seconds(), 1)
print("total time =", delta)
