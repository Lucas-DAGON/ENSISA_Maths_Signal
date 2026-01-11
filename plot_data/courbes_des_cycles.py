
import matplotlib.pyplot as plt

def plot_annual_cycles(var, monthly_cycle, months):
    """Plot annual cycles for each variable in monthly_cycle and tsun_cycle."""
    if var in monthly_cycle.columns:
        plt.figure(figsize=(6, 4))
        plt.plot(months, monthly_cycle[var], marker="o")
        plt.xlabel("Mois")
        plt.ylabel(var)
        plt.title(f"Cycle annuel – {var}")
        plt.xticks(months)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

