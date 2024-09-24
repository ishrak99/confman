import csv
import sys
from jinja2 import Environment, FileSystemLoader

# Get the uploaded CSV file and configuration type from command line arguments
csv_file = sys.argv[1]
config_type = sys.argv[2]

# Load the correct Jinja2 template based on the selected configuration type
env = Environment(loader=FileSystemLoader('.'))
if config_type == 'basic':
    template = env.get_template('basic_router_config.j2')
else:
    template = env.get_template('advanced_router_config.j2')

# Read the CSV file and generate configs for each router
with open(csv_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Render the template with CSV data
        config = template.render(
            hostname=row['hostname'],
            interface=row['interface'],
            ip_address=row['ip_address'],
            subnet_mask=row['subnet_mask']
        )

        # Write the generated config to a file
        config_filename = f"{row['hostname']}_config.txt"
        with open(config_filename, 'w') as config_file:
            config_file.write(config)

        print(f"Configuration for {row['hostname']} written to {config_filename}")

# Optionally, you can add the logic to run the Ansible playbook after generating the configuration.

