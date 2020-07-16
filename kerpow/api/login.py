from flask_restful import Resource
import logging as logger
from app import mysql
from flask import request, jsonify


class Login(Resource):

    def post(self):
        logger.debug('login')
        r=request.json
        email=r['user']
        password=r['password']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM users where email= %s and password = %s;",(email,password))
        if resultValue > 0:
            userDetails = cur.fetchall()
            user = {
                    'user': userDetails[0][0],
                    'email': userDetails[0][1],
                    'createdOn': userDetails[0][3]
                    }
        cur.close()
        return jsonify(user)