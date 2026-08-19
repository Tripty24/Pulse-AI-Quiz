# 🚀 Pulse-AI-Quiz

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=vercel)](https://livequiz-app-tawny.vercel.app/)

An interactive, AI-powered quiz application designed to test and expand your knowledge dynamically! Built with Python and modern web technologies, deployed seamlessly on Vercel.

---

## 🎥 Demo Video

[![Watch the demo video]the- https://github.com/user-attachments/assets/96d74362-a290-4484-a0c0-2dd72ea03bed



> *Tip: Record a quick screen recording of your quiz app running live from your Vercel URL, upload it to YouTube or Loom, and replace `YOUR_VIDEO_LINK_HERE` above.*

---

## ✨ Features

- **Dynamic AI Quiz Generation:** Engaging questions tailored for users.
- **Sleek Interface:** Clean and responsive modern UI (`index.html`).
- **Fast Backend:** Powered by Python (`index.py`).
- **Cloud Ready:** Configured for effortless deployment with `vercel.json`.

---

## 📐 Architecture & System Design

The **Pulse-AI-Quiz** follows a modern serverless architecture, separating the frontend interface from the dynamic Python backend logic.

### High-Level Flow

+--------------------+       HTTP Request        +-----------------------+
|                    |  --------------------->   |                       |
|    Web Browser     |                           |     Vercel Edge /     |
|  (User Interface)  |  <---------------------   |   Serverless Backend  |
|     index.html     |        JSON / HTML        |       index.py        |

+--------------------+                           +-----------------------+




### Component Breakdown
| Component | Technology | Role & Responsibility |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JS | Provides the user interface (`index.html`). |
| **Backend Logic** | Python (`index.py`) | Handles quiz generation and processes answers. |
| **Hosting** | Vercel (`vercel.json`) | Manages routing and serverless execution. |
| **Dependencies** | Pip (`requirements.txt`) | Manages Python packages. |



## 🚀 Check It Out Live
Experience the app directly at: https://livequiz-app-tawny.vercel.app/

