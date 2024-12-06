"""
Create html reports from python using simple objects

See module block for documentation on the blocks that can be added to reports.

Classes:
    Report
"""
from pathlib import Path
from datetime import datetime
from jinja2 import Template
from typing import Dict, Optional


from .block import Block
from .abstract import ReportInterface


class Report(ReportInterface):
    """
    Class representing a report
    """

    def __init__(self,
                 target_folder: Path = None,
                 template: Path = None,
                 filename: str = 'report',
                 template_content: Optional[Dict] = None,
                 ):
        """
        Create a report object
        Args:
            target_folder (Path): The folder where the report will be saved
            template (Path): The path to the template to be used for the report (Optional)
            filename: (str): The filename of the report (without suffix)
            template_content (dict): The content to be used for populating the template with the Jinja2 engine
        """

        if template_content is None:
            template_content = dict()
        self.template_content = template_content
        # To avoid long strings in documentation:
        if target_folder is None:
            raise AttributeError("Target folder is required")
        else:
            self.target_folder = target_folder

        if not self.target_folder.exists():
            self.target_folder.mkdir(parents=True)

        if template is None:
            self.template = Path(__file__).parent.joinpath('templates/report_template_numerous.html')
        else:
            self.template = template

        if not filename.endswith('.html'):
            filename += '.html'
        self.filename = filename

        self.report_header_info = None
        self.blocks = {}
        self.figure_number = 0
        self.table_number = 0

    def add_header_info(
            self,
            header: str,
            title: str,
            sub_title: str,
            sub_sub_title: str,
            footer_title: str="",
            footer_content: str=""
    ):
        """
        Adding information to be used for populating html template

        Args:
            header (str): String with header

            title (str): String with title

            sub_title (str):  String with sub title

            sub_sub_title (str): String with sub sub title

        """

        self.report_header_info = dict(
            report_header=header,
            report_type_title=header,
            report_title=title,
            report_sub_title=sub_title,
            report_sub_sub_title=sub_sub_title,
            report_date="{: %d-%m-%Y}".format(datetime.now()),
            footer_title=footer_title,
            footer_content=footer_content
        )

    def set_blocks(self, blocks: dict):
        """
        Overriding blocks to the report.

        Args:
            blocks (dict): Content of block. Values in the key can either be an instance of the class Tabs or Section.

        """
        self._check_blocks(blocks)
        self.blocks = blocks

    def add_blocks(self, blocks: dict):
        """
        Appending blocks to the report.

        Args:
            blocks (dict): Content of block. Values in the key can either be an instance of the class Tabs or Section.

        """
        self._check_blocks(blocks)
        self.blocks.update(blocks)

    def _check_blocks(self, blocks: dict):
        assert type(blocks) == dict, "blocks should be a dictionary"
        for instance in blocks.values():
            assert isinstance(instance, Block), \
                "values in blocks should be Section or Tabs Class instances"

    def generate_html(self):
        """
        Writing objects and header info into html template

        Returns: String html

        """
        assert self.report_header_info is not None, "Please fill out header info"

        html = ""
        for content in self.blocks.values():
            html += content._as_html(self)

        with open(self.template, 'r') as tf:
            template_str = tf.read()

        t = Template(template_str)

        self.template_content.update(self.report_header_info)

        rendered = t.render(report_content=html, **self.template_content).encode('utf-8')

        return rendered

    def save(
            self,
            images_as_bitmaps: bool = False,
            image_width: Optional[int] = None,
            image_height: Optional[int] = None
    ):

        """
        Args:
            images_as_bitmaps: [False, Boolean] to set if images are exported as bitmaps (PNG).
            image_width: [Optional] pixels width of bitmap images (if used)
            image_height: [Optional] pixels height of bitmap images

        Returns:

        """
        self.images_as_bitmaps = images_as_bitmaps
        self.image_width = image_width
        self.image_height = image_height
        
        """Saving the report to the target folder as html file"""
        with open(self.target_folder.joinpath(self.filename), 'wb') as outfile:
            outfile.write(self.generate_html())
