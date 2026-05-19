import numpy as np
import pandas as pd


def _interp(points, x_values):
    points = np.asarray(points, dtype=float)
    return np.interp(x_values, points[:, 0], points[:, 1])


def figure2_curves():
    users = np.arange(0, 401, 5)

    curves = {
        'oma': [(0, 0), (5, 8.0), (10, 10.0), (22, 10.9), (40, 10.5), (60, 9.5), (90, 7.5), (120, 5.5), (150, 3.5), (180, 1.5), (200, 0), (400, 0)],
        'conventional_noma': [(0, 0), (5, 3.6), (12, 5.2), (25, 6.2), (45, 6.4), (70, 6.1), (110, 5.6), (160, 4.7), (220, 3.4), (280, 2.2), (340, 1.0), (400, 0)],
        'swipt_noma_case1': [(0, 0), (5, 2.9), (15, 5.5), (30, 6.8), (60, 7.6), (100, 7.9), (150, 7.8), (200, 7.4), (250, 6.2), (300, 4.5), (350, 2.5), (400, 0)],
        'swipt_noma_case2': [(0, 0), (5, 3.1), (15, 5.7), (35, 7.2), (65, 8.4), (100, 8.7), (160, 8.9), (200, 8.5), (250, 7.4), (300, 5.5), (350, 3.0), (400, 0)],
        'swipt_noma_case3': [(0, 0), (5, 3.2), (15, 5.8), (35, 7.4), (65, 8.6), (100, 9.3), (160, 9.8), (200, 9.4), (250, 8.4), (300, 6.2), (350, 3.4), (400, 0)],
    }

    data = {'users': users}
    for name, points in curves.items():
        data[name] = _interp(points, users)
    return pd.DataFrame(data)


def figure3_curves():
    users = np.arange(0, 401, 5)

    curves = {
        'oma': [(0, 0), (5, 8.0), (10, 10.0), (22, 10.9), (40, 10.5), (60, 9.5), (90, 7.5), (120, 5.5), (150, 3.5), (180, 1.5), (200, 0), (400, 0)],
        'conventional_noma': [(0, 0), (5, 3.7), (12, 5.5), (30, 6.3), (45, 6.4), (70, 6.0), (110, 5.5), (160, 4.8), (220, 3.5), (280, 2.3), (340, 1.0), (400, 0)],
        'swipt_noma_case1': [(0, 0), (5, 2.0), (15, 4.4), (35, 5.2), (70, 5.7), (110, 5.8), (150, 6.1), (200, 5.5), (250, 4.6), (300, 3.5), (350, 1.9), (400, 0)],
        'swipt_noma_case2': [(0, 0), (5, 2.2), (15, 4.2), (35, 4.9), (70, 5.6), (110, 5.8), (150, 6.2), (200, 5.8), (250, 5.0), (300, 3.9), (350, 2.0), (400, 0)],
        'swipt_noma_case3': [(0, 0), (5, 2.4), (15, 4.0), (35, 4.6), (70, 5.4), (110, 5.8), (150, 6.2), (200, 5.9), (250, 5.1), (300, 4.1), (350, 2.1), (400, 0)],
    }

    data = {'users': users}
    for name, points in curves.items():
        data[name] = _interp(points, users)
    return pd.DataFrame(data)


def figure4_curves():
    ps_ratio = np.round(np.arange(0.02, 0.91, 0.02), 2)

    rho_1 = 4.55 + 5.15 * np.log1p(4.8 * ps_ratio) / np.log1p(4.8 * 0.9)
    rho_085 = 4.35 + 1.45 * np.log1p(5.5 * ps_ratio) / np.log1p(5.5 * 0.9)

    return pd.DataFrame({
        'power_splitting_ratio': ps_ratio,
        'rho_1': rho_1,
        'rho_085': rho_085,
    })
