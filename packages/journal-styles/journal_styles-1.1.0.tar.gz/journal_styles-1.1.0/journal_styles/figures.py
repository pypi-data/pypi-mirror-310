#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .parameters import journals
from .constants import golden_ratio, DECIMALS


def standard_figsize(journal="PR", aspect_ratio=golden_ratio):
    """returns the standard figsize for a given journal (1-D plot)
    example of usage
    fs = standard_figsize('PR')
    plt.figure(figsize = fs)"""
    d = journals[journal]
    w = d["onecolumn"]
    h = w / aspect_ratio
    return (round(w, DECIMALS), round(h, DECIMALS))


def standard_rect(journal="PR", aspect_ratio=golden_ratio):
    """returns the standard axes rectangle for a given journal (1-D plot)
    example of usage
    as = standard_rect('PR')
    plt.axes(rect = as)"""
    d = journals[journal]
    w = d["onecolumn"]
    h = w / aspect_ratio
    return [
        round(d["hspace_l"] / w, DECIMALS),
        round(d["vspace_l"] / h, DECIMALS),
        round(1.0 - (d["hspace_s"] + d["hspace_l"]) / w, DECIMALS),
        round(1.0 - (d["vspace_s"] + d["vspace_l"]) / h, DECIMALS),
    ]


class Figure_Frame:
    """Class for composing non-standard figures.
    Example of usage :
    ff = figure_frame('lMs','lMs')
    plt.figure(figsize = ff.figsize)
    plt.axes(ff.rects[0])

    methods
    -------
    __init__

    attributes
    ----------
    figsize (tuple) : figure width and height in inches
    rects (list) : each element is a list of type [left, bottom, width, height]
    representinx axes position expressed in units of figure width and height.
    """

    def __init__(
        self,
        h_spacing="lMs",
        v_spacing="lMs",
        aspect_ratio=golden_ratio,
        journal="PR",
        column="onecolumn",
        additional_axes=[],
    ):
        """
        parameters
        -----------
        h_spacing : string, horizontal division of the figure (left to right).
            Can contain 's' (small space), 'l' (large space), 'h' (half small space),
            'H' (half large space). Must contain 'M' (position of the main axes)
        v_spacing : string, vertical division of the figure (bottom to top).
        aspect_ratio : float, aspect ratio (width/heigth) of the main axes
        journal : string, name of an available journal
        column : string or float, name of an available column type (journal dependent)
            or float (column width in inches)
        additional_axes : list of (int, int) tuples, integer coordinates of the
            rectangle corresponding to secondary axes
        ---------
        returns
        ---------
        instance of the class
        """
        d = journals[journal]
        if isinstance(column, float):
            fig_width = column
        else:
            fig_width = d[column]
        dic_h = {
            "s": d["hspace_s"],
            "l": d["hspace_l"],
            "h": d["hspace_s"] / 2.0,
            "H": d["hspace_l"] / 2.0,
            "M": 0.0,
        }
        dic_v = {
            "s": d["vspace_s"],
            "l": d["vspace_l"],
            "h": d["vspace_s"] / 2.0,
            "H": d["vspace_l"] / 2.0,
            "M": 0.0,
        }
        diff = sum([dic_h[x] for x in h_spacing])
        dic_h["M"] = (fig_width - diff) / h_spacing.count("M")
        dic_v["M"] = dic_h["M"] / aspect_ratio
        fig_height = sum([dic_v[x] for x in v_spacing])
        figsize = (round(fig_width, DECIMALS), round(fig_height, DECIMALS))
        h_indices = [i for i, a in enumerate(h_spacing) if a == "M"]
        v_indices = [i for i, a in enumerate(v_spacing) if a == "M"]
        axes = [(i, j) for j in v_indices for i in h_indices] + additional_axes
        # [(h_spacing.index('M'), v_spacing.index('M'))]

        rects = []
        for ax in axes:
            x0 = sum([dic_h[h_spacing[i]] for i in range(ax[0])])
            y0 = sum([dic_v[v_spacing[i]] for i in range(ax[1])])
            rects.append(
                [
                    round(x0 / fig_width, DECIMALS),
                    round(y0 / fig_height, DECIMALS),
                    round(dic_h[h_spacing[ax[0]]] / fig_width, DECIMALS),
                    round(dic_v[v_spacing[ax[1]]] / fig_height, DECIMALS),
                ]
            )
        self.figsize = figsize
        self.rects = rects
