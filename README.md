# Thermal Demo App

A professional, interactive educational tool for demonstrating the First and Second Laws of Thermodynamics. Built with Python and Streamlit.

## Status

The local application and its thermodynamic calculation tests pass. The primary
remaining operational limitation is that this simulation uses idealized,
display-oriented coefficients rather than laboratory-calibrated measurements.

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
*   Git

Using a virtual environment is strongly recommended.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/ViraatC22/Thermal-Demo.git
    cd Thermal-Demo
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

### Running the App

Run the Streamlit application:
```bash
python3 -m streamlit run app.py
```

The application will open automatically in your default web browser.

## Verification

Run the calculation regression suite:

```bash
python3 -m unittest discover -s tests -v
```

For a startup smoke test, run the app and confirm the browser loads both
simulation tabs without an exception:

```bash
python3 -m streamlit run app.py
```

## Architecture

*   `app.py`: Streamlit controls, animation, charts, and experiment history.
*   `thermodynamics.py`: Pure, testable heat-transfer calculations and material
    properties.
*   `tests/`: Standard-library regression tests for equilibrium stability,
    energy conservation, entropy, and input validation.
*   `procedure.md`, `explanation.md`, and `materials.md`: Classroom instructions
    and model background.

The heat-transfer step caps explicit integration before the blocks can cross
equilibrium. Entropy is calculated from the finite temperature changes rather
than from a first-order approximation.

## Documentation

*   [Procedure](procedure.md): Step-by-step instructions for running the experiments.
*   [Explanation](explanation.md): Detailed theoretical background and mathematical models.
*   [Materials](materials.md): List of software tools and libraries used.
*   [Project audit](docs/PROJECT_AUDIT.md): Recovery findings and completion definition.
*   [Completion plan](docs/COMPLETION_PLAN.md): Verified work and remaining tasks.
*   [Final status](docs/FINAL_STATUS.md): Verification results and handoff state.

## Technologies Used
*   **Streamlit**: Web interface and interactivity.
*   **Matplotlib**: Custom vector graphics for physical models.
*   **Plotly**: Interactive real-time charting.
*   **NumPy & Pandas**: Numerical calculations and data management.

## Known Limitations

*   Material conductivity values and simulation time multipliers are chosen for
    an understandable classroom animation; they are not a calibrated prediction
    of real elapsed time.
*   Experiment history is held in the current Streamlit session and is not
    persisted after the session ends.
*   Browser interaction has a documented manual smoke test; the pure calculation
    layer carries the automated regression coverage.

## Security and Privacy

The app does not require credentials, accept file uploads, or send experiment
data to an external service. All calculations and session history remain local
to the running Streamlit process.

## Repository

GitHub: `https://github.com/ViraatC22/Thermal-Demo`

## License
This project is open source and available for educational use.
