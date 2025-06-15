from math import pi


def fun1(mass_flow, inlet_diameter, density_in, density_out, exit_diameter=None):
    """
    Calculates the kinetic energy change term for compressible flow between two pipe sections.

    This function computes the difference in kinetic energy per unit volume between an inlet and exit pipe,
    accounting for variable density (compressible flow) and optional diameter changes.

    Parameters:
    mass_flow (float): Mass flow rate through pipe [kg/s]
    inlet_diameter (float): Inner diameter of inlet pipe section [m]
    density_in (float): Fluid density at inlet conditions [kg/m³]
    density_out (float): Fluid density at exit conditions [kg/m³]
    exit_diameter (float, optional): Inner diameter of exit pipe section [m]. 
                                     Defaults to inlet_diameter if not provided.

    Returns:
    float: Kinetic energy change term [Pa] representing:
           0.5 * average_density * (velocity_in² - velocity_exit²)
    """
    # If exit diameter not provided, set equal to inlet diameter (constant cross-section)
    if exit_diameter is None:
        exit_diameter = inlet_diameter
    
    # Calculate pipe cross-sectional areas [m²]
    inlet_area = 0.25 * pi * inlet_diameter**2
    exit_area = 0.25 * pi * exit_diameter**2
    
    # Compute mean fluid densities at inlet and exit
    # This uses the simplified assumption that density averages linearly
    average_density = 0.5 * (density_in + density_out)
    
    # Calculate flow velocities using mass flow rate and continuity [m/s]
    velocity_inlet = mass_flow / (density_in * inlet_area)
    velocity_exit = mass_flow / (density_out * exit_area)
    
    # Compute kinetic energy change per unit volume (pressure equivalent) [Pa]
    return 0.5 * average_density * (velocity_inlet**2 - velocity_exit**2)
