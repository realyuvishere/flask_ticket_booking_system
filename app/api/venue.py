from flask_restful import Resource, reqparse, fields, marshal_with
from ..utils import ValidationError, NotFoundError
from ..controller import createVenue, editVenue, getAllVenues, getVenue, deleteVenue

create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('name')
create_venue_parser.add_argument('location')
create_venue_parser.add_argument('capacity')

venue_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'capacity': fields.Integer,
}


class VenueAPI(Resource):
    @marshal_with(venue_fields)
    def get(self, venue_id=None):
        venue = None
        if not (venue_id is None):
            venue = getVenue(id=venue_id)
            if not venue:
                raise NotFoundError()
        else:
            venue = getAllVenues()
        return venue
    
    def put(self, venue_id):
        args = create_venue_parser.parse_args()
        name = args.get("name", None)
        location = args.get("location", None)
        capacity = args.get("capacity", None)

        if venue_id is None:
            raise ValidationError(code=400, message="No venue ID provided")
        
        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if location is None:
            raise ValidationError(code=400, message="No location provided")

        if capacity is None:
            raise ValidationError(code=400, message="No seating capacity provided")
        
        data = dict()
        data['id'] = venue_id
        data['name'] = name
        data['location'] = location
        data['capacity'] = capacity
        venue = editVenue(data)

        if venue:
            return {'message': 'Venue updated'}
    
    def delete(self, venue_id):
        deleted = deleteVenue(venue_id)
        if (deleted):
            return {'message': 'Venue deleted'}
        else:
            return {'message': 'Something went wrong'}
    
    @marshal_with(venue_fields)
    def post(self):
        args = create_venue_parser.parse_args()
        name = args.get("name", None)
        location = args.get("location", None)
        capacity = args.get("capacity", None)

        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if location is None:
            raise ValidationError(code=400, message="No location provided")

        if capacity is None:
            raise ValidationError(code=400, message="No seating capacity provided")
        
        data = dict()
        data['name'] = name
        data['location'] = location
        data['capacity'] = capacity
        new_venue = createVenue(data)

        return new_venue