import json
from random import choice, randint, uniform, sample
from datetime import datetime, timedelta

# Define node types
node_types = [
    "Wall", "Door", "Window", "Ceiling Light", "HVAC Vent",
    "Fire Alarm", "Sprinkler", "Outlet", "Floor Finish", "Baseboard"
]

# Helper functions for random data
materials = ["Concrete", "Steel", "Wood", "Glass", "Gypsum", "Plastic"]
statuses = ["Installed", "Pending", "In Progress", "Defective", "Approved"]
asset_statuses = ["Open", "Closed", "Pending", "Resolved"]
roles = ["Project Manager", "Electrician", "Plumber", "Foreman", "Inspector"]
specialties = ["Electrical", "Plumbing", "General", "HVAC"]

# Generate random date
start_date = datetime(2023, 1, 1)
def random_date():
    return (start_date + timedelta(days=randint(0, 365))).strftime('%Y-%m-%d')

def random_email(name):
    return name.lower().replace(' ', '.') + '@example.com'

def random_phone():
    return f"+1-555-{randint(100,999)}-{randint(1000,9999)}"

# Define asset IDs with richer properties
def make_asset(asset_id, asset_type):
    return {
        "id": asset_id,
        "type": asset_type,
        "description": f"{asset_type} related to construction.",
        "date": random_date(),
        "status": choice(asset_statuses)
    }

asset_ids = [
    make_asset("DrawingA101", "Drawing"),
    make_asset("DrawingA102", "Drawing"),
    make_asset("DrawingA103", "Drawing"),
    make_asset("RFI001", "RFI"),
    make_asset("RFI002", "RFI"),
    make_asset("RFI003", "RFI"),
    make_asset("Issue101", "Issue"),
    make_asset("Issue102", "Issue"),
    make_asset("Issue103", "Issue")
]

# Define base nodes with richer properties
nodes = [
    {"id": "Project1", "type": "Project", "name": "Inertia Demo Building", "address": "123 Main St", "start_date": "2023-01-01", "status": "Active"},
    {"id": "Story1", "type": "Story", "name": "Level 1", "elevation": 0},
    {"id": "Story2", "type": "Story", "name": "Level 2", "elevation": 4},
    {"id": "Story3", "type": "Story", "name": "Level 3", "elevation": 8},
    {"id": "GeneralContractor", "type": "Company", "name": "BuildPro GC", "contact": "gc@buildpro.com", "phone": "+1-555-100-2000", "address": "456 Contractor Ave"},
    {"id": "Subcontractor1", "type": "Company", "name": "Ace Electric", "contact": "info@aceelectric.com", "phone": "+1-555-200-3000", "address": "789 Electric Rd"},
    {"id": "Subcontractor2", "type": "Company", "name": "FlowPlumb", "contact": "contact@flowplumb.com", "phone": "+1-555-300-4000", "address": "321 Plumber St"},
    {"id": "GCTeam1", "type": "Team", "name": "GC Field Crew", "specialty": "General"},
    {"id": "SubTeam1", "type": "Team", "name": "Electricians", "specialty": "Electrical"},
    {"id": "SubTeam2", "type": "Team", "name": "Plumbers", "specialty": "Plumbing"},
    {"id": "Person1", "type": "Person", "name": "John Smith", "role": "Project Manager", "email": random_email("John Smith"), "phone": random_phone()},
    {"id": "Person2", "type": "Person", "name": "Jane Doe", "role": "Electrician", "email": random_email("Jane Doe"), "phone": random_phone()},
    {"id": "Person3", "type": "Person", "name": "Bob Johnson", "role": "Plumber", "email": random_email("Bob Johnson"), "phone": random_phone()}
]

# Generate rooms for each story
room_types = ["Office", "Conference Room", "Break Room", "Restroom"]
for story_num in range(1, 4):
    for room_num in range(1, 5):
        room_id = f"Room{story_num}{room_num}"
        nodes.append({
            "id": room_id,
            "type": "Room",
            "name": f"{room_types[room_num-1]} {room_num}",
            "story": f"Story{story_num}",
            "area_sqm": round(uniform(15, 40), 1),
            "flooring": choice(["Carpet", "Tile", "Wood", "Vinyl"]),
            "status": choice(statuses)
        })

# Generate objects for each room with richer properties
for story_num in range(1, 4):
    for room_num in range(1, 5):
        for obj_num in range(1, 11):
            obj_type = choice(node_types)
            obj_id = f"Object{story_num}{room_num}{obj_num}"
            nodes.append({
                "id": obj_id,
                "type": obj_type,
                "name": f"{obj_type} {obj_num}",
                "room": f"Room{story_num}{room_num}",
                "dimensions_cm": {
                    "length": round(uniform(50, 300), 1),
                    "width": round(uniform(5, 100), 1),
                    "height": round(uniform(5, 300), 1)
                },
                "material": choice(materials),
                "status": choice(statuses),
                "installed_date": random_date()
            })

# Generate relationships
relationships = []

# Project to Stories
for story_num in range(1, 4):
    relationships.append({
        "source": "Project1",
        "target": f"Story{story_num}",
        "type": "contains"
    })

# Stories to Rooms
for story_num in range(1, 4):
    for room_num in range(1, 5):
        relationships.append({
            "source": f"Story{story_num}",
            "target": f"Room{story_num}{room_num}",
            "type": "contains"
        })

