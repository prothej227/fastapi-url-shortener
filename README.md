# 🚀 FastAPI URL Shortener

A simple and efficient URL shortener built with FastAPI and SQLAlchemy.

## 📌 Features

- Shorten URLs using different strategies (random, hash, custom alias, keyword-based)
- Redirect short codes to original URLs
- Track URL analytics (IP address, user agent)
- Delete short codes and analytics

---

## 🛠️ **Installation**

1. Clone the repository:

```
git clone <YOUR_REPO_URL>
cd <PROJECT_FOLDER>
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Start the server:

```
uvicorn main:app --reload
```

---

## 🔥 **API Endpoints**

### 🔍 **Health Check**

✅ Check if the server is running.  
**GET** `/`  
**Response:**

```
{
  "status": 200,
  "msg": "Server is healthy!"
}
```

---

### 🔗 **Shorten a URL**

✅ Generate a shortened URL with a selected strategy.  
**POST** `/shorten`  
**Request Body:**

```
{
  "original_url": "https://website.com",
  "strategy": "random",
  "custom_code": "my-alias"  // Optional (for custom alias strategy only)
}
```

**Response:**

```
{
  "id": 1,
  "short_code": "abc123",
  "original_url": "https://website.com",
  "created_at": "2025-03-16T12:00:00"
}
```

---

### 🔀 **Redirect to Original URL**

✅ Redirects the user to the original URL using the short code.  
**GET** `/{short_code}`  
**Response:**

- **301 Moved Permanently** → Redirects to the original URL
- **404** → URL not found

---

### 📊 **Get URL Analytics**

✅ Retrieve analytics for a specific short code.  
**GET** `/{short_code}/info`  
**Response:**

```
{
  "short_code": "abc123",
  "original_url": "https://example.com",
  "click_count": 10,
  "last_accessed_at": "2025-03-16T12:00:00"
}
```

---

### 🗑️ **Delete a Short Code**

✅ Remove a short code and its analytics.  
**DELETE** `/{short_code}`  
**Response:**

```
{
  "message": "Analytics deleted for abc123"
}
```

---

## 🛠️ **Environment Variables**

- `.env` file:

```
DATABASE_URL=sqlite:///./database.db
```

---
