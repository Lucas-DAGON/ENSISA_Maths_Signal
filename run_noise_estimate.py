from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from noise.estimate_noise import estimate_noise_proportion
from datetime import datetime

def noise_estimate(data, key='tsun'):
    """Estimate noise proportion and SNR for all key values in the provided data.

    Args:
        data (list of dict): Input data with key value and 'time' keys.

    Returns:
        None: Prints noise proportion and SNR, and shows a plot.
    """
    # convert key values to float and keep entries that have a valid time and numeric values
    data_types = []
    for entry in data:
        time = entry.get('time')
        if time is None:
            continue
        try:
            key_values = float(entry.get(key, 'nan'))
        except (ValueError, TypeError):
            continue
        if np.isfinite(key_values):
            data_types.append({'time': time, key: key_values})

    # build arrays from filtered entries
    times = np.array([entry['time'] for entry in data_types])
    values = np.array([entry[key] for entry in data_types], dtype=float)

    if len(values) == 0:
        print(f"No value found for '{key}'.")
        return

    est = estimate_noise_proportion(values, method='savgol', window=11, polyorder=2)
    print(f"Noice estimation for '{key}':")
    print(f"Noice Proportion (variance): {est['proportion_noise']:.2%}, SNR = {est['snr_db']:.2f} dB")
    print('-----------------------------------')

    # try to convert time strings to datetime objects for plotting
    try:
        dates = np.array([datetime.strptime(t, '%Y-%m-%d') if isinstance(t, str) else t for t in times])
    except Exception:
        dates = times

    # decimate arrays for plotting to avoid over-plotting (keep analysis on full arrays)
    def decimate(arr, max_points=2000):
        n = len(arr)
        if n <= max_points:
            return arr
        idx = np.linspace(0, n - 1, max_points, dtype=int)
        return arr[idx]

    plot_dates = decimate(dates)
    plot_values = decimate(values)
    plot_smooth = decimate(est['smooth'])
    plot_resid = decimate(est['resid'])

    plt.figure(figsize=(12, 6))
    plt.plot(plot_dates, plot_values, label='raw', linewidth=0.6)
    plt.plot(plot_dates, plot_smooth, label='smooth', linewidth=1.0)
    plt.plot(plot_dates, plot_resid, label='resid', alpha=0.6, linewidth=0.6)
    plt.legend()
    if len(plot_dates) > 0 and isinstance(plot_dates[0], datetime):
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))
        plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()