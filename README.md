# Common test project

> Development of a microservice for transaction management.

Task description:

To develop a microservice that provides a REST API for performing basic operations with financial transactions.

Requirements for implementation:

* Programming language: Python 3.10+

* Database: MySQL or PostgreSQL using SQLAlchemy.

* Framework: Facetapi or Flask.

* Containerization: Docker.

* Queues: Celery for a background task, Redis or RabbitMQ for a message broker.

* Testing: Pytest or Unittest.

Execution Steps:

1. Creating a data model:

    • Create a transaction model with the fields: id, amount, currency, timestamp, description.

2. API Implementation:

    • Implement CRUD operations for transactions (create, read, update, delete).

3. Background task:

    • Create a task to send an email notification about a new transaction using Celery and SMTP. Email can be set via environment variables.

4. Containerization:

    • Prepare the Dockerfile and configure docker-compose.yml for launching the application and database.

5. Testing:

    • Write simple tests for CRUD operations using Pytest or Unittest.

6. Documentation:

    • Prepare documentation for the endpoint API using Swagger.

---
> notes on source of project:

* Poetry used for managment.

* Some points:

  * To create db tables, from root project direcrory run `app/scripts/create_db_tables.py`

  * For export dependencies `poetry export -f requirements.txt --output app/requirements.txt`
