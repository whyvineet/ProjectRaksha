# Secure Route Algorithm

## Overview
The Secure Route Algorithm is a part of Project Raksha, designed to enhance women's safety by finding the safest route between two points. This implementation uses a grid-based system where each cell can be assigned a safety score, and the algorithm finds the path with the highest overall safety score.

## Features
- Grid-based representation of an area
- Assignable safety scores for each grid cell
- A* pathfinding algorithm optimized for safety
- Visual representation of the grid and path
- Interactive UI for setting start and end points, assigning safety scores, and finding the safest route

## Files
- `index.html`: The main HTML file containing the structure of the web application
- `styles.css`: CSS file for styling the application
- `script.js`: JavaScript file containing the core algorithm and UI interactions

## How to Use
1. Open `index.html` in a web browser to start the application.
2. Use the number buttons (1-10) to select a safety score.
3. Click on grid cells to assign the selected safety score to those cells.
4. Click "Select Start" and then click a cell to set the starting point.
5. Click "Select End" and then click a cell to set the ending point.
6. Click "Find Safest Route" to calculate and display the safest path.
7. Use "Reset Grid" to clear all assignments and start over.

## Algorithm Details
The core of the Secure Route Algorithm is based on the A* pathfinding algorithm, with the following modifications:
- The algorithm considers both distance and safety score when evaluating paths.
- Cells with a safety score of 0 are considered impassable.
- The heuristic function balances between finding the shortest path and the safest path.

## Customization
You can customize the algorithm by modifying the following parameters in `script.js`:
- `gridSize`: Change the dimensions of the grid (default is 10x10)
- `cellSize`: Adjust the visual size of each cell (default is 40 pixels)
- `colors`: Modify the color scheme used for different safety scores

## Limitations
- The current implementation is a prototype and may not scale well for very large grids.
- The algorithm assumes a static environment and does not account for real-time changes in safety conditions.

## Future Improvements
- Implement dynamic safety score updates based on time of day or real-time data
- Add support for different types of safety landmarks (e.g., police stations, well-lit areas)
- Integrate with real map data for practical use in navigation applications