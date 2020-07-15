import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from datetime import timedelta

class TestDataGenerator:

    def __init__(self, df, date_col, size):
        self.df = df
        self.date_col = date_col
        self.size = size

    def filterCharColumn(self):
        floatColumns = [];
        types = ['object', 'bool', 'category']
        columns = self.df.columns
        for col in columns:
            if (self.df[col].dtype in types):
                floatColumns.append(col)
        return self.removeDateCol(floatColumns)


    def removeDateCol(self, cols):
        for col in cols:
            if col == self.date_col:
                cols.remove(col)
        return cols

    def predictColumn(self, series_col):
        df = self.df.groupby(self.date_col).sum()[series_col]

        model = ARIMA(df, order=(2, 1, 2))
        results_ARIMA = model.fit(disp=-1)

        predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)

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
            random = self.df.sample(self.size)[col]
            data = pd.concat([data, random], axis =1)
        return data