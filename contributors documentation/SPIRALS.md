# UML → CRUD Generator

## Workload Management

## Work Flow

### Step-by-Step: Spiral in Our Project

Our project has 4 natural high-risk components:
1. XMI Parsing
2. Data Type Mapping
3. SQL Generation
4. Flask Code Generation

So we build them in spirals.

---

## Spiral 1 – Core Parsing Risk

### Objective
Can we reliably extract UML Classes and Attributes from XMI?

### Risks
- XMI structure inconsistency
- StarUML version differences
- Malformed files

### Activities
- Build minimal parser
- Extract class names + attributes only
- Ignore relationships
- Validate 3–4 sample XMI files

### Deliverable
- Parsed JSON representation of UML model

**If this fails → project fails. So we tackle it first.**

---

## Spiral 2 – Data Type & Schema Risk

### Objective
Can UML types be correctly converted to MySQL?

### Risks
- Incorrect type mapping
- Nullability handling
- Primary key strategy

### Activities
- Implement type mapping table
- Generate basic CREATE TABLE
- Test schema on MySQL

### Deliverable
- Working schema.sql generator

**Now risk reduces significantly.**

---

## Spiral 3 – Relationship & Foreign Key Risk

### Objective
Handle associations (1:1, 1:*).

### Risks
- Wrong FK placement
- Circular references
- Naming conflicts

### Activities
- Parse association tags
- Generate FK constraints
- Validate with sample UML models

### Deliverable
- Complete relational schema support

**This is technically complex → good Spiral use case.**

---

## Spiral 4 – Backend Code Generation

### Objective
Generate Flask CRUD layers.

### Risks
- Route generation errors
- SQL injection vulnerabilities
- Incorrect entity-table mapping

### Activities
- Generate Model layer first
- Then Repository
- Then Controller
- Test API using Postman

### Deliverable
- Fully working CRUD backend

---

## Final Spiral – Hardening & Validation

### Objective
Stability & polish.

### Activities
- Performance testing (≤5 sec for 20 classes)
- Invalid input handling
- Template separation (Jinja2)
- Determinism check

### Deliverable
- Final submission-ready system

---

## Summary: What We Actually Do

You divide implementation into risk-based phases:
1. Parser
2. Schema generator
3. Relationship handler
4. CRUD code generator
5. System hardening

Each phase:
- Plan
- Identify risk
- Implement
- Validate
- Move forward

---

# Workload Distribution

## 1st Spiral

### Objective of Spiral 1

**Deliverable at end:**
- Input: `input.xmi`
- Output: Clean internal JSON representation like:

```json
{
  "classes": [
    {
      "name": "Student",
      "attributes": [
        {"name": "id", "type": "Integer"},
        {"name": "name", "type": "String"}
      ]
    }
  ]
}
```

If this works reliably → project foundation is solid.

---

### Member 1 – XMI Structure Analyst

**Responsibility:** Understand and document StarUML XMI structure.

**Tasks:**
- Export 3–4 different UML models from StarUML
- Open XMI in text editor
- Identify:
  - Where classes are stored
  - Where attributes are stored
  - How associations appear
- Create a small documentation file explaining structure

**Deliverable:** Internal documentation + sample XMI test cases.

This reduces blind coding risk.

---

### Member 2 – Core Parser Developer

**Responsibility:** Implement XML parsing logic.

**Tasks:**
- Use lxml or ElementTree
- Extract:
  - Class names
  - Attribute names
  - Attribute types
- Return structured Python dictionary

No validation logic yet. Just extraction.

**Deliverable:** `parser.py` working on sample files.

---

### Member 3 – Validation & Error Handler

**Responsibility:** Add validation layer on top of parser.

**Tasks:**
- Detect duplicate class names
- Detect duplicate attributes in same class
- Detect empty class
- Detect malformed XML
- Produce clear error messages

**Deliverable:** Validation module integrated with parser.

---

### Member 4 – Integration & Test Lead

**Responsibility:** Make everything clean and testable.

**Tasks:**
- Design JSON output format
- Combine parser + validation
- Create CLI command:
  ```bash
  python generate.py input.xmi
  ```
- Test with:
  - Valid file
  - Invalid file
  - Missing attributes
  - Corrupted file

**Deliverable:** Working CLI prototype + test report.

---

### Why This Division Works
- No one is idle
- No one owns everything
- Everyone contributes technically
- Risk is distributed
- We avoid merge chaos

---

### Suggested Timeline (7–10 Days)
- **Day 1–2:** Member 1 analysis
- **Day 3–5:** Parser implementation
- **Day 6–7:** Validation + integration
- **Day 8–9:** Testing + fixing
- **Day 10:** Freeze Spiral 1

Then move to Spiral 2.

---

### At End of Spiral 1 You Should Have
- ✓ Stable UML → JSON extraction
- ✓ Error handling
- ✓ CLI working
- ✓ Test cases documented
- ✓ Confidence in foundation

That's a successful spiral.

---

## 2nd Spiral

### Objective of Spiral 2

**Input:**
```json
{
  "classes": [
    {
      "name": "Student",
      "attributes": [
        {"name": "name", "type": "String"},
        {"name": "age", "type": "Integer"}
      ]
    }
  ]
}
```

**Output:**
```sql
CREATE TABLE Student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT
);
```

---

### Member 1 – Data Type Mapping Designer

**Responsibility:** Design and implement UML → MySQL type conversion logic.

**Tasks:**
1. Create mapping table:
   - `String` → `VARCHAR(255)`
   - `Integer` → `INT`
   - `Boolean` → `TINYINT(1)`
   - `Float` → `DECIMAL(10,2)`
   - `Date` → `DATETIME`
