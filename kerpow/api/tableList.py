from flask_restful import Resource
import logging as logger
from flask import request, jsonify
import mysql.connector
from .selectedTable import SelectedTable

class TableList(Resource):

    def TestConnectDB(self, r):
        user = r['username']
        password = r['password']
        hosturl = r['hosturl']
        database = r['databasename']
        try:
            db = mysql.connector.connect(
                host = hosturl,
                user = user,
                password = password,
                database = database
            )
            db.close()
        except Exception as e:
            return {'connect' : False}
        return {'connect' : True}
    

    def ConnectDB(self, r):
        user = r['username']
        password = r['password']
        hosturl = r['hosturl']
        database = r['databasename']
        returnValues = []
        try:
            db = mysql.connector.connect(
                host = hosturl,
                user = user,
                password = password,
                database = database
            )
            cur = db.cursor()
            query ="USE "+database
            cur.execute(query)
            cur.execute("SHOW TABLES;")
            data = cur.fetchall()
            for i in data:
                tableName = i[0]
                getValues = {
                    'cursor' : cur,
                    'table' : tableName,
                    'from' : 'tableList'
                    }
                selectTable = SelectedTable()
                value = selectTable.TableInfo(getValues)
                returnValues.append(value)
            cur.close()
            db.close()
        except Exception as e:
            return {'connect' : False}
        return returnValues

    
    def post(self):
        r = request.json
        testDB = r['connect']
        if testDB:
           value = self.ConnectDB(r)
        else:
            value = self.TestConnectDB(r)
        
        return value
