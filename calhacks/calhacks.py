import reflex as rx

from . import pages
from . import styles

from .pages.dashboard import dashboard
from .pages.landing import landing
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




