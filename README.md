# Fun with Math 🎯

An interactive mathematical visualization tool that brings the beauty of fractals and mathematical curves to life through progressive animations.

**Created by Prof. Shahab Anbarjafari**  
© 2025 3S Holding OÜ

## 🌟 Overview

Fun with Math is an educational web application designed to demonstrate the mesmerizing beauty hidden within mathematical algorithms. Through real-time generation of fractals and curves, users can witness how simple mathematical rules create infinite complexity and natural patterns.

The application features four stunning mathematical visualizations:
- **Sierpinski Triangle**: Chaos game algorithm creating order from randomness
- **Logarithmic Spiral**: Nature's favorite growth pattern
- **Rose Curve**: Polar mathematics creating floral beauty
- **Dragon Curve**: L-system fractals with perfect tessellation

## 🎨 Design Philosophy

Following Steve Jobs' design principles, this application emphasizes:
- **Simplicity**: Clean, uncluttered interface focusing on the mathematical beauty
- **Elegance**: Smooth animations and thoughtful transitions
- **Intuitive Interaction**: Select → Generate → Explore
- **Educational Value**: Real-time visualization of mathematical concepts

## 🚀 Features

### Progressive Generation
- Watch fractals build point-by-point up to 25,000 iterations
- Real-time progress tracking with elegant progress bar
- Dynamic visualization updates every 50-200 iterations

### Mathematical Visualizations

#### 1. Sierpinski Triangle
- Implementation: Chaos game algorithm
- Color-coded by vertex selection (plasma colormap)
- Demonstrates how randomness creates deterministic patterns

#### 2. Logarithmic Spiral
- Formula: r = ae^(bθ)
- Displayed in polar coordinates
- Twilight gradient coloring with cyan glow effects
- Found in nautilus shells, galaxies, and hurricanes

#### 3. Rose Curve
- Formula: r = a·cos(kθ) where k = 5/3
- Creates 5-petaled flower patterns
- Pink gradient (RdPu colormap) with petal-based coloring
- Demonstrates trigonometric beauty

#### 4. Dragon Curve
- L-system implementation with pre-generated sequences
- Never self-intersecting path
- Dynamic coloring: construction order (early) → distance-based (later)
- Tessellates perfectly to fill the plane

### Technical Features
- **Flask** backend with threaded generation
- **Matplotlib** with Agg backend for server-side rendering
- **Base64** image encoding for seamless updates
- **Responsive design** with mobile support
- **Real-time progress polling** (100ms intervals)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fun-with-math.git
cd fun-with-math
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv myenv

# On macOS/Linux:
source myenv/bin/activate

# On Windows:
myenv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install flask numpy matplotlib
```

4. **Create required directories**
```bash
mkdir -p templates static/img
```

5. **Set up the files**
- Save `app.py` in the root directory
- Save `index.html` in `templates/index.html`
- Add your logo as `static/img/logo.png`

## 🚦 Running the Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Open your browser**
Navigate to `http://localhost:8000`

3. **Enjoy the mathematical journey!**

## 📁 Project Structure

```
fun-with-math/
├── app.py                  # Flask backend with fractal generators
├── templates/
│   └── index.html         # Frontend with animations
├── static/
│   └── img/
│       └── logo.png       # 3S Holding logo
├── README.md              # This file
└── requirements.txt       # Python dependencies (optional)
```

## 🔧 Configuration

### Port Configuration
Default port is 8000. To change:
```python
app.run(debug=True, port=YOUR_PORT, threaded=True)
```

### Iteration Count
Default is 25,000 iterations. Modify in generator functions:
```python
def generate_*_progressive(shape_id, max_iterations=25000):
```

### Update Frequency
Visualization updates are controlled by:
```python
if i % 200 == 0 or i == max_iterations - 1:  # Update every 200 iterations
```

### Color Schemes
- Sierpinski Triangle: `plt.cm.plasma`
- Logarithmic Spiral: `plt.cm.twilight`
- Rose Curve: `plt.cm.RdPu`
- Dragon Curve: `plt.cm.cool` / `plt.cm.twilight`

## 🎯 Mathematical Details

### Sierpinski Triangle
Uses the chaos game algorithm:
1. Start at a random point
2. Choose a random vertex
3. Move halfway toward that vertex
4. Repeat 25,000 times

### Logarithmic Spiral
Polar equation: r = 0.1 * e^(0.2θ)
- Maintains shape at all scales
- Growth rate controlled by parameter b

### Rose Curve
Polar equation: r = 5 * cos(5θ/3)
- Creates 5 petals (n=5, d=3)
- Complete pattern requires 2πd radians

### Dragon Curve
L-system rules:
- Axiom: FX
- X → X+YF+
- Y → -FX-Y
- F = forward, +/- = turn right/left 90°

## 🐛 Troubleshooting

### macOS Threading Error
If you encounter `NSInternalInconsistencyException`:
- The fix is already implemented using `matplotlib.use('Agg')`
- Ensures non-interactive backend for thread safety

### Template Not Found
Ensure `index.html` is in the `templates/` directory, not root

### Slow Generation
- Reduce update frequency in visualization loops
- Consider reducing max_iterations
- Ensure matplotlib backend is set to 'Agg'

## 🔄 Future Enhancements

Potential additions for version 2.0:
- Additional fractals (Julia sets, Mandelbrot)
- User-adjustable parameters
- Export functionality for generated images
- 3D fractal visualizations
- Interactive parameter sliders
- Multiple color scheme options

## 📚 Educational Use

This tool is perfect for:
- Mathematics courses (fractals, chaos theory)
- Computer science (algorithms, recursion)
- Art and design (mathematical beauty)
- STEM outreach programs

## 🙏 Acknowledgments

- Inspired by the intersection of mathematics and art
- Built with Flask and Matplotlib
- Design philosophy influenced by Apple's human interface guidelines

## 📄 License

© 2025 3S Holding OÜ. All rights reserved.

For academic use, please cite:
```
Anbarjafari, S. (2025). Fun with Math: Interactive Mathematical Visualizations. 
3S Holding OÜ. https://github.com/yourusername/fun-with-math
```

## 📧 Contact

**Prof. Shahab Anbarjafari**  
3S Holding OÜ  
Tallinn, Estonia

---

*"Mathematics is the language with which God has written the universe."* - Galileo Galilei

Experience the beauty of mathematics at your fingertips with Fun with Math!