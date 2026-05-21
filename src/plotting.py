from pathlib import Path

import matplotlib.pyplot as plt


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def _setup_axes(ax, xlim, xlabel):
    ax.set_xlim(*xlim)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Ergodic Sum Capacity (bps/Hz)', fontsize=12)
    ax.grid(True, linestyle='--', linewidth=0.8, color='black', alpha=0.8)
    ax.tick_params(labelsize=11)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)


def plot_user_capacity_curves(df, output_path):
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))

    ax.plot(df['users'], df['oma'], color='black', linewidth=2.0, label='OMA')
    ax.plot(df['users'], df['conventional_noma'], color='red', linewidth=2.0, label='Conventional NOMA')
    ax.plot(df['users'], df['swipt_noma_case1'], color='lime', linewidth=2.0, label='SWIPT-NOMA  Case1')
    ax.plot(df['users'], df['swipt_noma_case2'], color='blue', linewidth=2.0, label='SWIPT-NOMA  Case2')
    ax.plot(df['users'], df['swipt_noma_case3'], color='#b03060', linewidth=2.0, linestyle='-.', label='SWIPT-NOMA  Case3')

    _setup_axes(ax, (0, 400), 'Number of Users')
    ax.set_xticks(range(0, 401, 50))
    ax.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='black', fontsize=11)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_power_splitting_curves(df, output_path):
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))

    ax.plot(
        df['power_splitting_ratio'],
        df['rho_1'],
        linestyle='None',
        marker='$*$',
        color='blue',
        markersize=9,
        label='ρ=1',
    )
    ax.plot(
        df['power_splitting_ratio'],
        df['rho_085'],
        linestyle='None',
        marker='o',
        color='red',
        markersize=6,
        label='ρ=0.85',
    )

    _setup_axes(ax, (0, 0.92), 'Power Splitting Ratio')
    ax.set_xticks([i / 10 for i in range(0, 10)])
    ax.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='black', fontsize=11)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
