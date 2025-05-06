import math as math


class HydraulicSystem:

    def __init__(self, pipe_diameter):
        self.pipe_diameter = pipe_diameter
        self.adjusted_parameter = None

    @staticmethod
    def _calculate_correction_factor(liquid_holdup, froude_squared, property_term, inclination_angle, coeff_a, exp_b,
                                     exp_c, exp_d):
        log_argument = max(coeff_a * liquid_holdup ** exp_b * property_term ** exp_c * froude_squared ** exp_d, 1e-6)
        logarithmic_term = (1 - liquid_holdup) * math.log(log_argument)
        non_negative_term = max(logarithmic_term, 0)
        angle_ratio = math.sin(math.pi / 100 * inclination_angle)
        correction_factor = 1 + non_negative_term * (angle_ratio - 0.333 * angle_ratio ** 3)
        return correction_factor

    @staticmethod
    def _determine_flow_regime(froude_squared, liquid_holdup):
        bubble_threshold = 316 * liquid_holdup ** 0.302
        transition_low = 0.0009252 / liquid_holdup ** 2.4684
        transition_high = 0.1 / liquid_holdup ** 1.4516
        annular_threshold = 0.5 / liquid_holdup ** 6.738

        if (liquid_holdup < 0.4 and froude_squared >= bubble_threshold) or (
                liquid_holdup >= 0.4 and froude_squared > annular_threshold):
            regime = 2
        elif (liquid_holdup < 0.01 and froude_squared < bubble_threshold) or (
                liquid_holdup >= 0.01 and froude_squared < transition_low):
            regime = 0
        elif liquid_holdup >= 0.01 and transition_high >= froude_squared >= transition_low:
            regime = 3
        elif (0.4 > liquid_holdup >= 0.01 and transition_high < froude_squared <= bubble_threshold) or (
                liquid_holdup > 0.4 and transition_high <= froude_squared <= annular_threshold):
            regime = 1
        else:
            regime = 1
        return regime

    def _calculate_flow_component(self, regime, liquid_holdup, froude_squared, property_term, inclination_angle):
        if regime in {0, 3}:
            base_value = 0.98 * liquid_holdup ** 0.4846 / froude_squared ** 0.0868
            constrained_value = min(max(base_value, liquid_holdup), 1)

            if inclination_angle >= 0:
                a, b, c, d = 0.011, -3.768, 3.539, -1.614
            else:
                a, b, c, d = 4.70, -0.3692, 0.1244, -0.5056

            correction = self._calculate_correction_factor(liquid_holdup, froude_squared, property_term,
                                                           inclination_angle, a, b, c, d)
            adjusted_value = constrained_value * correction
            adjusted_value = max(min(adjusted_value, 1), 0.2 * liquid_holdup)
            stratified_value = adjusted_value

        if regime in {1, 3}:
            base_value = 0.845 * liquid_holdup ** 0.5351 / froude_squared ** 0.0173
            constrained_value = min(max(base_value, liquid_holdup), 1)

            if inclination_angle >= 0:
                a, b, c, d = 2.96, 0.305, -0.4473, 0.0978
            else:
                a, b, c, d = 4.70, -0.3692, 0.1244, -0.5056

            correction = self._calculate_correction_factor(liquid_holdup, froude_squared, property_term,
                                                           inclination_angle, a, b, c, d)
            adjusted_value = constrained_value * correction
            adjusted_value = max(min(adjusted_value, 1), 0.2 * liquid_holdup)
            slug_value = adjusted_value

        if regime == 3:
            transition_low = 0.0009252 / liquid_holdup ** 2.4684
            transition_high = 0.1 / liquid_holdup ** 1.4516
            blend_factor = (transition_high - froude_squared) / (transition_high - transition_low)
            adjusted_value = blend_factor * stratified_value + (1 - blend_factor) * slug_value

        if regime == 2:
            base_value = 1.065 * liquid_holdup ** 0.5824 / froude_squared ** 0.0609
            adjusted_value = min(max(base_value, liquid_holdup), 1)

        if inclination_angle >= 0:
            adjusted_value *= 0.924
            adjusted_value = max(liquid_holdup, adjusted_value)
        else:
            adjusted_value *= 0.685

        return adjusted_value

    def update_flow_parameters(self, inclination_angle, liquid_rate, gas_rate, liquid_density, gas_density, gravity, **kwargs):
        self.inclination = inclination_angle
        if liquid_rate == 0 and gas_rate == 0:
            self.liquid_holdup = 0
            self.liquid_velocity = 0
            self.gas_velocity = 0
            self.froude_squared = 1
            self.density = liquid_density * self.liquid_holdup + gas_density * (1 - self.liquid_holdup)
            self.flow_regime = 0
            self.froude_squared = 0
            self.flow_velocity = 0
            self.momentum_transfer = 0
        else:
            self.liquid_holdup = max(liquid_rate / (liquid_rate + gas_rate), 1e-6)
            self.liquid_velocity = liquid_rate / (math.pi * self.pipe_diameter**2 / 4)
            self.gas_velocity = gas_rate / (math.pi * self.pipe_diameter**2 / 4)
            self.flow_velocity = self.liquid_velocity + self.gas_velocity
            self.density = liquid_density * self.liquid_holdup + gas_density * (1 - self.liquid_holdup)
            self.froude_squared = self.flow_velocity**2 / (gravity * self.pipe_diameter)
            property_term = self.liquid_velocity * (liquid_density / (gravity * kwargs.get('viscosity', 1e-6)))**0.25 if None not in [self.density, kwargs.get('viscosity')] else 0
            self.flow_regime = self._determine_flow_regime(self.froude_squared, self.liquid_holdup)
            self.froude_squared = self._calculate_flow_component(self.flow_regime, self.liquid_holdup, self.froude_squared, self.density, inclination_angle)
        return self.liquid_holdup, self.liquid_velocity, self.gas_velocity, self.froude_squared