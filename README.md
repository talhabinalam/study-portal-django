# Study Portal

## Overview

The **Study Portal** is a comprehensive eLearning platform designed to empower students in managing their academic tasks effectively. The platform allows students to organize notes, assignments, and tasks, while integrating search capabilities for resources like YouTube videos, books, Wikipedia articles, and dictionaries. This project demonstrates a robust and user-friendly system for students, leveraging modern web technologies to create an interactive and efficient learning environment.

---

## Technologies Used

- **Python**: For backend functionality and server-side logic.
- **Django**: The web framework used to structure and handle backend operations.
- **HTML**: For defining the structure and content of the site.
- **CSS**: Styling the website for a clean and professional look.
- **JavaScript**: To enhance interactivity and dynamic features.
- **Bootstrap**: A responsive front-end framework for fast and mobile-friendly design.
- **Crispy Forms**: To create attractive and functional forms with minimal effort.
- **APIs**: Integrating YouTube, book searches, Wikipedia, and dictionary lookups into the platform.
- **SQLite**: Database management for storing user data such as notes, assignments, and tasks.

---

## Features

- **User Authentication**: Secure user registration, login, and logout functionality.
- **Manage Notes**: Students can create, view, update, and delete their notes.
  - View note details with `GET /notes/<int:pk>`.
  - Delete a note with `DELETE /delete_note/<int:pk>`.
- **Assignment and Task Management**: 
  - Add, update, or delete assignments.
  - Track homework with `GET /homework/`.
  - Update homework with `POST /update_homework/<int:pk>`.
  - Delete homework with `DELETE /delete_homework/<int:pk>`.
  - View assignment details with `GET /homework_detail/<int:pk>`.
- **To-Do List Management**:
  - Manage tasks with `GET /todo/`.
  - Update tasks with `POST /update_todo/<int:pk>`.
  - Delete tasks with `DELETE /delete_todo/<int:pk>`.
- **YouTube Search**: Search educational videos from YouTube with `GET /youtube/`.
- **Book Search**: Lookup books relevant to student needs with `GET /books/`.
- **Wikipedia Integration**: Retrieve articles with `GET /wiki/`.
- **Dictionary**: Look up word definitions with `GET /dictionary/`.
- **Unit Conversion**: Convert units for quick academic needs with `GET /conversion/`.
- **Responsive Design**: A mobile-friendly interface built with Bootstrap to ensure accessibility on all devices.

---

## API Endpoints

### Notes
- **Notes Overview**:
  - `GET /notes/`  
  - View all notes.
- **Delete Note**:
  - `DELETE /delete_note/<int:pk>`  
  - Delete a specific note.
- **Note Details**:
  - `GET /note_detail/<int:pk>`  
  - Retrieve details of a specific note.

### Homework
- **View Homework**:
  - `GET /homework/`  
  - Fetch all homework entries.
- **Update Homework**:
  - `POST /update_homework/<int:pk>`  
  - Update details of specific homework.
- **Delete Homework**:
  - `DELETE /delete_homework/<int:pk>`  
  - Delete a specific homework entry.
- **Homework Details**:
  - `GET /homework_detail/<int:pk>`  
  - Fetch details of a specific homework.

### To-Do List
- **View To-Dos**:
  - `GET /todo/`  
  - Fetch all tasks in the to-do list.
- **Update To-Do**:
  - `POST /update_todo/<int:pk>`  
  - Update a specific task.
- **Delete To-Do**:
  - `DELETE /delete_todo/<int:pk>`  
  - Delete a specific task.

### Search and Utilities
- **YouTube Search**:
  - `GET /youtube/`  
  - Search educational videos on YouTube.
- **Book Search**:
  - `GET /books/`  
  - Search for books.
- **Wikipedia Search**:
  - `GET /wiki/`  
  - Search Wikipedia for articles.
- **Dictionary Lookup**:
  - `GET /dictionary/`  
  - Look up word definitions.
- **Unit Conversion**:
  - `GET /conversion/`  
  - Perform unit conversions.

---

## How to Run This Project Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/talhabinalam/study-portal-django.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd study-portal-django
   ```
3. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Create Admin**:
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
7. **Access the application**: Open your browser and navigate to http://127.0.0.1:8000

## Overview:
![image](https://github.com/user-attachments/assets/d65b4b8c-eada-41fc-8799-5ad286a61383)
