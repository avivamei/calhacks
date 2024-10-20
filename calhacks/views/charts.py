import reflex as rx
from sqlmodel import select  # Ensure this import is included
from ..backend.backend import State, Customer

class StatsState(rx.State):
    application_status_data: list[dict] = []

    def calculate_application_status_counts(self):
        """Calculate the count of each status."""
        with rx.session() as session:
            # Retrieve all customers
            customers = session.exec(select(Customer)).all()

            status_counts = {
                "Applied": 0,
                "OA": 0,
                "Interview": 0,
                "Offer": 0,
                "Rejected": 0,
            }
        
            for c in customers:
                status = c.status
                if status in status_counts:
                    status_counts[status] += 1
        
            self.application_status_data = [
                {"name": status, "value": count, "fill": f"var(--{color}-11)"}
                for status, count, color in [
                    ("Applied", status_counts["Applied"], "yellow"),
                    ("OA", status_counts["OA"], "sky"),
                    ("Interview", status_counts["Interview"], "indigo"),
                    ("Offer", status_counts["Offer"], "mint"),
                    ("Rejected", status_counts["Rejected"], "red"),
                ]
            ]

def pie_chart() -> rx.Component:
    """Render a pie chart of customer status counts."""
    StatsState.calculate_application_status_counts()  # Update the state with the latest counts

    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=StatsState.application_status_data,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            padding_angle=1,
            inner_radius="70",
            outer_radius="100",
            label=True,
        ),
        rx.recharts.legend(),
        height=300,
    )