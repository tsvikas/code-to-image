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
code_input = st.text_area("Code Input", CODE_SAMPLE, height=300)
col1, col2 = st.columns(2)
with col1:
    line_length = st.slider("Line Length", 20, 120, 88)
with col2:
    line_numbers = st.checkbox("Show Line Numbers", True)
    string_normalization = st.checkbox("String Normalization", True)
    magic_trailing_comma = st.checkbox("Magic Trailing Comma", True)

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
download_filename = (
    TITLE.replace(" ", "")
    + "_"
    + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    + "."
    + IMAGE_FORMAT
)
st.download_button(
    "Download Image", code_image, mime=MIME_FORMAT, file_name=download_filename
)
st.image(code_image, output_format=IMAGE_FORMAT.upper(), use_column_width=False)
st.code(code_formatted + "\n", language="python")
