import textwrap

import streamlit as st
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from code_to_image.prettifiers import get_prettifier_by_name

IMAGE_FORMAT = "png"
MIME_FORMAT = f"image/{IMAGE_FORMAT.lower()}"
TITLE = "Code Formatter"
CODE_SAMPLE = "print('add your code here')"
LANGUAGES = [
    "Python",
    "Text",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "SQL",
    "Go",
    "Ruby",
    "Rust",
]
LANGUAGE_TO_ST_NAME = {
    "Python": "python",
    "Text": None,
    "C": "c",
    "C++": "cpp",
    "Java": "java",
    "JavaScript": "javascript",
    "SQL": "sql",
    "Go": "go",
    "Ruby": "ruby",
    "Rust": "rust",
}

# inputs
st.set_page_config("Code Formatter")
st.title(TITLE)
code_input = st.text_area("Code Input", placeholder=CODE_SAMPLE, height=200)
if not code_input:
    code_input = CODE_SAMPLE
col1, col2 = st.columns(2)
with col1:
    st.markdown("##### General options")
    language = st.selectbox("Language", LANGUAGES)
    output_type = st.radio("Output type", ["Image", "Text"])
    line_numbers = st.checkbox("Add line numbers", True)
with col2:
    st.markdown("##### Format options")
    dedent = st.checkbox("dedent", True)
    if language == "Python":
        line_length = st.slider("Line Length", 20, 120, 88)
        string_normalization = st.checkbox("normalize string quotes", True)
        magic_trailing_comma = st.checkbox(
            "use trailing commas as a reason to split lines", True
        )
        options = dict(
            line_length=line_length,
            string_normalization=string_normalization,
            magic_trailing_comma=magic_trailing_comma,
        )
    else:
        options = {}

# process
code_formatted = textwrap.dedent(code_input) if dedent else code_input
prettify_func = get_prettifier_by_name(language)
code_formatted, format_success = prettify_func(code_formatted, options)
lexer = get_lexer_by_name(language)

# outputs
with col1:
    guessed_lexer = guess_lexer(code_formatted)
    if guessed_lexer.name != lexer.name:
        st.markdown(f"Language: {guessed_lexer.name.replace(' only', '')}?")

st.header("Output")
if not format_success:
    st.caption("Auto-Format failed")
if output_type in ["Image"]:
    code_image = highlight(
        code_formatted,
        lexer,
        ImageFormatter(image_format=IMAGE_FORMAT, line_numbers=line_numbers),
    )
    st.image(code_image, output_format=IMAGE_FORMAT.upper())
elif output_type in ["Text"]:
    st.code(
        code_formatted + "\n",
        language=LANGUAGE_TO_ST_NAME[language],
        line_numbers=line_numbers,
    )
