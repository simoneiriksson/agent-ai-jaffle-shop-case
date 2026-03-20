"""Plot-construction helpers that map chart specs to Matplotlib figures."""

import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

def build_plot(chart_output_dict, result, log=print):
    """Build a Matplotlib chart from structured chart metadata and query results.

    Args:
        chart_output_dict: Model-produced chart specification.
        result: pandas DataFrame containing SQL results.
        log: Logging callable for diagnostics.

    Returns:
        Tuple of (figure, axes) for supported chart types, otherwise (None, None).
    """
    match chart_output_dict.get("chart_type", "").lower():
        case "bar":
            log("Interpreted as BAR chart with the following details:")
            log(chart_output_dict)
            fig, ax = plt.subplots()
            x_ticks = result[chart_output_dict["x"]].unique().tolist()
            x_pos = np.arange(len(x_ticks))

            ax.bar(result[chart_output_dict["x"]], result[chart_output_dict["y"]])
            ax.set_xlabel(chart_output_dict["xlabel"])
            ax.set_ylabel(chart_output_dict["ylabel"])
            ax.set_title(chart_output_dict["title"])
            ax.set_xticks(x_pos)
            ax.set_xticklabels(x_ticks, rotation=45, ha="right")
            return fig, ax

        case "grouped_bar":   
            log("Interpreted as GROUPED BAR chart with the following details:")
            log(chart_output_dict)
            fig, ax = plt.subplots()
            group_labels = sorted(result[chart_output_dict["group"]].unique().tolist())
            group_pos = np.arange(len(group_labels))
            xs = sorted(result[chart_output_dict["x"]].unique().tolist())
            for i, x in enumerate(xs):
                x_data = result[result[chart_output_dict["x"]] == x]
                ax.bar(group_pos + i*0.2, x_data[chart_output_dict["y"]], width=0.2, label=str(x))
            ax.set_ylabel(chart_output_dict["ylabel"])
            ax.set_title(chart_output_dict["title"])
            ax.set_xticks(group_pos + 0.2)
            ax.set_xticklabels(group_labels, rotation=45, ha="right")
            ax.legend()
            return fig, ax

        case "wacked_bar": # dropped. Looks aweful and I don't want to deal with the edge cases that will come with it.
            log("Interpreted as STACKED BAR chart with the following details:")
            log(chart_output_dict)
            fig, ax = plt.subplots()
            group_labels = sorted(result[chart_output_dict["stack"]].unique().tolist())
            group_pos = np.arange(len(group_labels))
            xs = sorted(result[chart_output_dict["x"]].unique().tolist())
            x_pos = np.arange(len(xs))
            cumulative_heights = np.zeros(len(xs))
            for i, group in enumerate(group_labels):
                group_data = result[result[chart_output_dict["stack"]] == group]
                ax.bar(x_pos, group_data[chart_output_dict["y"]], width=0.5, label=str(group), bottom=cumulative_heights)
                cumulative_heights += group_data[chart_output_dict["y"]].values
            ax.set_ylabel(chart_output_dict["ylabel"])
            ax.set_title(chart_output_dict["title"])
            ax.set_xticks(x_pos)
            ax.set_xticklabels(xs, rotation=45, ha="right")
            ax.legend()
            return fig, ax

        case "stacked_bar":
            log("Interpreted as STACKED BAR chart with the following details:")
            log(chart_output_dict)
            fig, ax = plt.subplots()
            group_labels = sorted(result[chart_output_dict["group"]].unique().tolist())
            group_pos = np.arange(len(group_labels))
            xs = sorted(result[chart_output_dict["x"]].unique().tolist())
            cumulative_heights = np.zeros(len(group_labels))
            for i, x in enumerate(xs):
                x_data = result[result[chart_output_dict["x"]] == x]
                ax.bar(group_pos, x_data[chart_output_dict["y"]], width=0.5, label=str(x), bottom=cumulative_heights)
                cumulative_heights += x_data[chart_output_dict["y"]].values
            ax.set_ylabel(chart_output_dict["ylabel"])
            ax.set_title(chart_output_dict["title"])
            ax.set_xticks(group_pos)
            ax.set_xticklabels(group_labels, rotation=45, ha="right")
            ax.legend()
            return fig, ax
            
        case "line":
            log("Interpreted as LINE chart with the following details:")
            log(chart_output_dict)                    
            fig, ax = plt.subplots()
            ax.plot(result[chart_output_dict["x"]], result[chart_output_dict["y"]])
            ax.set_xlabel(chart_output_dict["xlabel"])
            ax.set_ylabel(chart_output_dict["ylabel"])
            ax.set_title(chart_output_dict["title"])
            ax.tick_params(axis='x', rotation=45)
            return fig, ax

        case "line_grouped":
            log("Interpreted as GROUPED LINE chart with the following details:")
            log(chart_output_dict)
            fig, ax = plt.subplots()
            group_labels = sorted(result[chart_output_dict["group"]].unique().tolist())
            for group in group_labels:
                group_data = result[result[chart_output_dict["group"]] == group]
                ax.plot(group_data[chart_output_dict["x"]], group_data[chart_output_dict["y"]], label=str(group))
            ax.set_xlabel(chart_output_dict["xlabel"])
            ax.set_ylabel(chart_output_dict["ylabel"])
            ax.set_title(chart_output_dict["title"])
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            return fig, ax

        case "none":
            log("The model determined that no chart is appropriate for this result.")
            return None, None

        case _:
            log("Unknown or unspecified chart type. Raw output:")
            log(chart_output_dict)
            return None, None