# Microservices Application

## 1. Overview

This application contains three independent microservices:

- **Frontend:** Provides a web page where users can create and view messages.
- **Backend:** Receives messages, stores them in a JSON file, and sends notification requests.
- **Notification:** Receives notification requests from the backend and records them in a log file.

The services communicate with each other over HTTP. The application does not use a database.

## 2. Project Structure

```text
.
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
 ── notification/
    ├── app.py
    ├── requirements.txt
    └── Dockerfile

```

## 3. How the Services Work Together

```text
User / Browser
      |
      v
Frontend (port 3000)
      |
      | HTTP requests to the backend
      v
Backend (port 5000)
      |
      +---- Saves messages to messages.json
      |
      +---- Sends notification requests
                         |
                         v
                Notification (port 5001)
                         |
                         +---- Records notifications in a log file
```

Typical request flow:

1. A user opens the frontend and views the message list.
2. The frontend requests the existing messages from the backend.
3. When the user submits a message, the frontend sends it to the backend.
4. The backend saves the message in its JSON data file.
5. The backend sends a notification request to the notification service.
6. The notification service records the received message in its log file.
7. The frontend retrieves the messages from the backend and displays them.

The backend saves a message before attempting to send its notification. Therefore, a notification failure does not prevent the message from being stored.

## 4. Frontend Service

### Purpose

The frontend provides the user interface. Users can:

- View previously submitted messages.
- Submit new messages.
- Refresh the page to see the latest messages.
- See an error message if the backend is unavailable.

### Technology

- Python
- Flask
- Requests

### Listening Port

- **Port:** `3000`
- **Protocol:** HTTP

The application listens on port `3000` inside its runtime environment.

### Environment Variables

| Variable | Example | Description |
|---|---|---|
| `BACKEND_URL` | `http://backend:5000` | Base URL used to communicate with the backend. |

The frontend uses `BACKEND_URL` to retrieve messages and submit new ones. The hostname in the URL must be resolvable and reachable from the frontend's runtime environment.

### Backend API Calls

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/messages` | Retrieve all stored messages. |
| `POST` | `/messages` | Submit a new message. |

### Logging

The frontend writes errors, such as failed backend requests, through Python's standard logging output. It does not write a dedicated application log file.

## 5. Backend Service

### Purpose

The backend implements the application's main logic. It:

- Accepts and validates messages.
- Stores messages in a JSON file.
- Returns stored messages to the frontend.
- Sends notification requests to the notification service.
- Records application events and errors.

### Technology

- Python
- Flask
- Requests

### Listening Port

- **Port:** `5000`
- **Protocol:** HTTP

### Environment Variables

| Variable | Example | Description |
|---|---|---|
| `NOTIFICATION_URL` | `http://notification:5001/notify` | Full URL used to send requests to the notification service. |

The notification service hostname must be resolvable and reachable from the backend's runtime environment.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Returns the backend health status. |
| `GET` | `/messages` | Returns all stored messages as JSON. |
| `POST` | `/messages` | Validates and stores a new message. |

### Application Data

The backend stores messages in:

```text
/app/data/messages.json
```

Example contents:

```json
[
  "Hello Docker",
  "Learning microservices"
]
```

Each new message is added to the list and saved to the file. This is file-based storage; the application does not use a database.

### Logging

The backend writes application logs to:

```text
/app/logs/backend.log
```

Log entries include message retrieval, successful message creation, successful notification requests, notification failures, and errors reading stored messages.

## 6. Notification Service

### Purpose

The notification service receives requests from the backend and records the notifications. In this application, notification delivery is simulated: it does not send real emails, SMS messages, or push notifications.

### Technology

- Python
- Flask

### Listening Port

- **Port:** `5001`
- **Protocol:** HTTP

### Environment Variables

The notification service does not require any custom environment variables in the current implementation. The backend specifies the destination URL through its `NOTIFICATION_URL` variable.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Returns the notification service health status. |
| `POST` | `/notify` | Receives a message and records it in the application log. |

### Logging

The notification service writes its application logs to:

```text
/app/logs/notification.log
```

Log entries include notification messages received from the backend.

## 7. Ports Summary

| Service | Listening Port | Purpose |
|---|---:|---|
| Frontend | `3000` | Web interface |
| Backend | `5000` | Message processing and storage |
| Notification | `5001` | Notification request handling |

These are the ports on which the applications listen. How each port is exposed or reached depends on the deployment environment.

## 8. Environment Variables Summary

| Service | Variable | Example Value | Used For |
|---|---|---|---|
| Frontend | `BACKEND_URL` | `http://backend:5000` | Calling the backend API |
| Backend | `NOTIFICATION_URL` | `http://notification:5001/notify` | Sending notification requests |
| Notification | None | Not required | No custom environment variable is used |

The hostnames `backend` and `notification` are examples of service names. They must resolve to the corresponding services in the environment where the application runs. Inside an application process, `localhost` refers to that same runtime environment, not automatically to another microservice.

## 9. Data and Log Paths Summary

| Service | Path | Purpose |
|---|---|---|
| Frontend | Standard output/error | Frontend error messages |
| Backend | `/app/data/messages.json` | Stored application messages |
| Backend | `/app/logs/backend.log` | Backend application logs |
| Notification | `/app/logs/notification.log` | Notification service logs |

Application data and logs are kept in separate paths. The actual persistence of these files depends on how the services are deployed and how their filesystem paths are managed.

## 10. Important Notes

- The three services are separate applications with distinct responsibilities.
- The frontend calls the backend; it does not call the notification service directly.
- The backend calls the notification service after saving a message.
- The notification service simulates notification handling by writing log entries.
- The frontend uses standard logging output; the backend and notification service write dedicated log files.
- Service URLs and hostnames must be configured so that each caller can reach the destination service.
