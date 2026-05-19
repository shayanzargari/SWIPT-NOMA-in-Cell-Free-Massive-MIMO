#!/usr/bin/env bash

set -e

python scripts/rebuild_fig1.py
python scripts/rebuild_fig2.py --mc 500

echo "All paper figures generated successfully."
