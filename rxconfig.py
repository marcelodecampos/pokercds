#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import reflex as rx
from sqlalchemy import URL

url_object = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password="Curiosity killed the cat",  # plain (unescaped) text
    host="db.local",
    database="pokercds",
    query={
        "application_name": "reflex",
    },
).render_as_string(False)



config = rx.Config(
    app_name="PokerCDS",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    redis_url="redis://db.local:6379/0[&health_check_interval=10&retry_on_timeout=False]",
    db_url=url_object,
    async_db_url=url_object,
    echo=True,
    echo_pool=True,
    hide_parameters=False,
    pool_pre_ping=True,
    pool_size=30,
    max_overflow=5,
)