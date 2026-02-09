# InventoryAI Web Application (Week 7)

## Overview

During this week, the main focus of the InventoryAI project was the development of the web application interface and its interactive functionality.  
The goal was to create a simple yet professional and secure Streamlit-based web app that allows users to query an inventory database using natural language and receive fast, accurate responses.

This week primarily concentrated on the frontend experience, while the backend logic (vector database retrieval and AI-based question answering) had already been implemented in previous weeks.

---

## Weekly Focus Areas

### 1. Web Application Structure and UI Design

- **Streamlit Framework**  
  The entire frontend was built using Streamlit components, enabling rapid development and easy deployment.

- **Language Selection Support**  
  Users can switch between Hungarian and English, improving accessibility and usability for a wider audience.

- **Modern Styling and Layout**  
  Custom CSS was applied to enhance the appearance of the application, including chat bubbles, backgrounds, buttons, and other UI elements.  
  The result is a clean, modern, and user-friendly design.

- **Sidebar Controls**  
  The sidebar provides additional configuration options, such as setting the number of retrieved results (`top_k`), along with informative text to help users better understand and control the search process.

---

### 2. Interaction and State Management

- After entering a question, users can trigger the query using a dedicated search button.

- Responses are displayed dynamically, character by character, improving the conversational user experience.

- Chat history is presented in a dialogue-style format, making it easier to follow previous questions and answers.

- Conversation state is stored using Streamlit’s `session_state`, ensuring that earlier messages remain visible throughout the session.

---

### 3. Security Considerations

To ensure safe usage, all user-provided and system-generated text is processed with HTML escaping.  
This prevents potential Cross-Site Scripting (XSS) attacks and protects the application from malicious code injection.

---

### 4. Help and Navigation Features

The application also includes an additional help section containing the Óbuda University phone directory.  
This allows users to easily contact different university departments or staff members if further assistance is needed.

---

## Summary

Week 7 was primarily dedicated to building the interactive and visual layer of the InventoryAI system.  
While the backend retrieval and AI response generation pipeline was developed earlier, this week ensured that the full solution is easy to use, secure, and visually appealing through a modern Streamlit-based chat interface.

Future improvements may include additional UI features, authentication, and further performance optimizations.
