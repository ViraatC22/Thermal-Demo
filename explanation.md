# Demonstration Explanation

## Theoretical Basis

This application models two fundamental thermodynamic scenarios to interactively demonstrate the First and Second Laws.

### 1. The First Law of Thermodynamics (Work & Energy)
**Principle**: Energy is conserved. It can change forms (e.g., from Heat to Work) but cannot be created or destroyed.

**Scenario**: An **Isobaric Expansion** (Constant Pressure).
We heat a gas inside a cylinder with a movable piston. The added heat ($Q$) does two things:
1.  **Increases Internal Energy ($\Delta U$)**: The gas gets hotter.
2.  **Performs Work ($W$)**: The gas expands and pushes the piston up against atmospheric pressure.

**Mathematical Model**:
The First Law states:
$$\Delta U = Q - W$$

Where:
*   **$Q$ (Heat Input)**: Energy added by the flame.
*   **$W$ (Work Done)**: Energy expended to move the piston.
    $$W = P \cdot \Delta V = nR\Delta T$$
*   **$\Delta U$ (Internal Energy)**: Energy stored in the gas molecules.
    $$\Delta U = nC_v\Delta T$$

In the simulation, as you add Heat ($Q$), you will see the **Temperature** rise (increasing $\Delta U$) and the **Piston** rise (doing Work $W$).

### 2. The Second Law of Thermodynamics (Heat & Entropy)
**Principle**: Heat spontaneously flows from Hot to Cold, never the reverse. This process increases the total Entropy (disorder) of the universe.

**Scenario**: Two blocks of different materials and temperatures are placed in thermal contact.

**Mathematical Model**:
1.  **Heat Transfer**:
    The rate of heat flow is proportional to the temperature difference and the material's conductivity ($k$):
    $$\frac{dQ}{dt} \approx k \cdot (T_{hot} - T_{cold})$$
    
    *   **High Conductivity (e.g., Gold)**: Heat flows fast, equilibrium is reached quickly.
    *   **Low Conductivity (e.g., Wood)**: Heat flows slowly.

2.  **Entropy Change ($\Delta S$)**:
    Entropy measures the dispersal of energy.
    $$dS = \frac{dQ}{T}$$
    
    *   **Cold Block**: Gains heat ($+dQ$) at a low temp ($T_c$). This causes a **large increase** in entropy ($+dQ/T_c$).
    *   **Hot Block**: Loses heat ($-dQ$) at a high temp ($T_h$). This causes a **smaller decrease** in entropy ($-dQ/T_h$).
    
    **Net Result**: Since $T_c < T_h$, the gain is larger than the loss, so **Total Entropy always increases** ($\Delta S_{total} > 0$).

## Data Analysis & Verification

### Verification of Laws
*   **First Law**: The simulation calculates $W$ and $\Delta U$ independently. You can verify that their sum equals the Heat Input ($Q$).
*   **Second Law**: The simulation runs iteratively until thermal equilibrium is reached ($T_{hot} \approx T_{cold}$). The "Entropy" graph will always show a positive upward trend, confirming the Second Law.

### Assumptions
*   **Ideal Gas**: The First Law simulation assumes the gas behaves ideally ($PV=nRT$).
*   **Adiabatic System**: We assume no heat is lost to the outside environment during the experiment.
*   **Constant Pressure**: The piston moves freely, keeping pressure constant at 1 atm.
