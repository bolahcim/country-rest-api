from flask import Flask, jsonify, request, Response
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
        if "iso" not in posted_data or "countries" not in posted_data:
            return Response( "'iso' or 'countires' is undefined", status=422)

        # Define variables from request for ISO validation
        iso_in = str(posted_data["iso"])
        iso_in = iso_in.lower()

        # Validate ISO
        name_out = coco.convert(names=iso_in, to='name_official').lower()
        if name_out != "not found":
            pass
        else:
            return Response("Received ISO doesn't meet conditions for ISO 3166 International standards", status=406)

        # Check if there are countires in received request
        country_in = posted_data["countries"]
        if len(country_in) == 0:
            return Response("There are no countries in your request", status=406)
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
            return Response("No match for found received countries", status=406)
        else:
            ret_map = {
                'iso': iso_in,
                'match_count': match_count,
                'countries': country_out
            }
            return jsonify(ret_map)

@app.route('/')
def hello():
    return "Hello, I am available to receive requests!"

api.add_resource(MatchCountry, "/match_country")

if __name__ == "__main__":
    app.run(host ="0.0.0.0")