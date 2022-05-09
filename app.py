from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from main import validate_urls, run_bomber
app = Flask(__name__)
api = Api(app)

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

val_parser = reqparse.RequestParser()
val_parser.add_argument('urls')

barrage_parser = reqparse.RequestParser()
barrage_parser.add_argument("url")
barrage_parser.add_argument("vus", type=int)
barrage_parser.add_argument("dur", type=int)
barrage_parser.add_argument("host", type=str)
barrage_parser.add_argument("folder", type=str)

class Barrage(Resource):
    def post(self):
        args = barrage_parser.parse_args()
        run_bomber(args["url"], args["host"], args["folder"],
                   args["vus"], args["dur"])
        return 0


class ValidateUrls(Resource):
    def post(self):
        args = val_parser.parse_args()
        return validate_urls(args["urls"].split("\n"))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/config")
def config_page():
    return render_template("config.html")

api.add_resource(ValidateUrls, '/api/validate')
api.add_resource(Barrage, '/api/barrage')

app.run(host="0.0.0.0", port=5000, debug=True)