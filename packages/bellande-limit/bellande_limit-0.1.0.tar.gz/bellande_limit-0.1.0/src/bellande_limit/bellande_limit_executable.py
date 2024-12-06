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
    
    return os.path.join(application_path, 'Bellande_Limit')

def run_bellande_limit(node0, node1, environment, size, goal, obstacles=None, search_radius=50, sample_points=20):
    executable_path = get_executable_path()
    passcode = "bellande_limit_executable_access_key"
    
    # Convert string representations to actual lists/objects
    node0_list = json.loads(node0)
    node1_list = json.loads(node1)
    environment_list = json.loads(environment)
    size_list = json.loads(size)
    goal_list = json.loads(goal)
    obstacles_list = json.loads(obstacles) if obstacles else []
    
    # Validate input dimensions
    dimensions = len(environment_list)
    if not all(len(x) == dimensions for x in [node0_list, node1_list, size_list, goal_list]):
        raise ValueError(f"All coordinates must have {dimensions} dimensions")
    
    # Validate obstacles
    for obstacle in obstacles_list:
        if len(obstacle['position']) != dimensions or len(obstacle['dimensions']) != dimensions:
            raise ValueError(f"Obstacle position and dimensions must have {dimensions} dimensions")
    
    # Prepare the command
    command = [
        executable_path,
        passcode,
        json.dumps(node0_list),
        json.dumps(node1_list),
        json.dumps(environment_list),
        json.dumps(size_list),
        json.dumps(goal_list),
        json.dumps(obstacles_list),
        str(search_radius),
        str(sample_points)
    ]
    
    # Run the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
        print("Error output:", e.stderr)

def main():
    parser = argparse.ArgumentParser(description="Run Bellande Limit Executable")
    parser.add_argument("--node0", required=True, help="Starting point coordinates as JSON-formatted list")
    parser.add_argument("--node1", required=True, help="Target point coordinates as JSON-formatted list")
    parser.add_argument("--environment", required=True, help="Environment dimensions as JSON-formatted list")
    parser.add_argument("--size", required=True, help="Step sizes for each dimension as JSON-formatted list")
    parser.add_argument("--goal", required=True, help="Goal coordinates as JSON-formatted list")
    parser.add_argument("--obstacles", help="List of obstacles as JSON-formatted list of objects with 'position' and 'dimensions'")
    parser.add_argument("--search-radius", type=float, default=50.0, help="Search radius for obstacle detection")
    parser.add_argument("--sample-points", type=int, default=20, help="Number of sample points for obstacle detection")
    
    args = parser.parse_args()
    
    run_bellande_limit(
        args.node0,
        args.node1,
        args.environment,
        args.size,
        args.goal,
        args.obstacles,
        args.search_radius,
        args.sample_points
    )

if __name__ == "__main__":
    main()
