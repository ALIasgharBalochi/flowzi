# 🚀 Flowzi

**Flowzi** is a real-time private messaging platform built with **Django**, **Django Channels**, **WebSocket**, and **JWT Authentication**. This project is currently under active development and aims to be a fast, secure, and scalable communication system for users who value privacy, freedom, and seamless connectivity.

## Features

- 🔒 Secure private chat between users  
- 💬 Real-time messaging with WebSockets  
- 🧪 JWT-based authentication (no session handling)  
- 📁 RESTful APIs built with Django REST Framework  
- 🏗 Modular, scalable backend architecture  
- 🛡 Custom user model for flexibility and privacy  

## Tech Stack

- Backend: Django + Django Channels  
- Real-Time: WebSocket, Redis  
- Auth: JWT (djangorestframework-simplejwt)  
- Database: PostgreSQL / SQLite (dev)  
- Frontend: Not implemented yet (API ready)  
- Deployment: Docker (WIP)  

## Project Structure
flowzi/
├── accounts/ # User models and authentication <br/>
├── link/ # Chat logic and WebSocket consumers <br/>
├── core/ # Project configuration <br/>
├── media/ # Uploaded files (if any) <br/>

## Realtime Chat with WebSocket

Using Django Channels and Redis, each user can establish a WebSocket connection to communicate in real-time. The system uses `AsyncWebsocketConsumer` to handle message broadcasting and saving them to the database.

## JWT Authentication

Authentication is handled using **JSON Web Tokens (JWT)** which ensures stateless, scalable authentication. We're using `djangorestframework-simplejwt`.

## Work in Progress

Flowzi is currently in the **development phase**. We're actively building features like:

- User profile customization  
- Read receipts  
- Typing indicators  
- File sharing in chat  

---

Made with ☕ and a love for backend engineering.
