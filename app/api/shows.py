from flask_restful import Resource, reqparse, fields, marshal_with
from ..utils import ValidationError, NotFoundError
from ..controller import createShow, deleteShow, editShow, getShow, getAllShowsBasic

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('event_id')
create_show_parser.add_argument('venue_id')
create_show_parser.add_argument('timing')
create_show_parser.add_argument('price')
create_show_parser.add_argument('isActive')

show_fields = {
    'id': fields.Integer,
    'event_id': fields.Integer,
    'venue_id': fields.Integer,
    'timing': fields.Integer,
    'price': fields.Integer,
    'isActive': fields.Integer,
}


class ShowsAPI(Resource):
    @marshal_with(show_fields)
    def get(self, show_id=None):
        show = None
        if not (show_id is None):
            show = getShow(id=show_id)
            if not show:
                raise NotFoundError()
        else:
            show = getAllShowsBasic()
        return show
    
    def put(self, show_id):
        args = create_show_parser.parse_args()
        event_id = args.get("event_id", None)
        venue_id = args.get("venue_id", None)
        timing = args.get("timing", None)
        price = args.get("price", None)
        isActive = args.get("isActive", None)

        if event_id is None:
            raise ValidationError(code=400, message="No event ID provided")
        
        if venue_id is None:
            raise ValidationError(code=400, message="No venue ID provided")
        
        if timing is None:
            raise ValidationError(code=400, message="No timing provided")
        
        if price is None:
            raise ValidationError(code=400, message="No price provided")
        
        if isActive is None:
            raise ValidationError(code=400, message="Not specified if show is active")

        if venue_id is None:
            raise ValidationError(code=400, message="No stars provided")
        
        data = dict()
        data['id'] = show_id
        data['event_id'] = event_id
        data['venue_id'] = venue_id
        data['timing'] = timing
        data['price'] = price
        data['isActive'] = isActive
        show = editShow(data)

        if show:
            return {'message': 'Show updated'}
    
    def delete(self, show_id):
        deleted = deleteShow(show_id)
        if (deleted):
            return {'message': 'Show deleted'}
        else:
            return {'message': 'Something went wrong'}
    
    @marshal_with(show_fields)
    def post(self):
        args = create_show_parser.parse_args()
        event_id = args.get("event_id", None)
        venue_id = args.get("venue_id", None)
        timing = args.get("timing", None)
        price = args.get("price", None)
        isActive = args.get("isActive", None)

        if event_id is None:
            raise ValidationError(code=400, message="No event ID provided")
        
        if venue_id is None:
            raise ValidationError(code=400, message="No venue ID provided")
        
        if timing is None:
            raise ValidationError(code=400, message="No timing provided")
        
        if price is None:
            raise ValidationError(code=400, message="No price provided")
        
        if isActive is None:
            raise ValidationError(code=400, message="Not specified if show is active")

        if venue_id is None:
            raise ValidationError(code=400, message="No stars provided")
        
        data = dict()
        data['event_id'] = event_id
        data['venue_id'] = venue_id
        data['timing'] = timing
        data['price'] = price
        data['isActive'] = isActive
        new_show = createShow(data)

        return new_show