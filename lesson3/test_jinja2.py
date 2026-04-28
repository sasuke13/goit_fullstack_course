from jinja2 import Template, Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('jinja_test.html')

receivers_list = [
   {"name": "John", "age": 20},
   {"name": "Jane", "age": 20},
   {"name": "Jim", "age": 22},
   {"name": "Jill", "age": 23},
]

output_html = template.render(receivers_list=receivers_list)

with open('output.html', 'w', encoding='utf-8') as file:
    file.write(output_html)
