from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def plot_capacity(df, output_path):
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    plt.figure(figsize=(7, 5))
    plt.plot(df['users'], df['swipt_noma'], marker='o', linewidth=2, label='SWIPT-NOMA')
    plt.plot(df['users'], df['noma'], marker='s', linewidth=2, label='Conventional NOMA')
    plt.plot(df['users'], df['oma'], marker='^', linewidth=2, label='OMA')
    plt.xlabel('Number of users')
    plt.ylabel('Ergodic sum rate (bit/s/Hz)')
    plt.title('Ergodic Capacity Comparison')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def _arrow(ax, start, end, style='solid', width=1.7):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle='->',
        mutation_scale=14,
        linewidth=width,
        linestyle=style,
        alpha=0.85,
    )
    ax.add_patch(arrow)


def plot_system_model(output_path):
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    fig, ax = plt.subplots(figsize=(9, 5.8))

    ax.add_patch(Rectangle((0.03, 0.06), 0.94, 0.86, fill=False, linewidth=1.5))
    ax.text(0.05, 0.88, 'Cell-free massive MIMO network', fontsize=14, weight='bold')

    cpu = (0.50, 0.82)
    ax.add_patch(Rectangle((cpu[0] - 0.10, cpu[1] - 0.045), 0.20, 0.09, fill=False, linewidth=1.4))
    ax.text(cpu[0], cpu[1], 'CPU', ha='center', va='center', fontsize=11, weight='bold')

    aps = [(0.16, 0.72), (0.28, 0.42), (0.40, 0.66), (0.66, 0.65), (0.82, 0.38)]
    for idx, ap in enumerate(aps, start=1):
        ax.scatter(*ap, marker='^', s=170)
        ax.text(ap[0], ap[1] + 0.045, f'AP {idx}', ha='center', fontsize=9)
        _arrow(ax, cpu, ap, style='dotted', width=1.0)

    near_user = (0.58, 0.43)
    far_user = (0.78, 0.18)
    eh_user = (0.34, 0.20)

    ax.add_patch(Circle(near_user, 0.045, fill=False, linewidth=1.8))
    ax.text(near_user[0], near_user[1], 'U1', ha='center', va='center', fontsize=10, weight='bold')
    ax.text(near_user[0], near_user[1] + 0.07, 'near NOMA user', ha='center', fontsize=9)

    ax.add_patch(Circle(far_user, 0.045, fill=False, linewidth=1.8))
    ax.text(far_user[0], far_user[1], 'U2', ha='center', va='center', fontsize=10, weight='bold')
    ax.text(far_user[0], far_user[1] - 0.075, 'far NOMA user', ha='center', fontsize=9)

    ax.add_patch(Circle(eh_user, 0.045, fill=False, linewidth=1.8))
    ax.text(eh_user[0], eh_user[1], 'EH', ha='center', va='center', fontsize=10, weight='bold')
    ax.text(eh_user[0], eh_user[1] - 0.075, 'energy harvesting user', ha='center', fontsize=9)

    for ap in aps:
        _arrow(ax, ap, near_user, width=1.1)
        _arrow(ax, ap, far_user, style='dashed', width=1.0)

    _arrow(ax, near_user, far_user, width=2.0)
    ax.text(0.68, 0.31, 'DF relay', fontsize=10, rotation=-37)

    _arrow(ax, near_user, eh_user, style='dashed', width=2.0)
    ax.text(0.40, 0.31, 'SWIPT / power splitting', fontsize=10, rotation=30)

    ax.text(0.07, 0.11, 'Solid links: information transfer', fontsize=9)
    ax.text(0.07, 0.075, 'Dashed links: weak/relay/energy-related links', fontsize=9)
    ax.text(0.55, 0.075, 'APs jointly serve users without cell boundaries', fontsize=9)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
