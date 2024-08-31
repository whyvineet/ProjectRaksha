// DOM elements
const canvas = document.getElementById('grid-canvas');
const ctx = canvas.getContext('2d');
const findPathButton = document.getElementById('find-path');
const resetButton = document.getElementById('reset');
const selectStartButton = document.getElementById('select-start');
const selectEndButton = document.getElementById('select-end');
const pointButtonsContainer = document.getElementById('point-buttons');
const safetyScoreElement = document.getElementById('safety-score');
const routeDistanceElement = document.getElementById('route-distance');

// Grid configuration
const gridSize = 10;
const cellSize = 40;
const gridPoints = Array(gridSize * gridSize).fill(0);

// Canvas setup
canvas.width = gridSize * cellSize;
canvas.height = gridSize * cellSize;

// State variables
let startCell = null;
let endCell = null;
let currentPoints = null;
let selectingStart = false;
let selectingEnd = false;

// Color palette for safety points
const colors = [
    '#FFFFFF', '#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6',
    '#42A5F5', '#2196F3', '#1E88E5', '#1976D2', '#1565C0', '#0D47A1'
];

// Create buttons for assigning safety points
function createPointButtons() {
    for (let i = 1; i <= 10; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.addEventListener('click', () => {
            currentPoints = i;
            document.querySelectorAll('#point-buttons button').forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
        });
        pointButtonsContainer.appendChild(button);
    }
}

// Draw the grid
function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            const index = i * gridSize + j;
            const x = j * cellSize;
            const y = i * cellSize;
            
            ctx.strokeStyle = '#ccc';
            ctx.strokeRect(x, y, cellSize, cellSize);
            
            const points = gridPoints[index];
            ctx.fillStyle = colors[points];
            ctx.fillRect(x, y, cellSize, cellSize);
            
            if (points > 0) {
                ctx.fillStyle = 'black';
                ctx.font = '14px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(points, x + cellSize / 2, y + cellSize / 2);
            }
        }
    }
    
    if (startCell) {
        drawCell(startCell.x, startCell.y, '#E91E63');
    }
    if (endCell) {
        drawCell(endCell.x, endCell.y, '#9C27B0');
    }
}

// Draw a single cell
function drawCell(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
}

// Reset the grid
function resetGrid() {
    gridPoints.fill(0);
    startCell = null;
    endCell = null;
    currentPoints = null;
    selectingStart = false;
    selectingEnd = false;
    findPathButton.disabled = true;
    updateInfoPanel('N/A', 'N/A');
    drawGrid();
}

// Update the info panel
function updateInfoPanel(safetyScore, distance, mode) {
    safetyScoreElement.textContent = `Safety Score: ${safetyScore}`;
    routeDistanceElement.textContent = `Distance: ${distance} (${mode} mode)`;
}

// Get neighboring cells
function getNeighbors(id) {
    const neighbors = [];
    const row = Math.floor(id / gridSize);
    const col = id % gridSize;

    if (row > 0) neighbors.push(id - gridSize);
    if (row < gridSize - 1) neighbors.push(id + gridSize);
    if (col > 0) neighbors.push(id - 1);
    if (col < gridSize - 1) neighbors.push(id + 1);

    return neighbors;
}

// Heuristic function for A* algorithm (Manhattan distance)
function heuristic(a, b) {
    const [ax, ay] = [a % gridSize, Math.floor(a / gridSize)];
    const [bx, by] = [b % gridSize, Math.floor(b / gridSize)];
    return Math.abs(ax - bx) + Math.abs(ay - by);
}

// Improved A* algorithm considering both safety and distance
function findBestPath(startId, endId) {
    const shortestPath = findPath(startId, endId, 'shortest');
    const safestPath = findPath(startId, endId, 'safest');

    const shortestRatio = shortestPath.safetyScore / (shortestPath.path.length - 1);
    const safestRatio = safestPath.safetyScore / (safestPath.path.length - 1);

    if (safestRatio - shortestRatio > 0.5) {
        return { ...safestPath, mode: 'safest' };
    } else {
        return { ...shortestPath, mode: 'shortest' };
    }
}

