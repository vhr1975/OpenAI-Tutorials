# 📂 GitHub Project Guidelines (for Portfolio Showcases)

## 🎯 Role & Context

This repo is part of a **showcase portfolio** that highlights projects using **OpenAI APIs, modern frontend frameworks, and backend services**. The goal is to present code that is:

* **Clean and maintainable**
* **Secure and production-ready**
* **Easy for other developers to understand and reproduce**

---

## ✨ Code Style Guidelines

### General

* Use **clear, descriptive names** for variables, functions, and components.
* Follow **PEP 8** for Python code.
* Use **TypeScript** for React/Next.js components.
* Always add **type hints** in Python.
* Document public functions, classes, and APIs with concise docstrings or JSDoc.

---

### Python Example

```python
async def get_status() -> dict:
    """Return service health status."""
    return {"status": "healthy", "version": "1.0.0"}
```

### React/TypeScript Example

```typescript
interface StatusProps {
  message: string;
}

const StatusBanner: React.FC<StatusProps> = ({ message }) => {
  return <div className="status-banner">{message}</div>;
};
```

---

## 📁 Project Structure

Keep repos consistent for clarity:

```
project-name/
├── backend/             # Python FastAPI service (or Azure Functions equivalent)
│   ├── app/
│   ├── tests/
│   └── requirements.txt
└── frontend/            # React or Next.js frontend
    ├── src/
    └── package.json
```

* **Backend** → API endpoints, business logic, tests.
* **Frontend** → UI components, hooks, pages, tests.
* **Docs** → README, setup guides, and deployment instructions.

---

## 🧪 Testing Requirements

* Write **unit tests** for all backend endpoints and core functions.
* Cover both **success and error cases**.
* Backend → use **pytest**.
* Frontend → use **React Testing Library** or **Jest**.

---

## 🔒 Security Guidelines

* **Never commit secrets** (use `.env` + `.gitignore`).
* Use **environment variables** for configuration (API keys, endpoints).
* Apply **CORS best practices**.
* Validate all **input data** (backend + frontend forms).
* For OpenAI integrations, always **hide API keys** behind a backend proxy.

---

## 🚀 Deployment

* Containerize with **Docker** for reproducibility.
* Backend deployment options:

  * **Azure Functions** (Python) for serverless API demos.
  * **Cloudflare Workers** (JS) for lightweight edge APIs.
* Frontend deployment options:

  * **Azure Static Web Apps** or **Cloudflare Pages**.
  * **Vercel** for Next.js/React.
* Use **GitHub Actions** for CI/CD workflows (build, test, deploy).

---

## 📖 Documentation

Each project should include:

* **README.md** with:

  * Project overview
  * Architecture diagram
  * Setup instructions (local + deployment)
  * Example API requests/responses
* **Demo link** (if deployed).
* **Screenshots or short GIF/video** of the app in action.

Also review the for the openai dev role requirements 