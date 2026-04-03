import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from code_generator.model_generator import generate_models


def test_generate_models_writes_deterministic_python_file(tmp_path):
    output_file = tmp_path / "models.py"

    model_data = {
        "classes": {
            "Student": [
                {"name": "id", "type": "integer"},
                {"name": "name", "type": "string"},
                {"name": "age", "type": "integer"},
            ],
            "Course": [
                {"name": "title", "type": "string"},
            ],
        }
    }

    result_path = generate_models(model_data, output_file)

    assert result_path == str(output_file)
    generated = output_file.read_text(encoding="utf-8")

    assert "class Course:" in generated
    assert "class Student:" in generated
    assert "def __init__(self, id, name, age):" in generated
    assert "id, id" not in generated
    assert "self.name = name" in generated
    assert "self.age = age" in generated
    assert '"id": self.id' in generated
