import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from datetime import timedelta

class TestDataGenerator:

    def __init__(self, df, date_col, size, id):
        self.df = df
        self.date_col = date_col
        self.size = size
        self.id = id

    def filterCharColumn(self):
        floatColumns = []
        types = ["object", "bool"]
        columns = self.df.columns
        for col in columns:
            if (self.df[col].dtype in types):
                floatColumns.append(col)
        return self.removeCol(floatColumns, self.date_col)
    
    def filterNumColumn(self): 
        charCols = self.filterCharColumn()
        date_type = self.df[self.date_col].dtype
        cols = list(self.df.select_dtypes(exclude=[date_type]))
        for col in charCols:
            if col in cols:
                cols.remove(col)
        return self.removeCol(cols, self.id)

    def removeCol(self, cols, col_name):
        for col in cols:
            if col == col_name:
                cols.remove(col)
        return cols

    def predictColumn(self, series_col):
        df = self.df.groupby(self.date_col).sum()[series_col]
        model = ARIMA(df, order=(2, 1, 1))
        results_ARIMA = model.fit(disp=-1)

        predictions = results_ARIMA.forecast(steps=self.size)[0]
        pred_Series = round(pd.Series(predictions))

        sdate = pd.to_datetime(df.index[len(df) - 1])
        edate = sdate + timedelta(self.size)
        date_series = pd.date_range(sdate, edate, freq='d').strftime('%d-%m-%Y')[1:]

        df_pred = pd.DataFrame({series_col: pred_Series}).set_index(date_series)
        return df_pred

    def getForecastData(self, columns):
        data = pd.DataFrame()
        for col in columns:
            forecast = self.predictColumn(col)
            data = pd.concat([data, forecast], axis=1)
        return data

    def getRandomColumn(self,columns):
        data = pd.DataFrame()
        for col in columns:
            random = self.df.sample(self.size)[col].str.encode('utf8').reset_index()
            data = pd.concat([data, random], axis = 1)
        return data