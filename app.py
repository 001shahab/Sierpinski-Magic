from flask import Flask, render_template, jsonify, Response
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import base64
import os
import json
import time
from threading import Thread
import queue

app = Flask(__name__)

# Store generation progress
generation_progress = {}

def generate_sierpinski_triangle_progressive(shape_id, max_iterations=25000):
    """Generate Sierpinski Triangle progressively using chaos game method"""
    # Define triangle vertices
    vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
    
    # Initialize
    current = np.array([0.5, 0.25])
    points = []
    colors = []
    
    # Generate points progressively
    for i in range(max_iterations):
        vertex_idx = np.random.randint(0, 3)
        vertex = vertices[vertex_idx]
        current = (current + vertex) / 2
        points.append(current.copy())
        colors.append(vertex_idx)
        
        # Update every 100 points
        if i % 100 == 0 or i == max_iterations - 1:
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none')
            ax.set_facecolor('none')
            
            # Plot points with colors
            if points:
                points_array = np.array(points)
                colors_array = np.array(colors)
                scatter = ax.scatter(points_array[:, 0], points_array[:, 1], 
                                   c=colors_array, cmap='plasma', s=0.5, alpha=0.8)
            
            # Remove axes
            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, 1)
            ax.axis('off')
            
            # Save to buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', 
                        transparent=True, dpi=150, pad_inches=0)
            buffer.seek(0)
            plt.close()
            
            # Update progress
            generation_progress[shape_id] = {
                'iteration': i + 1,
                'max_iterations': max_iterations,
                'image': base64.b64encode(buffer.getvalue()).decode(),
                'complete': i == max_iterations - 1
            }
            
            time.sleep(0.01)  # Small delay for smooth animation

def generate_fibonacci_spiral_progressive(shape_id, max_iterations=25000):
    """Generate a continuously growing Fibonacci Spiral"""
    points = []
    
    # Fibonacci numbers - generate more for larger spiral
    fib = [1, 1]
    while len(fib) < 25:  # More squares for bigger spiral
        fib.append(fib[-1] + fib[-2])
    
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    for i in range(max_iterations):
        # Create spiral that grows continuously
        # Map iterations to spiral growth (0 to ~20 full rotations)
        theta = (i / max_iterations) * 20 * np.pi
        
        # Logarithmic spiral equation with golden ratio
        r = 0.01 * np.exp(theta * np.log(phi) / (2 * np.pi))
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        points.append([x, y])
        
        # Update visualization
        if i % 200 == 0 or i == max_iterations - 1:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none')
            ax.set_facecolor('none')
            
            # Calculate current spiral extent
            current_max_r = 0.01 * np.exp(theta * np.log(phi) / (2 * np.pi))
            
            # Determine how many Fibonacci squares to show based on spiral size
            # This ensures we keep adding squares as the spiral grows
            total_fib_size = 0
            squares_to_show = 0
            for j, f in enumerate(fib):
                total_fib_size += f * 0.005
                if total_fib_size < current_max_r * 2:
                    squares_to_show = j + 1
                else:
                    break
            
            squares_to_show = max(4, min(squares_to_show, 20))
            
            # Scale factor to fit current view
            scale = 0.005 * (1 + i / 5000)  # Gradually increase scale
            
            # Draw Fibonacci squares
            x_pos, y_pos = 0, 0
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            
            # Track bounds
            min_x, max_x = 0, 0
            min_y, max_y = 0, 0
            
            for j in range(min(squares_to_show, len(fib))):
                size = fib[j] * scale
                
                # Draw square
                rect = patches.Rectangle((x_pos, y_pos), size, size,
                                       fill=False, edgecolor='goldenrod', 
                                       linewidth=2, alpha=0.7)
                ax.add_patch(rect)
                
                # Update bounds
                min_x = min(min_x, x_pos, x_pos + size)
                max_x = max(max_x, x_pos, x_pos + size)
                min_y = min(min_y, y_pos, y_pos + size)
                max_y = max(max_y, y_pos, y_pos + size)
                
                # Add labels for smaller squares only
                if j < 6:
                    ax.text(x_pos + size/2, y_pos + size/2, str(fib[j]),
                           ha='center', va='center', fontsize=8,
                           color='darkgoldenrod', alpha=0.6)
                
                # Move to next position
                if j % 4 == 0:  # right
                    x_pos += size
                elif j % 4 == 1:  # up
                    x_pos -= fib[j-1] * scale if j > 0 else 0
                    y_pos += size
                elif j % 4 == 2:  # left
                    x_pos -= size
                    y_pos -= fib[j-1] * scale if j > 0 else 0
                elif j % 4 == 3:  # down
                    y_pos -= size
            
            # Draw the spiral
            if len(points) > 1:
                points_array = np.array(points[:i+1])
                
                # Draw spiral with gradient
                segments = len(points_array) - 1
                # Only draw last portion if too many points
                start_idx = max(0, segments - 5000) if segments > 5000 else 0
                
                for k in range(start_idx, segments):
                    progress = (k - start_idx) / (segments - start_idx)
                    color = plt.cm.plasma(progress)
                    alpha = 0.3 + 0.7 * progress
                    ax.plot(points_array[k:k+2, 0], points_array[k:k+2, 1],
                           color=color, linewidth=2, alpha=alpha)
            
            # Update view to show everything with margin
            if len(points) > 0:
                margin = 0.1 * max(max_x - min_x, max_y - min_y)
                ax.set_xlim(min_x - margin, max_x + margin)
                ax.set_ylim(min_y - margin, max_y + margin)
            
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Save to buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', 
                        transparent=True, dpi=150, pad_inches=0)
            buffer.seek(0)
            plt.close()
            
            generation_progress[shape_id] = {
                'iteration': i + 1,
                'max_iterations': max_iterations,
                'image': base64.b64encode(buffer.getvalue()).decode(),
                'complete': i == max_iterations - 1
            }
            
            time.sleep(0.01)

