import os
import pathlib
import re
import time

import streamlit as st


def _name_to_title(name: str) -> str:
    """Converts a camelCase or snake_case name to title case."""
    # If camelCase -> convert to snake case
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    # Convert to title case
    return name.replace("_", " ").strip().title()


start = time.time()

st.set_page_config(
    layout="wide",
    page_title="Conan + myGPT",
    page_icon=":robot_face:",
)
st.title("Aplicaciones de la IA")

DEFAULT_DEMO = "ex1.py"

path_of_script = pathlib.Path(__file__).resolve()
path_to_examples = pathlib.Path(path_of_script).parent.joinpath("examples").resolve()

demos = []
for example_file in os.listdir(path_to_examples):

    file_path = path_to_examples.joinpath(example_file).resolve()

    if not file_path.is_file():
        continue

    demos.append(example_file)

title_to_demo = {}

demo_titles = []
default_index = 0
for i, demo in enumerate(demos):
    if demo == DEFAULT_DEMO:
        # Use hello world as default
        default_index = i
    demo_title = _name_to_title(demo.replace(".py", ""))
    title_to_demo[demo_title] = demo
    demo_titles.append(demo_title)

selected_demo_title = st.selectbox(
    "Selecciona la app", options=demo_titles, index=default_index
)
selected_demo = title_to_demo[selected_demo_title]

exec(open(path_to_examples.joinpath(selected_demo)).read())
elapsed = time.time() - start
st.write(f"La carga de esta pagina ha costado {elapsed:.2f} segundos.")