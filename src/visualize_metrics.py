
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def set_custom_style():
    """
    Configure matplotlib style settings for consistent visualization appearance
    Sets white background and other visual parameters
    """
    plt.style.use('classic')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3

def load_metrics():
    """
    Load and preprocess metrics data from CSV file
    Converts time strings to datetime objects and processing time to float
    """
    df = pd.read_csv('output/logs/metrics.csv')
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df['processing_time'] = df['processing_time'].astype(float)
    return df

def create_bar_chart(df):
    """
    Create bar chart showing average processing time for each game server
    Includes custom styling, labels, and green color scheme
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Calculate average processing time per server
    avg_times = df.groupby('server_id')['processing_time'].mean()
    
    # Define green color palette
    colors = {
        'box_fill': '#2d6a4f',
        'box_edge': '#1b4332',
        'text': '#ffffff',
        'bars': ['#40916c', '#2d6a4f', '#1b4332']
    }
    
    # Create and style bars
    bars = plt.bar(avg_times.index, avg_times.values, color=colors['bars'], width=0.6)
    
    for bar in bars:
        bar.set_edgecolor(colors['box_edge'])
        bar.set_alpha(0.8)
    
    plt.title('Average Response Time by Game Server', 
              fontsize=16, 
              fontweight='bold', 
              pad=20,
              color=colors['box_edge'])
    
    plt.xlabel('Server ID', fontsize=12, color=colors['box_edge'], labelpad=10)
    plt.ylabel('Average Response Time (seconds)', fontsize=12, color=colors['box_edge'], labelpad=10)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.2f}s',
                ha='center', va='bottom',
                fontsize=10, fontweight='bold',
                color=colors['box_edge'])
    
    # Customize grid and spines
    ax.grid(True, linestyle='--', alpha=0.1)
    ax.set_axisbelow(True)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(colors['box_edge'])
    ax.spines['bottom'].set_color(colors['box_edge'])
    
    # Create output directory if it doesn't exist
    os.makedirs('output/visualizations', exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig('output/visualizations/server_performance_bar.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor=fig.get_facecolor(),
                edgecolor='none')
    plt.close()

def create_line_chart(df):
    """
    Create line chart showing response time trends for each game server
    Includes markers, legend, and custom styling
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    colors = {
        'lines': ['#40916c', '#2d6a4f', '#1b4332'],
        'text': '#1b4332',
        'grid': '#1b4332'
    }
    
    for idx, server in enumerate(sorted(df['server_id'].unique())):
        server_data = df[df['server_id'] == server].sort_values('start_time')
        plt.plot(range(len(server_data)), 
                server_data['processing_time'],
                marker='o',
                markersize=8,
                linewidth=2,
                color=colors['lines'][idx],
                label=server,
                alpha=0.8)
    
    plt.title('Response Time Trends by Game Server', 
              fontsize=16, 
              fontweight='bold', 
              pad=20,
              color=colors['text'])
    
    plt.xlabel('Player Request Sequence', fontsize=12, color=colors['text'], labelpad=10)
    plt.ylabel('Response Time (seconds)', fontsize=12, color=colors['text'], labelpad=10)
    
    legend = plt.legend(bbox_to_anchor=(1.02, 1), 
                       loc='upper left',
                       borderaxespad=0,
                       frameon=True,
                       facecolor='white',
                       edgecolor=colors['text'],
                       shadow=True)
    
    for text in legend.get_texts():
        text.set_color(colors['text'])
        text.set_fontweight('bold')
    
    ax.grid(True, linestyle='--', alpha=0.1)
    ax.set_axisbelow(True)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(colors['text'])
    ax.spines['bottom'].set_color(colors['text'])
    
    plt.tight_layout()
    plt.savefig('output/visualizations/server_performance_line.png',
                dpi=300,
                bbox_inches='tight',
                facecolor=fig.get_facecolor(),
                edgecolor='none')
    plt.close()

def create_player_distribution_chart(df):
    """
    Create pie chart showing distribution of players across game servers
    Includes percentage labels and shadow effect
    """
    plt.figure(figsize=(10, 8))
    fig = plt.gcf()
    fig.patch.set_facecolor('white')
    
    # Count players per server
    player_counts = df['server_id'].value_counts()
    
    # Green colors for pie chart
    colors = ['#40916c', '#2d6a4f', '#1b4332']
    
    wedges, texts, autotexts = plt.pie(player_counts.values,
                                      labels=player_counts.index,
                                      autopct='%1.1f%%',
                                      colors=colors,
                                      startangle=90,
                                      pctdistance=0.85,
                                      explode=[0.05] * len(player_counts),
                                      shadow=True)
    
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.setp(texts, size=12, weight="bold", color="#1b4332")
    
    plt.title('Player Distribution Across Game Servers', 
              fontsize=16, 
              fontweight='bold', 
              pad=20,
              color='#1b4332')
    
    plt.tight_layout()
    plt.savefig('output/visualizations/player_distribution_pie.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor=fig.get_facecolor(),
                edgecolor='none')
    plt.close()

def generate_summary_stats(df):
    """
    Calculate and display summary statistics for the game server performance
    Includes total players, average/min/max response times
    """
    stats = {
        'total_players': len(df),
        'avg_response_time': df['processing_time'].mean(),
        'min_response_time': df['processing_time'].min(),
        'max_response_time': df['processing_time'].max(),
        'total_processing_time': df['processing_time'].sum()
    }
    
    print("\n📊 Game Server Performance Summary:")
    print("=" * 50)
    print(f"Total Players Served: {stats['total_players']}")
    print(f"Average Response Time: {stats['avg_response_time']:.3f} seconds")
    print(f"Minimum Response Time: {stats['min_response_time']:.3f} seconds")
    print(f"Maximum Response Time: {stats['max_response_time']:.3f} seconds")
    print(f"Total Processing Time: {stats['total_processing_time']:.3f} seconds")

def main():
    """
    Main function to generate all visualizations and statistics
    """
    # Set up visualization style
    set_custom_style()
    
    # Load and process metrics data
    df = load_metrics()
    
    # Generate all visualizations
    print("Generating game server performance visualizations...")
    create_bar_chart(df)
    create_line_chart(df)
    create_player_distribution_chart(df)
    
    # Display summary statistics
    generate_summary_stats(df)
    
    print("\n📈 Visualization files generated in output/visualizations/:")
    print("  - server_performance_bar.png")
    print("  - server_performance_line.png")
    print("  - player_distribution_pie.png")

if __name__ == "__main__":
    main() 