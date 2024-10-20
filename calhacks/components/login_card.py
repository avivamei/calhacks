import reflex as rx
from ..backend.backend import State

def login_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.image(
                    src="/cat.svg",
                    width="2.5em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading(
                    "Sign in to your account",
                    size="6",
                    as_="h2",
                    text_align="left",
                    width="100%",
                ),
                # rx.hstack(
                #     rx.text(
                #         "New here?",
                #         size="3",
                #         text_align="left",
                #     ),
                #     rx.link("Sign up", href="/signup", size="3"),
                #     spacing="2",
                #     opacity="0.8",
                #     width="100%",
                # ),
                direction="column",
                justify="start",
                spacing="4",
                width="100%",
            ),
            rx.link(
                rx.button(
                rx.icon(tag="log-in"),
                "Sign in with Google",
                variant="outline",
                size="3",
                width="100%",
                ), 
            href="/dashboard"),
            on_click=State.init_dashboard(),
            spacing="6",
            width="100%",
        ),
        size="4",
        max_width="28em",
        width="100%",
    )