# Rooms to Objects
for story_num in range(1, 4):
    for room_num in range(1, 5):
        for obj_num in range(1, 11):
            relationships.append({
                "source": f"Room{story_num}{room_num}",
                "target": f"Object{story_num}{room_num}{obj_num}",
                "type": "contains"
            })

# Company to Team relationships
relationships.extend([
    {"source": "GeneralContractor", "target": "GCTeam1", "type": "manages"},
    {"source": "Subcontractor1", "target": "SubTeam1", "type": "manages"},
    {"source": "Subcontractor2", "target": "SubTeam2", "type": "manages"}
])

# Team to Person relationships
relationships.extend([
    {"source": "GCTeam1", "target": "Person1", "type": "includes"},
    {"source": "SubTeam1", "target": "Person2", "type": "includes"},
    {"source": "SubTeam2", "target": "Person3", "type": "includes"}
])

# Random asset relationships
for node in nodes:
    if node["type"] in ["Room", "Wall", "Door", "Window", "Ceiling Light", "HVAC Vent", "Fire Alarm", "Sprinkler", "Outlet", "Floor Finish", "Baseboard"]:
        num_assets = randint(1, 3)
        for _ in range(num_assets):
            asset = choice(asset_ids)
            relationships.append({
                "source": node["id"],
                "target": asset["id"],
                "type": "has_asset"
            })

# --- Drawings contain objects ---
drawing_ids = [a['id'] for a in asset_ids if a['type'] == 'Drawing']
rfi_ids = [a['id'] for a in asset_ids if a['type'] == 'RFI']
issue_ids = [a['id'] for a in asset_ids if a['type'] == 'Issue']

object_ids = [n['id'] for n in nodes if n['type'] in node_types]

# Map: Drawing -> list of objects
objects_per_drawing = max(1, len(object_ids) // len(drawing_ids))
drawing_object_map = {}
for i, drawing_id in enumerate(drawing_ids):
    drawing_object_map[drawing_id] = object_ids[i*objects_per_drawing:(i+1)*objects_per_drawing]
    # Add relationships: Drawing contains Object
    for obj_id in drawing_object_map[drawing_id]:
        relationships.append({
            "source": drawing_id,
            "target": obj_id,
            "type": "contains_object"
        })

# --- RFIs and Issues reference Drawings and Objects, and are assigned to a Person ---
person_ids = [n['id'] for n in nodes if n['type'] == 'Person']

# Helper to assign RFI/Issue to drawing, objects, and person
for rfi_id in rfi_ids:
    drawing_id = choice(drawing_ids)
    related_objects = sample(drawing_object_map[drawing_id], k=randint(1, 3))
    assigned_person = choice(person_ids)
    # RFI references Drawing
    relationships.append({
        "source": rfi_id,
        "target": drawing_id,
        "type": "references_drawing"
    })
    # RFI references Objects
    for obj_id in related_objects:
        relationships.append({
            "source": rfi_id,
            "target": obj_id,
            "type": "references_object"
        })
    # RFI assigned to Person
    relationships.append({
        "source": rfi_id,
        "target": assigned_person,
        "type": "assigned_to"
    })

for issue_id in issue_ids:
    drawing_id = choice(drawing_ids)
    related_objects = sample(drawing_object_map[drawing_id], k=randint(1, 3))
    assigned_person = choice(person_ids)
    # Issue references Drawing
    relationships.append({
        "source": issue_id,
        "target": drawing_id,
        "type": "references_drawing"
    })
    # Issue references Objects
    for obj_id in related_objects:
        relationships.append({
            "source": issue_id,
            "target": obj_id,
            "type": "references_object"
        })
    # Issue assigned to Person
    relationships.append({
        "source": issue_id,
        "target": assigned_person,
        "type": "assigned_to"
    })

# Add relationships between Assets and Project/Stories/Companies/Teams
project_id = "Project1"
story_ids = [n['id'] for n in nodes if n['type'] == 'Story']
company_ids = [n['id'] for n in nodes if n['type'] == 'Company']
team_ids = [n['id'] for n in nodes if n['type'] == 'Team']

all_asset_ids = [a['id'] for a in asset_ids]

for asset_id in all_asset_ids:
    # Randomly link some assets to the Project
    if randint(0, 1): # ~50% chance
        relationships.append({
            "source": project_id,
            "target": asset_id,
            "type": "has_asset"
        })

    # Randomly link some assets to Stories
    if randint(0, 1): # ~50% chance
        story_id = choice(story_ids)
        relationships.append({
            "source": story_id,
            "target": asset_id,
            "type": "has_related_asset"
        })

    # Randomly link some assets to Companies
    if randint(0, 1): # ~50% chance
        company_id = choice(company_ids)
        relationships.append({
            "source": company_id,
            "target": asset_id,
            "type": "submitted_asset"
        })

    # Randomly link some assets to Teams
    if randint(0, 1): # ~50% chance
        team_id = choice(team_ids)
        relationships.append({
            "source": team_id,
            "target": asset_id,
            "type": "created_asset"
        })

# Create the final data structure
data = {
    "nodes": nodes,
    "relationships": relationships,
    "assets": asset_ids
}

# Write to JSON file
with open("building_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Data has been generated and saved to building_data.json") 