def generate_dragon_curve_progressive(shape_id, max_iterations=25000):
    """Generate the mesmerizing Dragon Curve fractal"""
    # Pre-generate the full dragon curve sequence
    def generate_dragon_sequence(iterations):
        sequence = [1]  # 1 = turn right, -1 = turn left
        for _ in range(iterations):
            # Dragon curve rule: reverse the sequence, negate it, and insert between
            reversed_negated = [-x for x in reversed(sequence)]
            sequence = sequence + [1] + reversed_negated
        return sequence
    
    # Generate sequence up to level 14 (16384 turns)
    max_level = 14
    full_sequence = generate_dragon_sequence(max_level)
    
    # Starting position and direction
    points = [[0, 0]]
    x, y = 0, 0
    dx, dy = 1, 0  # Direction vector
    step_size = 0.01
    
    for i in range(max_iterations):
        # Move forward
        x += dx * step_size
        y += dy * step_size
        points.append([x, y])
        
        # Get the next turn from sequence
        if i < len(full_sequence):
            turn = full_sequence[i]
            # Rotate direction vector 90 degrees
            if turn == 1:  # Turn right
                dx, dy = dy, -dx
            else:  # Turn left
                dx, dy = -dy, dx
        
        # Update visualization more frequently at the beginning
        update_freq = 50 if i < 5000 else 100 if i < 15000 else 200
        
        if i % update_freq == 0 or i == max_iterations - 1:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none')
            ax.set_facecolor('none')
            
            if len(points) > 1:
                points_array = np.array(points)
                
                # Create different coloring based on progress
                progress = i / max_iterations
                
                if progress < 0.2:  # Early stage - show construction
                    # Color by segment order
                    for j in range(1, len(points_array)):
                        color = plt.cm.cool(j / len(points_array))
                        ax.plot(points_array[j-1:j+1, 0], points_array[j-1:j+1, 1],
                               color=color, linewidth=2, alpha=0.8)
                else:  # Later stages - show structure
                    # Color by distance from center
                    center_x = (points_array[:, 0].min() + points_array[:, 0].max()) / 2
                    center_y = (points_array[:, 1].min() + points_array[:, 1].max()) / 2
                    
                    for j in range(1, len(points_array)):
                        dist = np.sqrt((points_array[j, 0] - center_x)**2 + 
                                     (points_array[j, 1] - center_y)**2)
                        max_dist = np.sqrt((points_array[:, 0].max() - center_x)**2 + 
                                         (points_array[:, 1].max() - center_y)**2)
                        color_val = dist / max_dist if max_dist > 0 else 0
                        color = plt.cm.twilight(color_val)
                        ax.plot(points_array[j-1:j+1, 0], points_array[j-1:j+1, 1],
                               color=color, linewidth=1.5, alpha=0.8)
                
                # Add glow effect to recent segments
                if len(points_array) > 20:
                    for j in range(max(1, len(points_array)-20), len(points_array)):
                        ax.plot(points_array[j-1:j+1, 0], points_array[j-1:j+1, 1],
                               color='cyan', linewidth=4, alpha=0.3)
            
            # Dynamic limits that follow the curve with proper margin
            if len(points) > 10:
                margin = 0.1
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                x_range = max(x_coords) - min(x_coords)
                y_range = max(y_coords) - min(y_coords)
                
                # Keep aspect ratio while showing all content
                if x_range > y_range:
                    y_center = (max(y_coords) + min(y_coords)) / 2
                    ax.set_xlim(min(x_coords) - margin, max(x_coords) + margin)
                    ax.set_ylim(y_center - x_range/2 - margin, y_center + x_range/2 + margin)
                else:
                    x_center = (max(x_coords) + min(x_coords)) / 2
                    ax.set_xlim(x_center - y_range/2 - margin, x_center + y_range/2 + margin)
                    ax.set_ylim(min(y_coords) - margin, max(y_coords) + margin)
            else:
                ax.set_xlim(-0.5, 0.5)
                ax.set_ylim(-0.5, 0.5)
            
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Save to buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', 
                        transparent=True, dpi=150, pad_inches=0)
            buffer.seek(0)
            plt.close()
            
            generation_progress[shape_id] = {
                'iteration': i + 1,
                'max_iterations': max_iterations,
                'image': base64.b64encode(buffer.getvalue()).decode(),
                'complete': i == max_iterations - 1
            }
            
            time.sleep(0.01)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate/<shape>')
