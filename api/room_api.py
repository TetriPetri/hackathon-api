# api/room_api.py - Fixed for Vercel serverless deployment
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for LLM access

# Room Class
class Room:
    def __init__(self, room_id, name):
        self.room_id = room_id
        self.name = name
        self.connected_rooms = []

    def add_connection(self, room):
        self.connected_rooms.append(room)

    def __repr__(self):
        return f"Room(id={self.room_id}, name={self.name}, connections={[room.name for room in self.connected_rooms]})"


# RoomGraph Class
class RoomGraph:
    def __init__(self):
        self.rooms = {}
        self.rooms_by_name = {}

    def add_room(self, room_id, name):
        if room_id in self.rooms:
            raise ValueError(f"Room with ID {room_id} already exists.")
        room = Room(room_id, name)
        self.rooms[room_id] = room
        self.rooms_by_name[name.lower()] = room  # Store lowercase for case-insensitive lookup

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def get_room_by_name(self, room_name):
        return self.rooms_by_name.get(room_name.lower())

    def connect_rooms(self, room_id1, room_id2):
        room1 = self.rooms.get(room_id1)
        room2 = self.rooms.get(room_id2)
        if not room1 or not room2:
            raise ValueError("Both rooms must exist.")
        room1.add_connection(room2)
        room2.add_connection(room1)

    def get_connections(self, room_id):
        room = self.rooms.get(room_id)
        if not room:
            raise ValueError(f"Room with ID {room_id} not found.")
        return [r.name for r in room.connected_rooms]

    def find_shortest_path(self, start_id, end_id):
        if start_id not in self.rooms or end_id not in self.rooms:
            raise ValueError("Both rooms must exist.")

        queue = [(start_id, [start_id])]
        visited = set()

        while queue:
            current_room_id, path = queue.pop(0)
            if current_room_id == end_id:
                return path

            if current_room_id in visited:
                continue

            visited.add(current_room_id)

            for neighbor in self.rooms[current_room_id].connected_rooms:
                if neighbor.room_id not in visited:
                    queue.append((neighbor.room_id, path + [neighbor.room_id]))

        return None

# Initialize room graph globally (will be created once per cold start)
room_graph = RoomGraph()
room_graph.add_room("0", 'köket')
room_graph.add_room("1", 'mount everest')
room_graph.add_room("2", 'denali')
room_graph.add_room("3", 'cafét')
room_graph.add_room("4", 'fuji')
room_graph.add_room("5", 'mont blanc')
room_graph.add_room("6", 'k2')
room_graph.add_room("7", 'kilimanjaro')
room_graph.add_room("8", 'matterhorn')
room_graph.add_room("9", 'sockertoppen')
room_graph.add_room("10", 'kebnekaise')
room_graph.add_room("11", 'akkah')
room_graph.add_room("12", 'elbrus')
room_graph.add_room("13", 'makkarus')
room_graph.add_room("14", 'stora skärmrummet')
room_graph.add_room("15", 'korridoren')
room_graph.add_room("16", 'lilla skärmrummet')
room_graph.add_room("17", 'glittertind')
room_graph.add_room("18", 'helag')
room_graph.add_room("19", 'berit')

# Add all connections
room_graph.connect_rooms("0", "16")
room_graph.connect_rooms("0", "14")
room_graph.connect_rooms("16", "14")
room_graph.connect_rooms("16", "11")
room_graph.connect_rooms("16", "15")
room_graph.connect_rooms("16", "17")
room_graph.connect_rooms("16", "8")
room_graph.connect_rooms("14", "15")
room_graph.connect_rooms("14", "3")
room_graph.connect_rooms("14", "12")
room_graph.connect_rooms("14", "2")
room_graph.connect_rooms("14", "18")
room_graph.connect_rooms("14", "19")
room_graph.connect_rooms("15", "3")
room_graph.connect_rooms("15", "6")
room_graph.connect_rooms("15", "4")
room_graph.connect_rooms("3", "1")

