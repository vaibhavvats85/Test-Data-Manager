from flask_restful import Api
from app import app
from .login import Login
from .selectedTable import SelectedTable
from .tableList import TableList

restServer = Api(app)

restServer.add_resource(Login, '/login')
restServer.add_resource(SelectedTable, '/selectedTable/<string:tableName>')
restServer.add_resource(TableList, '/tableList')