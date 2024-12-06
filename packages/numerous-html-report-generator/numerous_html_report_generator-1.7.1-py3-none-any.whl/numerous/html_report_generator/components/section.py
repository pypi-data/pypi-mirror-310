from ..block import Block
from ..abstract import ReportInterface
from typing import Dict


class Section(Block):
    """
    Class representing a section in the report

    """

    def __init__(self,
                 section_title: str):
        """

        Args:
            section_title (str): The title of the section
        """
        self.section_title = section_title
        self.content: Dict[str, Block] = {}

    def set_content(self, content: Dict[str, Block]):
        """
        Set the content of the section
        Args:
            content (dict): A dictionary of the content of the section, the keys are the titles of the blocks and the values are the blocks themselves

        Returns:

        """
        self.check_content(content)
        self.content = content

    def add_content(self, content: Dict[str, Block]):
        """
        Add content to the section
        Args:
            content (dict): A dictionary of the content of the section, the keys are the titles of the blocks and the values are the blocks themselves

        Returns:

        """
        self.check_content(content)
        self.content.update(content)

    @staticmethod
    def check_content(content: Dict[str, Block]):
        assert type(content) is dict

    def _as_html(self, report: ReportInterface):
        html = f"<div><h1 class=\"section_title editable\">{self.section_title}</h1></div>"
        for item in self.content.values():
            html += item._as_html(report)

        return html


class Subsection(Section):
    def _as_html(self, report: ReportInterface):
        html = f"<div><h2 class=\"section_title editable\">{self.section_title}</h2></div>"
        for item in self.content.values():
            html += item._as_html(report)

        return html
