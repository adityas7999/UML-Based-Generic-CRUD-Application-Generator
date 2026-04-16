import os
from jinja2 import Environment, FileSystemLoader

def generate_api(json_model, output_dir="generated_app"):
    """
    Reads the JSON model and generates the Flask app.py using Jinja2.
    """
    # 1. Point Jinja2 to your templates folder
    template_dir = os.path.join("code_generator", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # 2. Load your specific template
    template = env.get_template("api_template.j2")
    
    # 3. Grab the "classes" dictionary from the parsed JSON
    classes_dict = json_model.get("classes", {})
    
    # 4. Render the Python code
    rendered_code = template.render(classes=classes_dict)
    
    # 5. Make sure the output folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    # 6. Save the generated Flask app
    output_path = os.path.join(output_dir, "app.py")
    with open(output_path, "w") as f:
        f.write(rendered_code)
        
    print(f"Flask API successfully generated and saved to {output_path}")