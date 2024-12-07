# Copyright (C) 2024 Bellande Robotics Sensors Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3

import requests
import argparse
import json
import sys

def make_node_importance_request(node, nodes, important_nodes, adjacent_segments, grid_steps, min_segment_coverage=0.5):
    url = "https://bellande-robotics-sensors-research-innovation-center.org/api/Bellande_Node_Importance/node_importance"
    
    # Convert string inputs to Python objects if they're strings
    if isinstance(node, str):
        node = json.loads(node)
    if isinstance(nodes, str):
        nodes = json.loads(nodes)
    if isinstance(important_nodes, str):
        important_nodes = json.loads(important_nodes)
    if isinstance(adjacent_segments, str):
        adjacent_segments = json.loads(adjacent_segments)
    if isinstance(grid_steps, str):
        grid_steps = json.loads(grid_steps)
    
    payload = {
        "node": node,
        "nodes": nodes,
        "important_nodes": important_nodes,
        "adjacent_segments": adjacent_segments,
        "grid_steps": grid_steps,
        "min_segment_coverage": min_segment_coverage,
        "auth": {
            "authorization_key": "bellande_web_api_opensource"
        }
    }
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error making request: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run Bellande Node Importance API")
    parser.add_argument("--node", required=True, 
                      help="Node to evaluate as JSON object with 'coords' and 'segment'")
    parser.add_argument("--nodes", required=True, 
                      help="List of recent nodes as JSON array of objects with 'coords' and 'segment'")
    parser.add_argument("--important-nodes", required=True, 
                      help="Dictionary of important nodes by segment as JSON object")
    parser.add_argument("--adjacent-segments", required=True, 
                      help="Dictionary of adjacent segments as JSON object")
    parser.add_argument("--grid-steps", required=True, 
                      help="Grid step sizes for each dimension as JSON array")
    parser.add_argument("--min-segment-coverage", type=float, default=0.5, 
                      help="Minimum required segment coverage ratio")
    
    args = parser.parse_args()
    
    try:
        result = make_node_importance_request(
            args.node,
            args.nodes,
            args.important_nodes,
            args.adjacent_segments,
            args.grid_steps,
            args.min_segment_coverage
        )
        
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in input parameters - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
