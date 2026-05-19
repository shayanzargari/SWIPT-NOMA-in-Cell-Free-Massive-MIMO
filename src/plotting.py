from pathlib import Path

import matplotlib.pyplot as plt


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def plot_capacity(df, output_path):
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    plt.figure(figsize=(7, 5))
    plt.plot(df['users'], df['swipt_noma'], marker='o', label='SWIPT-NOMA')
    plt.plot(df['users'], df['noma'], marker='s', label='Conventional NOMA')
    plt.plot(df['users'], df['oma'], marker='^', label='OMA')
    plt.xlabel('Number of users')
    plt.ylabel('Ergodic sum rate (bit/s/Hz)')
    plt.title('Ergodic Capacity Comparison')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_system_model(output_path):
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    fig, ax = plt.subplots(figsize=(8, 5))

    ap_x = [0.12, 0.25, 0.42, 0.72, 0.88]
    ap_y = [0.78, 0.35, 0.63, 0.82, 0.42]
    near_user = (0.58, 0.58)
    far_user = (0.78, 0.20)
    energy_user = (0.30, 0.18)

    ax.scatter(ap_x, ap_y, marker='^', s=160, label='Distributed APs')
    ax.scatter(*near_user, marker='o', s=170, label='Near NOMA user')
    ax.scatter(*far_user, marker='o', s=170, label='Far NOMA user')
    ax.scatter(*energy_user, marker='s', s=160, label='SWIPT / energy harvesting user')

    for x, y in zip(ap_x, ap_y):
        ax.plot([x, near_user[0]], [y, near_user[1]], linewidth=1, alpha=0.45)
        ax.plot([x, far_user[0]], [y, far_user[1]], linewidth=1, alpha=0.25)

    ax.annotate('', xy=far_user, xytext=near_user, arrowprops=dict(arrowstyle='->', linewidth=2))
    ax.text(0.66, 0.42, 'decode-forward relay', fontsize=10, rotation=-45)

    ax.annotate('', xy=energy_user, xytext=near_user, arrowprops=dict(arrowstyle='->', linewidth=2, linestyle='--'))
    ax.text(0.39, 0.36, 'energy transfer / SWIPT', fontsize=10, rotation=35)

    ax.text(0.05, 0.93, 'Cell-free massive MIMO network', fontsize=13, weight='bold')
    ax.text(0.05, 0.88, 'APs jointly serve paired NOMA users; near user supports SWIPT-assisted relaying.', fontsize=10)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
