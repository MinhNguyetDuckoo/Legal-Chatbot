# LightRAG Vietnamese Legal AI Platform

**Vietnamese Legal AI Chatbot** - Nền tảng tư vấn pháp luật thông minh sử dụng kiến trúc đồ thị tri thức kết hợp vector (RAG nâng cao). Dự án tích hợp các dữ liệu luật pháp Việt Nam để phân tích thực thể, suy luận liên kết và đưa ra phản hồi chính xác kèm theo nguồn trích dẫn điều luật gốc.

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

*   **RAG Engine:** [LightRAG-HKU](https://github.com/HKU-RAG/LightRAG) (Phiên bản nâng cấp tối ưu hóa cho Graph & Vector).
*   **Vector Database:** Milvus (Zilliz Cloud) & PGVector.
*   **Graph Database:** Neo4j (Neo4j Aura Cloud).
*   **Backend:** FastAPI (Python 3.10+), SQLAlchemy, Alembic.
*   **Cache & Session History:** Redis (Upstash Redis Cloud).
*   **Database chính & Logs:** PostgreSQL (Supabase Cloud).
*   **LLM & Reranker:** Ollama API (Rotating Keys) & Cohere Rerank API.
*   **Frontend:** React 18, Vite, TailwindCSS.

---

## 💻 Hướng Dẫn Chạy Cục Bộ (Local Setup)

### 1. Cấu hình file môi trường
Tạo file `.env` bên trong thư mục `backend/` dựa trên file `.env.example` hoặc tham khảo cấu hình kết nối local của bạn.

### 2. Cấu hình & Chạy Backend
```bash
cd backend

# Tạo và kích hoạt môi trường ảo (Windows)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Đối với macOS/Linux
# source venv/bin/activate

# Cài đặt thư viện phụ thuộc
pip install -r requirements.txt

# Khởi tạo các bảng dữ liệu qua migrations
alembic upgrade head

# Chạy server development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Cấu hình & Chạy Frontend
```bash
cd frontend

# Cài đặt các thư viện
npm install

# Khởi chạy giao diện nhà phát triển
npm run dev
```
Giao diện Chat: [http://localhost:3000](http://localhost:3000)

---

## 🚢 Hướng Dẫn Triển Khai Lên Cloud (Production Deployment)

Dự án đã được cấu hình sẵn sàng để deploy phân tán trên hạ tầng Cloud:

### 1. Database chính & Audit Logs (Supabase)
1. Đăng ký tài khoản và tạo cơ sở dữ liệu Postgres miễn phí trên [Supabase](https://supabase.com/).
2. Sao lưu dữ liệu ở local và khôi phục (restore) lên Supabase để giữ lại tài khoản người dùng cùng cache KV của LightRAG:
   ```bash
   # Bước A: Xuất file backup từ container Docker local
   docker exec -i legal_ai_postgres pg_dump -U admin -d legal_ai_audit > d:\legal_ai_audit_backup.sql
   
   # Bước B: Nhập dữ liệu vào Supabase bằng PowerShell (Cung cấp mật khẩu Supabase)
   $env:PGPASSWORD="[mật-khẩu-của-bạn]"
   psql -h aws-1-ap-southeast-1.pooler.supabase.com -U postgres.oazjemplvjaqjqacpasn -d postgres -f d:\legal_ai_audit_backup.sql
   ```

### 2. Session Cache (Upstash Redis)
1. Đăng ký tài khoản miễn phí trên [Upstash](https://upstash.com/) và tạo cơ sở dữ liệu Redis mới.
2. Lấy Connection URI định dạng `rediss://...` (lưu ý bật cổng kết nối bảo mật `rediss://` để kết nối an toàn).

### 3. Backend (Hugging Face Spaces - Docker SDK)
1. Tạo một **Space** mới trên Hugging Face, chọn SDK là **Docker** và Template là **Blank**.
2. Thêm tất cả cấu hình kết nối từ `.env` vào mục **Settings -> Variables and secrets** của Space (như `DATABASE_URL` trỏ về Supabase và `REDIS_URI` trỏ về Upstash).
3. Đẩy code của thư mục `backend/` lên Space bằng lệnh `git subtree`:
   ```bash
   git subtree split --prefix=backend -b deploy-backend
   git push huggingface deploy-backend:main --force
   git branch -D deploy-backend
   ```
4. Hugging Face sẽ tự động build image dựa trên file `backend/Dockerfile` và phơi cổng `7860`.

### 4. Frontend (Vercel)
1. Import dự án của bạn từ GitHub vào [Vercel](https://vercel.com/).
2. Cấu hình **Root Directory** là `legal_ai_platform/frontend`.
3. Điền biến môi trường:
   * `VITE_API_BASE_URL`: Link Space backend trên Hugging Face của bạn.
4. Bấm **Deploy**. Vercel sẽ tự động build và cung cấp tên miền miễn phí.
