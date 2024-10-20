import reflex as rx
from .. import styles

from reflex.components.radix.themes.base import LiteralAccentColor


def stats_card(
    stat_name: str,
    value: int,
    prev_value: int,
    icon: str,
    icon_color: LiteralAccentColor,
    extra_char: str = "",
) -> rx.Component:
    percentage_change = (
        round(((value - prev_value) / prev_value) * 100, 2)
        if prev_value != 0
        else 0 if value == 0 else float("inf")
    )
    change = "increase" if value > prev_value else "decrease"
    arrow_icon = "trending-up" if value > prev_value else "trending-down"
    arrow_color = "grass" if value > prev_value else "tomato"
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag=icon, size=34),
                    color_scheme=icon_color,
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(
                        f"{extra_char}{value:,}",
                        size="6",
                        weight="bold",
                    ),
                    rx.text(stat_name, size="4", weight="medium"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        tag=arrow_icon,
                        size=24,
                        color=rx.color(arrow_color, 9),
                    ),
                    rx.text(
                        f"{percentage_change}%",
                        size="3",
                        color=rx.color(arrow_color, 9),
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text(
                    f"{change} from last month",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                align="center",
                width="100%",
            ),
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )

def stats_cards() -> rx.Component:
    return rx.grid(
        stats_card(
            stat_name="Applied",
            value=150,
            prev_value=100,
            icon="loader",
            icon_color="yellow",
        ),
        stats_card(
            stat_name="OAs or Interviews",
            value=10,
            prev_value=3,
            icon="star",
            icon_color="indigo",
        ),
        stats_card(
            stat_name="Offers",
            value=2,
            prev_value=0,
            icon="check",
            icon_color="mint",
        ),
        stats_card(
            stat_name="Rejected",
            value=50,
            prev_value=20,
            icon="ban",
            icon_color="red",
        ),
        gap="1rem",
        grid_template_columns=[
            "repeat(1, 1fr)",  # For small screens
            "repeat(2, 1fr)",  # For medium screens
            "repeat(3, 1fr)",  # For large screens
            "repeat(4, 1fr)",  # For extra large screens (four cards)
            "repeat(4, 1fr)",  # For larger screens, maintain 4 in a row
        ],
        width="100%",
    )