2. Handle:
   - Unknown types → default to `VARCHAR(255)`
   - Log warning
3. Write: `type_mapper.py`
4. Unit test:
   - Known types
   - Unknown type
   - Case sensitivity

**Deliverable:** Reusable function:
```python
map_type("String") → "VARCHAR(255)"
```

This module must be clean and isolated.

---

### Member 2 – Table Generator Developer

**Responsibility:** Convert class object → SQL CREATE TABLE statement.

**Tasks:**
1. Write logic:
   - Loop over classes
   - Add `id INT AUTO_INCREMENT PRIMARY KEY`
   - Add attribute columns using type_mapper
   - Generate proper SQL syntax
   - Handle comma placement properly
2. Ensure:
   - Table name matches class name
   - No trailing commas
   - Valid SQL formatting
3. Output: `schema.sql`

**Deliverable:** Working `schema_generator.py`

---

### Member 3 – SQL Validation & Constraint Handler

**Responsibility:** Improve schema robustness.

**Tasks:**
1. Add:
   - `NOT NULL` if required (if your model supports it)
   - Basic constraints if defined
2. Validate:
   - No duplicate column names
   - SQL keyword conflicts (e.g., table named "Order")
3. Test:
   - Run generated SQL in MySQL
   - Check errors
   - Document issues
4. Improve formatting readability

**Deliverable:** Validated schema that runs without SQL errors.

---

### Member 4 – Integration & Architecture Control

**Responsibility:** System-level integration + quality control.

**Tasks:**
1. Integrate:
   - parser output
   - validation layer
   - type_mapper
   - schema_generator
2. Ensure pipeline:
   ```
   XMI → JSON → Type Mapping → SQL File
   ```
3. Define output structure:
   - Where schema.sql is saved
   - Overwrite behavior
4. Run:
   - End-to-end tests
   - Performance check (20 classes case)
5. Freeze stable version of Spiral 2

---

### Why This Division Is Smart
- Member 1 handles logic abstraction
- Member 2 handles SQL generation
- Member 3 ensures correctness & robustness
- You control system flow and stability

Nobody overlaps heavily. Nobody is idle. You maintain architectural overview.

---

### What Should NOT Do In Spiral 2
- ❌ Do not implement foreign keys (push to Spiral 3)
- ❌ Do not implement Flask
- ❌ Do not optimize prematurely
- ❌ Do not change internal JSON structure drastically

**Spiral 2 is about: Reliable Table Generation Only.**

---

### Suggested Timeline (7–8 Days)
- **Day 1–2:** Type mapping design
- **Day 3–4:** Table generation
- **Day 5–6:** SQL validation & MySQL testing
- **Day 7–8:** Integration + end-to-end testing

Then freeze.

---

### End of Spiral 2 You Should Have
- ✓ Valid schema.sql
- ✓ Deterministic output
- ✓ Clean architecture separation
- ✓ Fully tested table creation
- ✓ Zero SQL syntax errors

**Now system becomes real.**

# 🎯 Objective of Spiral 3

Spiral 3 focuses on **relationship handling and foreign key generation**.

Specifically:

* Parse **UML associations**
* Identify **1:1 and 1:* relationships**
* Generate **FOREIGN KEY constraints**
* Modify `schema.sql` accordingly
* Ensure SQL execution still works

No Flask CRUD yet (that can be Spiral 4).

---

# 👥 Proper Work Distribution (4 Members)

Each role should match the architecture you already have.

---

# 👤 Member 1 – Association Parser

### Responsibility

Extract relationship information from XMI.

### Tasks

1. Extend `parser.py` to detect:

```
uml:Association
```

2. Extract:

* Source class
* Target class
* Multiplicity
* Association direction

Example internal model:

```json
{
  "associations": [
    {
      "source": "Student",
      "target": "Department",
      "type": "many-to-one"
    }
  ]
}
```

3. Add this to the internal JSON structure.

### Deliverable

Parser now produces:

```
classes
attributes
associations
```

---

# 👤 Member 2 – Foreign Key Generator

### Responsibility

Convert parsed associations into SQL constraints.

### Tasks

Update `schema_generator.py`:

1. For each association:

Add column in child table:

```sql
department_id INT
```

2. Generate constraint:

```sql
FOREIGN KEY (department_id)
REFERENCES Department(id)
```

3. Place constraints inside CREATE TABLE block.

4. Ensure syntax validity.

### Deliverable

Schema example:

```sql
CREATE TABLE Student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department(id)
);
```

---

# 👤 Member 3 – Relationship Validation & SQL Testing

### Responsibility

Ensure relationships are logically valid and SQL-safe.

### Tasks

1. Detect errors like:

* Association with non-existent class
* Circular references
* Duplicate FK columns

2. Run generated `schema.sql` in MySQL.

3. Verify:

* Constraints work
* Tables create successfully

4. Test cases:

* 1:1 relationship
* 1:* relationship
* Multiple associations

### Deliverable

Validation report + SQL execution confirmation.

---

# 👤 Integration Lead (Member 4)

Your job remains **system control and stability**.

### Responsibilities

1. Integrate new association structure into pipeline:

```
XMI
↓
parser
↓
validator
↓
JSON model (with associations)
↓
schema generator
↓
schema.sql with foreign keys
```

2. Define rules for FK naming:

Example:

```
<Class>_id
```

3. Ensure deterministic output again.

4. Run full pipeline tests.

5. Freeze Spiral 3 when stable.


# ⏱ Suggested Timeline

| Day | Task                   |
| --- | ---------------------- |
| 1–2 | Association parsing    |
| 3–4 | Foreign key generation |
| 5–6 | SQL validation         |
| 7   | Integration & testing  |



At that point, our **database layer is fully generated from UML**.

