import pandas as pd
from MySql_connector import MySqlConnection
from Test_Data_Generator import TestDataGenerator
import numpy as np
from flask import Flask, request, jsonify
app = Flask(__name__)



@app.route('/generate',methods = ['POST'])
def generateData():
    # body = request.get_json()
    body = {
	"table": "atm_data",
	"date_column": "Transaction Date",
	"record_size": 200,
	"id": "primary key"
}
    table = body["table"]
    size = body["record_size"]
    date_col = body["date_column"]
    # id = body["id"]
    recordStmt = "select * from " + table
    columnStmt = "show columns from " +  table
    # maxKey = "select MAX( " + id + " ) from " + table
    maxKey = 120
    connect = MySqlConnection(host='localhost', port=3306, user='root', password='root', database='time_series')
    records = connect.getRecords(recordStmt, 'all')

    columns = connect.getRecords(columnStmt, 'all')
    colNames = np.array(columns)[:, 0]

    data = pd.DataFrame(records, columns=colNames)

    test_data = TestDataGenerator(data, date_col, size)
    int_columns = test_data.filterNumColumn()
    pred_data = test_data.getForecastData(int_columns)
    pred_data = pred_data.reset_index().rename(columns={'index': date_col})

    object_columns = test_data.filterCharColumn()
    ran_data = test_data.getRandomColumn(object_columns)

    # generate keys
    key_list = list(range(maxKey,maxKey+size))
    key_column = pd.DataFrame({body["id"]:key_list})

    # remove index
    ran_data = ran_data.reset_index()
    response = pd.concat([key_column,pred_data, ran_data], axis=1)

    # Drop index columns
    response = response.drop(columns=['index'])
    print(response.to_json(orient='records'))
    return response.to_json(orient='records')

if __name__ == '__main__':
    app.run(port=8080)
