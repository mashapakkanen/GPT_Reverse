from math import pi


def fun1(mass_flow_rate, diameter1, density1, density2, diameter2=None):
    """
    Calculate the dynamic pressure difference between two pipe sections.

    The function computes the difference in dynamic pressure between two sections of a pipe
    with different diameters and fluid densities, based on the mass flow rate. The dynamic
    pressure difference is calculated using the average density and the velocities in the
    two sections.

    Parameters:
    mass_flow_rate (float): The mass flow rate of the fluid (kg/s).
    diameter1 (float): Diameter of the first pipe section (m).
    density1 (float): Density of the fluid in the first pipe section (kg/m³).
    density2 (float): Density of the fluid in the second pipe section (kg/m³).
    diameter2 (float, optional): Diameter of the second pipe section. Defaults to diameter1.

    Returns:
    float: The dynamic pressure difference between the two sections (Pa).
    """
    # Use diameter1 for diameter2 if not provided
    if diameter2 is None:
        diameter2 = diameter1

    # Calculate cross-sectional areas of the pipe sections
    area_section2 = 0.25 * pi * diameter2 ** 2  # Area of second section (m²)
    area_section1 = 0.25 * pi * diameter1 ** 2  # Area of first section (m²)

    # Compute volume flow rates for each section
    volume_flow_section2 = mass_flow_rate / density2  # Q = m_dot / rho (m³/s)
    volume_flow_section1 = mass_flow_rate / density1  # Q = m_dot / rho (m³/s)

    # Calculate velocities in each section (velocity = Q / A)
    velocity_section2 = volume_flow_section2 / area_section2  # v2 (m/s)
    velocity_section1 = volume_flow_section1 / area_section1  # v1 (m/s)

    # Compute average density between the two sections
    average_density = 0.5 * (density1 + density2)  # Average rho (kg/m³)

    # Calculate dynamic pressure difference using average density and velocity difference
    dynamic_pressure_diff = 0.5 * average_density * (velocity_section1 ** 2 - velocity_section2 ** 2)  # ΔP (Pa)

    return dynamic_pressure_diff
