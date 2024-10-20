from ..templates import template
import reflex as rx

from ..components.heading import heading 
from ..components.login_card import login_card

def landing() -> rx.Component:
    return rx.flex(
        heading(),

        login_card(),
        align="center",
        spacing="10",
        flex_direction="column",
        width="100%",
        top="0px",
        padding_top="2em",


    )

        
    