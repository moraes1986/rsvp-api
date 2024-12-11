from jinja2 import Environment

environment = Environment()

def datetime_format(value, format="%H:%M %d-%m-%y"):
    print(value.strftime(format))
    print(value)
    return value.strftime(format)

environment.filters["datetime_format"] = datetime_format