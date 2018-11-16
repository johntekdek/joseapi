from flask import Flask,request
from flask_restful import Resource, Api
from jwt import PyJWT

from security import authenticate,identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = PyJWT(app,authenticate,identity)
items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name']== name,items),None)
        return {'item':item},200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name']== name,items),None) :
            return {'message': "An item with name '{}' already exists.".format(name)},400

        data = request.get_json()
        item = {'name': data['name'], 'price':data['price']}
        items.append(item)
        return item,201


class ItemList(Resource):
    def get(self):
        return {'items':items}


api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items/')

if __name__ == '__main__':

    for item in items:
        print(item)
    app.run(debug=True)
