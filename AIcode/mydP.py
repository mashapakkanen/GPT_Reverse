from math import pi

def fun1(mass_flow, exit_diameter, inlet_density, outlet_density, inlet_diameter=None):
    """
    Compute the kinetic energy change per unit volume of a flowing fluid between two sections.

    This function calculates the change in kinetic energy per unit volume by comparing fluid flow 
    parameters between an inlet section and an outlet section. The kinetic energy difference is 
    based on velocities derived from mass flow rate, cross-sectional areas, and fluid densities.

    Parameters:
    mass_flow (float): Mass flow rate of the fluid [kg/s]
    exit_diameter (float): Diameter of the outlet pipe [m]
    inlet_density (float): Fluid density at the inlet section [kg/m³]
    outlet_density (float): Fluid density at the outlet section [kg/m³]
    inlet_diameter (float, optional): Diameter of the inlet pipe [m]. 
        If not provided, defaults to exit_diameter.

    Returns:
    float: Change in kinetic energy per unit volume [J/m³]
    """
    # Use exit_diameter if inlet_diameter is not provided
    if inlet_diameter is None:
        inlet_diameter = exit_diameter

    # Calculate cross-sectional area at inlet and outlet
    inlet_area = 0.25 * pi * inlet_diameter**2
    outlet_area = 0.25 * pi * exit_diameter**2

    # Calculate velocities at inlet and outlet using mass flow rate and densities
    # velocity = mass_flow / (density * area)
    inlet_velocity = mass_flow / (outlet_density * inlet_area)
    outlet_velocity = mass_flow / (inlet_density * outlet_area)

    # Calculate average density between inlet and outlet
    average_density = 0.5 * (inlet_density + outlet_density)

    # Compute kinetic energy change per unit volume:
    # ΔKE = (1/2) * average_density * (outlet_velocity² - inlet_velocity²)
    return 0.5 * average_density * (outlet_velocity**2 - inlet_velocity**2)
