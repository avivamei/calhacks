import reflex as rx

from . import views

from .views.dashboard import dashboard
from .views.landing import landing
from .views.navbar import navbar

def index() -> rx.Component:
    return landing(),
    

app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="violet"
    ),
)

app.add_page(
    index, 
    title="Login"
)

app.add_page(
    views.dashboard,
    route='/dashboard',
    title="Customer Data App",
    description="A simple app to manage customer data."
)



