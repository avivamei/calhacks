import reflex as rx
from ..components.stats_cards import stats_cards_group
from ..views.navbar import navbar
from ..views.table import main_table
from ..views.sidebar import sidebar


def dashboard() -> rx.Component:
    return rx.vstack(
        navbar(),
        # stats_cards_group(),
        rx.image(src="/cat.svg", height="156px"),
        rx.box(
            main_table(),
            width="100%",
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )
