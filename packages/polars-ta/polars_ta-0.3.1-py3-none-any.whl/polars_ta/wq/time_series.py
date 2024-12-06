import polars_ols as pls
from polars import Expr, Int32, UInt16, struct
from polars import arange, repeat
from polars import rolling_corr, rolling_cov
from polars_ols import RollingKwargs

from polars_ta import TA_EPSILON
from polars_ta.utils.numba_ import batches_i1_o1, batches_i2_o1, batches_i2_o2
from polars_ta.utils.pandas_ import roll_kurt, roll_rank
from polars_ta.wq._nb import roll_argmax, roll_argmin, roll_prod, roll_co_kurtosis, roll_co_skewness, roll_moment, roll_partial_corr, roll_triple_corr, _zip_prod, _zip_sum, signals_to_amount, _cum_sum_reset, _split_sum


def ts_arg_max(x: Expr, d: int = 5, reverse: bool = True) -> Expr:
    return x.map_batches(lambda x1: batches_i1_o1(x1.to_numpy(), roll_argmax, d, reverse, dtype=UInt16))


def ts_arg_min(x: Expr, d: int = 5, reverse: bool = True) -> Expr:
    return x.map_batches(lambda x1: batches_i1_o1(x1.to_numpy(), roll_argmin, d, reverse, dtype=UInt16))


def ts_co_kurtosis(x: Expr, y: Expr, d: int = 5, ddof: int = 0) -> Expr:
    return struct([x, y]).map_batches(lambda xx: batches_i2_o1([xx.struct[i].to_numpy() for i in range(2)], roll_co_kurtosis, d))


def ts_co_skewness(x: Expr, y: Expr, d: int = 5, ddof: int = 0) -> Expr:
    return struct([x, y]).map_batches(lambda xx: batches_i2_o1([xx.struct[i].to_numpy() for i in range(2)], roll_co_skewness, d))


def ts_corr(x: Expr, y: Expr, d: int = 5, ddof: int = 1) -> Expr:
    # x, y is indifferent with y, x
    # x、y不区分先后
    return rolling_corr(x, y, window_size=d, ddof=ddof)


def ts_count(x: Expr, d: int = 30) -> Expr:
    return x.cast(Int32).rolling_sum(d)


def ts_count_nans(x: Expr, d: int = 5) -> Expr:
    # null or nan?
    # null与nan到底用哪一个？
    return x.is_null().rolling_sum(d)


def ts_covariance(x: Expr, y: Expr, d: int = 5, ddof: int = 1) -> Expr:
    # x, y is indifferent with y, x
    # x、y不区分先后
    return rolling_cov(x, y, window_size=d, ddof=ddof)


def ts_cum_max(x: Expr) -> Expr:
    """时序累计最大"""
    return x.cum_max()


def ts_cum_min(x: Expr) -> Expr:
    """时序累计最小"""
    return x.cum_min()


def ts_cum_prod(x: Expr) -> Expr:
    """时序累乘"""
    return x.cum_prod()


def ts_cum_sum(x: Expr) -> Expr:
    """时序累加"""
    return x.cum_sum()


def ts_cum_sum_reset(x: Expr) -> Expr:
    """时序累加。遇到0、nan、相反符号时重置。可用于统计连板数

    1 0 1 2 None 3 -2 -3
    1 0 1 3 0    3 -2 -5
    """
    return x.map_batches(lambda x1: batches_i1_o1(x1.to_numpy().astype(float), _cum_sum_reset))


def ts_decay_exp_window(x: Expr, d: int = 30, factor: float = 1.0) -> Expr:
    # TODO weights not yet supported on array with null values
    y = arange(d - 1, -1, step=-1, eager=False)
    weights = repeat(factor, d, eager=True).pow(y)
    return x.rolling_mean(d, weights=weights)


def ts_decay_linear(x: Expr, d: int = 30) -> Expr:
    # TODO weights not yet supported on array with null values
    weights = arange(1, d + 1, eager=True)
    return x.rolling_mean(d, weights=weights)


