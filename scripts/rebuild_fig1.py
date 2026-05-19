from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.plotting import plot_system_model


if __name__ == '__main__':
    plot_system_model(PROJECT_ROOT / 'figures' / 'figure1_system_model.png')
    print('Saved Figure 1 reconstruction.')
