#!/usr/bin/env bash

set -e

python scripts/rebuild_fig2.py
python scripts/rebuild_fig3.py
python scripts/rebuild_fig4.py

echo "Figures 2, 3, and 4 generated successfully."
