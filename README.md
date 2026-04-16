# UML-Based-Generic-CRUD-Application-Generator
Automated UML Class Diagram (XMI) parser that generates backend-ready models, relationships, and schema structures.

## 🚀 Overview 

This project implements an automated system that converts **UML Class Diagrams (XMI format)** into backend-ready code structures.

The system parses UML 2.x XMI files exported from tools like **StarUML** and extracts:

* Classes
* Attributes
* Primitive data types
* Associations
* Inheritance relationships

The extracted structural model is then transformed into backend artifacts such as:

* Database schema definitions
* Model representations
* CRUD API scaffolding (extensible design)

---

## 🎯 Problem Statement

Software development often requires manually translating UML designs into:

* Database tables
* Backend models
* API endpoints

This process is repetitive, error-prone, and time-consuming.

This project automates the structural transformation of UML class diagrams into executable backend code structures.

---

## 🧠 Key Features

* ✅ Parses UML 2.x XMI files to extract Classes, Attributes, and Types.
* ✅ Smart Primary Key detection (Dynamically identifies `id`, `courseId`, etc.).
* ✅ Identifies `uml:Association` relationships and maps Foreign Keys perfectly.
* ✅ **Web GUI:** Includes a local web interface to upload XMI files and download a compiled `.zip` backend.
* ✅ **Full REST API Auto-Generation:** Instantly generates routing, JSON validation, and error handling.
* ✅ **Interactive Documentation:** Auto-generates Flasgger (Swagger UI) specs based on your UML attributes.

---

## 🏗 Architecture Overview

1. **Input:** UML Class Diagram (XMI 2.x)
2. **Parser Layer:** Extract structural elements
3. **Model Resolver:** Resolve ID-based type references
4. **Transformation Layer:** Map UML structure to backend schema
5. **Output:** Generated backend components

---

## 📂 Supported UML Constructs

| UML Construct       | Supported        |
| ------------------- | ---------------- |
| Classes             | ✔                |
| Attributes          | ✔                |
| Primitive Types     | ✔                |
| Associations        | ✔                |
| Multiplicity        | ✔                |
| Inheritance         | ✔                |
| Behavioral Diagrams | ✘ (Out of Scope) |

---

## 📦 Example Use Case

A UML class diagram containing:

* Person (Base Class)
* Student (inherits Person)
* Course
* Enrollment (1:* relationship)

Can automatically generate:

* SQL schema
* Model classes
* Relationship mappings

---

## 🛠 Technology Stack

* UML 2.x (XMI)
* XML Parsing
* Backend Language (C++ / Python – configurable)
* JSON intermediate model

---

## 📈 Development Model

This project follows the **Spiral Model**, emphasizing:

* Risk identification (XMI structural variations)
* Iterative parsing refinement
* Controlled feature expansion

---

## 🔍 Future Scope

* GUI upload interface
* Support for additional UML tools
* Behavioral diagram interpretation
* Full REST API auto-generation
* ORM integration

---

## 📚 Academic Context

Developed as part of a structured software engineering project focusing on:

* Model-driven development
* Automated code generation
* UML structural analysis

## 📦 Quick Start

1. Clone the repository and install requirements: `pip install flask flasgger mysql-connector-python jinja2`
2. Run the generator interface: `python web_ui.py`
3. Open `http://127.0.0.1:8080` in your browser.
4. Upload your StarUML `.xmi` file and click **Generate**.
5. Extract your downloaded `.zip` file and follow the instructions in the included Manual!

For detailed step-by-step instructions on designing your UML and deploying the generated API, please see the [USER_MANUAL.md](USER_MANUAL.md).

