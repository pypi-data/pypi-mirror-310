#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
def hello():
    return 'hello, world!'

def get_weather():
    return 'Windy'
