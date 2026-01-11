import os
import sys

# Add the zadanie package directory to sys.path so tests running from repo root
# can import `main` as a top-level module.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
