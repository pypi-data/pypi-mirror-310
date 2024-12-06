from typing import Dict, Optional
from abc import ABC, abstractmethod
from pathlib import Path



class ReportInterface(ABC):
    figure_number: int
    table_number: int
    target_folder: Path
    images_as_bitmaps: bool = False
    image_width: Optional[int] = None
    image_height: Optional[int] = None

    @abstractmethod
    def add_header_info(
            self,
            header: str,
            title: str,
            sub_title: str,
            sub_sub_title: str,
            footer_title: str,
            footer_content: str,
    ):
        pass

    @abstractmethod
    def set_blocks(
            self,
            blocks: Dict,
            ):
        pass

    @abstractmethod
    def add_blocks(
            self,
            blocks: Dict,
    ):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def generate_html(self):
        pass






