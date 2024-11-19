from jinja2 import Template

# Define a simple HTML template
template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
</head>
<body>
    <h1>{{ message }}</h1>
</body>
</html>
""")

# Render the template with a welcome message
html_content = template.render(message="Welcome to the Python App!")

# Save the HTML file
with open("welcome.html", "w") as file:
    file.write(html_content)

print("Welcome page created: open 'welcome.html' in your browser!")
