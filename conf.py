import yaml
from jinja2 import Template

try:
    with open('data.yml') as data_file:
        config_data = yaml.load(data_file, Loader=yaml.FullLoader)
except yaml.YAMLError as e:
    print(f"Error parsing YAML: {e}")
    exit(0)
try:
    with open('vhosts.j2') as template_file:
        template_html = template_file.read()
except IOError as e:
    print(f"Error reading template file: {e}")
    exit(0)

template = Template(template_html)
vhosts_conf = template.render(config_data)

try:
    with open('vhosts.conf', 'w') as vhosts_file:
        vhosts_file.write(vhosts_conf)
except IOError as e:
    print(f"Error writing output file: {e}")
    exit(0)