import numpy as np
from scipy import stats
from scipy import signal
import mne
from typing import Union, Literal

def segment_signal(
    x: np.ndarray,
    w: int,
    s: int = 1,
    alpha: float = 0.05,
    win_fn: Union[str, np.ndarray] = "hamming",
    engine: Literal["c", "npy"] = "c"
) -> np.ndarray:
    """Performs adaptive segmentation using CTX-SEG on a signal.
        C is number of channels. N is length of signal.

    Args:
        x (np.ndarray): Signal, shape (C, N).
        w (int): Window size.
        s (int, optional): Stride. Defaults to 1.
        alpha (float, optional): Significance threshold. Defaults to 0.05.
        win_fn (Union[str, np.ndarray], optional): Window function to apply
            before performing FFT. Defaults to "hamming".
        engine (["c" | "npy"], optional): Backend implementation to use.
            Defaults to "c".

    Raises:
        NotImplementedError: If an unsupported engine is specified.

    Returns:
        np.ndarray: Segment boundaries, shape (C, N).
    """
    assert len(x.shape) == 2, "[ctxseg] signal x must have shape (C, N)"

    print(
        f"[ctxseg] segmenting with w={w}, s={s}, α={alpha}"
    )

    # Getting p-values on every iteration is very slow
    # instead, check the t_stat directly, assuming a symmetrical distribution
    dof = w // 2
    t_thresh = stats.t.ppf(1 - (alpha / 2), dof)

    # Handle window function
    if isinstance(win_fn, str):
        win_fn = signal.windows.get_window(window=win_fn, Nx=w)
    assert isinstance(win_fn, np.ndarray), "[ctxseg] window fn must be an array"
    assert win_fn.shape == (w,), "[ctxseg] window fn must have shape (w,)"

    # Perform segmentation
    if engine == "c":
        from ctxseg.c import seg_ttest

    elif engine == "npy":
        from ctxseg.seg_ttest import seg_ttest

    else:
        raise NotImplementedError(f"[ctxseg] {engine} is not a valid engine")

    z = seg_ttest(x=x, win=win_fn, w=w, s=s, t_thresh=t_thresh)

    return z

def segment_raw(
    raw: mne.io.Raw,
    w: int,
    s: int = 1,
    alpha: float = 0.05,
    win_fn: Union[str, np.ndarray] = "hamming",
    engine: Literal["c", "npy"] = "c",
    picks: Union[str, list, np.ndarray] = None
) -> mne.io.Raw:

    x = raw.get_data(picks=picks)
    z = segment_signal(x=x, w=w, s=s, alpha=alpha, win_fn=win_fn, engine=engine)
    # TODO add z as annotation
    raise NotImplementedError("[ctxseg] not implemented")

    return