import itertools
import logging
import matplotlib.pyplot as plt
from typing import List, Union, Optional
from yupi import Trajectory
from yupi.graphics._style import YUPI_COLORS, LINE


def plot_2D(
    trajs: Union[List[Trajectory], Trajectory],
    line_style: str = LINE,
    title: Optional[str] = None,
    legend: bool = True,
    show: bool = True,
    connected: bool = False,
    units: str = "m",
    color=None,
    **kwargs,
):
    """
    Plot all the points of trajectories from ``trajs`` in a 2D plane.

    Parameters
    ----------
    trajs : Union[List[Trajectory], Trajectory]
        Input trajectories.
    line_style : str
        Type of the trajectory line to plot. It uses the matplotlib,
        notation, by default '-'.
    title : str, optional
        Title of the plot, by default None.
    legend : bool, optional
        If True, legend is shown. By default True.
    show : bool, optional
        If True, the plot is shown. By default True.
    connected : bool
        If True, all the trajectory points of same index will be,
        connected.

        If the trajectories do not have same length then the points
        will be connected until the shortest trajectory last index.
    color : str or tuple or list
        Defines the color of the trajectories, by default None.

        If color is of type ``str`` or ``tuple`` (rgb) then the color
        is applied to all trajectories. If color is of type ``list``
        then the trajectories take the color according to the index.

        If there are less colors than trajectories then the remaining
        trajectories are colored automatically (not with the same
        color).
    """

    if isinstance(trajs, Trajectory):
        trajs = [trajs]

    units = "" if units is None else f" [{units}]"

    cycle = itertools.cycle(YUPI_COLORS)
    colors = [cycle.__next__() for _ in trajs]

    if color is not None:
        if isinstance(color, (str, tuple)):
            kwargs["color"] = color
        elif isinstance(color, list):
            colors = color

    if connected:
        lengths = list(map(len, trajs))
        min_len = min(lengths)
        max_len = max(lengths)
        if min_len != max_len:
            logging.warning("Not all the trajectories have the same length.")
        for i in range(min_len):
            traj_points = [t[i] for t in trajs]
            traj_points.append(traj_points[0])
            for tp1, tp2 in zip(traj_points[:-1], traj_points[1:]):
                xs = [tp1.r[0], tp2.r[0]]
                ys = [tp1.r[1], tp2.r[1]]
                plt.plot(xs, ys, color=(0.2, 0.2, 0.2), linewidth=0.5)

    for i, traj in enumerate(trajs):

        if traj.dim != 2:
            logging.warning(
                f"Using plot_2D with a trajectory of {traj.dim} "
                f" dimensions. Trajectory No. {i} with id"
                f" {traj.traj_id})"
            )

        # Plotting
        x, y = traj.r.x, traj.r.y
        if colors is not None:
            if i < len(colors):
                kwargs["color"] = colors[i]
            else:
                kwargs.pop("color")
        traj_plot = plt.plot(x, y, line_style, **kwargs)
        color = traj_plot[-1].get_color()
        traj_id = traj.traj_id if traj.traj_id is not None else f"traj {i}"
        plt.plot(
            x[0],
            y[0],
            "o",
            mfc="white",
            zorder=2,
            label=f"{traj_id} initial position",
            color=color,
        )
        plt.plot(x[-1], y[-1], "o", mfc="white", zorder=2, color=color)
        plt.plot(
            x[-1],
            y[-1],
            "o",
            alpha=0.5,
            label=f"{traj_id} final position",
            color=color,
        )

        if legend:
            plt.legend()

        plt.title(title)
        plt.tick_params(direction="in")
        plt.axis("equal")
        plt.grid(True)
        plt.xlabel(f"x{units}")
        plt.ylabel(f"y{units}")

    if show:
        plt.show()


def plot_3D(
    trajs: Union[List[Trajectory], Trajectory],
    line_style: str = LINE,
    title: Optional[str] = None,
    legend: bool = True,
    show: bool = True,
    connected: bool = False,
    units: str = "m",
    color=None,
    **kwargs,
):
    """
    Plot all the points of trajectories from ``trajs`` in a 3D space.

    Parameters
    ----------
    trajs : Union[List[Trajectory], Trajectory]
        Input trajectories.
    line_style : str
        Type of the trajectory line to plot. It uses the matplotlib,
        notation, by default '-'.
    title : str, optional
        Title of the plot, by default None.
    legend : bool, optional
        If True, legend is shown. By default True.
    show : bool, optional
        If True, the plot is shown. By default True.
    connected : bool
        If True, all the trajectory points of same index will be,
        connected.

        If the trajectories do not have same length then the points
        will be connected until the shortest trajectory last index.
    color : str or tuple or list
        Defines the color of the trajectories, by default None.

        If color is of type ``str`` or ``tuple`` (rgb) then the color
        is applied to all trajectories. If color is of type ``list``
        then the trajectories take the color according to the index.

        If there are less colors than trajectories then the remaining
        trajectories are colored automatically (not with the same
        color).
    """

    if isinstance(trajs, Trajectory):
        trajs = [trajs]

    units = "" if units is None else f" [{units}]"

    cycle = itertools.cycle(YUPI_COLORS)
    colors = [cycle.__next__() for _ in trajs]

    if color is not None:
        if isinstance(color, (str, tuple)):
            kwargs["color"] = color
        elif isinstance(color, list):
            colors = color

    ax = plt.axes(projection="3d")

    if connected:
        lengths = list(map(len, trajs))
        min_len = min(lengths)
        max_len = max(lengths)
        if min_len != max_len:
            logging.warning("Not all the trajectories have the same length.")
        for i in range(min_len):
            traj_points = [t[i] for t in trajs]
            traj_points.append(traj_points[0])
            for tp1, tp2 in zip(traj_points[:-1], traj_points[1:]):
                xs = [tp1.r[0], tp2.r[0]]
                ys = [tp1.r[1], tp2.r[1]]
                zs = [tp1.r[2], tp2.r[2]]
                ax.plot(xs, ys, zs, color=(0.2, 0.2, 0.2), linewidth=0.5)

    for i, traj in enumerate(trajs):

        if traj.dim != 3:
            logging.warning(
                f"Using plot_3D with a trajectory of {traj.dim} "
                f" dimensions. Trajectory No. {i} with id"
                f" {traj.traj_id})"
            )

        # Plotting
        x, y, z = traj.r.x, traj.r.y, traj.r.z

        if colors is not None:
            if i < len(colors):
                kwargs["color"] = colors[i]
            else:
                kwargs.pop("color")
        traj_plot = ax.plot(x, y, z, line_style, **kwargs)
        color = traj_plot[-1].get_color()
        traj_id = traj.traj_id if traj.traj_id is not None else f"traj {i}"

        ax.plot(
            x[0],
            y[0],
            z[0],
            "o",
            mfc="white",
            label=f"{traj_id} initial position",
            color=color,
        )

        ax.plot(x[-1], y[-1], z[-1], "o", mfc="white", color=color)
        ax.plot(
            x[-1],
            y[-1],
            z[-1],
            "o",
            alpha=0.5,
            label=f"{traj_id} final position",
            color=color,
        )

        if legend:
            plt.legend()

        plt.title(title)
        plt.tick_params(direction="in")
        plt.grid(True)
        ax.set_xlabel(f"x{units}")
        ax.set_ylabel(f"y{units}")
        ax.set_zlabel(f"z{units}")

    if show:
        plt.show()
