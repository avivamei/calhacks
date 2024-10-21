import reflex as rx
from ..backend.backend import State

def login_card() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.image(
                        src="/cat.svg",
                        width="8em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Welcome to JobCat!",
                        size="6",
                        as_="h2",
                        text_align="center",  # Center the heading text
                        width="100%",
                    ),
                    direction="column",
                    justify="center",
                    align="center",
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
                    href="/dashboard",
                    justify="center",
                    align="center",
                ),
                spacing="6",
                width="100%",
                justify="center",
                align="center",
            ),
            size="4",
            max_width="28em",  # Ensures a nice max-width for the card
            width="100%",
            justify="center",
            align="center",
        ),
        justify="center",
        align="center",
        width="480px"
    )

# import reflex as rx
# from ..backend.backend import State

# def login_card() -> rx.Component:
#     return rx.card(
#         rx.vstack(
#             rx.flex(
#                 rx.image(
#                     src="/cat.svg",
#                     width="8em",
#                     height="auto",
#                     border_radius="25%",
#                 ),
#                 rx.heading(
#                     "Sign in to your account",
#                     size="6",
#                     as_="h2",
#                     text_align="left",
#                     width="100%",
#                 ),
#                 direction="column",
#                 justify="center",
#                 align="center",
#                 spacing="4",
#                 width="100%",
#             ),
#             rx.link(
#                 rx.button(
#                     rx.icon(tag="log-in"),
#                     "Sign in with Google",
#                     variant="outline",
#                     size="3",
#                     width="100%",
#                 ), 
#                 justify="center",
#                 align="center",
#                 href="/dashboard"
#             ),
#             on_click=State.init_dashboard(),
#             spacing="6",
#             width="100%",
#             justify="center",
#             align="center",
#         ),
#         size="4",
#         max_width="28em",
#         width="100%",
#         justify="center",
#         align="center",
#     )