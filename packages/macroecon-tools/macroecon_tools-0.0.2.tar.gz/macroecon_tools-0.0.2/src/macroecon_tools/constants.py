class Constants:
    """
    A class to hold constant mappings and scales used throughout the application.

    Attributes
    ----------
    freq_map : dict
        A dictionary mapping time frequencies to their corresponding pandas resample codes.
        Keys are:
            'quarterly' -> 'Q'
            'monthly' -> 'M'
            'yearly' -> 'Y'
    agg_map : dict
        A dictionary mapping aggregation methods to their corresponding pandas aggregation functions.
        Keys are:
            'lastvalue' -> 'last'
            'mean' -> 'mean'
            'sum' -> 'sum'
            'min' -> 'min'
            'max' -> 'max'
    ANNSCALE_MAP : dict
        A dictionary mapping time frequencies to their corresponding annualization scales.
        Keys are:
            'daily' -> 36500
            'weekly' -> 5200
            'monthly' -> 1200
            'quarterly' -> 400
            'yearly' -> 100
            'annual' -> 100
    """
    # MATLAB retime map to pandas resample
    freq_map = {
        'quarterly': 'Q',
        'monthly': 'M',
        'yearly': 'Y'
    }
    agg_map = {
        'lastvalue': 'last',
        'mean': 'mean',
        'sum': 'sum',
        'min': 'min',
        'max': 'max'
    }

    # Annualization scales
    ANNSCALE_MAP = {
        'daily': 36500,
        'weekly' : 5200,
        'monthly' : 1200,
        'quarterly' : 400,
        'yearly' : 100,
        "annual": 100
    }