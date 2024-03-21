# Project Name

Note taking app

## Introduction

A demo of a note taking app


## Installation

- create virtual environment
```bash
virtualenv env
```
- activate virtual environment
```bash
source env/bin/activate
```
- Install requirements
```bash
pip install -r requirements.txt
```
## API Endpoints

### Fetch a Note

- **URL:** `/api/notes/{note_id}/`
- **Method:** `GET`
- **Description:** Retrieves a specific note by its ID.
- **Parameters:**
  - `note_id`: ID of the note to retrieve.
- **Response:**
  - **Success:** HTTP 200 OK
    ```json
    {
        "id": 1,
        "title": "Sample Note",
        "content": "This is a sample note.",
        "created_at": "2024-03-21T12:00:00Z",
        "updated_at": "2024-03-21T12:00:00Z"
    }
    ```
  - **Not Found:** HTTP 404 Not Found
    ```json
    {
        "detail": "Note not found."
    }
    ```

### Update a Note

- **URL:** `/api/notes/{note_id}/`
- **Method:** `PUT`
- **Description:** Updates a specific note.
- **Parameters:**
  - `note_id`: ID of the note to update.
  - Request Body:
    ```json
    {
        "title": "Updated Note",
        "content": "This is the updated content."
    }
    ```
- **Response:**
  - **Success:** HTTP 200 OK
    ```json
    {
        "id": 1


### Register

- **URL:** `/api/register/`
- **Method:** `POST`
- **Description:** Creates an account.
- **Parameters:**
  - `user_id`: Automatically generate.
  - `first_name`: First name of the user.
  - `last_name`: Last name of the user.
  - `email`: Email of the user.
  - `password`: Password of the user.

  - Request Body:
    ```json
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "password": "string"
        }
    ```
- **Response:**
  - **Success:** HTTP 201 Created
    ```json
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        }
    ```

