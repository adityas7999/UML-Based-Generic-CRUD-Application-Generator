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

* ✅ Parses UML 2.x XMI files
* ✅ Extracts `uml:Class` elements
* ✅ Resolves `ownedAttribute` types (direct & referenced)
* ✅ Identifies `uml:Association` relationships
* ✅ Handles multiplicity (1:1, 1:*, default omitted cases)
* ✅ Supports inheritance (`generalization`)
* ✅ Generates structured internal representation (JSON-ready)

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