def ts_delay(x: Expr, d: int = 1, fill_value=None) -> Expr:
    return x.shift(d, fill_value=fill_value)


def ts_delta(x: Expr, d: int = 1) -> Expr:
    return x.diff(d)


def ts_fill_null(x: Expr) -> Expr:
    """ffill方式填充None"""
    return x.forward_fill()


def ts_ir(x: Expr, d: int = 1) -> Expr:
    return ts_mean(x, d) / ts_std_dev(x, d, 0)


def ts_kurtosis(x: Expr, d: int = 5) -> Expr:
    # TODO 等待polars官方出rolling_kurt
    return x.map_batches(lambda a: roll_kurt(a, d))


def ts_l2_norm(x: Expr, d: int = 5) -> Expr:
    """Euclidean norm"""
    return x.pow(2).rolling_sum(d).sqrt()


def ts_log_diff(x: Expr, d: int = 1) -> Expr:
    """Returns log(current value of input or x[t] ) - log(previous value of input or x[t-1])."""
    return x.log().diff(d)


def ts_max(x: Expr, d: int = 30) -> Expr:
    return x.rolling_max(d)


def ts_max_diff(x: Expr, d: int = 30) -> Expr:
    return x - ts_max(x, d)


def ts_mean(x: Expr, d: int = 5) -> Expr:
    return x.rolling_mean(d)


def ts_median(x: Expr, d: int = 5) -> Expr:
    return x.rolling_median(d)


def ts_min(x: Expr, d: int = 30) -> Expr:
    return x.rolling_min(d)


def ts_min_diff(x: Expr, d: int = 30) -> Expr:
    return x - ts_min(x, d)


def ts_min_max_cps(x: Expr, d: int, f: float = 2) -> Expr:
    """Returns (ts_min(x, d) + ts_max(x, d)) - f * x. If not specified, by default f = 2"""
    return (ts_min(x, d) + ts_max(x, d)) - f * x


def ts_min_max_diff(x: Expr, d: int, f: float = 0.5) -> Expr:
    """Returns x - f * (ts_min(x, d) + ts_max(x, d)). If not specified, by default f = 0.5"""
    return x - f * (ts_min(x, d) + ts_max(x, d))


def ts_moment(x: Expr, d: int, k: int = 0) -> Expr:
    """Returns K-th central moment of x for the past d days."""
    return x.map_batches(lambda x1: batches_i1_o1(x1.to_numpy(), roll_moment, d, k))


def ts_partial_corr(x: Expr, y: Expr, z: Expr, d: int) -> Expr:
    """Returns partial correlation of x, y, z for the past d days."""
    return struct([x, y, z]).map_batches(lambda xx: batches_i2_o1([xx.struct[i].to_numpy() for i in range(3)], roll_partial_corr, d))


def ts_percentage(x: Expr, d: int, percentage: float = 0.5) -> Expr:
    """Returns percentile value of x for the past d days."""
    return x.rolling_quantile(percentage, window_size=d)


def ts_product(x: Expr, d: int = 5) -> Expr:
    return x.map_batches(lambda x1: batches_i1_o1(x1.to_numpy(), roll_prod, d))


def ts_rank(x: Expr, d: int = 5) -> Expr:
    # TODO 等待polars官方出rolling_rank，并支持pct
    # bottleneck长期无人维护，pydata/bottleneck#434 没有合并
    # pandas中已经用跳表实现了此功能，速度也不差
    return x.map_batches(lambda a: roll_rank(a, d, True))


def ts_returns(x: Expr, d: int = 1) -> Expr:
    return x.pct_change(d)


def ts_scale(x: Expr, d: int = 5) -> Expr:
    a = ts_min(x, d)
    b = ts_max(x, d)
    return (x - a) / (b - a + TA_EPSILON)


def ts_skewness(x: Expr, d: int = 5, bias: bool = False) -> Expr:
    # same with pandas when bias=False
    # bias=False与pandas结果一样
    return x.rolling_skew(d, bias=bias)


def ts_std_dev(x: Expr, d: int = 5, ddof: int = 0) -> Expr:
    return x.rolling_std(d, ddof=ddof)


