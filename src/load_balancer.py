import time
import random
from datetime import datetime
import threading
from queue import Queue
import logging
import csv
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class PlayerMetrics:
    """
    Data class to store metrics for each player request
    Tracks player ID, server assignment, timing, and processing duration
    """
    player_id: str
    server_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    processing_time: Optional[float] = None

    def to_dict(self):
        """Convert metrics to dictionary format for CSV logging"""
        return {
            'player_id': self.player_id,
            'server_id': self.server_id,
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S.%f") if self.end_time else '',
            'processing_time': f"{self.processing_time:.3f}" if self.processing_time else ''
        }

class MetricsLogger:
    """
    Handles logging of player request metrics to both text and CSV files
    Provides thread-safe logging operations
    """
    def __init__(self):
        # Create output/logs directory if it doesn't exist
        os.makedirs('output/logs', exist_ok=True)
        
        # Configure text file logging
        logging.basicConfig(
            filename='output/logs/server_logs.txt',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set up CSV logging
        self.csv_file = 'output/logs/metrics.csv'
        self.write_csv_header()
        
        # Thread-safe lock for file operations
        self.log_lock = threading.Lock()

    def write_csv_header(self):
        """Initialize CSV file with column headers"""
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['player_id', 'server_id', 'start_time', 'end_time', 'processing_time'])
            writer.writeheader()

    def log_request(self, metrics: PlayerMetrics):
        """Log player request metrics to both text and CSV files"""
        with self.log_lock:
            # Log to text file
            logging.info(
                f"Player: {metrics.player_id}, Server: {metrics.server_id}, "
                f"Processing Time: {metrics.processing_time:.3f}s"
            )
            
            # Log to CSV file
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['player_id', 'server_id', 'start_time', 'end_time', 'processing_time'])
                writer.writerow(metrics.to_dict())

class GameServer:
    """
    Represents a game server instance that processes player requests
    Includes request queue management and metric tracking
    """
    def __init__(self, id, metrics_logger):
        self.id = id
        self.players = []
        self.is_active = True
        self.request_queue = Queue()
        self.metrics_logger = metrics_logger
        self.load_balancer = None
        self.processing_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.processing_thread.start()

    def handle_player(self, player_id):
        """Add a new player request to the server's processing queue"""
        if self.is_active:
            self.players.append(player_id)
            metrics = PlayerMetrics(
                player_id=player_id,
                server_id=self.id,
                start_time=datetime.now()
            )
            self.request_queue.put((player_id, metrics))
            return True
        return False

    def _process_queue(self):
        """Background thread that continuously processes queued player requests"""
        while True:
            if not self.request_queue.empty():
                player_id, metrics = self.request_queue.get()
                self._handle_request(player_id, metrics)
            time.sleep(0.1)

    def _handle_request(self, player_id, metrics: PlayerMetrics):
        """Process a single player request and update its metrics"""
        # Simulate processing time between 1-3 seconds
        processing_time = random.uniform(1, 3)
        time.sleep(processing_time)
        
        # Update metrics
        metrics.end_time = datetime.now()
        metrics.processing_time = processing_time
        
        # Log metrics
        self.metrics_logger.log_request(metrics)
        
        # Update load balancer statistics
        if self.load_balancer:
            self.load_balancer.update_metrics(self.id, processing_time)
        
        # Log completion to console
        completion_time = datetime.now().strftime("%H:%M:%S")
        print(f"✨ [{completion_time}] {self.id} processed request from Player_{player_id} in {processing_time:.2f} seconds")

    def get_status(self):
        """Return current server status and statistics"""
        return {
            'id': self.id,
            'active': self.is_active,
            'player_count': len(self.players),
            'players': self.players,
            'queued_requests': self.request_queue.qsize()
        }

