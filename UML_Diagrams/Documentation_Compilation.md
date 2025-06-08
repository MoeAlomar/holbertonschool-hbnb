# HBnB Evolution: Technical Documentation

## Introduction

The HBnB project is a simplified version of an AirBnB-like application, designed to manage user accounts, property listings, reviews, and amenities. This technical documentation serves as a comprehensive blueprint for the HBnB system, providing a detailed reference for its architecture, design, and interactions. The document is intended to guide developers through the implementation phases, ensuring alignment with the project’s requirements and best practices.

### This document includes:

- High-Level Architecture: An overview of the system’s layered structure and communication patterns.

- Business Logic Layer: A detailed view of the core entities and their relationships.

- API Interaction Flow: Sequence diagrams illustrating key interactions between system components

--- 

## High-Level Architecture

The HBnB application is structured using a three-layer architecture, designed to separate concerns and enhance modularity. This section presents the high-level package diagram, illustrating the organization of the application’s components across the Presentation Layer, Business Logic Layer, and Persistence Layer, with communication facilitated by the facade pattern.

## 📊 Package Diagram

Below is the high-level package diagram created using Mermaid.js, showcasing the three layers, their key components, and their dependencies:

![IMG_20250604_130944_008(1)](https://github.com/user-attachments/assets/8a2b7574-bb6c-4a8a-81f4-482a1f3f2270)

## 📝 Explanatory Notes

The package diagram represents the high-level structure of the HBnB application, a simplified AirBnB-like system. Each layer has distinct responsibilities, and the facade pattern is employed to streamline communication between them. Below is a detailed breakdown:

### Presentation Layer

Purpose: Manages all user-facing interactions.

Components:

1. User Interface: The front-end (e.g., web or mobile interface) where users interact with the application.
2. API Endpoints: RESTful services that handle external requests and responses.
3. Presentation Facade: Acts as the unified interface to the Business Layer, managing cross-cutting concerns like security and load balancing.

Interactions: Users access the system via the User Interface, which communicates with API Endpoints. The Presentation Facade then routes requests to the Business Layer.

### Business Logic Layer

Purpose: Encapsulates the core functionality and business rules of the application.

Components:

1. Models: Represent the entities such as User, Place, Review, and Amenity.
2. Services: Implement operations like user management, property listing, and review processing (e.g., UserService, PlaceService).

Interactions: Services depend on Models for data representation and communicate with the Persistence Layer via the Persistence Facade.

Persistence Layer

Purpose: Handles data storage, retrieval, and management.

Components:

1. Persistence Facade: Abstracts database operations, providing a simplified interface for the Business Layer.
2. Repositories: Manage specific data access logic for each entity.
3. DBMS Connection: Interfaces with the database management system.

Data Replication: Ensures data redundancy and availability.

Interactions: The Persistence Facade receives requests from the Business Layer, delegating them to Repositories, which interact with the DBMS Connection and Data Replication.

### Facade Pattern

Role: Simplifies interlayer communication by providing a single entry point per layer.

Implementation:

- The Presentation Facade connects the Presentation Layer to the Business Layer, routing requests to the appropriate Services.
- The Persistence Facade abstracts data operations, allowing the Business Layer to perform CRUD (Create, Read, Update, Delete) tasks without direct database interaction.

Benefits: Enhances modularity, reduces coupling, and improves maintainability.



## 🛠 Design Decisions

Layered Architecture: Chosen to separate concerns, making the system scalable and easier to maintain.

Facade Pattern: Adopted to abstract complex interactions, ensuring each layer remains independent yet interoperable.

Component Placement: External users are shown outside the layers, emphasizing their role as actors interacting with the system via the Presentation Layer.

This high-level architecture provides a clear foundation for the HBnB application, guiding subsequent design and implementation phases.

---

## Business Logic Layer

The Business Logic Layer forms the heart of the HBnB application, encapsulating the essential entities and their interactions. This section presents a detailed class diagram, illustrating the structure of the key entities—User, Place, Review, and Amenity—along with their attributes, methods, and relationships.

## 📊 Class Diagram

Below is the detailed class diagram for the Business Logic Layer, created using Mermaid.js. It showcases the entities, their properties, operations, and how they relate to one another:

![Class_Diagram](https://github.com/user-attachments/assets/f0c9111f-07b6-4523-901c-24d5ca6f00b3)


## 📝 Explanatory Notes

The class diagram represents the internal structure of the Business Logic Layer, focusing on the core entities that drive the HBnB application’s functionality. Each entity is designed with attributes and methods that reflect their roles and interactions within the system.

### Entities and Their Roles:

- ### User:

- Role: Represents a user of the application, who can be either a regular user or an administrator.
- Attributes: Includes personal details (first_name, last_name, email, password), a role flag (is_admin), and audit timestamps (created_at, updated_at).
- Methods: Supports user registration (register), profile updates (updateProfile), deletion (delete), and management of owned places (getPlaces, addPlace).

### Place:

- Role: Represents a property listing created by a user, which can have associated amenities and reviews.
- Attributes: Includes descriptive details (title, description, price, latitude, longitude), references to the owner (owner), a list of amenities (amenities), and audit timestamps.
- Methods: Facilitates place creation (create), updates (update), deletion (delete), listing (list), and management of amenities and reviews (addAmenity, getReviews).

### Review:

- Role: Represents a user’s feedback on a place, including a rating and comment.
- Attributes: Contains the review content (rating, comment), references to the user and place (user, place), and audit timestamps.
- Methods: Allows review creation (create), updates (update), deletion (delete), and listing by place (listByPlace).

### Amenity:

- Role: Represents a feature (e.g., Wi-Fi, pool) that can be associated with multiple places.
- Attributes: Includes details (name, description) and audit timestamps.
- Methods: Supports amenity creation (create), updates (update), deletion (delete), listing (list), and retrieval of associated places (getPlaces).

Relationships





User-Place (1 to 0..*): A user can own multiple places, while each place is owned by one user.



Place-Amenity (0.. to 0..*)*: A many-to-many relationship where a place can have multiple amenities, and an amenity can be associated with multiple places.



Review-User (0.. to 1)*: Multiple reviews can be written by a single user.



Review-Place (0.. to 1)*: Multiple reviews can be associated with a single place.

These relationships are depicted using UML associations with appropriate multiplicity, ensuring the diagram accurately reflects the system’s business logic.

Design Decisions





Unique Identifiers: Each entity includes a String id attribute (UUID4) for unique identification.



Timestamps: created_at and updated_at attributes are included for auditing purposes.



Methods with Parameters: Methods like register and create take parameters to explicitly define the data required for entity creation, enhancing clarity.



Relationship Management: Methods such as addPlace and addAmenity are included to manage associations between entities, providing a clear interface for interaction.

This class diagram serves as a blueprint for the Business Logic Layer, ensuring that the core entities and their interactions are well-defined and aligned with the project’s requirements.



API Interaction Flow

To be completed with the Sequence Diagrams for API calls and explanatory notes.

