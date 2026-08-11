import numpy as np
import plotly.graph_objects as go


def create_3d_globe_figure(
    temp_matrix: np.ndarray,
    latitudes: np.ndarray,
    longitudes: np.ndarray,
    title: str = "3D Surface Temperature Globe",
) -> go.Figure:
    """
    Project a 2D temperature grid onto a 3D spherical surface (X, Y, Z).
    """
    lat_rad = np.radians(latitudes)
    lon_rad = np.radians(longitudes)
    lon_grid, lat_grid = np.meshgrid(lon_rad, lat_rad)

    # Convert spherical coordinates to 3D Cartesian coordinates
    r = 1.0
    x = r * np.cos(lat_grid) * np.cos(lon_grid)
    y = r * np.cos(lat_grid) * np.sin(lon_grid)
    z = r * np.sin(lat_grid)

    fig = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                surfacecolor=temp_matrix,
                colorscale="Plasma",
                colorbar=dict(title="Temperature (K)"),
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=600,
    )
    return fig