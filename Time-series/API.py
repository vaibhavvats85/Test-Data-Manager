import pandas as pd
from MySql_connector import MySqlConnection
from Test_Data_Generator import TestDataGenerator
import numpy as np
from sqlalchemy import create_engine
from flask_cors import CORS
from flask import Flask, request, jsonify
app = Flask(__name__)

CORS(app)


@app.route('/generate', methods=['POST'])
def generateData():
    body = request.get_json()
    table = body["table"]
    size = body["noOfRecords"]
    date_col = body["date_column"]
    id = body["id"]
    recordStmt = "select * from " + table
    columnStmt = "show columns from " + table
    maxKey = "select MAX('" + id + "') from " + table
    connect = MySqlConnection(
        host=body["hosturl"],
        user=body["username"],
        password=body["password"],
        database=body["databasename"]
    )
    maxKey = connect.getRecords(maxKey, 'all')
    maxKey = maxKey[0][0]

    records = connect.getRecords(recordStmt, 'all')

    columns = connect.getRecords(columnStmt, 'all')
    colNames = np.array(columns)[:, 0]

    data = pd.DataFrame(records, columns=colNames)
    data.dropna()

    test_data = TestDataGenerator(data, date_col, size, id)

    object_columns = test_data.filterCharColumn()
    ran_data = test_data.getRandomColumn(object_columns)

    int_columns = test_data.filterNumColumn()
    pred_data = test_data.getForecastData(int_columns)
    pred_data = pred_data.reset_index().rename(columns={'index': date_col})
    # generate keys
    key_column = pd.DataFrame()
    maxId = data[maxKey].max();
    if id:
        key_list = list(range(maxId+1, maxId+size+1))
        key_column = pd.DataFrame({body["id"]: key_list})

    # remove index
    ran_data = ran_data.reset_index()
    response = pd.concat([key_column, pred_data,ran_data], axis=1)

    engine = create_engine("mysql://root:root@localhost/time_series")
    con = engine.connect()

    # Drop index columns
    response = response.drop(columns=['index','level_0'])
    response.to_sql(name='test_data', con=con,
                    if_exists='replace', index=False)
    response = {
        "noOfRecords": response.shape[0],
        "data": response.to_json(orient='records')
    }
    return response


@app.route('/confirm', methods=['GET', 'POST'])
def confirmData():
    body = request.get_json()

    connection = body['connection']
    updateCol = body['info']
    table = connection['table']
    id = connection['id']
    connect = MySqlConnection(
        host=connection["hosturl"],
        user=connection["username"],
        password=connection["password"],
        database=connection["databasename"]
    )
    stmts = []
    for col in updateCol:
        print(id)
        stmt = """UPDATE test_data SET `%s` = %s WHERE `%s` = %s""" % (
            col['column'], col['value'], id, col['id'])
        print(stmt);
        stmts.append(stmt)
        connect.mydb.cursor(buffered=True).execute(stmt)
        connect.mydb.commit()
    test_record_stmt = "Select * from test_data"
    test_column_stmt = 'Show columns from  test_data'
    test_records = connect.getRecords(test_record_stmt, 'all')
    test_columns = connect.getRecords(test_column_stmt, 'all')
    columns = np.array(test_columns)[:, 0]
    columns = ', '.join('`{0}`'.format(w) for w in columns[columns != 'index'])
    for record in test_records:
        print("""Insert into `%s` (%s) Values %s""" %
              (table, columns, record))
        connect.mydb.cursor(buffered=True).execute(
            """Insert into `%s` (%s) Values %s""" % (table, columns, record))
        connect.mydb.commit()

    return str(columns)


if __name__ == '__main__':
    app.run(port=8080)
