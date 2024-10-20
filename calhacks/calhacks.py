import reflex as rx

from . import pages
from . import styles

from .pages.dashboard import dashboard
from .pages.landing import landing
from .views.navbar import navbar

def index() -> rx.Component:
    return landing(),
    

app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,

)

app.add_page(
    index, 
    title="Login"
)




