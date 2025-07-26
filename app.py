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
    
    # Generate points progressively
    for i in range(max_iterations):
        vertex = vertices[np.random.randint(0, 3)]
        current = (current + vertex) / 2
        points.append(current.copy())
        
        # Update every 100 points
        if i % 100 == 0 or i == max_iterations - 1:
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none')
            ax.set_facecolor('none')
            
            # Plot points
            if points:
                points_array = np.array(points)
                ax.scatter(points_array[:, 0], points_array[:, 1], 
                          s=0.5, c='black', alpha=0.8)
            
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

def generate_sierpinski_square_progressive(shape_id, max_iterations=25000):
    """Generate a mesmerizing square fractal using IFS"""
    points = []
    
    # IFS transformations for a beautiful square fractal
    # Each transformation: (scale_x, scale_y, translate_x, translate_y, rotation)
    transforms = [
        (0.5, 0.5, 0, 0, 0),           # Bottom left
        (0.5, 0.5, 0.5, 0, 0),         # Bottom right
        (0.5, 0.5, 0, 0.5, 0),         # Top left
        (0.5, 0.5, 0.5, 0.5, 0),       # Top right
        (0.3, 0.3, 0.35, 0.35, 45),    # Center rotated
    ]
    
    # Start with random point
    x, y = 0.5, 0.5
    colors = []
    
    for i in range(max_iterations):
        # Choose random transformation
        t_idx = np.random.choice(len(transforms), p=[0.22, 0.22, 0.22, 0.22, 0.12])
        t = transforms[t_idx]
        
        # Apply rotation if present
        if t[4] != 0:
            angle = np.radians(t[4])
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            x_rot = x * cos_a - y * sin_a
            y_rot = x * sin_a + y * cos_a
            x, y = x_rot, y_rot
        
        # Apply scaling and translation
        x = x * t[0] + t[2]
        y = y * t[1] + t[3]
        
        points.append([x, y])
        colors.append(t_idx)
        
        # Update visualization
        if i % 200 == 0 or i == max_iterations - 1:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none')
            ax.set_facecolor('none')
            
            if points:
                points_array = np.array(points)
                colors_array = np.array(colors)
                
                # Create color map
                cmap = plt.cm.viridis
                scatter = ax.scatter(points_array[:, 0], points_array[:, 1], 
                                   c=colors_array, cmap=cmap, s=0.5, alpha=0.7)
            
            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, 1.1)
            ax.axis('off')
            
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

def generate_sierpinski_circle_progressive(shape_id, max_iterations=25000):
    """Generate a stunning circular fractal using strange attractors"""
    points = []
    
    # Parameters for a circular strange attractor
    a, b, c, d = 2.0, -2.0, -1.2, 2.0
    x, y = 0.1, 0.1
    
    # Color based on angle for rainbow effect
    colors = []
    
    for i in range(max_iterations):
        # De Jong attractor equations modified for circular motion
        x_new = np.sin(a * y) - np.cos(b * x)
        y_new = np.sin(c * x) - np.cos(d * y)
        
        # Add spiral motion
        r = np.sqrt(x_new**2 + y_new**2)
        theta = np.arctan2(y_new, x_new) + i * 0.001
        
        # Normalize and add some variation
        x = x_new * 0.3 + 0.1 * np.cos(theta)
        y = y_new * 0.3 + 0.1 * np.sin(theta)
        
        points.append([x, y])
        
        # Color based on iteration for gradient effect
        colors.append(i)
        
        # Update visualization
        if i % 200 == 0 or i == max_iterations - 1:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='none')
            ax.set_facecolor('none')
            
            if points:
                points_array = np.array(points)
                colors_array = np.array(colors)
                
                # Create beautiful color gradient
                cmap = plt.cm.twilight
                scatter = ax.scatter(points_array[:, 0], points_array[:, 1], 
                                   c=colors_array, cmap=cmap, s=0.3, alpha=0.6)
            
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.set_aspect('equal')
            ax.axis('off')
            
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
    elif shape == 'square':
        thread = Thread(target=generate_sierpinski_square_progressive, args=(shape_id,))
    elif shape == 'circle':
        thread = Thread(target=generate_sierpinski_circle_progressive, args=(shape_id,))
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