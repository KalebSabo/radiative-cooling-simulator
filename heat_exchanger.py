import numpy as np

def calculate_ntu(U, A, C_min):
    """Calculate Number of Transfer Units (NTU)."""
    return U * A / C_min

def calculate_cr(C_min, C_max):
    """Calculate capacity ratio (C_r)."""
    return C_min / C_max

def calculate_effectiveness_counterflow(NTU, C_r):
    """Effectiveness for counterflow heat exchanger."""
    if C_r == 1:
        return NTU / (1 + NTU)
    else:
        exp_term = np.exp(-NTU * (1 - C_r))
        return (1 - exp_term) / (1 - C_r * exp_term)

def calculate_heat_transfer(epsilon, C_min, T_h_in, T_c_in):
    """Actual heat transfer rate (q)."""
    q_max = C_min * (T_h_in - T_c_in)
    return epsilon * q_max

def calculate_outlet_temps(q, C_hot, C_cold, T_h_in, T_c_in):
    """Outlet temperatures."""
    T_h_out = T_h_in - q / C_hot
    T_c_out = T_c_in + q / C_cold
    return T_h_out, T_c_out