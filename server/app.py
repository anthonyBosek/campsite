from datetime import datetime

from flask import Flask, abort, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Campsite, Park, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Note: `app.json.compact = False` Configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Parks(Resource):
    def get(self):
        parks = [park.to_dict() for park in Park.query.all()]
        if not len(parks):
            abort(404, description="No parks found")
        return make_response(parks, 200)

    def post(self):
        request_data = request.get_json()
        new_park = Park(
            name=request_data["name"],
            address=request_data["address"],
            entrance_fee=request_data["entrance_fee"],
            has_trails=request_data["has_trails"],
            has_RV_cleanout=request_data["has_RV_cleanout"],
            begin_camping_season=datetime.strptime(
                request_data["begin_camping_season"], "%Y-%m-%d"
            ),
            end_camping_season=datetime.strptime(
                request_data["end_camping_season"], "%Y-%m-%d"
            ),
        )
        db.session.add(new_park)
        db.session.commit()
        return make_response(new_park.to_dict(), 201)


class ParkById(Resource):
    def get(self, id):
        park = Park.query.get_or_404(id)
        return make_response(park.to_dict(), 200)

    def patch(self, id):
        park = Park.query.get_or_404(id)
        request_data = request.get_json()
        for key, value in request_data.items():
            setattr(park, key, value)
        db.session.commit()
        return make_response(park.to_dict(), 200)

    def delete(self, id):
        park = Park.query.get_or_404(id)
        db.session.delete(park)
        db.session.commit()
        return make_response("", 204)


class Campsites(Resource):
    def post(self):
        request_data = request.get_json()
        new_campsite = Campsite(**request_data)
        db.session.add(new_campsite)
        db.session.commit()
        return make_response(new_campsite.to_dict(), 201)


class CampsiteById(Resource):
    def get(self, id):
        campsite = Campsite.query.get_or_404(id)
        return make_response(campsite.to_dict(), 200)

    def patch(self, id):
        campsite = Campsite.query.get_or_404(id)
        request_data = request.get_json()
        for key, value in request_data.items():
            setattr(campsite, key, value)
        db.session.commit()
        return make_response(campsite.to_dict(), 200)


api.add_resource(Parks, "/parks")
api.add_resource(ParkById, "/parks/<int:id>")
api.add_resource(Campsites, "/campsites")
api.add_resource(CampsiteById, "/campsites/<int:id>")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
