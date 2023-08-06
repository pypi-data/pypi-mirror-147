import numpy as np

def normal_incidence(z_i, z_t):

    R = (z_t - z_i) / (z_t + z_i)

    T = 1 + R

    return R, T

def transmitted_angle(c_i, c_t, theta_i):

    theta_t = np.arcsin(c_t /c_i * np.sin(theta_i))

    return theta_t

def critical_angle(c_i, c_t):

    theta_c = np.arcsin(c_i / c_t)

    return theta_c

def intromission_angle(z_i, z_t, c_i, c_t):

    numerator = (z_t/z_i)**2 - 1
    denominator = (z_t/z_i)**2 - (c_t*c_i)**2

    if numerator / denominator >= 0 and np.sqrt(numerator / denominator) <= 1:
        theta_intro = np.arcsin(np.sqrt( numerator / denominator))
    else:
        theta_intro = float("NaN")

    return theta_intro

def oblique_incidence(z_i, z_t, c_i, c_t, theta_i):

    if c_i < c_t:

        theta_c = critical_angle(c_i,c_t)

        if theta_i > theta_c:
            R = 1
            T = 1 + R

            return R, T

    theta_t = transmitted_angle(c_i, c_t, theta_i)

    R = (z_t/np.cos(theta_t) - z_i/np.cos(theta_i)) / (z_t/np.cos(theta_t) + z_i/np.cos(theta_i))

    T = 1 + R
    
    return R, T