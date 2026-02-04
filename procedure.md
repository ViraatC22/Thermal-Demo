# Detailed Procedure and Data Collection Plan

## Overview
This interactive application demonstrates the First and Second Laws of Thermodynamics using two distinct physical models:
1.  **First Law**: An **Isobaric Expansion** of a gas in a piston cylinder.
2.  **Second Law**: The **Thermal Equilibrium** of two blocks in contact.

## Step-by-Step Instructions

1.  **Launch the Application**:
    *   Open a terminal in the project directory.
    *   Run the command: `streamlit run app.py`.
    *   Open the provided local URL in your web browser.

2.  **Navigation**:
    *   Use the **Sidebar** to review the theoretical concepts and instructions.
    *   Select the desired simulation from the **Tabs** at the top:
        *   `🔥 First Law: Work & Energy`
        *   `🧊 Second Law: Heat & Entropy`

### Experiment A: First Law (Work & Energy)
*   **Goal**: Observe how heat energy ($Q$) is converted into Work ($W$) and Internal Energy ($\Delta U$).
*   **Controls**:
    *   **Gas Amount**: Adjust the number of moles of gas (affects volume).
    *   **Heat Input**: Set the amount of energy (Joules) to inject into the system.
*   **Run**:
    *   Click `🔥 Inject Heat & Run`.
    *   **Observe**:
        *   The **Flame** appears and heats the cylinder.
        *   The **Gas** changes color (Temperature increase).
        *   The **Piston** moves up (Work done via expansion).
        *   **Real-time Metrics** update for $Q$, $W$, and $\Delta U$.

### Experiment B: Second Law (Heat & Entropy)
*   **Goal**: Observe spontaneous heat flow and the increase of total entropy.
*   **Controls**:
    *   **Block Material**: Select a material (Iron, Gold, Wood, etc.) to change thermal conductivity.
    *   **Initial Temperatures**: Set the starting temperatures for the Hot and Cold blocks.
    *   **Mass**: Adjust the mass of the blocks.
*   **Run**:
    *   Click `▶️ Start Simulation`.
    *   **Observe**:
        *   The **Blocks** change color as heat flows.
        *   The **Temperature Graph** shows the values converging to equilibrium.
        *   The **Entropy Graph** (dotted green line) shows the total system entropy increasing.

## First Law of Thermodynamics (Energy Conservation)

### Objective
Verify the First Law equation for an isobaric process: $\Delta U = Q - W$.

### Data Collection
*   **Inputs**:
    *   Heat Added ($Q$)
*   **Outputs**:
    *   **Work Done ($W$)**: Energy used to push the piston ($P\Delta V$).
    *   **Internal Energy Change ($\Delta U$)**: Energy stored in the gas (Temperature rise).

### Verification
*   The app calculates these values independently based on the ideal gas law.
*   Verify that the sum of Work and Internal Energy equals the total Heat input: $Q \approx W + \Delta U$.

## Second Law of Thermodynamics (Entropy Increase)

### Objective
Verify that heat flows spontaneously from Hot to Cold and that this process increases the total disorder (Entropy) of the system.

### Data Collection
*   **Temperatures**: $T_{hot}$ and $T_{cold}$ over time.
*   **Entropy ($S$)**: The cumulative change in system entropy ($\Delta S_{total}$).

### Verification
*   **Equilibrium**: The simulation runs until $T_{hot} \approx T_{cold}$.
*   **Entropy Principle**:
    *   The cold block gains entropy ($\Delta S > 0$).
    *   The hot block loses entropy ($\Delta S < 0$).
    *   **Crucial Check**: The *Total Entropy* must always increase ($\Delta S_{total} > 0$).

## Safety Considerations
*   **Virtual Simulation**: No physical hazards (no real fire or high pressure).
*   **Performance**: The Second Law simulation uses adaptive rendering to ensure smooth performance even for slow-conducting materials like Wood.
