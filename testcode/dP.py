from math import cos, exp, isinf, log, log10, pi, radians, sin, sqrt, tan
from fluids.constants import g as const1, inch as const2


def fun1(local1, local2, local3, local4, local5=None):
    if local5 is None:
        local5 = local2
    local6 = 0.25 * pi * local5 * local5
    local7 = 0.25 * pi * local2 * local2

    local8 = local1 / local4
    local9 = local8 / local6

    local10 = local1 / local3
    local11 = local10 / local7

    local12 = 0.5 * (local3 + local4)

    return 0.5 * local12 * (local11 * local11 - local9 * local9)
