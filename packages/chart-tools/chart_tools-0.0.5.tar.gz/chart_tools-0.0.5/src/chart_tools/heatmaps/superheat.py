import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def superheat(corr, title=None, size=13, masked=True, **kwargs):
    marker = kwargs.get('marker', 's')

    # Data
    dfc = corr.copy()
    dfc = dfc.reindex(sorted(dfc.columns), axis=1)
    if masked:
        for i, c in enumerate(dfc.columns):
            # Remove self-self correlations
            dfc.loc[c,c] = 0.0
            # Remove duplicate correlations
            for col in list(dfc.columns[0:i]):
                dfc.loc[col, c] = 0

    dfc = pd.melt(dfc.reset_index(), id_vars='index') # Unpivot the dataframe, so we can get pair of arrays for x and y
    dfc.columns = ['x', 'y', 'value']
    x = dfc['x']
    y=dfc['y']
    size=dfc['value'].abs()

    fig, ax = plt.subplots()
    plot_grid = plt.GridSpec(1,30,hspace=0.2,wspace=0.1)
    ax = plt.subplot(plot_grid[:,:-1])
    ax.set_title(title)

    # Color
    n_colors = 256
    palette = sns.diverging_palette(20, 220, n=n_colors)
    color_min, color_max = [-1, 1]
    def value_to_color(val):
        val_position = float((val - color_min)) / (color_max - color_min) # position of value in the input range, relative to the length of the input range
        ind = int(val_position * (n_colors - 1)) # target index in the color palette
        return palette[ind]
    
    # Mapping from column names to integer coordinates
    x_labels = [v for v in sorted(x.unique())]
    y_labels = [v for v in sorted(y.unique())]
    x_to_num = {p[1]:p[0] for p in enumerate(x_labels)} 
    y_to_num = {p[1]:p[0] for p in enumerate(y_labels)} 
    xmap = x.map(x_to_num)
    ymap = y.map(y_to_num)
    
    # Draw
    size_scale = 500
    ax.scatter(
        **kwargs,
        x=xmap,
        y=ymap,
        s=size * size_scale, # Vector of square sizes, proportional to size parameter
        c=dfc['value'].apply(value_to_color),
        marker=marker# Use square as scatterplot marker
    )
    
    # Show column labels on the axes
    ax.set_xticks([x_to_num[v] for v in x_labels])
    ax.set_xticklabels(x_labels, rotation=45, horizontalalignment='right')
    ax.set_yticks([y_to_num[v] for v in y_labels])
    ax.set_yticklabels(y_labels)
    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)
    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    ax.invert_xaxis()
    # Color Bar
    ax = plt.subplot(plot_grid[:,-1])

    col_x = [1]*len(palette)
    bar_y = np.linspace(color_min, color_max, n_colors)
    
    bar_height = bar_y[1] - bar_y[0]
    ax.barh(
        y=bar_y,
        width=[2]*len(palette), # make bars 5 units wide
        left=col_x, # Make bars start at 0
        height=bar_height,
        color=palette,
        linewidth=0
    )
    ax.set_xlim(1, 2) # Bars are going from 0 to 5, so lets crop the plot somewhere in the middle
    ax.grid(False) # Hide grid
    ax.set_facecolor('white') # Make background white
    ax.set_xticks([]) # Remove horizontal ticks
    ax.set_yticks(np.linspace(min(bar_y), max(bar_y), 5)) # Show vertical ticks for min, middle and max
    ax.yaxis.tick_right() # Show vertical ticks on the right
