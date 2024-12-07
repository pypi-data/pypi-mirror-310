"""
Filename: __init__.py
Description: long-s is a tool that takes modern text and 
             inserts the archaic letter of the long S (ſ) where it fits.

Author: TravisGK
Version: 1.0.32

License: MIT License
"""


from ._convert import (
    convert_text_file,
    convert_docx_file,
    convert_odf_file,
    convert,
)
