import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

######################################################################################################################

def histogram_interactive(X, figsize=(800,600), font_family='Comic Sans MS',  
                          xlabel_size=16, ylabel_size=16, xticks_size=13, yticks_size=13, 
                          color='tomato', nbins=10,
                          margin_l=50, margin_r=40, margin_t=60, margin_b=50, 
                          title=None, title_size=20, title_width=0.5, title_height=1.08):

    X_np = X.drop_nulls().to_numpy()
    df_to_plot = pd.DataFrame({X.name: X_np})

    fig = px.histogram(df_to_plot, x=X.name, nbins=nbins, histnorm='percent')

    if title is None:
        title = f'<b>Histogram - {X.name}<b>'

    # Set the bar color
    fig.update_traces(marker_color=color)

    # Adjust the plot size
    fig.update_layout(
        width=figsize[0],  # width of the plot in pixels
        height=figsize[1]  # height of the plot in pixels
    )

    # Update layout for axis titles
    fig.update_layout(
        xaxis_title=dict(
            text=X.name,
            font=dict(
                family=font_family,
                size=xlabel_size,
                color="black"
            )
        ),
        yaxis_title=dict(
            text='Percentage',
            font=dict(
                family=font_family,
                size=ylabel_size,
                color="black"
            )
        )
    )

    fig.update_layout(
        annotations=[
            dict(
                text=title,
                x=title_width,
                y=title_height,
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(
                    family=font_family,
                    size=title_size,
                    color="black"
                )
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=margin_l, r=margin_r, t=margin_t, b=margin_b)
    )

    fig.update_layout(
        plot_bgcolor='white'
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        tickfont=dict(
            family=font_family,
            size=xticks_size,
            color='black'
        )
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='white',
        automargin=True,
        title_standoff=20,  # Increase this value to add more space between y-axis label and ticks
        tickfont=dict(
            family=font_family,
            size=yticks_size,
            color='black'
        ),
        tickformat='.2f'  # Round to 0 decimal places
    )

    return fig

######################################################################################################################


def barplot_interactive(X, figsize=(800,600), font_family='Comic Sans MS', 
                        xlabel_size=12, ylabel_size=12, xticks_size=10, yticks_size=10, 
                        color='tomato', categories_order=None, orientation='h',
                        margin_l=50, margin_r=40, margin_t=60, margin_b=50, 
                        title=None, title_size=20, title_width=0.5, title_height=1.08):

    X_np = X.drop_nulls().to_numpy()
    unique_values, rel_freq = get_frequencies(X_np)
    # sorting in descending order
    sorted_idx = np.argsort(rel_freq)
    unique_values = unique_values[sorted_idx]
    rel_freq = rel_freq[sorted_idx]
    rel_freq_perc = np.round(rel_freq*100, 2)
    df_to_plot = pd.DataFrame({'Value': unique_values, 'Percentage': rel_freq_perc})

    if orientation == 'h':
        if categories_order is not None:
            fig = px.bar(df_to_plot, y='Value', x='Percentage', category_orders={"Value": categories_order})  
        else:
            fig = px.bar(df_to_plot, y='Value', x='Percentage')
    elif orientation == 'v':
        if categories_order is not None:
            fig = px.bar(df_to_plot, x='Value', y='Percentage', category_orders={"Value": categories_order})  
        else:
            fig = px.bar(df_to_plot, x='Value', y='Percentage')

    if title is None:
        title = f'<b>Barplot - {X.name}<b>'

    # Set the bar color 
    fig.update_traces(marker_color=color)

    # Adjust the plot size
    fig.update_layout(
        width=figsize[0],  # width of the plot in pixels
        height=figsize[1]  # height of the plot in pixels
    )

    # Update layout for axis titles
    fig.update_layout(
        xaxis_title=dict(
            text='Percentage',
            font=dict(
                family=font_family,
                size=xlabel_size,
                color="black"
            )
        ),
        yaxis_title=dict(
            text=X.name,
            font=dict(
                family=font_family,
                size=ylabel_size,
                color="black"
            )
        )
    )

    fig.update_layout(
        annotations=[
            dict(
                text=title,
                x=title_width,
                y=title_height,
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(
                    family=font_family,
                    size=title_size,
                    color="black"
                )
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=margin_l, r=margin_r, t=margin_t, b=margin_b)
    )

    fig.update_layout(
        plot_bgcolor='white'
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        tickfont=dict(
            family=font_family,
            size=xticks_size,
            color='black'
        )
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='white',
        automargin=True,
        title_standoff=20,  # Increase this value to add more space between y-axis label and ticks
        tickfont=dict(
            family=font_family,
            size=yticks_size,
            color='black'
        )
    )

    return fig

######################################################################################################################


def scatterplot_interactive(df, x, y, z_size=None, z_color=None, point_labels=None, hover_name=None, 
                        figsize=(800,600), font_family='Comic Sans MS', 
                        xlabel=None, xlabel_size=12, ylabel_size=12, 
                        xticks_size=10, yticks_size=10, legend_title_side='top',
                        color='tomato', point_size=10, colorscale='Cividis',
                        margin_l=50, margin_r=40, margin_t=60, margin_b=50, 
                        title=None, title_size=20, title_width=0.5, title_height=1.08,
                        point_labels_size=10, point_labels_position='top center'):
    
    fig = px.scatter(df, x=x, y=y, size=z_size, hover_name=hover_name, color=z_color, text=point_labels)

    if title is None:
        title = f'<b>Scatterplot - {y} vs {x}<b>'

    # Adjust the plot size
    fig.update_layout(
        width=figsize[0],  # width of the plot in pixels
        height=figsize[1]  # height of the plot in pixels
    )

    # Update layout for axis titles
    fig.update_layout(
        xaxis_title=dict(
            text=xlabel if xlabel is not None else x,
            font=dict(
                family=font_family,
                size=xlabel_size,
                color="black"
            )
        ),
        yaxis_title=dict(
            text=y,
            font=dict(
                family=font_family,
                size=ylabel_size,
                color="black"
            )
        )
    )

    fig.update_layout(
        annotations=[
            dict(
                text=title,
                x=title_width,
                y=title_height,
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(
                    family=font_family,
                    size=title_size,
                    color="black"
                )
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=margin_l, r=margin_r, t=margin_t, b=margin_b)
    )

    fig.update_layout(
        plot_bgcolor='white'
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        tickfont=dict(
            family=font_family,
            size=xticks_size,
            color='black'
        )
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        automargin=True,
        title_standoff=20,  # Increase this value to add more space between y-axis label and ticks
        tickfont=dict(
            family=font_family,
            size=yticks_size,
            color='black'
        )
    )

    # Add hover label styling
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=13,
            font_family=font_family,
            font_color="black"
        )
    )
    
    # Apply color scale if z_color is specified
    if z_color:
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(
                    text=z_color,
                    font=dict(
                        family=font_family,
                        size=15,
                        color='black'
                    ),
                    side=legend_title_side  # Position of the colorbar title
                )
            )
        )

        fig.update_layout(coloraxis_colorscale=colorscale)  
    else:
        # Apply default color and point size if z_color is not specified
        fig.update_traces(marker=dict(color=color, size=point_size))

    # Set text position on points
    fig.update_traces(textposition=point_labels_position)
    # Set text position, font, and size on points
    fig.update_traces(
        textposition=point_labels_position,
        textfont=dict(
            family=font_family,
            size=point_labels_size,
            color='black'
        )
    )
    return fig

