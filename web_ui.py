import os
import tempfile
import zipfile
import shutil
from flask import Flask, request, send_file, render_template_string

# Import your existing pipeline functions
# (Adjust these imports based on your actual parser/generator file names)
from parser import parse_xmi  # Assuming you have a function that returns model_data
from schema_generator.schema_generator import generate_schema
from code_generator.model_generator import generate_models
from code_generator.repository_generator import generate_repository
from code_generator.api_generator import generate_api

app = Flask(__name__)

# Basic HTML template for the upload form
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>UML to API Generator</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        .container { max-width: 500px; margin: auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        input[type="file"] { margin: 20px 0; }
        button { background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 UML to API Generator</h2>
        <p>Upload your StarUML XMI file to generate your backend.</p>
        <form action="/generate" method="post" enctype="multipart/form-data">
            <input type="file" name="xmi_file" accept=".xmi" required>
            <br>
            <button type="submit">Generate App (ZIP)</button>
        </form>
    </div>
</body>
</html>
"""

def create_manual(output_dir):
    """Generates a README/Manual for the user's zip file."""
    manual_content = """# Auto-Generated CRUD API
    
Congratulations! Your backend has been successfully generated.

## Next Steps:
1. Ensure MySQL is running on your machine.
2. Open your terminal and import the database schema:
   mysql -u root -p < schema.sql

3. Install the required Python packages:
   pip install flask flasgger mysql-connector-python

4. Start your API:
   cd generated_app
   python app.py

5. View your interactive API documentation:
   Open http://127.0.0.1:5000/apidocs/ in your browser.
"""
    manual_path = os.path.join(output_dir, "README_MANUAL.txt")
    with open(manual_path, "w") as f:
        f.write(manual_content)


@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_PAGE)


@app.route('/generate', methods=['POST'])
def generate_zip():
    if 'xmi_file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['xmi_file']
    if file.filename == '':
        return "No file selected", 400

    # 1. Create a secure temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save the uploaded XMI file temporarily
        xmi_path = os.path.join(temp_dir, "uploaded_model.xmi")
        file.save(xmi_path)

        # 2. Parse the XMI
        model_data = parse_xmi(xmi_path)

        # 3. Define output paths inside the temporary folder
        generated_app_dir = os.path.join(temp_dir, "generated_app")
        os.makedirs(generated_app_dir, exist_ok=True)

        schema_out = os.path.join(temp_dir, "schema.sql")
        models_out = os.path.join(generated_app_dir, "models.py")
        repo_out = os.path.join(generated_app_dir, "repository.py")
        api_out = os.path.join(generated_app_dir, "app.py")
        
        # We also need to copy/generate config.py so their app works!
        config_out = os.path.join(generated_app_dir, "config.py")
        shutil.copy("generated_app/config.py", config_out) # Assumes you have a base config.py

        # 4. Run your generators using the temp paths
        generate_schema(model_data, output_file=schema_out)
        generate_models(model_data, output_file=models_out)
        generate_repository(model_data, output_file=repo_out)
        generate_api(model_data, output_file=api_out)

        # 5. Create the manual
        create_manual(temp_dir)

        # 6. Zip the entire temporary directory
        zip_filename = "Generated_Backend.zip"
        zip_filepath = os.path.join(tempfile.gettempdir(), zip_filename)
        
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file == "uploaded_model.xmi": 
                        continue # Don't include the raw XMI in the output
                    
                    file_path = os.path.join(root, file)
                    # Create a clean folder structure inside the zip
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)

        # 7. Send the zip file to the user
        return send_file(zip_filepath, as_attachment=True, download_name="My_API_Backend.zip")

    except Exception as e:
        return f"An error occurred during generation: {str(e)}", 500
        
    finally:
        # Cleanup: Delete the temporary directory from the server
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    print("Starting Web UI on http://127.0.0.1:8080")
    # Using port 8080 so it doesn't conflict with their generated app on 5000
    app.run(debug=True, port=8080)