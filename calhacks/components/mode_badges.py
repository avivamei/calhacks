import reflex as rx

def _badge(mode: str):
    badge_mapping = {
        "Remote": ("Remote", "pink"),
        "Hybrid": ("Hybrid", "violet"),
        "In Person": ("In Person", "orange"),
        "Unknown": ("Unknown", "gray"),
    }
    text, color_scheme = badge_mapping.get(mode, ("Unknown", "gray"))
    return rx.badge(
        text,
        color_scheme=color_scheme,
        radius="large",
        variant="surface",
        size="2",
    )

def mode_badge(mode: str):
    return rx.match(
        mode,
        ("Remote", _badge("Remote")),
        ("Hybrid", _badge("Hybrid")),
        ("In Person", _badge("In Person")),
        ("Unknown", _badge("Unknown")),
        _badge("Unknown"),
    )