def ts_sum(x: Expr, d: int = 30) -> Expr:
    return x.rolling_sum(d)


def ts_triple_corr(x: Expr, y: Expr, z: Expr, d: int) -> Expr:
    """Returns triple correlation of x, y, z for the past d days."""
    return struct([x, y, z]).map_batches(lambda xx: batches_i2_o1([xx.struct[i].to_numpy() for i in range(3)], roll_triple_corr, d))


def ts_weighted_delay(x: Expr, k: float = 0.5) -> Expr:
    return x.rolling_sum(2, weights=[1 - k, k])


def ts_zscore(x: Expr, d: int = 5) -> Expr:
    return (x - ts_mean(x, d)) / ts_std_dev(x, d)


def ts_zip_prod(v: Expr, r: Expr) -> Expr:
    """z字形累乘。可用于市值累乘日收益率的情况，如成份股权重按行情更新"""
    return struct([v, r]).map_batches(lambda xx: batches_i2_o1([xx.struct[i].to_numpy() for i in range(2)], _zip_prod))


def ts_zip_sum(x: Expr, y: Expr) -> Expr:
    """z字形累加"""
    return struct([x, y]).map_batches(lambda xx: batches_i2_o1([xx.struct[i].to_numpy() for i in range(2)], _zip_sum))


def ts_regression_resid(y: Expr, x: Expr, d: int) -> Expr:
    return pls.compute_rolling_least_squares(y, x, mode='residuals', add_intercept=True, rolling_kwargs=RollingKwargs(window_size=d, min_periods=d))


def ts_regression_pred(y: Expr, x: Expr, d: int) -> Expr:
    return pls.compute_rolling_least_squares(y, x, mode='predictions', add_intercept=True, rolling_kwargs=RollingKwargs(window_size=d, min_periods=d))


def ts_regression_intercept(y: Expr, x: Expr, d: int) -> Expr:
    return pls.compute_rolling_least_squares(y, x, mode='coefficients', add_intercept=True, rolling_kwargs=RollingKwargs(window_size=d, min_periods=d)).struct[1]


def ts_regression_slope(y: Expr, x: Expr, d: int) -> Expr:
    return pls.compute_rolling_least_squares(y, x, mode='coefficients', add_intercept=True, rolling_kwargs=RollingKwargs(window_size=d, min_periods=d)).struct[0]


def ts_resid(y: Expr, *more_x: Expr, d: int) -> Expr:
    """多元时序滚动回归取残差"""
    return pls.compute_rolling_least_squares(y, *more_x, mode='residuals', rolling_kwargs=RollingKwargs(window_size=d, min_periods=d))


def ts_pred(y: Expr, *more_x: Expr, d: int) -> Expr:
    """多元时序滚动回归预测"""
    return pls.compute_rolling_least_squares(y, *more_x, mode='predictions', rolling_kwargs=RollingKwargs(window_size=d, min_periods=d))


def ts_weighted_mean(x: Expr, w: Expr, d: int) -> Expr:
    """时序加权平均"""
    return (x * w).rolling_sum(d) / w.rolling_sum(d)


def ts_weighted_sum(x: Expr, w: Expr, d: int) -> Expr:
    """时序加权求和"""
    return (x * w).rolling_sum(d)


def ts_split_sum(a: Expr, b: Expr, d: int, n: int) -> Expr:
    """切割论求和，以b为依据，对a进行切割

    在d窗口范围内以b为依据进行从小到大排序。最大的N个和最小的N个和
    """
    return struct([a, b]).map_batches(lambda xx: batches_i2_o2([xx.struct[i].to_numpy() for i in range(2)], _split_sum, d, n))


def ts_signals_to_amount(long_entry: Expr, long_exit: Expr,
                         short_entry: Expr, short_exit: Expr,
                         accumulate: bool = False, action: bool = False) -> Expr:
    """多空信号转持仓"""
    return struct([long_entry, long_exit, short_entry, short_exit]).map_batches(lambda xx: batches_i2_o1([xx.struct[i].to_numpy().astype(float) for i in range(4)], signals_to_amount, accumulate, action))
