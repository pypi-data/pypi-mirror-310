"""PQ strEEm Exploratory Data Analysis tool."""

from ._version import __version__

import sys
import matplotlib

# Set non-interactive backend before importing pyplot anywhere
try:
    matplotlib.use('Agg')
except ImportError as e:
    print(f"Warning: Failed to set non-interactive matplotlib backend: {e}",
          file=sys.stderr)
    # Continue anyway since we're only using savefig()

# Now safe to import pyplot
import matplotlib.pyplot as plt

# Configure default plot settings
plt.rcParams.update({
    'figure.subplot.left': 0.15,
    'figure.subplot.right': 0.95,
    'figure.subplot.top': 0.9
})

