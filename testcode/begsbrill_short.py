import math as mt

class ClassB:

    def __init__(self, local_1):
        self.local_1 = local_1
        self.local_2 = None

    @staticmethod
    def _func_x(local_3, local_4, local_5, local_6, local_7, local_8, local_9, local_10):
        local_11 = (1 - local_3) * mt.log(
            max(local_7 * local_3 ** local_8 * local_5 ** local_9 * local_4 ** local_10, 0.000001))
        local_11 = max(local_11, 0)
        local_12 = mt.sin(mt.pi / 100 * local_6)
        local_13 = 1 + local_11 * (local_12 - 0.333 * local_12 ** 3)
        return local_13

    @staticmethod
    def _func_y(local_4, local_3):
        local_14 = 316 * local_3 ** 0.302
        local_15 = 0.0009252 / (local_3 ** 2.4684)
        local_16 = 0.1 / (local_3 ** 1.4516)
        local_17 = 0.5 / (local_3 ** 6.738)
        if (local_3 < 0.4 and local_4 >= local_14) or (local_3 >= 0.4 and local_4 > local_17):
            local_18 = 2
        elif (local_3 < 0.01 and local_4 < local_14) or (local_3 >= 0.01 and local_4 < local_15):
            local_18 = 0
        elif local_3 >= 0.01 and local_16 >= local_4 >= local_15:
            local_18 = 3
        elif (0.4 > local_3 >= 0.01 and local_16 < local_4 <= local_14) or (
                local_3 > 0.4 and local_16 <= local_4 <= local_17):
            local_18 = 1
        else:
            local_18 = 1
        return local_18

    def _func_z(self, local_18, local_3, local_4, local_5, local_6):
        if local_18 in {0, 3}:
            local_19 = 0.98 * local_3 ** 0.4846 / (local_4 ** 0.0868)
            local_19 = min(local_19, 1)
            local_19 = max(local_3, local_19)
            if local_6 >= 0:
                local_7, local_8, local_9, local_10 = 0.011, -3.768, 3.539, -1.614
            else:
                local_7, local_8, local_9, local_10 = 4.70, -0.3692, 0.1244, -0.5056
            local_13 = self._func_x(local_3, local_4, local_5, local_6, local_7, local_8, local_9, local_10)
            local_20 = local_19 * local_13
            local_20 = max(local_20, 0.2 * local_3)
            local_20 = min(local_20, 1)
            local_21 = local_20

        if local_18 in {1, 3}:
            local_19 = 0.845 * local_3 ** 0.5351 / (local_4 ** 0.0173)
            local_19 = min(local_19, 1)
            local_19 = max(local_3, local_19)
            if local_6 >= 0:
                local_7, local_8, local_9, local_10 = 2.96, 0.305, -0.4473, 0.0978
            else:
                local_7, local_8, local_9, local_10 = 4.70, -0.3692, 0.1244, -0.5056
            local_13 = self._func_x(local_3, local_4, local_5, local_6, local_7, local_8, local_9, local_10)
            local_20 = local_19 * local_13
            local_20 = max(local_20, 0.2 * local_3)
            local_20 = min(1, local_20)
            local_22 = local_20

        if local_18 == 3:
            local_15 = 0.0009252 / local_3 ** 2.4684
            local_16 = 0.1 / local_3 ** 1.4516
            local_23 = (local_16 - local_4) / (local_16 - local_15)
            local_20 = local_23 * local_21 + (1 - local_23) * local_22

        if local_18 == 2:
            local_19 = 1.065 * local_3 ** 0.5824 / local_4 ** 0.0609
            local_19 = min(local_19, 1)
            local_19 = max(local_3, local_19)
            local_20 = local_19

        if local_6 >= 0:
            local_20 *= 0.924
            local_20 = max(local_3, local_20)
        else:
            local_20 *= 0.685

        return local_20


    def fun_3(self, local_6, local_28, local_43, local_44, local_45, local_46, **kwargs):
        self.local_47 = local_6
        if local_28 == 0 and local_43 == 0:
            self.local_3 = 0
            self.local_48 = 0
            self.local_49 = 0
            self.local_4 = 1
            self.local_26 = local_44 * self.local_3 + local_45 * (1 - self.local_3)
            self.local_18 = 0
            self.local_4 = 0
            self.local_32 = 0
            self.local_51 = 0
        else:
            self.local_3 = max(local_28 / (local_28 + local_43), 0.000001)
            self.local_48 = local_28 / (3.1415926 * self.local_1**2 / 4)
            self.local_49 = local_43 / (3.1415926 * self.local_1**2 / 4)
            self.local_32 = self.local_48 + self.local_49
            self.local_26 = local_44 * self.local_3 + local_45 * (1 - self.local_3)
            self.local_4 = self.local_32**2 / (9.81 * self.local_1)
            if self.local_26 is None or local_46 is None:
                local_5 = 0
            else:
                local_5 = self.local_48 * (local_44 / (9.81 * local_46)) ** 0.25
            self.local_18 = self._func_y(self.local_4, self.local_3)
            self.local_4 = self._func_z(self.local_18, self.local_3, self.local_4, self.local_26, local_6)
        return self.local_3, self.local_48, self.local_49, self.local_4
