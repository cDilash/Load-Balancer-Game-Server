# Game Server Load Balancer System

A Python implementation of a round-robin load balancer for game servers with real-time metrics tracking and visualization capabilities.

## System Components

1. **Game Load Balancer (load_balancer.py)**
   - Implements round-robin player distribution
   - Real-time game request processing simulation
   - Thread-safe metrics logging
   - Performance monitoring

2. **System Architecture (system.py)**
   - Generates visual game server architecture diagram
   - Shows component relationships and data flow
   - Uses custom styling with green theme

3. **Metrics Visualization (visualize_metrics.py)**
   - Creates performance visualizations:
     - Bar chart: Average response time per game server
     - Line chart: Response time trends
     - Pie chart: Player distribution
   - Generates summary statistics

## Setup and Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the game server simulation:
   ```bash
   python src/load_balancer.py
   ```

2. Generate system architecture diagram:
   ```bash
   python src/system.py
   ```

3. Create performance visualizations:
   ```bash
   python src/visualize_metrics.py
   ```

## Output Files

- **Logs:**
  - `output/logs/server_logs.txt`: Detailed player request logs
  - `output/logs/metrics.csv`: Raw performance metrics

- **Visualizations:**
  - `output/visualizations/Game_Server_Architecture.png`
  - `output/visualizations/server_performance_bar.png`
  - `output/visualizations/server_performance_line.png`
  - `output/visualizations/player_distribution_pie.png`

## Features

- Round-robin game server load balancing
- Real-time player request simulation
- Thread-safe operations
- Performance metrics tracking
- Custom styled visualizations
- Comprehensive logging system

## Customization

- Adjust number of game servers: Modify `server_count` in `load_balancer.py`
- Change number of players: Modify `num_players` in simulation
- Customize processing time: Adjust `random.uniform(1, 3)` range