class GameLoadBalancer:
    """
    Implements a round-robin load balancer for game servers
    Distributes player requests evenly across multiple servers
    """
    def __init__(self, server_count=3):
        self.metrics_logger = MetricsLogger()
        self.servers = [GameServer(f"Game_Server_{i+1}", self.metrics_logger) for i in range(server_count)]
        self.current_server_index = 0
        self.player_counter = 0
        self.start_time = None
        self.server_metrics = {server.id: {'total_requests': 0, 'total_time': 0.0} for server in self.servers}

    def get_next_server(self):
        """Select the next available server using round-robin algorithm"""
        start_index = self.current_server_index
        while True:
            server = self.servers[self.current_server_index]
            self.current_server_index = (self.current_server_index + 1) % len(self.servers)
            
            if server.is_active:
                return server
                
            if self.current_server_index == start_index:
                return None

    def connect_player(self, player_id):
        """Assign a player to the next available game server"""
        if self.start_time is None:
            self.start_time = datetime.now()

        current_time = datetime.now().strftime("%H:%M:%S")
        server = self.get_next_server()
        
        if server is None:
            print(f"❌ [{current_time}] No available servers for Player_{player_id}")
            return False
            
        if server.handle_player(player_id):
            print(f"➡️  [{current_time}] Player_{player_id} connected to {server.id}")
            return True
        
        return False

    def get_server_stats(self):
        """Generate performance statistics for all game servers"""
        stats = []
        for server in self.servers:
            metrics = self.server_metrics[server.id]
            total_requests = metrics['total_requests']
            avg_time = metrics['total_time'] / total_requests if total_requests > 0 else 0
            
            stats.append({
                'id': server.id,
                'active': server.is_active,
                'request_count': total_requests,
                'avg_response_time': avg_time,
                'players': server.players,
                'queued_requests': server.request_queue.qsize()
            })
        return stats

    def update_metrics(self, server_id, processing_time):
        """Update performance metrics for a specific server"""
        metrics = self.server_metrics[server_id]
        metrics['total_requests'] += 1
        metrics['total_time'] += processing_time

def simulate_game_server(num_players=20, delay_between_requests=0.5):
    """
    Run a simulation of the game server load balancer
    Simulates player connections and request processing
    """
    # Initialize load balancer
    load_balancer = GameLoadBalancer()
    
    # Set up bidirectional reference
    for server in load_balancer.servers:
        server.load_balancer = load_balancer
    
    print("\n🎮 Starting Game Server Simulation with 20 players...\n")
    
    # Simulate player connections
    for i in range(num_players):
        player_id = f"{i+1}"
        load_balancer.connect_player(player_id)
        time.sleep(delay_between_requests)
    
    # Wait for all requests to complete
    all_queues_empty = False
    while not all_queues_empty:
        all_queues_empty = True
        for server in load_balancer.servers:
            if not server.request_queue.empty():
                all_queues_empty = False
                break
        time.sleep(0.1)
    
    time.sleep(0.5)
    
    # Print final statistics
    print("\n📊 Final Server Statistics:")
    print("=" * 50)
    
    total_players = 0
    total_time = 0.0
    
    for server in load_balancer.get_server_stats():
        total_players += server['request_count']
        total_time += server['request_count'] * server['avg_response_time']
        
        print(f"\n{server['id']}:")
        print(f"  Players Handled: {server['request_count']}")
        print(f"  Average Response Time: {server['avg_response_time']:.3f} seconds")
        print(f"  Player List: {', '.join([f'Player_{p}' for p in server['players']])}")
    
    print("\n📈 Overall Statistics:")
    print("=" * 50)
    print(f"Total Players Connected: {total_players}")
    print(f"Average Response Time Across All Servers: {(total_time/total_players):.3f} seconds")
    
    print("\n📝 Detailed logs have been saved to:")
    print(f"  - Text logs: output/logs/server_logs.txt")
    print(f"  - CSV metrics: output/logs/metrics.csv")

if __name__ == "__main__":
    simulate_game_server(20, delay_between_requests=0.5) 