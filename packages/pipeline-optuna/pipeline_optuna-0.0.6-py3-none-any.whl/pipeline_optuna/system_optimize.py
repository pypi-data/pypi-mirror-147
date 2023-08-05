import numpy as np
import pandas as pd

# reduce memory
def reduce_mem_usage(df):
  start_mem = df.memory_usage().sum() / 1024**2
  print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
  for col in df.columns:
    col_type = df[col].dtype
    name =df[col].dtype.name
    if col_type != object and col_type.name != 'category':
      c_min = df[col].min()
      c_max = df[col].max()
      if str(col_type)[:3] == 'int':
        if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
          df[col] = df[col].astype(np.int8)
        elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
          df[col] = df[col].astype(np.int16)
        elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
          df[col] = df[col].astype(np.int32)
        elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
          df[col] = df[col].astype(np.int64)  
      else:
        if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
          df[col] = df[col].astype(np.float16)
        elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
          df[col] = df[col].astype(np.float32)
        else:
          df[col] = df[col].astype(np.float64)
    else:
      df[col] = df[col].astype('category')
  end_mem = df.memory_usage().sum() / 1024**2
  print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
  print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
  return df

# get dummy data
def get_date_dummy(df, date_column = 'DATE'):
  df = df.sort_values(by = date_column)
  df[date_column] = pd.to_datetime(df[date_column], infer_datetime_format=True)
  df['month'] = df[date_column].dt.month
  df['dayofmonth'] = df[date_column].dt.day
  df['weekofyear'] = df[date_column].map(lambda x:x.isocalendar()[1])
  df['dayofweek'] = df[date_column].map(lambda x:x.dayofweek+1)
  raw_data_dummy = pd.get_dummies(df, columns=[ 'month', 'weekofyear', 'dayofweek', 'dayofmonth'])
  return raw_data_dummy