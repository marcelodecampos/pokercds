import reflex as rx

config = rx.Config(
    app_name="PokerCDS",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)