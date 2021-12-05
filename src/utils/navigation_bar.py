import streamlit as st
from utils import constants as const

class Navigation:

    def __init__(self) -> None:
        self.pages = []

    def add_page(self, title, func) -> None:

        self.pages.append({

                "title": title,
                "function": func
            })

    def run(self):
        page = st.sidebar.selectbox(
            const.navigation_title,
            self.pages,
            format_func=lambda page: page['title']
        )
        page['function']()
