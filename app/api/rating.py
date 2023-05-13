from flask_restful import Resource, reqparse, fields, marshal_with
from ..utils import ValidationError
from ..controller import createRating, getAvgRating

create_rating_parser = reqparse.RequestParser()
create_rating_parser.add_argument('stars')
create_rating_parser.add_argument('comment')

rating_fields = {
    'id': fields.Integer,
    'event_id': fields.Integer,
    'stars': fields.Integer,
    'comment': fields.String,
}


class RatingAPI(Resource):
    @marshal_with({'avg_rating': fields.Float})
    def get(self, event_id):
        rating = getAvgRating(event_id=event_id)
        print(rating)
        return rating

    @marshal_with(rating_fields)
    def post(self, event_id):
        args = create_rating_parser.parse_args()
        stars = args.get("stars", None)
        comment = args.get("comment", None)

        if event_id is None:
            raise ValidationError(code=400, message="No event ID provided")

        if stars is None:
            raise ValidationError(code=400, message="No stars provided")
        
        data = dict()
        data['stars'] = stars
        data['event_id'] = event_id
        data['comment'] = comment
        new_rating = createRating(data)

        return new_rating