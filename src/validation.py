import numpy as np


def validate_capacity_scale(df):
    numeric_cols = [col for col in df.columns if col != 'users']
    values = df[numeric_cols].to_numpy(dtype=float)

    if not np.isfinite(values).all():
        raise ValueError('Capacity validation failed: results contain NaN or infinite values.')

    min_value = float(values.min())
    if min_value < -1e-12:
        raise ValueError(
            f'Capacity validation failed: minimum value {min_value:.3f} is negative.'
        )