######################################################################################################################

def lineplot_interactive(df, x, y, figsize=(800,600), font_family='Arial', 
                         xlabel_size=16, ylabel_size=16, xticks_size=13, yticks_size=13, 
                         color='royalblue', line_width=3, num_xticks=10,
                         margin_l=50, margin_r=40, margin_t=60, margin_b=50, 
                         title=None, title_size=20, title_width=0.5, title_height=0.95):

    df_to_plot = df.to_pandas()
    df_to_plot = df_to_plot.sort_values(by=x)
    fig = px.line(df_to_plot, x=x, y=y)

    if title is None:
        title = f'<b>Lineplot - {y} vs {x}<b>'

    # Customize the line color
    fig.update_traces(line_color=color, line_width=line_width)

    # Adjust the plot size
    fig.update_layout(
        width=figsize[0],
        height=figsize[1]
    )

    # Update layout for axis titles
    fig.update_layout(
        xaxis_title=dict(
            text=x,
            font=dict(
                family=font_family,
                size=xlabel_size,
                color="black"
            )
        ),
        yaxis_title=dict(
            text=y,
            font=dict(
                family=font_family,
                size=ylabel_size,
                color="black"
            )
        )
    )

    # Update title
    fig.update_layout(
        title={'text': title,
               'y':title_height,
               'x': title_width,
               'xanchor': 'center',
               'yanchor': 'top'},
            font=dict(
                family=font_family,
                size=title_size,
                color="black"
            )
        )

    # Update margins
    fig.update_layout(
        margin=dict(l=margin_l, r=margin_r, t=margin_t, b=margin_b)
    )

    # Update plot background color
    fig.update_layout(
        plot_bgcolor='white'
    )

    # Update x-axis
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        automargin=True,
        title_standoff=20,
        tickfont=dict(
            family=font_family,
            size=xticks_size,
            color='black'
        )
    )

    # Update y-axis
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='white',
        automargin=True,
        title_standoff=20,
        tickfont=dict(
            family=font_family,
            size=yticks_size,
            color='black'
        )
    )

    # Set the number of x-ticks if specified
    if num_xticks is not None:
        x_vals = df_to_plot[x].unique()
        tick_vals = x_vals[::max(1, len(x_vals) // num_xticks)]
        fig.update_xaxes(tickvals=tick_vals)

    return fig

######################################################################################################################


def time_series_interactive_multiplot(dic_df, y, figsize=(800,600), font_family='Comic Sans MS', 
                        xlabel_size=12, ylabel_size=12, xticks_size=10, yticks_size=10, 
                        n_cols=2, wspace=0.5, hspace=0.5, subtitle_size=15, tickangle=90,
                        margin_l=50, margin_r=40, margin_t=60, margin_b=50, line_width=3, color=None,
                        title=None, title_size=20, title_width=0.5, title_height=1.08, nxticks=5):
    
    periods = dic_df.keys()
    n_subplots = len(periods)
    n_rows = int(np.ceil(n_subplots / n_cols))
    colors = px.colors.qualitative.Plotly[:n_subplots] 
    fig = make_subplots(rows=n_rows, cols=n_cols, shared_xaxes=False, shared_yaxes=False,
                        subplot_titles=[f"{y} by {period}" for period in periods],
                        vertical_spacing=hspace, horizontal_spacing=wspace)

    for i, period in enumerate(periods):
        df_to_plot = dic_df[period].to_pandas().sort_values(by=period)
        line_fig = px.line(df_to_plot, x=period, y=y)
        line_fig.update_traces(line_color=colors[i], line_width=line_width) if color is None else line_fig.update_traces(line_color=color, line_width=line_width) 
        row = (i // n_cols) + 1
        col = (i % n_cols) + 1
        for trace in line_fig['data']:
            fig.add_trace(trace, row=row, col=col)

        # Customize x-axis tick format
        fig.update_xaxes(title_text=period, row=row, col=col, title_font=dict(family=font_family, size=xlabel_size, color="black"),
                         tickangle=tickangle[period], tickfont=dict(family=font_family, size=xticks_size, color='black'),
                         tickformat='%Y-%m-%d', nticks=nxticks[period])
        fig.update_yaxes(title_text=y, row=row, col=col, title_font=dict(family=font_family, size=ylabel_size, color="black"))

        # Remove the y-axis labels for the right subplots
        if col > 1:
            fig.update_yaxes(title_text='', row=row, col=col)

    if title is None:
        title = f'<b>Multiple Times Series - {y}<b>'

    # Adjust the plot size
    fig.update_layout(
        width=figsize[0],  # width of the plot in pixels
        height=figsize[1],  # height of the plot in pixels
        margin=dict(l=margin_l, r=margin_r, t=margin_t, b=margin_b)  # increase top margin for title
    )

    # Ensure subplot titles are not overridden
    annotations = list(fig['layout']['annotations'])
    annotations.append(
        dict(
            text=title,
            x=title_width,
            y=title_height, # Position above the subplots
            xref='paper',
            yref='paper',
            showarrow=False,
            font=dict(
                family=font_family,
                size=title_size,
                color="black"
            )
        )
    )
    fig.update_layout(annotations=annotations)
    
    # Explicitly update subplot title sizes
    for annotation in fig['layout']['annotations']:
        for period in periods:
            if 'text' in annotation and period in annotation['text']:
                annotation['font']['size'] = subtitle_size
                annotation['font']['family'] = font_family
                annotation['font']['color'] = 'black'

    fig.update_layout(
        plot_bgcolor='white'
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        tickfont=dict(
            family=font_family,
            size=xticks_size,
            color='black'
        )
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='white',
        automargin=True,
        title_standoff=20,
        tickfont=dict(
            family=font_family,
            size=yticks_size,
            color='black'
        )
    )

    # Add hover label styling
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family=font_family,
            font_color="black"
        )
    )
    
    return fig

######################################################################################################################


def barplot_interactive_2D(df, x, y, figsize=(800,600), font_family='Comic Sans MS', 
                        xlabel=None, ylabel=None, xlabel_size=12, ylabel_size=12, xticks_size=10, yticks_size=10, 
                        color='tomato', margin_l=50, margin_r=40, margin_t=60, margin_b=50, 
                        title=None, title_size=20, title_width=0.5, title_height=1.08,
                        x_grid_color='lightgrey', y_grid_color='lightgrey'):
    
    fig = px.bar(df, x=x, y=y)

    if title is None:
        title = f'<b>Conditional Barplot - {x} | {y}<b>'

    # Set the bar color 
    fig.update_traces(marker_color=color)

    # Adjust the plot size
    fig.update_layout(
        width=figsize[0],  # width of the plot in pixels
        height=figsize[1]  # height of the plot in pixels
    )

    # Update layout for axis titles
    fig.update_layout(
        xaxis_title=dict(
            text=xlabel if xlabel is not None else x,
            font=dict(
                family=font_family,
                size=xlabel_size,
                color="black"
            )
        ),
        yaxis_title=dict(
            text=ylabel if ylabel is not None else y,
            font=dict(
                family=font_family,
                size=ylabel_size,
                color="black"
            )
        )
    )

    fig.update_layout(
        annotations=[
            dict(
                text=title,
                x=title_width,
                y=title_height,
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(
                    family=font_family,
                    size=title_size,
                    color="black"
                )
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=margin_l, r=margin_r, t=margin_t, b=margin_b)
    )

    fig.update_layout(
        plot_bgcolor='white'
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor=x_grid_color ,
        tickfont=dict(
            family=font_family,
            size=xticks_size,
            color='black'
        )
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor=y_grid_color,
        automargin=True,
        title_standoff=20,  # Increase this value to add more space between y-axis label and ticks
        tickfont=dict(
            family=font_family,
            size=yticks_size,
            color='black'
        )
    )

    # Add hover label styling
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=13,
            font_family=font_family,
            font_color="black"
        )
    )
    
    return fig

