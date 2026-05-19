def validate_capacity_scale(df, max_allowed=20.0):
    numeric_cols = [col for col in df.columns if col != 'users']
    max_value = float(df[numeric_cols].max().max())

    if max_value > max_allowed:
        raise ValueError(
            f'Capacity scale check failed: max value {max_value:.3f} exceeds {max_allowed}. '
            'This usually means rates were summed over clusters instead of averaged, '
            'or inter-cluster interference was omitted.'
        )
