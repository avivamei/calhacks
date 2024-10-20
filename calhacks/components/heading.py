import reflex as rx


def heading():
    return rx.flex(
        rx.flex(
            rx.icon(tag="paw-print", size=50),
            rx.heading("JobCat", size="9"),
            # color_scheme="green",
            radius="large",
            align="center",
            # variant="outline",
            padding="0.65rem",
            spacing="8px"
        ),
        rx.spacer(),
        rx.hstack(
            rx.logo(),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",        
        padding_x=["1.5em", "1.5em", "3em"],
        padding_bottom="10em"

    )