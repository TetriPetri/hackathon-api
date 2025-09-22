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
        self.rooms_by_name[name.lower()] = room

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

# Initialize room graph
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

# Add connections
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

@app.route('/api/room_api', methods=['GET', 'POST'])
@app.route('/api/room_api/', methods=['GET', 'POST'])
@app.route('/api/room_api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path=''):
    """Route all requests through this handler"""
    
    # Home/documentation
    if path == '' or path == '/':
        return jsonify({
            "name": "Room Navigation API",
            "status": "online",
            "endpoints": {
                "/api/room_api/rooms": "List all rooms",
                "/api/room_api/rooms/{id}": "Get room by ID",
                "/api/room_api/rooms/byname/{name}": "Get room by name",
                "/api/room_api/rooms/{id}/connections": "Get connections",
                "/api/room_api/route/byids?from=X&to=Y": "Route by IDs",
                "/api/room_api/route/bynames?from=X&to=Y": "Route by names"
            },
            "example": "/api/room_api/route/bynames?from=köket&to=cafét"
        }), 200
    
    # List all rooms
    elif path == 'rooms':
        rooms_list = []
        for room_id, room in room_graph.rooms.items():
            rooms_list.append({
                "room_id": room.room_id,
                "name": room.name,
                "connections": [r.name for r in room.connected_rooms]
            })
        return jsonify({"rooms": rooms_list}), 200
    
    # Route by names
    elif path == 'route/bynames':
        start_name = request.args.get('from', '').lower()
        end_name = request.args.get('to', '').lower()
        
        if not start_name or not end_name:
            return jsonify({"error": "Parameters 'from' and 'to' required"}), 400
        
        start_room = room_graph.get_room_by_name(start_name)
        end_room = room_graph.get_room_by_name(end_name)
        
        if not start_room:
            return jsonify({"error": f"Room '{start_name}' not found"}), 404
        if not end_room:
            return jsonify({"error": f"Room '{end_name}' not found"}), 404
        
        path_ids = room_graph.find_shortest_path(start_room.room_id, end_room.room_id)
        if path_ids:
            named_path = [room_graph.rooms[rid].name for rid in path_ids]
            return jsonify({
                "from": start_room.name,
                "to": end_room.name,
                "path": named_path,
                "hops": len(named_path) - 1
            }), 200
        else:
            return jsonify({"error": "No path found"}), 404
    
    # Route by IDs
    elif path == 'route/byids':
        start_id = request.args.get('from')
        end_id = request.args.get('to')
        
        if not start_id or not end_id:
            return jsonify({"error": "Parameters 'from' and 'to' required"}), 400
        
        if start_id not in room_graph.rooms or end_id not in room_graph.rooms:
            return jsonify({"error": "Invalid room ID"}), 404
        
        path_ids = room_graph.find_shortest_path(start_id, end_id)
        if path_ids:
            named_path = [room_graph.rooms[rid].name for rid in path_ids]
            return jsonify({
                "from": room_graph.rooms[start_id].name,
                "to": room_graph.rooms[end_id].name,
                "path": named_path,
                "hops": len(named_path) - 1
            }), 200
        else:
            return jsonify({"error": "No path found"}), 404
    
    # Get room by ID with connections
    elif path.startswith('rooms/') and path.endswith('/connections'):
        room_id = path.replace('rooms/', '').replace('/connections', '')
        room = room_graph.get_room(room_id)
        if room:
            return jsonify({
                "room_id": room.room_id,
                "connections": [r.name for r in room.connected_rooms]
            }), 200
        else:
            return jsonify({"error": f"Room {room_id} not found"}), 404
    
    # Get room by name
    elif path.startswith('rooms/byname/'):
        room_name = path.replace('rooms/byname/', '')
        room = room_graph.get_room_by_name(room_name)
        if room:
            return jsonify({
                "room_id": room.room_id,
                "name": room.name,
                "connections": [r.name for r in room.connected_rooms]
            }), 200
        else:
            return jsonify({"error": f"Room '{room_name}' not found"}), 404
    
    # Get room by ID
    elif path.startswith('rooms/'):
        room_id = path.replace('rooms/', '')
        room = room_graph.get_room(room_id)
        if room:
            return jsonify({
                "room_id": room.room_id,
                "name": room.name,
                "connections": [r.name for r in room.connected_rooms]
            }), 200
        else:
            return jsonify({"error": f"Room {room_id} not found"}), 404
    
    else:
        return jsonify({"error": f"Unknown endpoint: {path}"}), 404