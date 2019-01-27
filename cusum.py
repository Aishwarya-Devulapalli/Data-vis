import pandas as pd
import numpy as np
#import datetime
import collections
from itertools import zip_longest as zip
import csv



def f(x):
    return pd.Series(dict(Pageviews = "{%s}" % x,
                          Date = x['Date'] ))

def calc_cusum(csum):

 #event = {}
 event = collections.defaultdict(dict)
 for row in csum:
  c = []

  page = csum[row]
  m = np.mean(page['Views'])
  std = np.std(page['Views'])
  ucl = m + 2*std

  # print("mean =",m,"ucl=",ucl)
  for i, x in enumerate(page['Views']):
   T = (x-m)+c[i-1] if i>0 else x-m
   if (m/2 > T):
    c.append(m/2)
   else:
    c.append(T)

   if c[i] > ucl:  #Event start
    try:
     event[row]['Date'].append(page['Date'][i])
     event[row]['Views'].append(page['Views'][i])
    except KeyError:
     event[row]['Date'] = [page['Date'][i]]
     event[row]['Views'] = [page['Views'][i]]

 return event


i = 0
headers = ["Page", "Pageviews", "Date"]
df = pd.DataFrame(columns=headers)
df1 = pd.DataFrame()
#df_final = df_final.fillna(0)

ext = '.csv'
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
while i <= 11:

 file_name = r"D:\College\Sem1\DV\Project\PageViews2017" + "\\" + months[i] + "\\" + months[i] +ext
 df_temp = pd.read_csv(file_name, index_col=False) # header=0)#, header = None)
 df1 = df1.append(df_temp)

 i = i+1
#  df.to_csv(file_name, index = False)
df_dup = pd.concat(g for _, g in df1.groupby("Page") if len(g) > 1)
#df_final['Pageviews'] = df.groupby('Page').Pageviews.apply(lambda x: "[%s]" % x)
#df_unique = df_dup.groupby('Page').Pageviews.agg('sum')
#print(df_dup) #["Pageviews"])

#df_final = df_dup.groupby('Page')['Date'].apply(lambda x: "{%s}" % ', ' .join(x))

prev = ""
csum = collections.defaultdict(dict)

for row in df_dup.itertuples():
#  if prev == "":
#   prev = row.Index
#print(row.Page)
#  if prev == row.Index:
 try:
  csum[row.Page]['Views'].append(row.Pageviews)
  csum[row.Page]['Date'].append(row.Date)
 except KeyError:
  csum[row.Page]['Views'] = [row.Pageviews] #, 'Date': row.Date}]
  csum[row.Page]['Date'] = [row.Date]

cusum = calc_cusum(csum)
file_n = r"PageViews2017\cusum.csv"

with open(file_n, "w", newline='', encoding="utf-8") as f:
    wr = csv.writer(f)  # delimiter= ' ')
    wr.writerow(headers)
    for r, i in enumerate(cusum):
     for (d, v) in zip(cusum[i]['Views'], cusum[i]['Date']):
      row = []
      row.append(i)
      row.append(d)
      row.append(v)
      wr.writerow(row)

f.close()

df_cusum = pd.read_csv(file_n, index_col= False)
df_cdup = pd.concat(g for _, g in df_cusum.groupby("Page") if len(g) > 10)


file_c = r"PageViews2017\cusum_filter.csv"
df_cdup.to_csv(file_c, index= False)