def generate(shape):
    shape_id = f"{shape}_{int(time.time() * 1000)}"
    generation_progress[shape_id] = {
        'iteration': 0,
        'max_iterations': 25000,
        'image': None,
        'complete': False
    }
    
    # Start generation in background thread
    if shape == 'triangle':
        thread = Thread(target=generate_sierpinski_triangle_progressive, args=(shape_id,))
    elif shape == 'spiral':
        thread = Thread(target=generate_fibonacci_spiral_progressive, args=(shape_id,))
    elif shape == 'dragon':
        thread = Thread(target=generate_dragon_curve_progressive, args=(shape_id,))
    else:
        return jsonify({'error': 'Invalid shape'}), 400
    
    thread.start()
    
    return jsonify({'shape_id': shape_id})

@app.route('/progress/<shape_id>')
def get_progress(shape_id):
    if shape_id in generation_progress:
        progress = generation_progress[shape_id]
        return jsonify({
            'iteration': progress['iteration'],
            'max_iterations': progress['max_iterations'],
            'percentage': (progress['iteration'] / progress['max_iterations']) * 100,
            'image': f"data:image/png;base64,{progress['image']}" if progress['image'] else None,
            'complete': progress['complete']
        })
    else:
        return jsonify({'error': 'Shape ID not found'}), 404

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    
    app.run(debug=True, port=8000, threaded=True)