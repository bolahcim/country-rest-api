from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from googletrans import Translator


translator = Translator()
app = Flask(__name__)
api = Api(app)

#defines db address and access details
client = MongoClient("mongodb://mongo-seed-db:27017", username='admin',password='admin')
#defines name of db to connect to
db = client.country
#defines collection that we are going to use
mycol = db['iso']


class MatchCountry(Resource):
    def post(self):
        # Get posted data
        posted_data = request.get_json()
        # Define variables from request and DB
        iso_in = str(posted_data["iso"])
        country_name_db = mycol.find_one({"iso": iso_in},{"_id": 0,"iso": 0})
        name_out = country_name_db.get('name')
        country_in = posted_data["countries"]
        country_out = []
        y = 0
        # Verify posted data
        status_code = checkPostedData(posted_data, "match_country")
        if status_code!=200:
            ret_json = {
                "Message": "An error occured",
                "Status Code":status_code
            }
            return jsonify(ret_json)
        # Compare received array with saved value for iso
        for x in country_in:
            # Translate received countries
            trans_out = translator.translate(x, dest="en")
            translated_name = str(trans_out.text)
            translated_name = translated_name[0].upper() + translated_name[1:]
            # Compare translation with country name from DB
            if translated_name == name_out:
                country_out.append(country_in[y])
                y = y + 1
            else:
                y = y + 1
        # Count number of suitable results and sent response
        match_count = len(country_out)
        if match_count == 0:
            ret_json = {
                "Message": "No match found",
                "Status Code": 404
            }
            return jsonify(ret_json)
        else:
            ret_map = {
                'iso': iso_in,
                'Status Code': 200,
                'count': match_count,
                'countries': country_out
            }
        return jsonify(ret_map)

class MatchIso(Resource):
    def get(self):
        # Get posted data
        posted_data = request.get_json()

        # Verify posted data
        status_code = checkPostedData(posted_data, "match_iso")
        if status_code!=200:
            ret_json = {
                "Message": "An error occured",
                "Status Code":status_code
            }
            return jsonify(ret_json)

        # Define variables from request
        iso_in = str(posted_data["iso"])

        # Exctract variables from DB
        country_name_db = mycol.find_one({"iso": iso_in},{"_id": 0,"iso": 0})
        name_out = str(country_name_db.get('name'))

        # Count number of suitable results and sent response
        match_count = len(name_out)
        if match_count == 0:
            ret_json = {
                "Message": "No match found",
                "Status Code": 404
            }
            return jsonify(ret_json)
        else:
            ret_map = {
                'iso': iso_in,
                'Status Code': 200,
                'countries': name_out
            }
            return jsonify(ret_map)

# Check if posted data are present
def checkPostedData(posted_data, functionName):
    if functionName == "match_country":
        if "iso" not in posted_data or "countries" not in posted_data:
            return 422 # Missing parameter
        else:
            return 200
    if functionName == "match_iso":
        if "iso" not in posted_data:
            return 422 # Missing parameter
        else:
            return 200 # Found

@app.route('/')
def hello():
    return "Hello, I am available to receive requests!"

api.add_resource(MatchCountry, "/match_country")
api.add_resource(MatchIso, "/match_iso")

if __name__ == "__main__":
    app.run(host ="0.0.0.0")