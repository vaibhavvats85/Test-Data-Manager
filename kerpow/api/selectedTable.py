from flask_restful import Resource
import logging as logger
from app import mysql
from flask import request, jsonify

class SelectedTable(Resource):

    def TableInfo(self, getValues):
        table = getValues['table']
        cur = getValues['cursor']
        returnValue = []
        
        queryForRecords = 'SELECT COUNT(*) FROM '+table
        cur.execute(queryForRecords)
        noOfRecords = cur.fetchall()

        query = 'SHOW COLUMNS FROM '+table
        resultValue = cur.execute(query)
        columns = cur.fetchall()

        columnList = []
        for c in columns:
            col = {
                'name': c[0],
                'type': c[1]
                 }
            columnList.append(col)
        value = {
                 'noOfRecords' : noOfRecords[0][0],
                 'columns' : columnList,
                 'table' : table
                 }
        return value
    

    def get(self, tableName):
        logger.debug('selected table ',tableName)
        cur = mysql.connection.cursor()
        getValues = {
            'cursor' : cur,
            'table' : tableName,
            'from' : 'SelectedTable'
        }
        
        returnValue = self.TableInfo(getValues)
        cur.close()
        return jsonify(returnValue)