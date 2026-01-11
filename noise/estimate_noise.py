import numpy as np
from scipy.signal import savgol_filter



def estimate_noise_proportion(values, method='savgol', window=11, polyorder=2):
    vals = np.asarray(values, dtype=float)
    if len(vals) < window:
        window = max(3, len(vals) // 2 * 2 + 1)
    # ensure window is odd and not larger than signal length
    if window % 2 == 0:
        window += 1
    window = min(window, len(vals)) if len(vals) > 0 else 3
    if method == 'savgol' and len(vals) >= window:
        smooth = savgol_filter(vals, window_length=window, polyorder=min(polyorder, window-1))
    else:
        kernel = np.ones(window) / window
        smooth = np.convolve(vals, kernel, mode='same')
    resid = vals - smooth
    var_noise = np.nanvar(resid)
    var_total = np.nanvar(vals)
    var_signal = max(0.0, var_total - var_noise)
    proportion = var_noise / var_total if var_total > 0 else 0.0
    snr_db = 10 * np.log10(var_signal / var_noise) if var_noise > 0 and var_signal > 0 else float('inf')
    return {'proportion_noise': proportion, 'snr_db': snr_db, 'smooth': smooth, 'resid': resid}