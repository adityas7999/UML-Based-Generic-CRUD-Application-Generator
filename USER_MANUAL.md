
***

# User Manual: UML to API Generator

Welcome to the **UML-Based Generic CRUD Application Generator**! This tool transforms your architectural designs into a fully functional Flask-based REST API with a MySQL backend.

---

## 📋 Prerequisites
Before you begin, ensure your environment meets the following requirements:
* **Python 3.8+**
* **MySQL 8.0+**
* **StarUML** (or any UML tool capable of exporting standard **XMI 2.1**)
* **Pip** (Python package manager)

---

## 🎨 Phase 1: Designing Your UML
To ensure the generator accurately maps your diagram to a database and API, follow these modeling rules:

1.  **Class Names:** Use **PascalCase** for your classes (e.g., `Course`, `StudentProfile`, `Department`).
2.  **Attributes:** Define attributes with specific types (e.g., `name: string`, `enrollmentDate: date`, `rollNumber: int`).
3.  **Primary Keys:** The generator identifies Primary Keys automatically:
    * It looks for attributes named `id` or `<ClassName>Id` (e.g., `courseId`).
    * If neither is found, it defaults to the **first attribute** in your class.
4.  **Exporting:** * In StarUML, go to **File > Export > XMI**.
    * Ensure the format is **XMI v2.1** or **UML 2.x**.
    * Save the resulting `.xmi` file.

---

## 🚀 Phase 2: Generating Your Application
1.  **Start the Generator:** Open your terminal in the generator project directory and run:
    ```bash
    python web_ui.py
    ```
2.  **Access the UI:** Open your web browser and navigate to `http://127.0.0.1:8080`.
3.  **Upload & Convert:** * Click **Choose File** and select your exported `.xmi` file.
    * Click the **Generate App (ZIP)** button.
4.  **Download:** A file named `Generated_Backend.zip` will download to your machine.

---

## ⚙️ Phase 3: Running Your Generated API
Extract the `Generated_Backend.zip` file. You will find a `generated_app` folder, a `schema.sql` file, and a README.

### Step 1: Setup the Database
You must import the auto-generated SQL schema into your MySQL instance.

1.  **Open your terminal and log into MySQL:**
    ```bash
    mysql -u root -p
    ```
2.  **Run the schema script:**
    ```sql
    -- Replace with the actual path to your extracted file
    source /path/to/extracted/schema.sql;
    ```
    *(Alternatively, run `mysql -u root -p < schema.sql` directly from your terminal prompt).*

### Step 2: Configure Environment Variables
To keep your credentials secure, the application uses environment variables for database connectivity. Set these in the terminal where you will run the app.

| Variable | Description |
| :--- | :--- |
| `DB_HOST` | Usually `localhost` |
| `DB_USER` | Your MySQL username (e.g., `root`) |
| `DB_PASSWORD` | Your actual MySQL password |
| `DB_NAME` | The database name (usually `uml_crud_db`) |

**Windows (Command Prompt):**
```cmd
set DB_HOST=localhost
set DB_USER=root
set DB_PASSWORD=your_password
set DB_NAME=uml_crud_db
```

**Mac / Linux:**
```bash
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="your_password"
export DB_NAME="uml_crud_db"
```

### Step 3: Start the Flask API
1.  **Install Dependencies:**
    ```bash
    pip install flask flasgger mysql-connector-python
    ```
2.  **Navigate and Run:**
    ```bash
    cd path/to/extracted/generated_app
    python app.py
    ```
    The terminal should indicate the app is running on `http://127.0.0.1:5000`.

---

## 🧪 Phase 4: Test Your Endpoints
The generator automatically creates a **Swagger UI** dashboard, allowing you to test your API without writing a single line of frontend code.

1.  Open your browser and go to: **`http://127.0.0.1:5000/apidocs/`**
2.  **Interact:** You will see a list of your classes. Click on any `POST`, `GET`, `PUT`, or `DELETE` endpoint.
3.  **Try it out:** Click the "Try it out" button, enter your data, and click "Execute" to interact directly with your MySQL database!