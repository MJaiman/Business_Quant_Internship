from flask import *
import numpy as np
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('Assignment-Business-Quant.csv')

#Identify last year’s sales for each item and save the values in a new column called “Sales Last Year”
df = df.sort_values(['Item','Year']).reset_index()
df.loc[0,'Sales Last Year'] = np.nan
for i in range(1,df.shape[0]):
    if df.loc[i,'Item']==df.loc[i-1,'Item']:
        df.loc[i,'Sales Last Year'] = df.loc[i-1,'Sales']
    else:
        df.loc[i,'Sales Last Year'] = np.nan

df = df[['Item','Year','Sales','Sales Last Year','Sales Growth %']]

#calculate sales growth for all the items and save the values in a new column titled “Sales Growth”.
df['Sales Growth %'] = df['Sales']/df['Sales Last Year']-1
for i in range(len(df['Sales Growth %'])):
  x=df['Sales Growth %'][i]
  x=str('%.1f'%(x*100))+'%'
  df['Sales Growth %'][i]=x

# Replacing nan with blank
df = df.replace(np.nan, '', regex=True)
df = df.replace('nan%','',regex=True)

@app.route('/')
def home():
    data = dict()
    for col in df.columns:
        data[col] = df[col].values.tolist()
    return render_template("index.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
    app.run(debug=True)


# Code by Mitesh Jaiman