"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .pages.login import login_page
from .pages.profile import profile_page
from .pages.change_password import change_password_page


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


# Create the main app with dark theme
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="sky",
        gray_color="sand",
        has_background=True,
        radius="large",
        scaling="100%",
    )
)

# Add pages
app.add_page(login_page)
app.add_page(profile_page)
app.add_page(change_password_page)
