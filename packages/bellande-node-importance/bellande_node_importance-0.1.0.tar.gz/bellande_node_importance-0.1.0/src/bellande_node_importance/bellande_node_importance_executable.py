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

import subprocess
import argparse
import json
import os
import sys

def get_executable_path():
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(application_path, 'Bellande_Node_Importance')

def run_node_importance(node, nodes, important_nodes, adjacent_segments, grid_steps, min_segment_coverage=0.5):
    executable_path = get_executable_path()
    passcode = "bellande_node_importance_executable_access_key"
    
    # Convert string representations to actual objects
    node_obj = json.loads(node)
    nodes_list = json.loads(nodes)
    important_nodes_dict = json.loads(important_nodes)
    adjacent_segments_dict = json.loads(adjacent_segments)
    grid_steps_list = json.loads(grid_steps)
    
    # Validate input dimensions
    dimensions = len(node_obj['coords'])
    if not all(len(n['coords']) == dimensions for n in nodes_list):
        raise ValueError(f"All nodes must have {dimensions} dimensions")
    
    # Validate important nodes dimensions
    for segment_nodes in important_nodes_dict.values():
        if not all(len(n['coords']) == dimensions for n in segment_nodes):
            raise ValueError(f"All important nodes must have {dimensions} dimensions")
    
    # Validate grid steps
    if len(grid_steps_list) != dimensions:
        raise ValueError(f"Grid steps must have {dimensions} dimensions")
    
    # Prepare the command
    command = [
        executable_path,
        passcode,
        json.dumps(node_obj),
        json.dumps(nodes_list),
        json.dumps(important_nodes_dict),
        json.dumps(adjacent_segments_dict),
        json.dumps(grid_steps_list),
        str(min_segment_coverage)
    ]
    
    # Run the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
        print("Error output:", e.stderr)

def main():
    parser = argparse.ArgumentParser(description="Run Bellande Node Importance Executable")
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
    
    run_node_importance(
        args.node,
        args.nodes,
        args.important_nodes,
        args.adjacent_segments,
        args.grid_steps,
        args.min_segment_coverage
    )

if __name__ == "__main__":
    main()
