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

def generate_logarithmic_spiral_progressive(shape_id, max_iterations=25000):
    """Generate a beautiful Logarithmic Spiral in polar coordinates"""
    points = []
    
    # Parameters for logarithmic spiral
    a = 0.1  # Initial radius
    b = 0.2  # Growth rate
    
    for i in range(max_iterations):
        # Angle grows linearly
        theta = i * 0.05
        
        # Logarithmic spiral: r = a * e^(b * theta)
        r = a * np.exp(b * theta)
        
        # Convert to Cartesian
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        points.append([x, y, theta, r])
        
        # Update visualization
        if i % 200 == 0 or i == max_iterations - 1:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none', subplot_kw=dict(projection='polar'))
            ax.set_facecolor('none')
            
            if len(points) > 1:
                points_array = np.array(points[:i+1])
                thetas = points_array[:, 2]
                rs = points_array[:, 3]
                
                # Create gradient effect
                segments = len(points_array) - 1
                for j in range(segments):
                    color = plt.cm.twilight(j / segments)
                    ax.plot(thetas[j:j+2], rs[j:j+2], color=color, linewidth=2, alpha=0.8)
                
                # Add glow effect for recent points
                if len(points_array) > 50:
                    ax.plot(thetas[-50:], rs[-50:], color='cyan', linewidth=4, alpha=0.3)
            
            # Polar grid styling
            ax.grid(True, alpha=0.3)
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            
            # Dynamic radius limit
            if len(points) > 0:
                max_r = max([p[3] for p in points]) * 1.1
                ax.set_ylim(0, max_r)
            
            # Remove radius labels for cleaner look
            ax.set_yticklabels([])
            
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

def generate_archimedean_spiral_progressive(shape_id, max_iterations=25000):
    """Generate an Archimedean Spiral with evenly spaced arms"""
    points = []
    
    # Parameter for Archimedean spiral
    a = 0.5  # Controls spacing between arms
    
    for i in range(max_iterations):
        # Angle grows to create multiple rotations
        theta = i * 0.02
        
        # Archimedean spiral: r = a * theta
        r = a * theta
        
        # Store polar and Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        points.append([x, y, theta, r])
        
        # Update visualization
        if i % 200 == 0 or i == max_iterations - 1:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none', subplot_kw=dict(projection='polar'))
            ax.set_facecolor('none')
            
            if len(points) > 1:
                points_array = np.array(points[:i+1])
                thetas = points_array[:, 2]
                rs = points_array[:, 3]
                
                # Create rainbow gradient
                segments = len(points_array) - 1
                for j in range(segments):
                    color = plt.cm.rainbow(j / segments)
                    ax.plot(thetas[j:j+2], rs[j:j+2], color=color, linewidth=2, alpha=0.8)
                
                # Add sparkle effect
                if len(points_array) > 100:
                    # Add dots at regular intervals for sparkle
                    sparkle_indices = range(0, len(points_array), 50)
                    ax.scatter(thetas[sparkle_indices], rs[sparkle_indices], 
                             color='white', s=20, alpha=0.8, zorder=10)
            
            # Polar grid styling
            ax.grid(True, alpha=0.3)
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            
            # Dynamic radius limit
            if len(points) > 0:
                max_r = max([p[3] for p in points]) * 1.1
                ax.set_ylim(0, max_r)
            
            ax.set_yticklabels([])
            
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

def generate_rose_curve_progressive(shape_id, max_iterations=25000):
    """Generate beautiful Rose Curves (rhodonea curves)"""
    points = []
    
    # Parameters for rose curve
    # Using k = 5/3 for a beautiful 5-petaled rose
    n = 5  # numerator
    d = 3  # denominator
    k = n / d
    a = 5  # amplitude
    
    for i in range(max_iterations):
        # Map iterations to full pattern (need 2π*d for complete pattern when k is rational)
        theta = (i / max_iterations) * 2 * np.pi * d
        
        # Rose curve: r = a * cos(k * theta)
        r = a * np.cos(k * theta)
        
        # Store both positive and reflected points for full pattern
        points.append([theta, abs(r)])
        
        # Update visualization
        if i % 200 == 0 or i == max_iterations - 1:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none', subplot_kw=dict(projection='polar'))
            ax.set_facecolor('none')
            
            if len(points) > 1:
                points_array = np.array(points[:i+1])
                thetas = points_array[:, 0]
                rs = points_array[:, 1]
                
                # Create petal gradient effect
                segments = len(points_array) - 1
                for j in range(segments):
                    # Color based on radius for petal effect
                    color_val = rs[j] / a
                    color = plt.cm.RdPu(color_val)
                    ax.plot(thetas[j:j+2], rs[j:j+2], color=color, linewidth=3, alpha=0.9)
                
                # Add symmetric reflection for complete rose
                ax.plot(thetas, rs, color='none')  # Invisible line for proper scaling
                
                # Draw the negative part too
                for j in range(segments):
                    r_neg = a * np.cos(k * thetas[j])
                    if r_neg < 0:
                        color_val = abs(r_neg) / a
                        color = plt.cm.RdPu(color_val)
                        ax.plot([thetas[j], thetas[j]], [0, abs(r_neg)], 
                               color=color, linewidth=3, alpha=0.9)
                
                # Add center glow
                ax.scatter([0], [0], color='pink', s=100, alpha=0.5, zorder=10)
            
            # Polar grid styling
            ax.grid(True, alpha=0.2, linestyle='--')
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            
            # Fixed radius for rose curves
            ax.set_ylim(0, a * 1.2)
            ax.set_yticklabels([])
            
            # Add title showing the rose type
            if i == max_iterations - 1:
                ax.text(0, a * 1.15, f'{n}-petaled rose', ha='center', 
                       transform=ax.transData, fontsize=12, alpha=0.7)
            
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
    elif shape == 'logarithmic':
        thread = Thread(target=generate_logarithmic_spiral_progressive, args=(shape_id,))
    elif shape == 'rose':
        thread = Thread(target=generate_rose_curve_progressive, args=(shape_id,))
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