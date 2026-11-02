import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv()

from app.core.config import settings
from app.services.lightrag_orchestrator import LightRAGOrchestrator

async def main():
    print("🚀 Đang khởi tạo hệ thống...")
    
    # Sử dụng nguyên bộ cấu hình chuẩn của bạn
    orchestrator = LightRAGOrchestrator()
    await orchestrator.initialize()
    
    rag = orchestrator.rag
    
    json_path = "custom_kg_full.json"
    
    if not os.path.exists(json_path):
        print(f"❌ KHÔNG TÌM THẤY FILE: Hãy đảm bảo bạn đã copy file '{json_path}' vào thư mục backend!")
        return

    print("📖 Đang đọc file custom_kg_full.json...")
    with open(json_path, "r", encoding="utf-8") as f:
        kg_data = json.load(f)

    print(f"✅ Đã tải: {len(kg_data.get('chunks', []))} Chunks, {len(kg_data.get('entities', []))} Entities, {len(kg_data.get('relationships', []))} Relations")
    print("⏳ Đang nạp toàn bộ vào Postgres, Milvus và Neo4j (Quá trình này không tốn API, vui lòng chờ khoảng 2-5 phút)...")
    
    # Nạp dữ liệu tĩnh (không tốn tiền gọi LLM)
    await rag.insert_custom_kg(kg_data)
    
    print("🎉 HOÀN TẤT NẠP DỮ LIỆU! Bây giờ bạn có thể bật server FastAPI lên và chat bình thường.")

if __name__ == "__main__":
    asyncio.run(main())
