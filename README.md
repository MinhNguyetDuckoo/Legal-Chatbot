# ⚖️ Legal AI Chatbot — Tư Vấn Pháp Luật Việt Nam

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)
![LightRAG](https://img.shields.io/badge/LightRAG--HKU-1.4.14-FF6B35?style=flat-square)

**Nền tảng chatbot tư vấn pháp luật Việt Nam thông minh, kết hợp đồ thị tri thức (Knowledge Graph) và tìm kiếm vector (Vector Search) để trả lời chính xác kèm trích dẫn điều luật gốc.**

</div>

---

## 📖 Giới Thiệu

**Legal AI Chatbot** là hệ thống hỏi đáp pháp luật tự động dành riêng cho người dùng Việt Nam. Thay vì tìm kiếm thủ công trong hàng trăm văn bản luật, người dùng chỉ cần đặt câu hỏi bằng ngôn ngữ tự nhiên — hệ thống sẽ phân tích, suy luận và trả lời kèm **nguồn trích dẫn điều khoản cụ thể**.

### Điểm nổi bật:
- 🔍 **Dual-mode RAG**: Kết hợp tìm kiếm **vector (semantic)** và **đồ thị tri thức (graph reasoning)** cho độ chính xác cao nhất
- 📜 **Trích dẫn gốc**: Mỗi câu trả lời đều có liên kết tới điều luật cụ thể trong văn bản pháp luật
- 🧠 **LightRAG-HKU Engine**: Sử dụng kiến trúc RAG nâng cao, tối ưu hóa cho tiếng Việt và dữ liệu pháp lý
- 💬 **Lịch sử hội thoại**: Nhớ ngữ cảnh hội thoại qua Redis session cache
- 🔐 **Xác thực người dùng**: Hệ thống đăng ký/đăng nhập với JWT
- ☁️ **Sẵn sàng Cloud**: Kiến trúc phân tán, dễ dàng deploy lên Hugging Face + Vercel

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────┐
│                     NGƯỜI DÙNG                          │
│              React 19 + Vite + TailwindCSS              │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/REST API
┌─────────────────────▼───────────────────────────────────┐
│                   BACKEND                               │
│              FastAPI (Python 3.10+)                     │
│    ┌──────────┐  ┌──────────┐  ┌───────────────────┐   │
│    │   Auth   │  │  Chat    │  │  Legal Doc Viewer  │  │
│    │  (JWT)   │  │  API     │  │  (BeautifulSoup)   │  │
│    └────┬─────┘  └────┬─────┘  └───────────────────┘   │
│         │             │                                  │
│    ┌────▼─────────────▼──────────────────────────────┐  │
│    │          LightRAG-HKU RAG Engine                 │  │
│    │   ┌─────────────┐    ┌──────────────────────┐   │  │
│    │   │ Vector Store │    │   Knowledge Graph    │   │  │
│    │   │  (Milvus)   │    │      (Neo4j)         │   │  │
│    │   └─────────────┘    └──────────────────────┘   │  │
│    └────────────────────────────────────────────────┘  │
│                                                         │
│    ┌──────────────┐    ┌──────────┐    ┌────────────┐  │
│    │  PostgreSQL  │    │  Redis   │    │   Cohere   │  │
│    │  (Supabase)  │    │(Upstash) │    │  Reranker  │  │
│    └──────────────┘    └──────────┘    └────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| **RAG Engine** | [LightRAG-HKU](https://github.com/HKUDS/LightRAG) v1.4.14 |
| **Vector Database** | Milvus (Zilliz Cloud) / PGVector |
| **Graph Database** | Neo4j (Neo4j Aura Cloud) |
| **Backend** | FastAPI · SQLAlchemy · Alembic · Uvicorn |
| **LLM** | Ollama API (Qwen, LLaMA...) |
| **Reranker** | Cohere Rerank API |
| **Cache & Session** | Redis (Upstash Cloud) |
| **Database** | PostgreSQL (Supabase Cloud) |
| **Frontend** | React 19 · Vite · TailwindCSS · React Router |
| **Containerization** | Docker · Docker Compose |

---

## 📁 Cấu Trúc Dự Án

```
Legal-Chatbot/
├── source_project/
│   ├── backend/                    # FastAPI Server
│   │   ├── app/
│   │   │   ├── api/                # REST API endpoints
│   │   │   ├── core/               # Config, security, JWT
│   │   │   ├── domain/             # Models, schemas
│   │   │   ├── infrastructure/     # DB, Redis, Milvus, Neo4j
│   │   │   ├── services/           # Business logic, RAG pipeline
│   │   │   ├── prompts/            # Prompt templates
│   │   │   └── main.py             # Entry point
│   │   ├── alembic/                # Database migrations
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml      # Postgres + Redis local
│   │   └── requirements.txt
│   │
│   └── frontend/                   # React App
│       ├── src/
│       │   ├── api/                # API client
│       │   ├── components/         # UI components
│       │   ├── pages/              # Chat, Login, Register...
│       │   ├── contexts/           # Auth context
│       │   └── App.jsx
│       ├── package.json
│       └── vite.config.js
│
├── build_database/                 # Scripts xây dựng vector/graph DB
├── finetune_model_embedding/       # Fine-tune embedding model
├── crawler/                        # Thu thập văn bản pháp luật
└── Guide.txt                       # Hướng dẫn chạy local
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Local

### Yêu cầu hệ thống

- **Python** 3.10+
- **Node.js** LTS (18+)
- **Docker Desktop** (đang chạy)
- **Ollama** (tùy chọn — để chạy LLM local)

---

### Bước 1: Clone repo

```bash
git clone https://github.com/MinhNguyetDuckoo/Legal-Chatbot.git
cd Legal-Chatbot/source_project
```

---

### Bước 2: Khởi động Database (Docker)

```bash
cd backend

# Khởi động PostgreSQL + Redis bằng Docker Compose
docker-compose up -d

# Kiểm tra containers đang chạy
docker ps
```

> ✅ Chờ đến khi thấy `Started` cho cả **Postgres**, **pgAdmin** và **Redis**.

---

### Bước 3: Cài đặt & chạy Backend

```bash
cd backend

# Tạo và kích hoạt môi trường ảo
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
# source venv/bin/activate

# Cài thư viện
pip install -r requirements.txt

# Tạo bảng dữ liệu (migrations)
alembic upgrade head

# Chạy server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

📌 API Docs: **http://localhost:8000/docs**

---

### Bước 4: Cài đặt & chạy Frontend

```bash
# Mở terminal mới
cd frontend

npm install
npm run dev
```

📌 Giao diện chat: **http://localhost:3000**

---

### Cấu hình LLM (file `.env`)

Mở `backend/.env` và điền thông tin kết nối:

```env
# === LLM (Ollama local) ===
LLM_MODEL="qwen2.5:7b"
OLLAMA_API_KEY=""
LLM_BASE_URL="http://localhost:11434"

# === Vector DB (Milvus/Zilliz) ===
MILVUS_URI=...
MILVUS_TOKEN=...

# === Graph DB (Neo4j) ===
NEO4J_URI=...
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=...

# === Cache (Redis) ===
REDIS_URI=...

# === Database (PostgreSQL) ===
DATABASE_URL=postgresql+asyncpg://...

# === Reranker (Cohere) ===
COHERE_API_KEY=...
```

---

## ☁️ Triển Khai Cloud (Production)

| Thành phần | Dịch vụ | Ghi chú |
|-----------|---------|---------|
| **PostgreSQL** | [Supabase](https://supabase.com) | Free tier |
| **Redis** | [Upstash](https://upstash.com) | Free tier |
| **Vector DB** | [Zilliz Cloud](https://zilliz.com) | Milvus managed |
| **Graph DB** | [Neo4j Aura](https://neo4j.com/cloud/platform/aura-graph-database/) | Free tier |
| **Backend** | [Hugging Face Spaces](https://huggingface.co/spaces) | Docker SDK |
| **Frontend** | [Vercel](https://vercel.com) | Auto-deploy |

### Deploy Backend lên Hugging Face Spaces

```bash
# Tách thư mục backend thành branch riêng và push
git subtree split --prefix=source_project/backend -b deploy-backend
git push huggingface deploy-backend:main --force
git branch -D deploy-backend
```

### Deploy Frontend lên Vercel

1. Import repo từ GitHub vào Vercel
2. Đặt **Root Directory**: `source_project/frontend`
3. Thêm biến môi trường: `VITE_API_BASE_URL=<URL Hugging Face Space>`
4. Bấm **Deploy** ✅

---

## 🤝 Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repo này
2. Tạo branch mới: `git checkout -b feature/ten-tinh-nang`
3. Commit thay đổi: `git commit -m "feat: mô tả ngắn gọn"`
4. Push branch: `git push origin feature/ten-tinh-nang`
5. Tạo Pull Request

---

## 📄 Giấy Phép

Dự án được phân phối dưới giấy phép **MIT**. Xem chi tiết tại [LICENSE](LICENSE).

---

<div align="center">
  <sub>Made with ❤️ for Vietnamese Legal Community</sub>
</div>