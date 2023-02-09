from datetime import datetime

import black
import streamlit as st
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import PythonLexer

IMAGE_FORMAT = "png"
MIME_FORMAT = f"image/{IMAGE_FORMAT.lower()}"
TITLE = "Code Formatter"
CODE_SAMPLE = "print ( 'hello, world' )"

# inputs
st.set_page_config("Code Formatter")
st.title(TITLE)
code_input = st.text_area("Code Input", CODE_SAMPLE, height=200)
col1, col2 = st.columns(2)
with col1:
    line_length = st.slider("Line Length", 20, 120, 88)
with col2:
    line_numbers = st.checkbox("Line Numbers", True)
    string_normalization = st.checkbox("-S", True)
    magic_trailing_comma = st.checkbox("-C", True)

# process
code_formatted = black.format_str(
    code_input, mode=black.Mode(
        line_length=line_length,
        string_normalization=string_normalization,
        magic_trailing_comma=magic_trailing_comma,
    )
)
code_image = highlight(
    code_formatted,
    PythonLexer(),
    ImageFormatter(
        image_format=IMAGE_FORMAT, line_numbers=line_numbers
    ),
)

# outputs
st.subheader("Output")
st.image(code_image, output_format=IMAGE_FORMAT.upper())
st.code(code_formatted + "\n", language="python")
