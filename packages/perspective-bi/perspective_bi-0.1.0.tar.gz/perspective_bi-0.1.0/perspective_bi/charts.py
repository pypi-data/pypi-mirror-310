import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Union, Dict, Any, List
from .dataset import DataSet

# Default configuration to hide specific modebar buttons
DEFAULT_CONFIG = {
    'displayModeBar': True,
    'modeBarButtonsToRemove': [
        'pan',
        'zoom',
        'zoomIn',
        'zoomOut',
        'autoScale',
        'resetScale',
    ],
    'displaylogo': False
}

class Figure(go.Figure):
    """Custom Figure class that overrides show method with our default configuration."""
    def show(self, config: Optional[Dict] = None, **kwargs):
        """Show the figure with custom configuration."""
        config = config or DEFAULT_CONFIG
        return super().show(config=config, **kwargs)

def bar(
    data: DataSet,
    x: str,
    y: str,
    title: Optional[str] = None,
    color: Optional[str] = None,
    orientation: str = 'v',
    template: str = 'plotly_white',
    **kwargs
) -> Figure:
    """Create a bar chart using Plotly Express."""
    fig = px.bar(
        data.df,
        x=x,
        y=y,
        title=title,
        color=color,
        orientation=orientation,
        template=template,
        **kwargs
    )
    fig.update_layout(
        showlegend=True if color else False,
    )
    # Convert to our custom Figure class
    return Figure(fig)

def line(
    data: DataSet,
    x: str,
    y: Union[str, List[str]],
    title: Optional[str] = None,
    color: Optional[str] = None,
    template: str = 'plotly_white',
    **kwargs
) -> Figure:
    """Create a line chart using Plotly Express."""
    fig = px.line(
        data.df,
        x=x,
        y=y,
        title=title,
        color=color,
        template=template,
        **kwargs
    )
    fig.update_layout(
        showlegend=True if color else False,
    )
    return Figure(fig)

def scatter(
    data: DataSet,
    x: str,
    y: str,
    title: Optional[str] = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
    template: str = 'plotly_white',
    **kwargs
) -> Figure:
    """Create a scatter plot using Plotly Express."""
    fig = px.scatter(
        data.df,
        x=x,
        y=y,
        title=title,
        color=color,
        size=size,
        template=template,
        **kwargs
    )
    fig.update_layout(
        showlegend=True if color else False,
    )
    return Figure(fig)

def pie(
    data: DataSet,
    values: str,
    names: str,
    title: Optional[str] = None,
    template: str = 'plotly_white',
    **kwargs
) -> Figure:
    """Create a pie chart using Plotly Express."""
    fig = px.pie(
        data.df,
        values=values,
        names=names,
        title=title,
        template=template,
        **kwargs
    )
    return Figure(fig)

def histogram(
    data: DataSet,
    x: str,
    nbins: Optional[int] = None,
    title: Optional[str] = None,
    color: Optional[str] = None,
    template: str = 'plotly_white',
    **kwargs
) -> Figure:
    """Create a histogram using Plotly Express."""
    fig = px.histogram(
        data.df,
        x=x,
        nbins=nbins,
        title=title,
        color=color,
        template=template,
        **kwargs
    )
    fig.update_layout(
        showlegend=True if color else False,
    )
    return Figure(fig)
