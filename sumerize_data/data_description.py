import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.signal import welch
import csv
from pandas import Series
from datetime import datetime

def descriptive_stats(data, key='tsun', time_key='time', save_csv: str | None = None, show_plots: bool = True):
    """Compute a descriptive statistical summary for `key` from a list of dict `data`.

    Returns a summary dict. Optionally shows plots and saves the summary to CSV.
    This function does not modify existing functions and keeps imports local to avoid
    changing top-level imports.
    """
    
    # extract numeric values and times (if present)
    vals = []
    times = []
    for entry in data:
        times.append(entry.get(time_key))
        v = entry.get(key)
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = np.nan
        vals.append(v)

    arr = np.array(vals, dtype=float)
    mask = np.isfinite(arr)
    clean = arr[mask]

    summary = {}
    summary['count'] = int(mask.sum())
    summary['missing'] = int((~mask).sum())
    if summary['count'] == 0:
        return summary

    summary['mean'] = float(np.mean(clean))
    summary['std'] = float(np.std(clean, ddof=1))
    summary['min'] = float(np.min(clean))
    summary['max'] = float(np.max(clean))
    for q in (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99):
        summary[f'q_{int(q*100)}'] = float(np.quantile(clean, q))
    summary['skew'] = float(stats.skew(clean))
    summary['kurtosis'] = float(stats.kurtosis(clean))

    # simple outlier count using IQR rule
    q1, q3 = np.quantile(clean, 0.25), np.quantile(clean, 0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    summary['outliers_count'] = int(((clean < lo) | (clean > hi)).sum())

    # PSD peak frequency (if enough points)
    if len(clean) > 1:
        f, Pxx = welch(clean, fs=1.0)
        summary['psd_peak_freq'] = float(f[np.argmax(Pxx)])

    # save CSV if requested
    if save_csv:
        with open(save_csv, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.writer(fh)
            writer.writerow(['metric', 'value'])
            for k, v in summary.items():
                writer.writerow([k, v])

    # plotting (histogram, boxplot, autocorr, PSD)
    if show_plots:
        plt.figure(); plt.hist(clean, bins=50); plt.title(f'Histogram - {key}')
        plt.figure(); plt.boxplot(clean, vert=False); plt.title(f'Boxplot - {key}')

        # autocorrelation (first N lags)
        def autocorr(x, nlags=100):
            x = x - np.mean(x)
            r = np.correlate(x, x, mode='full')
            mid = len(r) // 2
            ac = r[mid: mid + nlags + 1]
            ac = ac / ac[0]
            return ac

        nl = min(200, len(clean) - 1)
        if nl > 0:
            ac = autocorr(clean, nlags=nl)
            plt.figure()
            plt.stem(range(len(ac)), ac)
            plt.title('Autocorrelation')

        if len(clean) > 1:
            plt.figure(); plt.semilogy(f, Pxx); plt.title('PSD (Welch)')

        # optional: rolling mean vs raw if time values look like dates
        try:
            parsed = [datetime.strptime(t, '%Y-%m-%d') if isinstance(t, str) else None for t in times]
            if any(parsed):
                dates = np.array([d for d in parsed if d is not None])
                vals_for_dates = np.array([float(v) for v, d in zip(vals, parsed) if d is not None])
                if len(vals_for_dates) > 1:
                    window = max(3, min(30, len(vals_for_dates) // 50))
                    rmean = Series(vals_for_dates).rolling(window=window, min_periods=1).mean().values
                    plt.figure(figsize=(10, 4))
                    plt.plot(dates, vals_for_dates, alpha=0.3, label='raw')
                    plt.plot(dates, rmean, label=f'rolling({window})')
                    plt.legend(); plt.title('Rolling mean')
        except Exception:
            pass

        plt.tight_layout(); plt.show()

    return summary