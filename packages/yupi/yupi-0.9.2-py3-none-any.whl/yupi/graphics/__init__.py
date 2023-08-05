"""
This module constains a set of functions dadicated to plot
trajectories and extracted statistical data from ``yupi.stats``

All the resources of this module should be imported directly
from ``yupi.graphics``.
"""

from yupi.graphics._stats_plots import (
    plot_angles_hist,
    plot_kurtosis,
    plot_msd,
    plot_vacf,
    plot_speed_hist,
    plot_psd,
    plot_hist,
    plot_hists
)

from yupi.graphics._trajs_plots import plot_2D, plot_3D

from yupi.graphics._style import (
    LINE,
    LINE_DOTTED,
    DOTTED
)

__all__ = [
    'plot_angles_hist',
    'plot_kurtosis',
    'plot_msd',
    'plot_vacf',
    'plot_speed_hist',
    'plot_2D',
    'plot_3D',
    'plot_psd',
    'plot_hist',
    'plot_hists',
    'LINE',
    'LINE_DOTTED',
    'DOTTED'
]
