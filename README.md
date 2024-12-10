Email Dashboard 📧
==================

This is a web-based email dashboard that integrates Generative AI powered by OpenAI to provide functionalities like generating email responses and summarizing emails. The dashboard allows users to search emails, toggle between dark mode and light mode, and interact with email categories like Inbox, Spam, Sent, and Drafts. The project also includes OAuth for secure user authentication.

Features
--------

-   **Email Display**: Shows emails with subject, sender, and body preview.

-   **Generative AI**: Uses OpenAI to generate responses for emails.

-   **Email Summarization**: Summarizes the email content using AI.

-   **Search Functionality**: Search emails by subject or sender.

-   **Dark Mode**: Toggle between light and dark themes for better readability.

-   **Category Management**: Mark emails with categories like Inbox, Spam, Sent, and Drafts.

-   **OAuth Authentication**: Secure user authentication using OAuth for accessing the email data.

Tech Stack
----------

-   **Frontend**: HTML, CSS, JavaScript

-   **Backend**: Python, FastAPI

-   **AI Integration**: OpenAI API (Generative AI for email responses and summarization)

-   **OAuth Authentication**: Secure login via OAuth for accessing email data.

-   **Environment**: Conda (Python 3.10)

Requirements
------------

### Conda Environment Setup

1.  Create a Conda environment with Python 3.10:

    bash

    ```
    conda create --name email-dashboard python=3.10
    conda activate email-dashboard

    ```

2.  Install required dependencies:

    bash

    ```
    pip install -r requirements.txt

    ```

Ensure you have your OpenAI API key to integrate the AI functionalities.

Backend (FastAPI)
-----------------

The backend is powered by FastAPI, which serves the AI models for generating responses and summarizing emails. It also handles OAuth authentication to ensure that only authorized users can access the email data.

Install FastAPI, OAuth, and other dependencies:

bash

```
pip install fastapi uvicorn openai python-dotenv

```

You can start the backend server using:

bash

```
uvicorn app:app --reload

```

OAuth Authentication
--------------------

-   **OAuth Setup**: To secure access to email data, OAuth is used for authentication. The backend will handle user logins via OAuth providers (e.g., Google, Microsoft) and ensure secure access to email data.

-   **OAuth Credentials**: You need to configure your OAuth credentials (client ID, client secret) in the `.env` file for the application to function correctly.

Frontend (HTML, CSS, JavaScript)
--------------------------------

The frontend is built using HTML, CSS, and JavaScript for rendering the dashboard interface and interacting with the backend.

OAuth Authentication Flow
-------------------------

-   **Login via OAuth**: When a user tries to access the email dashboard, they are prompted to log in using an OAuth provider (e.g., Google). This ensures that only authorized users can access the dashboard.

-   **Token Validation**: Once logged in, the backend validates the OAuth token to verify the user's identity before granting access to email data.

-   **Secure API Access**: All communication between the frontend and backend is secured through OAuth tokens, ensuring that user data is protected.

Usage
-----

1.  **Start the backend**: Run the FastAPI server.

    bash

    ```
    uvicorn app:app --reload

    ```

2.  **Authenticate via OAuth**: Users will be prompted to log in using their OAuth provider (e.g., Google).

3.  **Access the frontend**: After successful authentication, users can open the `index.html` file in a browser.

4.  **Toggle Dark Mode**: Use the Dark Mode toggle on the top right corner to switch between light and dark themes.

5.  **Generate Responses**: Click "📝 Generate Response" to get an AI-generated reply to the email.

6.  **Summarize Emails**: Click "📑 Summarize Email" to generate a brief summary of the email.

Screenshots
-----------

Here are some screenshots of the email dashboard in different modes:



### Light Mode
![Light Mode](images/Screenshot%202024-12-11%20034251.png)

### Dark Mode
![Dark Mode](images/Screenshot%202024-12-11%20034239.png)

### View Full Body
![View Full Body](images/Screenshot%202024-12-11%20034339.png)

### Generated Response
![Generated Response](images/Screenshot%202024-12-11%20034426.png)

### Summary
![Summary](images/Screenshot%202024-12-11%20034448.png)