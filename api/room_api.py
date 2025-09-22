from flask import Flask, jsonify, request, abort

app = Flask(__name__)

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
        self.rooms_by_name[name] = room

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def get_room_by_name(self, room_name):
        return self.rooms_by_name.get(room_name)

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

        queue = [(start_id, [start_id])]  # (current_room_id, path_so_far)
        visited = set()

        while queue:
            current_room_id, path = queue.pop(0)
            if current_room_id == end_id:
                return path  # Found the path

            if current_room_id in visited:
                continue

            visited.add(current_room_id)

            for neighbor in self.rooms[current_room_id].connected_rooms:
                if neighbor.room_id not in visited:
                    queue.append((neighbor.room_id, path + [neighbor.room_id]))

        return None  # No path found

# Instantiate the RoomGraph
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

room_graph.connect_rooms("0", "16")     #köket mot lilla
room_graph.connect_rooms("0", "14")     #köket mot stora
room_graph.connect_rooms("16", "14")    #lilla mot stora
room_graph.connect_rooms("16", "11")    #lilla mot akkah
room_graph.connect_rooms("16", "15")    #lilla mot korridoren
room_graph.connect_rooms("16", "17")    #lilla mot glittertind
room_graph.connect_rooms("16", "8")     #lilla mot matterhorn
room_graph.connect_rooms("14", "15")    #stora mot korridoren
room_graph.connect_rooms("14", "3")     #stora mot cafet
room_graph.connect_rooms("14", "12")    #stora mot elbrus
room_graph.connect_rooms("14", "2")     #stora mot denali
room_graph.connect_rooms("14", "18")    #stora mot helag
room_graph.connect_rooms("14", "19")    #stora mot berit

room_graph.connect_rooms("15", "3")     # korridoren mot cafeet
room_graph.connect_rooms("15", "6")     # korridoren mot k2
room_graph.connect_rooms("15", "4")     # korridoren mot fuji

room_graph.connect_rooms("3", "1")      # cafet mot mount everest

# Route to create a new room
@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room_id = data.get('room_id')
    name = data.get('name')

    if not room_id or not name:
        abort(400, description="Room ID and name are required.")
    
    try:
        room_graph.add_room(room_id, name)
        return jsonify({"message": f"Room '{name}' created successfully."}), 201
    except ValueError as e:
        abort(400, description=str(e))

# Route to connect two rooms
@app.route('/rooms/connect', methods=['POST'])
def connect_rooms():
    data = request.get_json()
    room_id1 = data.get('room_id1')
    room_id2 = data.get('room_id2')

    if not room_id1 or not room_id2:
        abort(400, description="Both room IDs are required.")
    
    try:
        room_graph.connect_rooms(room_id1, room_id2)
        return jsonify({"message": f"Rooms {room_id1} and {room_id2} connected successfully."}), 200
    except ValueError as e:
        abort(400, description=str(e))

# Route to get a room's connections
@app.route('/rooms/<room_id>/connections', methods=['GET'])
def get_connections(room_id):
    try:
        connections = room_graph.get_connections(room_id)
        return jsonify({"room_id": room_id, "connections": connections}), 200
    except ValueError as e:
        abort(404, description=str(e))

# Route to get a room by ID
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

# Route to get a room by name
@app.route('/rooms/<room_name>', methods=['GET'])
def get_room_by_name(room_name):
    room = room_graph.get_room_by_name(room_name)
    if not room:
        abort(404, description=f"Room with name {room_name} not found.")
    return jsonify({
        "room_id": room.room_id,
        "name": room.name,
        "connections": [r.name for r in room.connected_rooms]
    }), 200

# Route for getting a route between room A and room B
@app.route('/rooms/route/names', methods=['GET'])
def get_shortest_route_by_names():
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

# Error handler
@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(error):
    response = jsonify({"message": error.description})
    response.status_code = error.code
    return response

# Run the application
if __name__ == '__main__':
    app.run(debug=True)