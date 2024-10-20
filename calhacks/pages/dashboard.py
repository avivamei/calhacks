import reflex as rx
from ..components.stats_cards import stats_cards_group
from ..views.navbar import navbar
from ..views.table import main_table
from ..templates import template


"""The overview page of the app."""

import reflex as rx
from .. import styles
from ..templates import template
from ..views.stats_cards import stats_cards
from ..views.charts import (
    users_chart,
    revenue_chart,
    orders_chart,
    area_toggle,
    pie_chart,
    timeframe_select,
    StatsState,
)
from ..views.adquisition_view import adquisition
from ..components.notification import notification
from ..components.card import card
from .profile import ProfileState
import datetime


def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%b %d, %Y')} - {datetime.datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Last 30 days", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )


def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )


@template(route="/dashboard", title="Overview", on_load=StatsState.randomize_data)
def dashboard() -> rx.Component:
    """The overview page.

    Returns:
        The UI for the overview page.
    """
    return rx.vstack(
        rx.flex(
            rx.heading("Welcome, Jennifer!", size="9"),
            margin_top="20px",

        ),
        rx.flex(
            rx.text("Job Cat will help you land on your feet", size="6"),
            margin_top="-28px",
        ),
        stats_cards(),
        # rx.grid(
        #     card(
        #         rx.hstack(
        #             rx.hstack(
        #                 rx.icon("user-round-search", size=20),
        #                 rx.text("Visitors Analytics", size="4", weight="medium"),
        #                 align="center",
        #                 spacing="2",
        #             ),
        #             timeframe_select(),
        #             align="center",
        #             width="100%",
        #             justify="between",
        #         ),
        #         pie_chart(),
        #     ),
        #     card(
        #         rx.hstack(
        #             rx.icon("globe", size=20),
        #             rx.text("Acquisition Overview", size="4", weight="medium"),
        #             align="center",
        #             spacing="2",
        #             margin_bottom="2.5em",
        #         ),
        #         rx.vstack(
        #             adquisition(),
        #         ),
        #     ),
        #     gap="1rem",
        #     grid_template_columns=[
        #         "1fr",
        #         "repeat(1, 1fr)",
        #         "repeat(2, 1fr)",
        #         "repeat(2, 1fr)",
        #         "repeat(2, 1fr)",
        #     ],
        #     width="100%",
        # ),
        rx.box(
            main_table(),
            width="100%",
        ),
        spacing="8",
        width="100%",
    )
