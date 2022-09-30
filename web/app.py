from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from googletrans import Translator
import country_converter as coco

translator = Translator()
app = Flask(__name__)
api = Api(app)

class MatchCountry(Resource):
    def post(self):
        # Get posted data
        posted_data = request.get_json()

        # Verify posted data
        status_code = checkPostedData(posted_data, "match_country")
        if status_code != 200:
            ret_json = {
                "Message": "Missing parameter",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        # Define variables from request for ISO validation
        iso_in = str(posted_data["iso"])
        iso_in = iso_in.lower()
        special_char = ''.join(filter(str.isalnum, iso_in))

        # Validate ISO
        name_out = coco.convert(names=iso_in, to='name_official').lower()
        if name_out != "not found":
            pass
        else:
            ret_json = {
                "Message": "Received ISO doesn't meet conditions for ISO 3166 International standards",
                "Status Code": 406
            }
            return jsonify(ret_json)

        # Check if there are countires in received request
        country_in = posted_data["countries"]
        if len(country_in) == 0:
            ret_json = {
                "Message": "There are no countries in your request",
                "Status Code": 400
            }
            return jsonify(ret_json)
        country_out = []
        # Compare received array with saved value for iso
        y = 0
        for country in country_in:
            # Translate received countries
            trans_out = translator.translate(country, dest="en")
            translated_name = str(trans_out.text).lower()
            name_to_compare = coco.convert(names=translated_name, to='name_official').lower()
            # Compare translation with country name from DB
            if name_to_compare == name_out:
                country_out.append(country_in[y].lower())
                y = y + 1
            else:
                y = y + 1

        # Count number of suitable results and sent response
        match_count = len(country_out)
        if match_count == 0:
            ret_json = {
                "Message": "No match for found received countries",
                "Status Code": 406
            }
            return jsonify(ret_json)
        else:
            ret_map = {
                'iso': iso_in,
                'Status Code': status_code,
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