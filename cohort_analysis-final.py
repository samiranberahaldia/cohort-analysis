#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

import missingno as msno
from textwrap import wrap


# In[2]:


transaction_df = pd.read_excel('transaction.xlsx')
print(transaction_df.shape)
transaction_df.head().T


# In[3]:



for col in ['order_status','brand','product_line','product_class','product_size']:
    print(col, transaction_df[col].unique())
    


# In[4]:


df         = transaction_df.copy()
stats      = [df.isna().sum(), df.count(), df.nunique(),df.dtypes, df.min(), df.median(), df.max(), df.skew()]
stats_name = {0:'missing', 
              1:'total', 
              2:'unique', 
              3:'dtypes', 
              4:'minimum', 
              5:'median', 
              6:'maximum', 
              7:'skewness'}

df_info = pd.DataFrame(stats).T.rename(columns=stats_name)
df_info


# In[5]:


import pandas as pd
import seaborn as sns
from tqdm.notebook import tqdm
import warnings
warnings.simplefilter('ignore')
tqdm.pandas()


# In[6]:



def prepare_data(df, select_columns):
    df             = df[select_columns]
    df['margin']   = df['list_price'] - df['standard_cost']
    return df

df = pd.read_excel('transaction.xlsx')
select_columns = ['transaction_date', 'customer_id','list_price','standard_cost']
df = prepare_data(df, select_columns)
df.head(2)


# In[7]:



def get_cohort_timestamp(df, col_name, new_col_name):
    transaction_year  = df[col_name].dt.year
    transaction_month = df[col_name].dt.month
    df[new_col_name]  = [dt.datetime(i,j,1) for i,j in zip(transaction_year, transaction_month)]
    
    return df

df = get_cohort_timestamp(df, 'transaction_date', 'cohort_timestamp')
df.head()


# In[8]:



def add_cohort_index(df, transaction_column, cohort_column, focus_column):
    gpy_info           = df.groupby(by = focus_column).min()[cohort_column].reset_index()
    df                 = df.drop(columns = cohort_column).merge(gpy_info, on=focus_column)
    year_diff          = df[transaction_column].dt.year  - df[cohort_column].dt.year
    month_diff         = df[transaction_column].dt.month - df[cohort_column].dt.month
    df['cohort_index'] = [12*i + j + 1 for i, j in zip(year_diff, month_diff)]
    return df


df = add_cohort_index(df, 'transaction_date', 'cohort_timestamp', 'customer_id')    
df.head()


# In[9]:



def plot_heatmap(df, title=''):
    plt.figure(figsize=(15,7))
    plt.title(title)
    sns.heatmap(df, cmap='YlGnBu', annot=True, fmt='g')
    plt.show()
    


# In[10]:



def get_chort_chart(df, row, column, value, function):
    
    if function == 'customer_retention_by_orders':
        table  = df.groupby(by = [row, column]).nunique()[value]
             
    elif function in ['customer_retention_by_revenue', 'customer_retention_by_profit']:
        table  = df.groupby(by = [row, column]).sum()[value]
    
    data     = pd.DataFrame(table).reset_index()
    absolute = data.pivot(index = row, columns = column, values=value)
    ratio    = round(absolute.divide(absolute.iloc[:,0], axis=0)*100,2)

    plot_heatmap(absolute, function+' (Absolute)')
    plot_heatmap(ratio, function+' (Ratio)')
        

get_chort_chart(df, 'cohort_timestamp','cohort_index', 'customer_id', 'customer_retention_by_orders')    
get_chort_chart(df, 'cohort_timestamp','cohort_index', 'list_price' , 'customer_retention_by_revenue')    
get_chort_chart(df, 'cohort_timestamp','cohort_index', 'margin'     , 'customer_retention_by_profit')    


# In[ ]:





# In[ ]:




