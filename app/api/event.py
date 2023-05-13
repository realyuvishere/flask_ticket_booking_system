from flask_restful import Resource, reqparse, fields, marshal_with
from ..utils import ValidationError, NotFoundError
from ..controller import createEvent, deleteEvent, editEvent, getAllEvents, getEvent

create_event_parser = reqparse.RequestParser()
create_event_parser.add_argument('name')
create_event_parser.add_argument('description')
create_event_parser.add_argument('tags')

event_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'tags': fields.String,
}

class EventAPI(Resource):
    @marshal_with(event_fields)
    def get(self, event_id=None):
        event = None
        if not (event_id is None):
            event = getEvent(id=event_id)
            if not event:
                raise NotFoundError()
        else:
            event = getAllEvents()
        return event
    
    def put(self, event_id):
        args = create_event_parser.parse_args()
        name = args.get("name", None)
        description = args.get("description", None)
        tags = args.get("tags", None)

        if event_id is None:
            raise ValidationError(code=400, message="No event ID provided")
        
        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if description is None:
            raise ValidationError(code=400, message="No description provided")
        
        if tags is None:
            raise ValidationError(code=400, message="No tags provided")
        
        data = dict()
        data['id'] = event_id
        data['name'] = name
        data['description'] = description
        data['tags'] = tags
        event = editEvent(data)

        if event:
            return {'message': 'Event updated'}
    
    def delete(self, event_id):
        deleted = deleteEvent(event_id)
        if (deleted):
            return {'message': 'Event deleted'}
        else:
            return {'message': 'Something went wrong'}
    
    @marshal_with(event_fields)
    def post(self):
        args = create_event_parser.parse_args()
        name = args.get("name", None)
        description = args.get("description", None)
        tags = args.get("tags", None)
        
        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if description is None:
            raise ValidationError(code=400, message="No description provided")
        
        if tags is None:
            raise ValidationError(code=400, message="No tags provided")
        
        data = dict()
        data['name'] = name
        data['description'] = description
        data['tags'] = tags
        new_event = createEvent(data)

        return new_event