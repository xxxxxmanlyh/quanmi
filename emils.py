import pandas as pd
from pandas import DataFrame

data = pd.read_excel('圈米资料.xlsx')

# data.loc[5,8] = '已完成'

# data.loc[data[5,8] == 'null'] = '已完成'


print(data['状态'].count())

# num = data.iloc[:,0].size


# print(data.columns.size)
# print(data.iloc[:,0].size)


