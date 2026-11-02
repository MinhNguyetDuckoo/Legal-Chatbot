import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Load biến môi trường
BACKEND_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BACKEND_DIR / ".env")

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "legal_ai")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

async def make_admin(email: str):
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        # Kiểm tra xem user có tồn tại không
        result = await conn.execute(text("SELECT id, role FROM users WHERE email = :email"), {"email": email})
        user = result.fetchone()
        
        if not user:
            print(f"❌ Không tìm thấy tài khoản với email: {email}")
            print("Vui lòng đăng ký tài khoản trên web/app trước, sau đó chạy lại lệnh này.")
        elif user.role == "admin":
            print(f"✅ Tài khoản {email} hiện đã là ADMIN rồi!")
        else:
            # Cập nhật role
            await conn.execute(text("UPDATE users SET role = 'admin' WHERE email = :email"), {"email": email})
            print(f"🎉 Đã nâng cấp thành công tài khoản {email} lên quyền ADMIN!")
    
    await engine.dispose()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python make_admin.py <email_cua_ban>")
        sys.exit(1)
        
    email_to_upgrade = sys.argv[1]
    asyncio.run(make_admin(email_to_upgrade))
