from jinja2 import Template

name = "John"

template = Template("Hello, {{ name }}!")
print(template.render(name=name))
