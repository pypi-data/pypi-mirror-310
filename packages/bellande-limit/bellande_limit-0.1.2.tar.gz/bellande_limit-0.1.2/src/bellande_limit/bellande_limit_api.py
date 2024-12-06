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

def make_bellande_limit_request(node0, node1, environment, size, goal, obstacles=None, search_radius=50, sample_points=20):
    url = "https://bellande-robotics-sensors-research-innovation-center.org/api/Bellande_Limit/bellande_limit"
    
    # Convert string inputs to lists if they're strings
    if isinstance(node0, str):
        node0 = json.loads(node0)
    if isinstance(node1, str):
        node1 = json.loads(node1)
    if isinstance(environment, str):
        environment = json.loads(environment)
    if isinstance(size, str):
        size = json.loads(size)
    if isinstance(goal, str):
        goal = json.loads(goal)
    if isinstance(obstacles, str):
        obstacles = json.loads(obstacles)
        
    payload = {
        "node0": node0,
        "node1": node1,
        "environment": environment,
        "size": size,
        "goal": goal,
        "obstacles": obstacles or [],
        "search_radius": search_radius,
        "sample_points": sample_points,
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
    parser = argparse.ArgumentParser(description="Run Bellande Limit API")
    parser.add_argument("--node0", required=True, help="Starting point coordinates as JSON-formatted list")
    parser.add_argument("--node1", required=True, help="Target point coordinates as JSON-formatted list")
    parser.add_argument("--environment", required=True, help="Environment dimensions as JSON-formatted list")
    parser.add_argument("--size", required=True, help="Step sizes for each dimension as JSON-formatted list")
    parser.add_argument("--goal", required=True, help="Goal coordinates as JSON-formatted list")
    parser.add_argument("--obstacles", help="List of obstacles as JSON-formatted list of objects with 'position' and 'dimensions'")
    parser.add_argument("--search-radius", type=float, default=50.0, help="Search radius for obstacle detection")
    parser.add_argument("--sample-points", type=int, default=20, help="Number of sample points for obstacle detection")
    
    args = parser.parse_args()
    
    try:
        result = make_bellande_limit_request(
            args.node0,
            args.node1,
            args.environment,
            args.size,
            args.goal,
            args.obstacles,
            args.search_radius,
            args.sample_points
        )
        
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in input parameters - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
