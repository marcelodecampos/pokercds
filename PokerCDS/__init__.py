#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import URL

url_object = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password="Curiosity killed the cat",  # plain (unescaped) text
    host="db.local",
    database="allsystems",
    query={
        "application_name": "reflex",
    },
).render_as_string(False)
