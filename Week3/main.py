#%%
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import numpy as np

#%%
ecoupon = pd.read_csv("./Dataset/ECoupon.csv", dtype="unicode")
ecoupon.head()

#%%
member = pd.read_csv("./Dataset/Member.csv", dtype="unicode")
member.head()

#%%
order = pd.read_csv("./Dataset/Orders.csv", dtype="unicode")
order.head()

#%%
promotion_condition = pd.read_csv("./Dataset/PromotionConditions.csv", dtype="unicode")
promotion_condition.head()

#%%
promotion_order = pd.read_csv("./Dataset/PromotionOrders.csv", dtype="unicode")
promotion_order.head()

#%%
register = member["RegisterSourceTypeDef"].value_counts()

#%%
fig = plt.figure(figsize=(15, 7))
ax = fig.add_subplot(111)

#%%
#以橫向柱狀圖顯示使用者性別分布
gender = member["GenderTypeDef"].value_counts()
gender.plot.barh()
plt.show()

#計算使用者性別比例
gender = gender.to_frame().reset_index().rename(columns= {"index": "Gender", "GenderTypeDef": "Counts"})
gender["Percentage"] = None
gender["Percentage"].iloc[0] = gender["Counts"].iloc[0]/(gender["Counts"].iloc[0]+gender["Counts"].iloc[1])
gender["Percentage"].iloc[1] = gender["Counts"].iloc[1]/(gender["Counts"].iloc[0]+gender["Counts"].iloc[1])
gender.head()
##91APP的目標族群為女性，佔所有用戶的 98.8%，男性則僅佔 1.12%

#%%
#以橫向柱狀圖顯示使用者使用平台分布
register = member["RegisterSourceTypeDef"].value_counts()
register.plot.barh()
plt.show()

#計算使用者使用平台比例
register = register.to_frame().reset_index().rename(columns= {"index": "Platform", "RegisterSourceTypeDef": "Counts"})
register["Percentage"] = None
total_register = register["Counts"].sum()
register["Percentage"].iloc[0] = register["Counts"].iloc[0]/total_register
register["Percentage"].iloc[1] = register["Counts"].iloc[1]/total_register
register["Percentage"].iloc[2] = register["Counts"].iloc[2]/total_register
register.head()
##91APP多數使用者使用網頁進行消費，Android則稍多餘iOS用戶數

#%%
min_order = member["MinOrderDate"].value_counts().to_frame().reset_index().rename(columns= {"index": "Date", "MinOrderDate": "Counts"})
min_order["Date"] = pd.to_datetime(min_order["Date"])
min_order.sort_values(by=["Date"], inplace=True, ascending=True)
min_order.reset_index().drop(columns="index")
plt.figure(figsize=(15,7))
plt.plot(min_order["Date"], min_order["Counts"])

#%%
last_birthday = member["LastBirthdayPresentYear"].value_counts()
last_birthday.sort_index(inplace=True, ascending=True)
plt.figure(figsize=(15,7))
last_birthday.plot.barh()
plt.show()

last_birthday = last_birthday.to_frame().reset_index().rename(columns= {"index": "Year", "LastBirthdayPresentYear": "Counts"})
last_birthday["Percentage"] = None
total_last_birthday = last_birthday["Counts"].sum()
last_birthday["Percentage"].iloc[0] = last_birthday["Counts"].iloc[0]/total_last_birthday
last_birthday["Percentage"].iloc[1] = last_birthday["Counts"].iloc[1]/total_last_birthday
last_birthday["Percentage"].iloc[2] = last_birthday["Counts"].iloc[2]/total_last_birthday
last_birthday["Percentage"].iloc[3] = last_birthday["Counts"].iloc[3]/total_last_birthday
last_birthday.head()