import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

plt.style.use('classic')

fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

colors = {
    'box_fill': '#2d6a4f',
    'box_edge': '#1b4332',
    'text': '#ffffff',
    'arrow': '#40916c',
    'arrow_text': '#1b4332',
    'title': '#1b4332'
}

components = {
    "Players\n(Game Requests)": (1, 4),
    "Game Load\nBalancer": (4, 4),
    "Game Server 1": (7, 5),
    "Game Server 2": (7, 4),
    "Game Server 3": (7, 3),
    "Metrics Logger": (10, 4)
}

for comp, (x, y) in components.items():
    if "Players" in comp:
        width = 1.6
        height = 0.8
        x_offset = 0.8
    else:
        width = 1.2
        height = 0.6
        x_offset = 0.6
    
    shadow = patches.FancyBboxPatch((x - x_offset, y - 0.35), width, height + 0.1,
                                   boxstyle="round,pad=0.1",
                                   facecolor='gray', alpha=0.3)
    ax.add_patch(shadow)
    
    box = patches.FancyBboxPatch((x - x_offset, y - 0.3), width, height,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['box_fill'],
                                edgecolor=colors['box_edge'])
    ax.add_patch(box)
    
    if "Players" in comp:
        font_size = 9
    else:
        font_size = 10
        
    ax.text(x, y, comp, fontsize=font_size, fontweight='bold',
            ha="center", va="center", color=colors['text'])

arrows = [
    ("Players\n(Game Requests)", "Game Load\nBalancer", "Player Requests"),
    ("Game Load\nBalancer", "Game Server 1", "Distribute Players"),
    ("Game Load\nBalancer", "Game Server 2", "Distribute Players"),
    ("Game Load\nBalancer", "Game Server 3", "Distribute Players"),
    ("Game Server 1", "Metrics Logger", "Log Performance"),
    ("Game Server 2", "Metrics Logger", "Log Performance"),
    ("Game Server 3", "Metrics Logger", "Log Performance")
]

for start, end, label in arrows:
    start_x, start_y = components[start]
    end_x, end_y = components[end]
    
    ax.annotate("",
                xy=(end_x - 0.6, end_y),
                xytext=(start_x + 0.6, start_y),
                arrowprops=dict(arrowstyle="fancy",
                              connectionstyle="arc3,rad=.1",
                              color=colors['arrow'],
                              lw=2))
    
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2 + 0.1
    text = ax.text(mid_x, mid_y, label,
                   fontsize=9, ha="center", va="center",
                   color=colors['arrow_text'],
                   fontweight='medium',
                   bbox=dict(facecolor='white',
                           edgecolor='none',
                           alpha=0.7,
                           pad=2))

ax.set_xlim(0, 12)
ax.set_ylim(2, 6)
ax.axis("off")

plt.title("Game Server Architecture",
          fontsize=16,
          fontweight='bold',
          color=colors['title'],
          pad=20)

ax.grid(True, linestyle='--', alpha=0.1)

os.makedirs('output/visualizations', exist_ok=True)

plt.tight_layout()
plt.savefig("output/visualizations/Game_Server_Architecture.png", 
            dpi=300, 
            bbox_inches='tight',
            facecolor=fig.get_facecolor(),
            edgecolor='none')
plt.show() 
