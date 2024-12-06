from plotly import graph_objects as go
from plotly.basedatatypes import BaseTraceType
from typing import Union, Optional
from pathlib import Path

from ..figure import Figure
from ...abstract import ReportInterface


def wrap_div(html, class_=None):
    if class_:
        return f"<div class='{class_}'>\n{html}\n</div>\n"
    else:
        return f'<div>\n{html}\n</div>\n'


class GoFigure(Figure):
    """
    Class representing a plotly go figure in the report
    """
    def __init__(
            self,
            figure_data: Union[list[BaseTraceType], dict, go.Figure],
            caption: str = "",
            notes: Optional[list[str]] = None,
            post_script: str = ""
    ):
        """
        The constructor of the GoFigure class
        Args:
            figure_data (dict|go.Figure): The figure data or the go.Figure object
            caption(str): The caption text
            notes (List[str]): The notes to be added to the caption
            post_script: javascript code to be executed after the figure is rendered
        """
        super(GoFigure, self).__init__(caption, notes)
        self.figure_data = figure_data
        self.post_script = post_script
        self.figure_obj = go.Figure(self.figure_data)
        self.image_name: Optional[Path] = None

    def _as_html_figure_content(self, report: ReportInterface):

        if report.images_as_bitmaps:
            self.image_name = report.target_folder / Path(self.id + ".png")
            self.figure_obj.write_image(
                file=report.target_folder / Path(self.id + ".png"),
                format="png",
                width=report.image_width,
                height=report.image_height,
            )
            html = wrap_div(
                html=f"<img src={self.image_name.name} alt=Figure {report.figure_number}",
                class_="figure_div",
            )
        else:

            html = wrap_div(
                self.figure_obj.to_html(
                    config={"displayModeBar": True},
                    include_plotlyjs=False,
                    full_html=False,
                    post_script=self.post_script
                ),
                class_='figure_div'
            )

        return html
