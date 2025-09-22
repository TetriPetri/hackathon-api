# api/index.py - Room Navigation API for Vercel
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

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

    def find_shortest_path(self, start_id, end_id):
        if start_id not in self.rooms or end_id not in self.rooms:
            return None

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # Remove leading slash and /api prefix if present
        if path.startswith('/api/'):
            path = path[5:]  # Remove '/api/'
        elif path.startswith('/api'):
            path = path[4:]  # Remove '/api'
        elif path.startswith('/'):
            path = path[1:]  # Remove just '/'
        
        # Route handling
        response_data = None
        status_code = 200
        
        # Debug: log the path being processed
        print(f"Processing path: '{path}', query: {query}")
        
        # Home endpoint
        if path == '' or path == '/' or path == 'api':
            response_data = {
                "name": "Room Navigation API",
                "status": "online",
                "endpoints": {
                    "/": "API documentation",
                    "/rooms": "List all rooms",
                    "/rooms/{id}": "Get room by ID",
                    "/route": "Find route (?from=X&to=Y using names)",
                    "/route-ids": "Find route (?from=X&to=Y using IDs)"
                },
                "example": "/route?from=köket&to=cafét"
            }
        
        # List all rooms
        elif path == 'rooms':
            rooms_list = []
            for room_id, room in room_graph.rooms.items():
                rooms_list.append({
                    "room_id": room.room_id,
                    "name": room.name,
                    "connections": [r.name for r in room.connected_rooms]
                })
            response_data = {"rooms": rooms_list}
        
        # Get specific room
        elif path.startswith('rooms/'):
            room_id = path.replace('rooms/', '')
            room = room_graph.get_room(room_id)
            if room:
                response_data = {
                    "room_id": room.room_id,
                    "name": room.name,
                    "connections": [r.name for r in room.connected_rooms]
                }
            else:
                status_code = 404
                response_data = {"error": f"Room {room_id} not found"}
        
        # Find route by names
        elif path == 'route':
            from_param = query.get('from', [''])[0].lower()
            to_param = query.get('to', [''])[0].lower()
            
            if not from_param or not to_param:
                status_code = 400
                response_data = {"error": "Parameters 'from' and 'to' are required"}
            else:
                start_room = room_graph.get_room_by_name(from_param)
                end_room = room_graph.get_room_by_name(to_param)
                
                if not start_room:
                    status_code = 404
                    response_data = {"error": f"Room '{from_param}' not found"}
                elif not end_room:
                    status_code = 404
                    response_data = {"error": f"Room '{to_param}' not found"}
                else:
                    path_ids = room_graph.find_shortest_path(start_room.room_id, end_room.room_id)
                    if path_ids:
                        named_path = [room_graph.rooms[rid].name for rid in path_ids]
                        response_data = {
                            "from": start_room.name,
                            "to": end_room.name,
                            "path": named_path,
                            "hops": len(named_path) - 1
                        }
                    else:
                        status_code = 404
                        response_data = {"error": "No path found"}
        
        # Find route by IDs
        elif path == 'route-ids':
            from_param = query.get('from', [''])[0]
            to_param = query.get('to', [''])[0]
            
            if not from_param or not to_param:
                status_code = 400
                response_data = {"error": "Parameters 'from' and 'to' are required"}
            elif from_param not in room_graph.rooms or to_param not in room_graph.rooms:
                status_code = 404
                response_data = {"error": "Invalid room ID"}
            else:
                path_ids = room_graph.find_shortest_path(from_param, to_param)
                if path_ids:
                    named_path = [room_graph.rooms[rid].name for rid in path_ids]
                    response_data = {
                        "from": room_graph.rooms[from_param].name,
                        "to": room_graph.rooms[to_param].name,
                        "path": named_path,
                        "hops": len(named_path) - 1
                    }
                else:
                    status_code = 404
                    response_data = {"error": "No path found"}
        
        else:
            status_code = 404
            response_data = {"error": f"Unknown endpoint: {path}"}
        
        # Send response
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
        return
    
    def do_POST(self):
        # Handle POST requests if needed
        self.do_GET()
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return