# Copyright 2021 Cognite AS

import numpy as np
import pandas as pd

from scipy.stats import shapiro

from ..exceptions import UserValueError
from ..ts_utils import generate_step_series
from ..type_check import check_types
from ..validations import validate_series_has_time_index, validate_series_is_not_empty


@check_types
def gaps_identification_z_scores(
    data: pd.Series, cutoff: float = 3.0, test_normality_assumption: bool = False
) -> pd.Series:
    """Gaps detection, Z-scores

    Detect gaps in the time stamps using `Z-scores <https://en.wikipedia.org/wiki/Standard_score>`_. Z-score stands for
    the number of standard deviations by which the value of a raw score (i.e., an observed value or data point) is
    above or below the mean value of what is being observed or measured. This method assumes that the time step sizes
    are normally distributed. Gaps are defined as time periods where the Z-score is larger than cutoff.

    Args:
        data (pd.Series): Time series
        cutoff (float, optional): Cut-off
            Time periods are considered gaps if the Z-score is over this cut-off value. Default 3.0.
        test_normality_assumption (bool, optional): Test for normality
            Raise a warning if the data is not normally distributed.
            The Shapiro-Wilk test is used. The test is only performed if the the time series contains at least 50 data points.

    Returns:
        pd.Series: Time series
            The returned time series is an indicator function that is 1 where there is a gap, and 0 otherwise.

    Raises:
        UserTypeError: data is not a time series
        UserTypeError: cutoff is not a number
        UserValueError: data is empty
        UserValueError: time steps of time series are not normally distributed
    """
    validate_series_has_time_index(data)
    validate_series_is_not_empty(data)

    if len(data) < 2:
        return pd.Series([0] * len(data), index=data.index)

    timestamps = data.index.to_numpy(np.int64)
    diff = np.diff(timestamps)

    if test_normality_assumption and len(data) >= 50:
        W, p_value = shapiro(diff)
        # W is between 0 and 1, small values lead to a rejection of the
        # normality assumption. Ref: https://www.nrc.gov/docs/ML1714/ML17143A100.pdf
        if len(data) < 5000 and p_value < 0.05 or W < 0.5:
            raise UserValueError("The time steps are not normally distibuted")

    if (std := diff.std()) == 0.0:
        z_scores = np.zeros(len(diff))
    else:
        z_scores = (diff - diff.mean()) / std

    is_gap = np.where(z_scores > cutoff, 1, 0)

    return generate_step_series(pd.Series(is_gap, index=data.index[1:]))


@check_types
def gaps_identification_modified_z_scores(data: pd.Series, cutoff: float = 3.5) -> pd.Series:
    """Gaps detection, mod. Z-scores

    Detect gaps in the time stamps using modified Z-scores. Gaps are defined as time periods
    where the Z-score is larger than cutoff.

    Args:
        data (pd.Series): Time series
        cutoff (float, optional): Cut-off
            Time-periods are considered gaps if the modified Z-score is over this cut-off value. Default 3.5.

    Returns:
        pd.Series: Time series
            The returned time series is an indicator function that is 1 where there is a gap, and 0 otherwise.

    Raises:
        UserTypeError: data is not a time series
        UserTypeError: cutoff has to be of type float
        UserValueError: data is empty
    """
    validate_series_has_time_index(data)
    validate_series_is_not_empty(data)

    if len(data) < 2:
        return pd.Series([0] * len(data), index=data.index)

    timestamps = data.index.to_numpy(np.int64)
    diff = np.diff(timestamps)

    median = np.median(diff)
    if (mad := np.median(np.abs(diff - median))) == 0.0:
        modified_z_scores = np.zeros(len(diff))
    else:
        modified_z_scores = 0.6745 * (diff - median) / mad

    is_gap = np.where(modified_z_scores > cutoff, 1, 0)

    return generate_step_series(pd.Series(is_gap, index=data.index[1:]))


@check_types
def gaps_identification_iqr(data: pd.Series) -> pd.Series:
    """Gaps detection, IQR

    Detect gaps in the time stamps using the `interquartile range (IQR)
    <https://en.wikipedia.org/wiki/Interquartile_range>`_ method. The IQR is a measure of statistical
    dispersion, which is the spread of the data. Any time steps that are more than 1.5 IQR above Q3 are considered
    gaps in the data.

    Args:
        data (pd.Series): time series

    Returns:
        pd.Series: time series
            The returned time series is an indicator function that is 1 where there is a gap, and 0 otherwise.

    Raises:
        UserTypeError: data is not a time series
        UserValueError: data is empty
    """
    validate_series_has_time_index(data)
    validate_series_is_not_empty(data)

    if len(data) < 2:
        return pd.Series([0] * len(data), index=data.index)

    timestamps = data.index.to_numpy(np.int64)
    diff = np.diff(timestamps)

    percentile25 = np.quantile(diff, 0.25)
    percentile75 = np.quantile(diff, 0.75)

    iqr = percentile75 - percentile25
    upper_limit = percentile75 + 1.5 * iqr
    is_gap = np.where(diff > upper_limit, 1, 0)

    return generate_step_series(pd.Series(is_gap, index=data.index[1:]))


@check_types
def gaps_identification_threshold(data: pd.Series, time_delta: pd.Timedelta = pd.Timedelta("5m")) -> pd.Series:
    """Gaps detection, threshold

    Detect gaps in the time stamps using a timedelta threshold.

    Args:
        data (pd.Series): time series
        time_delta (pd.Timedelta): Time threshold
            Maximum time delta between points. Defaults to 5min.

    Returns:
        pd.Series: time series
            The returned time series is an indicator function that is 1 where there is a gap, and 0 otherwise.

    Raises:
        UserTypeError: data is not a time series
        UserValueError: data is empty
        UserTypeError: time_delta is not a pd.Timedelta
    """
    validate_series_has_time_index(data)
    validate_series_is_not_empty(data)

    if len(data) < 2:
        return pd.Series([0] * len(data), index=data.index)

    diff = data.index.to_series().diff().dropna()
    is_gap_series = diff > time_delta
    is_gap_series = is_gap_series.astype(int)

    return generate_step_series(is_gap_series)