function findPath(startId, endId, mode) {
    const openSet = [startId];
    const cameFrom = {};
    const gScore = Array(gridSize * gridSize).fill(Infinity);
    const fScore = Array(gridSize * gridSize).fill(Infinity);
    const safetyScore = Array(gridSize * gridSize).fill(0);

    gScore[startId] = 0;
    fScore[startId] = heuristic(startId, endId);

    while (openSet.length > 0) {
        const current = openSet.reduce((a, b) => fScore[a] < fScore[b] ? a : b);

        if (current === endId) {
            const path = reconstructPath(cameFrom, current);
            return { path, safetyScore: safetyScore[current] };
        }

        openSet.splice(openSet.indexOf(current), 1);

        for (const neighbor of getNeighbors(current)) {
            if (gridPoints[neighbor] === 0) continue;

            const tentativeGScore = gScore[current] + 1;
            const tentativeSafetyScore = safetyScore[current] + gridPoints[neighbor];

            if (tentativeGScore < gScore[neighbor]) {
                cameFrom[neighbor] = current;
                gScore[neighbor] = tentativeGScore;
                safetyScore[neighbor] = tentativeSafetyScore;
                
                if (mode === 'shortest') {
                    fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, endId);
                } else { // 'safest'
                    fScore[neighbor] = gScore[neighbor] - (safetyScore[neighbor] * 2) + heuristic(neighbor, endId);
                }

                if (!openSet.includes(neighbor)) {
                    openSet.push(neighbor);
                }
            }
        }
    }

    return { path: [], safetyScore: 0 };
}

// Helper function to reconstruct the path
function reconstructPath(cameFrom, current) {
    const path = [current];
    while (current in cameFrom) {
        current = cameFrom[current];
        path.unshift(current);
    }
    return path;
}

// Highlight the found path
function highlightPath(path) {
    drawGrid(); // Redraw the grid to clear previous path
    if (path.length === 0) {
        // Display "Path Not Found" on the canvas
        ctx.fillStyle = 'red';
        ctx.font = '24px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Path Not Found', canvas.width / 2, canvas.height / 2);
    } else {
        ctx.strokeStyle = '#FF5722';
        ctx.lineWidth = 3;
        ctx.beginPath();
        path.forEach((id, index) => {
            const x = (id % gridSize) * cellSize + cellSize / 2;
            const y = Math.floor(id / gridSize) * cellSize + cellSize / 2;
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();
    }
}

// Event Listeners
canvas.addEventListener('click', (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) / cellSize);
    const y = Math.floor((event.clientY - rect.top) / cellSize);
    const index = y * gridSize + x;

    if (selectingStart) {
        startCell = { x, y };
        selectingStart = false;
        selectStartButton.classList.remove('selected');
    } else if (selectingEnd) {
        endCell = { x, y };
        selectingEnd = false;
        selectEndButton.classList.remove('selected');
    } else if (currentPoints !== null) {
        gridPoints[index] = currentPoints;
    }

    drawGrid();
    findPathButton.disabled = !(startCell && endCell);
});

selectStartButton.addEventListener('click', () => {
    selectingStart = true;
    selectingEnd = false;
    selectStartButton.classList.add('selected');
    selectEndButton.classList.remove('selected');
});

selectEndButton.addEventListener('click', () => {
    selectingEnd = true;
    selectingStart = false;
    selectEndButton.classList.add('selected');
    selectStartButton.classList.remove('selected');
});

findPathButton.addEventListener('click', () => {
    if (startCell && endCell) {
        const startId = startCell.y * gridSize + startCell.x;
        const endId = endCell.y * gridSize + endCell.x;

        const result = findBestPath(startId, endId);
        highlightPath(result.path);
        if (result.path.length === 0) {
            updateInfoPanel('N/A', 'N/A');
        } else {
            updateInfoPanel(result.safetyScore, result.path.length - 1, result.mode);
        }
    }
});

resetButton.addEventListener('click', resetGrid);

// Initialize the grid
createPointButtons();
drawGrid();