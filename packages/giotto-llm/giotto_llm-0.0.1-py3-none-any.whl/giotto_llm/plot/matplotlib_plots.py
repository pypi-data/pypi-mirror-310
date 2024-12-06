import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure

from giotto_llm.type_aliases import Grid, JSONTask

ARC_colors = [
    "#000000",
    "#1E93FF",
    "#F93C31",
    "#4FCC30",
    "#FFDC00",
    "#999999",
    "#E53AA3",
    "#FF851B",
    "#87D8F1",
    "#921231",
    "#FFFFFF",
]
ARC_colormap = plt.matplotlib.colors.ListedColormap(ARC_colors)


def plot_ARC(
    task: JSONTask,
    plot_size: int = 2,
    title: str = "",
    grid_lines_color: str = "#AAAAAA",
) -> Figure:
    """Plot one ARC task.

    :param task: dictionary containing train and test pairs, as read from a JSON
    :param plot_size: dimension of the plot
    :param title: title to be added above the plot
    :param grid_lines_color: color to be used to visually separate grid cells.
        The default is #AAAAAA, i.e. gray.
    """
    assert "train" in task
    assert "test" in task

    # Note: the `fake_pair` is just used to visually separate the
    # train and test pairs
    fake_pair = {
        "input": [[0], [0], [0]],
        "output": [[0], [0], [0]],
    }
    all_pairs = task["train"] + [fake_pair] + task["test"]
    grid_lines_colors = (
        [grid_lines_color for _ in range(len(task["train"]))]
        + ["#FFFFFF"]
        + [grid_lines_color for _ in range(len(task["test"]))]
    )
    titles = (
        [f"Train {i}" for i in range(len(task["train"]))]
        + [""]
        + [f"Test {i}" for i in range(len(task["test"]))]
    )
    fig = _plot_pairs(
        pairs=all_pairs,
        plot_size=plot_size,
        grid_lines_colors=grid_lines_colors,
        titles=titles,
    )
    fig.suptitle(title, fontsize=16)
    fig.subplots_adjust(top=0.88)
    return fig


def _plot_pairs(
    pairs: list[dict],
    plot_size: int,
    grid_lines_colors: list[str],
    titles: list[str],
) -> Figure:
    """Plot ARC pairs.

    :param pairs: list of dictionaries representing input/output pairs, as read from a JSON
    :param plot_size: dimension of the plot
    :param grid_lines_colors: list of colors to be used to visually separate grid cells.
    :param titles: titles to be added above columns in plot
    """
    num_pairs = len(pairs)
    assert num_pairs > 0

    if num_pairs == 1:
        return _plot_arc_one_pair(pairs, titles[0], plot_size, grid_lines_colors[0])
    else:
        return _plot_arc_more_than_one_pair(pairs, titles, plot_size, grid_lines_colors)


def _plot_arc_more_than_one_pair(
    pairs: list[dict],
    titles: list[str],
    plot_size: int,
    grid_lines_colors: list[str],
) -> Figure:
    """Internal function used to plot multiple grid pairs in a ARC task."""
    num_pairs = len(pairs)
    fig, ax = plt.subplots(2, num_pairs, figsize=(plot_size * num_pairs, plot_size * 2))

    for index, (pair, title) in enumerate(zip(pairs, titles)):
        _draw_one_grid(
            ax=ax[0, index],
            grid=pair["input"],
            grid_lines_color=grid_lines_colors[index],
            title=title,
        )
        _draw_one_grid(
            ax=ax[1, index],
            grid=pair["output"],
            grid_lines_color=grid_lines_colors[index],
        )

    fig.tight_layout()
    return fig


def _plot_arc_one_pair(
    pairs: list[dict],
    title: str,
    plot_size: int = 3,
    grid_lines_color: str = "#AAAAAA",
) -> Figure:
    """Internal function used to plot one single grid pair in a ARC task."""
    num_pairs = len(pairs)
    fig, ax = plt.subplots(2, num_pairs, figsize=(plot_size * num_pairs, plot_size * 2))
    fig.suptitle(title, fontsize=14)

    pair = pairs[0]
    _draw_one_grid(ax=ax[0], grid=pair["input"], grid_lines_color=grid_lines_color)
    _draw_one_grid(ax=ax[1], grid=pair["output"], grid_lines_color=grid_lines_color)

    fig.tight_layout()
    return fig


def _draw_one_grid(
    ax: Axes,
    grid: Grid,
    grid_lines_color: str = "#AAAAAA",
    title: str = "",
) -> None:
    """Draw one Grid as a pcolormesh."""
    np_grid = np.array(grid, dtype=np.uint8)
    ax.pcolormesh(
        np_grid,
        edgecolors=grid_lines_color,
        linewidth=0.5,
        cmap=ARC_colormap,
        vmin=0,
        vmax=10,
    )
    ax.invert_yaxis()
    ax.set_aspect("equal")
    if len(title) > 0:
        ax.set_title(title)
    ax.axis("off")


def plot_predictions(task: JSONTask, save_path: str, test_id=0, predictions=None, test_ouput_exists=True) -> None:  # type: ignore
    num_train = len(task["train"])
    num_predictions = len(predictions) if predictions is not None else 0
    fig, axes = plt.subplots(
        num_train + 1 + num_predictions, 2, figsize=(4 * 3, 4 * (num_train + num_predictions + 1))
    )

    # Use fixed color map settings for consistent coloring
    cmap = plt.cm.viridis  # type: ignore # Choose a colormap
    vmin, vmax = 0, 10  # Set color map range for values from 0 to 10

    # Plot training examples
    for i, train_example in enumerate(task["train"]):
        # Training input
        axes[i, 0].imshow(
            train_example["input"], cmap=cmap, vmin=vmin, vmax=vmax, interpolation="none"
        )
        axes[i, 0].set_title(f"Train Input {i+1}")
        axes[i, 0].axis("off")

        # Training output
        axes[i, 1].imshow(
            train_example["output"], cmap=cmap, vmin=vmin, vmax=vmax, interpolation="none"
        )
        axes[i, 1].set_title(f"Train Output {i+1}")
        axes[i, 1].axis("off")

    # Test input and expected output
    test_input = task["test"][test_id]["input"]

    axes[num_train, 0].imshow(test_input, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="none")
    axes[num_train, 0].set_title("Test Input")
    axes[num_train, 0].axis("off")

    if test_ouput_exists:
        test_output = task["test"][test_id]["output"]
    else:
        test_output = np.zeros_like(test_input)

    axes[num_train, 1].imshow(test_output, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="none")
    axes[num_train, 1].set_title("Expected Test Output")
    axes[num_train, 1].axis("off")

    # Plot predictions and missed pixels
    if predictions is not None:
        for j, prediction in enumerate(predictions):
            # Prediction
            axes[num_train + j + 1, 0].imshow(
                prediction, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="none"
            )
            axes[num_train + j + 1, 0].set_title(f"Prediction {j+1}")
            axes[num_train + j + 1, 0].axis("off")

            min_row = min(len(test_output), len(prediction))
            min_col = min(len(test_output[0]), len(prediction[0]))
            # Missed pixels (difference between prediction and expected output)
            missed_pixels = (
                np.array(prediction)[:min_row, :min_col]
                != np.array(test_output)[:min_row, :min_col]
            ).astype(float)
            axes[num_train + j + 1, 1].imshow(missed_pixels, cmap="hot", interpolation="none")
            axes[num_train + j + 1, 1].set_title(f"Missed Pixels {j+1}")
            axes[num_train + j + 1, 1].axis("off")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
