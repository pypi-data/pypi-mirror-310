from typing import Optional


class Caption:
    """
    Class representing a caption for a figure or table
    """
    def __init__(self, caption: str, notes: Optional[list[str]] = None, type: str = "Figure"):
        """

        Args:
            caption: The caption text. An empty caption disables the caption and numbering.
            notes:  Notes to be added to the caption
            type: A string indicating the type of caption, e.g. "Figure" or "Table"
        """
        self.caption = caption
        if notes:
            self.notes = notes
        else:
            self.notes = []
        self.type = type

    def caption_as_html(self, number: int):
        """
        Returns the caption as html

        """
        notes_str = ''.join([f'<div class="note"> <i>Note: {n} </i></div>' for n in self.notes])

        if self.caption:
            return f'<div class="caption-section"><div class="caption"><b>{self.type} {number}:</b> {self.caption}</div>{notes_str}</div>'
        else:
            return f'<div class="caption-section">{notes_str}</div>'
