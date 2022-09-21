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

        # Verify posted data
        status_code = checkPostedData(posted_data, "match_country")
        if status_code != 200:
            ret_json = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        # Define variables from request for iso validation
        iso_in = str(posted_data["iso"])
        iso_in = iso_in.lower()

        # Chose alpha2 or alpha3 based on length of iso_in
        if len(iso_in) == 2:
            country_name_db = mycol.find_one({"iso2": iso_in},{"_id": 0,"iso2": 0,"iso3": 0})
        elif len(iso_in) == 3:
            country_name_db = mycol.find_one({"iso3": iso_in},{"_id": 0,"iso2": 0,"iso3": 0})
        else:
            return 400

        # Define name_out and check if there are more values in DB
        name_out = country_name_db.get('name')
        if isinstance(name_out, str):
            name_out = [name_out]
        else:
            name_out = name_out
        country_in = posted_data["countries"]
        country_out = []

        # Compare received array with saved value for iso
        for name in name_out:
            y = 0
            for x in country_in:
                # Translate received countries
                trans_out = translator.translate(x, dest="en")
                translated_name = str(trans_out.text)
                translated_name = translated_name.lower()
                # Compare translation with country name from DB
                if translated_name == name:
                    country_out.append(country_in[y].lower())
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

# Check if posted data are present
def checkPostedData(posted_data, functionName):
    if functionName == "match_country":
        if "iso" not in posted_data or "countries" not in posted_data:
            return 422 # Missing parameter
        else:
            return 200

@app.route('/')
def hello():
    return "Hello, I am available to receive requests!"

api.add_resource(MatchCountry, "/match_country")

if __name__ == "__main__":
    app.run(host ="0.0.0.0")