from django.test import TestCase

import colorsys



def hex2rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

d = {
    "name": "Первая",
    "type": "2",
    "form": "1",
    "style": "1",
    "body_material": "3",
    "facades_material": "3",
    "tabletop_material": "3",
    "price": 123123,
    "text": "qweqweqweqweqweqweqweq\n2ewe",
    "tags": [
        {
            "id": 1
        },
        {
            "id": 2
        }
    ],
    "purposes": [
        {
            "id": 1
        },
        {
            "id": 2
        }
    ],
    "images": [
        {
            "image": "http://127.0.0.1:8000/media/div.1_11.jpg"
        },
        {
            "image": "http://127.0.0.1:8000/media/drag.jpg"
        }
    ]
}



