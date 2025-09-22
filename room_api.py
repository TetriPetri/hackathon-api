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

    def add_room(self, room_id, name):
        if room_id in self.rooms:
            raise ValueError(f"Room with ID {room_id} already exists.")
        self.rooms[room_id] = Room(room_id, name)

    def get_room(self, room_id):
        return self.rooms.get(room_id)

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

# Instantiate the RoomGraph
room_graph = RoomGraph()
room_graph.add_room(0, 'köket')
room_graph.add_room(1, 'mount everest')
room_graph.add_room(2, 'denali')
room_graph.add_room(3, 'cafét')
room_graph.add_room(4, 'fuji')
room_graph.add_room(5, 'mont blanc')
room_graph.add_room(6, 'k2')
room_graph.add_room(7, 'kilimanjaro')
room_graph.add_room(8, 'matterhorn')
room_graph.add_room(9, 'sockertoppen')
room_graph.add_room(10, 'kebnekaise')
room_graph.add_room(11, 'akkah')
room_graph.add_room(12, 'elbrus')
room_graph.add_room(13, 'makkarus')
room_graph.add_room(14, 'stora skärmrummet')
room_graph.add_room(15, 'korridoren')
room_graph.add_room(16, 'lilla skärmrummet')
room_graph.add_room(17, 'glittertind')
room_graph.add_room(18, 'helag')
room_graph.add_room(19, 'berit')

room_graph.connect_rooms(0, 16)     #köket mot lilla
room_graph.connect_rooms(0, 14)     #köket mot stora
room_graph.connect_rooms(16, 14)    #lilla mot stora
room_graph.connect_rooms(16, 11)    #lilla mot akkah
room_graph.connect_rooms(16, 15)    #lilla mot korridoren
room_graph.connect_rooms(16, 17)    #lilla mot glittertind
room_graph.connect_rooms(16, 8)     #lilla mot matterhorn
room_graph.connect_rooms(14, 15)    #stora mot korridoren
room_graph.connect_rooms(14, 3)     #stora mot cafet
room_graph.connect_rooms(14, 12)    #stora mot elbrus
room_graph.connect_rooms(14, 2)     #stora mot denali
room_graph.connect_rooms(14, 18)    #stora mot helag
room_graph.connect_rooms(14, 19)    #stora mot berit

room_graph.connect_rooms(15, 3)     # korridoren mot cafeet
room_graph.connect_rooms(15, 6)     # korridoren mot k2
room_graph.connect_rooms(15, 4)     # korridoren mot fuji

room_graph.connect_rooms(3, 1)      # cafet mot mount everest



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