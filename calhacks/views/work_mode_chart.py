import reflex as rx
from reflex.components.radix.themes.base import LiteralAccentColor
from ..backend.backend import State, Customer
from sqlmodel import select  # Ensure this import is included

def item(
    mode: str, count: int, color: LiteralAccentColor
) -> rx.Component:
    return (
        rx.hstack(
            rx.hstack(
                rx.text(
                    mode,
                    size="3",
                    weight="medium",
                    display=["none", "none", "none", "none", "flex"],
                ),
                width=["10%", "10%", "10%", "10%", "25%"],
                align="center",
                spacing="3",
            ),
            rx.flex(
                rx.text(
                    f"{count}%",
                    position="absolute",
                    top="50%",
                    left=["90%", "90%", "90%", "90%", "95%"],
                    transform="translate(-50%, -50%)",
                    size="1",
                ),
                rx.progress(
                    value=int(count),
                    height="19px",
                    color_scheme=color,
                    width="100%",
                ),
                position="relative",
                width="100%",
            ),
            width="100%",
            border_radius="10px",
            align="center",
            justify="between",
        ),
    )

def work_mode_chart() -> rx.Component:
    with rx.session() as session:
        customers = session.exec(select(Customer)).all()

        mode_counts = {
            "Remote": 0,
            "Hybrid": 0,
            "In Person": 0,
            "Unknown": 0,
        }

        total = 0

        for c in customers:
            total += 1
            mode = c.mode
            if mode in mode_counts:
                mode_counts[mode] += 1

    return rx.vstack(
        item("Remote", int(mode_counts["Remote"] / total* 100), "blue"),
        item("Hybrid", int(mode_counts["Hybrid"] / total * 100), "crimson"),
        item("In Person", int(mode_counts["In Person"] / total * 100), "plum"),
        item("Unknown", int(mode_counts["Unknown"] / total * 100), "gray"),
        width="100%",
        spacing="6",
    )
