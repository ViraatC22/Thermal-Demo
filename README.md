# Thermal Demo App

A professional, interactive educational tool for demonstrating the First and Second Laws of Thermodynamics. Built with Python and Streamlit.

## Features

### 🔥 First Law: Work & Energy
*   **Interactive Simulation**: Visualize an isobaric expansion of a gas in a piston cylinder.
*   **Real-time Physics**: Watch as Heat ($Q$) is converted into Work ($W$) and Internal Energy ($\Delta U$).
*   **Vector Graphics**: High-quality, scalable visualizations using Matplotlib patches.
*   **Dynamic Metrics**: See the values update in real-time as the simulation runs.

### 🧊 Second Law: Heat & Entropy
*   **Thermal Equilibrium**: Simulate two blocks of different materials coming into contact.
*   **Material Selection**: Choose from Iron, Aluminum, Copper, Gold, or Wood to see how thermal conductivity ($k$) affects heat flow.
*   **Entropy Visualization**: Track the total entropy of the system and verify it always increases ($\Delta S_{total} > 0$).
*   **Adaptive Rendering**: Optimized simulation loop ensures smooth performance even for slow processes.

## Getting Started

### Prerequisites
*   Python 3.8 or higher

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/ViraatC22/Thermal-Demo.git
    cd Thermal-Demo
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open automatically in your default web browser.

## Documentation

*   [Procedure](procedure.md): Step-by-step instructions for running the experiments.
*   [Explanation](explanation.md): Detailed theoretical background and mathematical models.
*   [Materials](materials.md): List of software tools and libraries used.

## Technologies Used
*   **Streamlit**: Web interface and interactivity.
*   **Matplotlib**: Custom vector graphics for physical models.
*   **Plotly**: Interactive real-time charting.
*   **NumPy & Pandas**: Numerical calculations and data management.

## License
This project is open source and available for educational use.