######################################################################################################################


def barplot_interactive_2D_multiplot(df, x, y, figsize=(800,600), font_family='Comic Sans MS', 
                        xlabel=None, xlabel_size=12, ylabel=None, ylabel_size=12, xticks_size=10, yticks_size=10, 
                        n_cols=2, wspace=0.5, hspace=0.5, subtitle_size=15,
                        margin_l=50, margin_r=40, margin_t=60, margin_b=50, orientation='h',
                        title=None, title_size=20, title_width=0.5, title_height=1.08):
    
    y_categories = df[y].unique()
    n_subplots = len(y_categories)
    n_rows = int(np.ceil(n_subplots / n_cols))
    colors = (px.colors.qualitative.Plotly +
              px.colors.qualitative.D3 +
              px.colors.qualitative.Pastel +
              px.colors.qualitative.Set3)[:n_subplots]
    fig = make_subplots(rows=n_rows, cols=n_cols, shared_xaxes=False, shared_yaxes=False,
                        subplot_titles=[f"{cat}" for cat in y_categories],
                        vertical_spacing=hspace, horizontal_spacing=wspace)

    for i, cat in enumerate(y_categories):
        df_to_plot = df.filter(pl.col(y) == cat).to_pandas()
        if orientation == 'v':
            bar_fig = px.bar(df_to_plot, x='percentage')
        elif orientation == 'h':
            bar_fig = px.bar(df_to_plot, y='percentage', x=x)
        bar_fig.update_traces(marker_color=colors[i])
        row = (i // n_cols) + 1
        col = (i % n_cols) + 1
        for trace in bar_fig['data']:
            fig.add_trace(trace, row=row, col=col)
        fig.update_xaxes(title_text=xlabel if xlabel != None else y, row=row, col=col, title_font=dict(family=font_family, size=xlabel_size, color="black"))
        fig.update_yaxes(title_text=ylabel if ylabel != None else x, row=row, col=col, title_font=dict(family=font_family, size=ylabel_size, color="black"))

        # Remove the y-axis labels for the right subplots
        if col > 1:
            fig.update_yaxes(title_text='', row=row, col=col)
        if row < n_rows:
            fig.update_xaxes(title_text='', row=row, col=col)

    if title is None:
        title = f'<b>Conditional Barplot - {x} | {y}<b>'

    # Adjust the plot size
    fig.update_layout(
        width=figsize[0],  # width of the plot in pixels
        height=figsize[1],  # height of the plot in pixels
        margin=dict(l=margin_l, r=margin_r, t=margin_t + 40, b=margin_b)  # increase top margin for title
    )

    # Ensure subplot titles are not overridden
    annotations = list(fig['layout']['annotations'])
    annotations.append(
        dict(
            text=title,
            x=title_width,
            y=title_height,  # Position above the subplots
            xref='paper',
            yref='paper',
            showarrow=False,
            font=dict(
                family=font_family,
                size=title_size,
                color="black"
            )
        )
    )
    fig.update_layout(annotations=annotations)
    
    # Explicitly update subplot title sizes
    for annotation in fig['layout']['annotations']:
        for cat in y_categories:
            if 'text' in annotation and cat in annotation['text']:
                annotation['font']['size'] = subtitle_size
                annotation['font']['family'] = font_family
                annotation['font']['color'] = 'black'

    fig.update_layout(
        plot_bgcolor='white'
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        tickfont=dict(
            family=font_family,
            size=xticks_size,
            color='black'
        )
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='white',
        automargin=True,
        title_standoff=20,
        tickfont=dict(
            family=font_family,
            size=yticks_size,
            color='black'
        )
    )

    # Add hover label styling
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family=font_family,
            font_color="black"
        )
    )
    
    return fig

