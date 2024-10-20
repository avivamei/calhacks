import reflex as rx
from ..backend.backend import State, Customer
from ..components.form_field import form_field
from ..components.form_text_area import form_text_area
from ..components.status_badges import status_badge
from ..components.mode_badges import mode_badge


def show_customer(user: Customer):
    """Show a customer in a table row."""

    return rx.table.row(
        rx.table.cell(user.company, font_weight="bold"),
        rx.table.cell(user.position),
        rx.table.cell(
            rx.match(
                user.mode,
                ("Remote", mode_badge("Remote")),
                ("Hybrid", mode_badge("Hybrid")),
                ("In Person", mode_badge("In Person")),
                ("Unkown", mode_badge("Unknown")),
                mode_badge("Unknown"),
            )
        ),
        rx.table.cell(user.location),
        rx.table.cell(f"${user.payments:,}"),
        rx.table.cell(user.date),
        rx.table.cell(
            rx.match(
                user.status,
                ("Applied", status_badge("Applied")),
                ("OA", status_badge("OA")),
                ("Interview", status_badge("Interview")),
                ("Offer", status_badge("Offer")),
                ("Rejected", status_badge("Rejected")),
                status_badge("Pending"),
            )
        ),
        rx.table.cell(
            rx.hstack(
                update_customer_dialog(user),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    on_click=lambda: State.delete_customer(getattr(user, "id")),
                    size="2",
                    variant="solid",
                    color_scheme="red",
                ),
            )
        ),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def add_application_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Application", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="notebook-pen", size=34),
                    color_scheme="sky",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Application",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the application's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Company
                        form_field(
                            "Company",
                            "Company Name",
                            "text",
                            "company",
                            "rocket",
                        ),
                        # Position
                        form_field(
                            "Position", 
                            "Job Position", 
                            "text", 
                            "position", 
                            "briefcase"
                        ),
                        # Mode
                        rx.vstack(
                            rx.hstack(
                                rx.icon("sparkles", size=16, stroke_width=1.5),
                                rx.text("Work Mode"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Remote", "Hybrid", "In Person", "Unknown"],
                                name="mode",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        # Location
                        form_field(
                            "Location", 
                            "Job Location", 
                            "text", 
                            "location", 
                            "map-pin"
                        ),
                        # Payments
                        form_field(
                            "Payment ($)",
                            "Customer Payment",
                            "number",
                            "payments",
                            "dollar-sign",
                        ),
                        # Status
                        rx.vstack(
                            rx.hstack(
                                rx.icon("loader", size=16, stroke_width=1.5),
                                rx.text("Status"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Applied", "OA", "Interview", "Offer", "Rejected"],
                                name="status",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        # Description
                        form_text_area(
                            "Description",
                            "Job Description",
                            "text",
                            "description",
                            "list",
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Save Application"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.add_customer_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def update_customer_dialog(user):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("eye", size=22),
                rx.text("Edit", size="2"),
                color_scheme="iris",
                size="3",
                variant="ghost",
                on_click=lambda: State.get_user(user),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Edit Application",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edit the Application's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Company
                        form_field(
                            "Company",
                            "Company Name",
                            "text",
                            "company",
                            "rocket",
                            user.company,
                        ),
                        # Position
                        form_field(
                            "Position",
                            "Job Position",
                            "text",
                            "position",
                            "briefcase",
                            user.position,
                        ),
                        # Mode
                        rx.vstack(
                            rx.hstack(
                                rx.icon("sparkles", size=16, stroke_width=1.5),
                                rx.text("Work Mode"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Remote", "Hybrid", "In Person", "Unknown"],
                                default_value=user.mode,
                                name="mode",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        # Location
                        form_field(
                            "Location",
                            "Job Location",
                            "text",
                            "location",
                            "map-pin",
                            user.location,
                        ),
                        # Payments
                        form_field(
                            "Payment ($)",
                            "Customer Payment",
                            "number",
                            "payments",
                            "dollar-sign",
                            user.payments.to(str),
                        ),
                        # Status
                        rx.vstack(
                            rx.hstack(
                                rx.icon("loader", size=16, stroke_width=1.5),
                                rx.text("Status"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Delivered", "Pending", "Cancelled"],
                                default_value=user.status,
                                name="status",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Update Application"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.update_customer_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def main_table():
    return rx.fragment(
        rx.flex(
            add_application_button(),
            rx.spacer(),
            rx.cond(
                State.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
            ),
            rx.select(
                ["date","company", "position", "mode", "location", "payments", "status", "description"],
                placeholder="Sort By: Date",
                size="3",
                on_change=lambda sort_value: State.sort_values(sort_value),
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Search here...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=lambda value: State.filter_values(value),
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Company", "rocket"),
                    _header_cell("Position", "briefcase"),
                    _header_cell("Mode", "sparkles"),
                    _header_cell("Location", "map-pin"),
                    _header_cell("Salary", "dollar-sign"),
                    _header_cell("Date", "calendar"),
                    _header_cell("Status", "loader"),
                    _header_cell("Description", "list"),
                ),
            ),
            rx.table.body(rx.foreach(State.users, show_customer)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=State.load_entries,
        ),
    )