# Root route - API documentation
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "name": "Room Navigation API",
        "description": "API for finding shortest paths between rooms",
        "endpoints": {
            "/": "API documentation",
            "/rooms": "List all rooms",
            "/rooms/<room_id>": "Get room by ID",
            "/rooms/byname/<room_name>": "Get room by name",
            "/rooms/<room_id>/connections": "Get room connections",
            "/rooms/route/byids?from=X&to=Y": "Find route by room IDs",
            "/rooms/route/bynames?from=X&to=Y": "Find route by room names"
        },
        "example_usage": {
            "find_route": "/rooms/route/bynames?from=köket&to=mount%20everest"
        }
    }), 200

# List all rooms
@app.route('/rooms', methods=['GET'])
def list_rooms():
    rooms_list = []
    for room_id, room in room_graph.rooms.items():
        rooms_list.append({
            "room_id": room.room_id,
            "name": room.name,
            "connections": [r.name for r in room.connected_rooms]
        })
    return jsonify({"rooms": rooms_list}), 200

# Get room by ID
@app.route('/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    room = room_graph.get_room(room_id)
    if not room:
        abort(404, description=f"Room with ID {room_id} not found.")
    return jsonify({
        "room_id": room.room_id,
        "name": room.name,
        "connections": [r.name for r in room.connected_rooms]
    }), 200

# Get room by name
@app.route('/rooms/byname/<path:room_name>', methods=['GET'])
def get_room_by_name(room_name):
    room = room_graph.get_room_by_name(room_name)
    if not room:
        abort(404, description=f"Room with name '{room_name}' not found.")
    return jsonify({
        "room_id": room.room_id,
        "name": room.name,
        "connections": [r.name for r in room.connected_rooms]
    }), 200

# Get room connections
@app.route('/rooms/<room_id>/connections', methods=['GET'])
def get_connections(room_id):
    try:
        connections = room_graph.get_connections(room_id)
        return jsonify({"room_id": room_id, "connections": connections}), 200
    except ValueError as e:
        abort(404, description=str(e))

# Find route by IDs
@app.route('/rooms/route/byids', methods=['GET'])
def get_shortest_route_by_ids():
    start_id = request.args.get('from')
    end_id = request.args.get('to')

    if not start_id or not end_id:
        abort(400, description="Query parameters 'from' and 'to' are required.")

    try:
        path = room_graph.find_shortest_path(start_id, end_id)
        if path:
            named_path = [room_graph.rooms[rid].name for rid in path]
            return jsonify({
                "from": room_graph.rooms[start_id].name,
                "to": room_graph.rooms[end_id].name,
                "path": named_path,
                "hops": len(named_path) - 1
            }), 200
        else:
            return jsonify({
                "message": f"No route found between '{start_id}' and '{end_id}'."
            }), 404
    except ValueError as e:
        abort(400, description=str(e))

# Find route by names
@app.route('/rooms/route/bynames', methods=['GET'])
def get_shortest_route_by_names():
    start_name = request.args.get('from')
    end_name = request.args.get('to')

    if not start_name or not end_name:
        abort(400, description="Query parameters 'from' and 'to' are required.")

    start_room = room_graph.get_room_by_name(start_name)
    end_room = room_graph.get_room_by_name(end_name)

    if not start_room:
        abort(404, description=f"Room '{start_name}' not found")
    if not end_room:
        abort(404, description=f"Room '{end_name}' not found")

    start_id = start_room.room_id
    end_id = end_room.room_id

    try:
        path = room_graph.find_shortest_path(start_id, end_id)
        if path:
            named_path = [room_graph.rooms[rid].name for rid in path]
            return jsonify({
                "from": room_graph.rooms[start_id].name,
                "to": room_graph.rooms[end_id].name,
                "path": named_path,
                "hops": len(named_path) - 1
            }), 200
        else:
            return jsonify({
                "message": f"No route found between '{start_name}' and '{end_name}'."
            }), 404
    except ValueError as e:
        abort(400, description=str(e))

# Error handlers
@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(error):
    response = jsonify({"error": error.description})
    response.status_code = error.code
    return response

# CRITICAL: This is the Vercel serverless handler
# Vercel expects this exact format
def handler(request, context):
    with app.test_request_context(
        path=request.path,
        method=request.method,
        headers=request.headers,
        data=request.get_data(),
        query_string=request.query_string
    ):
        try:
            response = app.full_dispatch_request()
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# For local testing
if __name__ == '__main__':
    app.run(debug=True)