######################################################################################################################


def map_interactive(geojson, locations, z, featureidkey, colorscale, marker_opacity, marker_line_width, mapbox_zoom,
                    mapbox_center, title, title_size, title_height, title_width, hue_title, width, height, font_family='Comic Sans MS',
                    margin_l=50, margin_r=40, margin_t=60, margin_b=50):

    # Create the choropleth map
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=locations,
        z=z,
        featureidkey=featureidkey,
        colorscale=colorscale,
        marker_opacity=marker_opacity,
        marker_line_width=marker_line_width,
        coloraxis="coloraxis"
    ))

    # Update the layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=mapbox_zoom,
        mapbox_center=mapbox_center,
        title={
            'text': title,
            'y': title_height,
            'x': title_width,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
                family=font_family,
                size=title_size,
                color="black"
            ),
        coloraxis=dict(
            colorscale=colorscale,
            colorbar=dict(
                title=hue_title,
                titleside="right",
                ticks="outside",
                ticklen=5,
                tickwidth=2,
                tickcolor='rgba(0,0,0,0.5)',
                tickfont=dict(size=12),
                titlefont=dict(size=15)
            )
        ),
        margin={"r": margin_r, "t": margin_t, "l": margin_l, "b": margin_b},
        width=width,  # Set the desired width in pixels
        height=height  # Optional: set the height to maintain aspect ratio
    )

    # Update hover information
    fig.update_traces(
        hovertemplate=f'<b>{locations.name}:</b> ' + '%{location}<br>' + f'<b>{z.name}:</b> ' + '%{z:.2f}<extra></extra>'
    )

    return fig

##########################################################################################

def map_interactive_multiplot(n_cols, geojson, locations, z_dict, subtitles, featureidkey, colorscale, marker_opacity, marker_line_width, mapbox_zoom,
                              mapbox_center, title, title_size, subtitle_size, title_height, title_width, hue_titles, width, height, font_family='Comic Sans MS',
                              margin_l=50, margin_r=40, margin_t=60, margin_b=50, hspace=0.1, wspace=0.1, subtitles_height=0.90, hue_height=0.8, hue_vspace=0.2):

    n_maps = len(z_dict)
    n_rows = int(np.ceil(n_maps / n_cols))
    
    fig = make_subplots(rows=n_rows, cols=n_cols, shared_xaxes=False, shared_yaxes=False,
                        subplot_titles=list(subtitles.values()),
                        vertical_spacing=hspace, horizontal_spacing=wspace,
                        specs=[[{'type': 'mapbox'} for _ in range(n_cols)] for _ in range(n_rows)])

    coloraxis_counter = 1

    for i, z_key in enumerate(z_dict.keys()):
       
        row = (i // n_cols) + 1
        col = (i % n_cols) + 1

        coloraxis_name = f"coloraxis{coloraxis_counter}"
        coloraxis_counter += 1

        fig.add_trace(
            go.Choroplethmapbox(
                geojson=geojson,
                locations=locations,
                z=z_dict[z_key],
                featureidkey=featureidkey,
                colorscale=colorscale,
                marker_opacity=marker_opacity,
                marker_line_width=marker_line_width,
                name=subtitles[z_key],
                hovertemplate=f'<b>{locations.name}:</b> ' + '%{location}<br>' + f'<b>{z_dict[z_key].name}:</b> ' + '%{z:.2f}<extra></extra>',
                coloraxis=coloraxis_name
            ), 
            row=row, col=col
        )

        fig.update_layout(
            **{coloraxis_name: dict(
                colorscale=colorscale,
                colorbar=dict(
                    title=hue_titles[z_key],
                    titleside="right",
                    ticks="outside",
                    ticklen=5,
                    tickwidth=2,
                    tickcolor='rgba(0,0,0,0.5)',
                    tickfont=dict(size=12),
                    titlefont=dict(size=12),
                    x=1.03,  # Adjust x position based on column index
                    y=hue_height - i*hue_vspace,  # Center color bar vertically
                    len=0.3 / n_rows,  # Adjust length of color bar
                    thickness=15  # Adjust thickness of color bar
            ))}
        )

        fig.layout[f'mapbox{i+1}'] = dict(
            style="carto-positron",
            center=mapbox_center,
            zoom=mapbox_zoom,
            domain={
                'x': [0.05 + (col-1)*(1/n_cols) + wspace*(col-1), (col)*(1/n_cols) - wspace],
                'y': [1 - row/n_rows, 1 - (row-1)/n_rows - hspace]
            }
        )

    # Add custom annotations for subtitles
    annotations = []
    for i, (key, subtitle) in enumerate(subtitles.items()):
        row = (i // n_cols) + 1
        col = (i % n_cols) + 1
        x_pos = (0.05 + (col-1)*(1/n_cols) + (col)*(1/n_cols) - wspace) / 2
        y_pos =  subtitles_height - (row-1)/n_rows - hspace / 21

        annotations.append(dict(
            x=x_pos,
            y=y_pos,
            xref='paper',
            yref='paper',
            text=subtitle,
            showarrow=False,
            font=dict(
                size=subtitle_size,
                family=font_family,
                color='black'
            ),
            xanchor='center',
            yanchor='bottom'
        ))

    fig.update_layout(
        title={
            'text': title,
            'y': title_height,
            'x': title_width,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family=font_family,
            size=title_size,
            color="black"
        ),
        margin={"r": margin_r, "t": margin_t, "l": margin_l, "b": margin_b},
        width=width,
        height=height,
        annotations=annotations
    )
    
    return fig

##########################################################################################