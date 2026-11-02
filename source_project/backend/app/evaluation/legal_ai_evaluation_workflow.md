# Luồng Đánh Giá RAGAS - Legal AI Platform

Tài liệu này mô tả quy trình đánh giá của script [eval_legal_rag.py](eval_legal_rag.py) trong backend. Mục tiêu là kiểm tra chất lượng hệ thống RAG theo từng câu hỏi mẫu, sau đó tổng hợp thành báo cáo JSON/CSV.

## Mục tiêu của quy trình

Quy trình này trả lời 4 câu hỏi chính:

1. Câu trả lời của hệ thống có đúng với context không?
2. Context retrieve có đủ thông tin để trả lời không?
3. Context có sạch hay bị nhiễu nhiều không?
4. Câu trả lời có bám đúng câu hỏi không?

## Kiến trúc thực thi

Script evaluation chạy như một process độc lập và gọi thẳng vào backend, không đi qua HTTP API.

So sánh nhanh:

- API thông thường: `client -> FastAPI -> LightRAGOrchestrator -> databases`
- Evaluation script: `python -m app.evaluation.eval_legal_rag -> LightRAGOrchestrator -> databases -> RAGAS`

> [!IMPORTANT]
> - Web server FastAPI không bắt buộc phải chạy.
> - Milvus, Neo4j, PostgreSQL và endpoint LLM/embeddings phải sẵn sàng.

## Điều kiện trước khi chạy

Trước khi đánh giá, cần có:

1. File `.env` trong backend với các biến môi trường cho LLM, embeddings và database.
2. Dataset test dạng JSON, mặc định là `legal_test_dataset.json`.
3. Hệ thống storage và model đã sẵn sàng để `LightRAGOrchestrator` khởi tạo thành công.

## Luồng chạy tổng quát

### 1. Khởi tạo

1. Load biến môi trường từ `.env`.
2. Khởi tạo judge LLM bằng `ChatOpenAI` compatible client.
3. Nếu có thể, khởi tạo embeddings cho metric `Answer Relevancy`.
4. Tải dataset test từ file JSON.
5. Tạo thư mục `results/` để lưu báo cáo.

### 2. Chạy từng test case

Với mỗi dòng trong dataset, script thực hiện 2 bước.

#### Bước 1: sinh câu trả lời RAG

Script gọi trực tiếp:

```python
result = await rag_orchestrator.query(
    message=question,
    mode="mix",
    history=[],
    stream=False,
)
```

Sau đó trích xuất:

- `answer`: câu trả lời do hệ thống sinh ra
- `contexts`: nội dung các chunk đã retrieve
- `entities_count`, `relations_count`, `chunks_count`: số liệu phụ trợ để quan sát chất lượng truy xuất

Nếu không có context nào được retrieve, case đó sẽ bị bỏ qua phần RAGAS và nhận điểm 0.

#### Bước 2: chấm bằng RAGAS

Script tạo một `Dataset` với các cột:

- `question`
- `answer`
- `contexts`
- `ground_truth`

Sau đó gọi `evaluate(...)` của RAGAS để tính các metric.

## Các metrics được tính như thế nào

### Faithfulness

Đo mức độ câu trả lời bám vào context đã retrieve.

Ý nghĩa thực tế:

- cao: answer không bịa ngoài context
- thấp: answer có dấu hiệu suy diễn hoặc hallucination

### Context Recall

Đo context retrieve có chứa đủ thông tin để trả lời ground truth hay không.

Ý nghĩa thực tế:

- cao: hệ thống retrieve được đúng phần cần thiết
- thấp: thiếu tài liệu quan trọng

### Context Precision

Đo độ sạch của context.

Ý nghĩa thực tế:

- cao: context liên quan nhiều, ít nhiễu
- thấp: context trả về nhiều phần không hữu ích

### Answer Relevancy

Đo mức độ câu trả lời liên quan trực tiếp đến câu hỏi.

Metric này chỉ chạy khi embeddings khởi tạo được. Nếu embeddings không khả dụng, metric này bị bỏ qua.

## RAGAS dùng gì để chấm

RAGAS không tự tính toàn bộ bằng công thức cố định trong script. Nó dùng:

- LLM judge cho các metric cần suy luận ngữ nghĩa
- embeddings cho `Answer Relevancy`

Trong code hiện tại:

- judge LLM được khởi tạo bằng `ChatOpenAI` với `base_url` và `api_key`
- embeddings được khởi tạo bằng `OpenAIEmbeddings` nếu endpoint hỗ trợ

Nói ngắn gọn: script chỉ chuẩn bị dữ liệu và gọi RAGAS; việc chấm điểm do RAGAS thực hiện.

## Cách tính điểm tổng hợp

Sau khi RAGAS trả kết quả cho một test case, script:

1. Lấy từng metric ra từ dataframe.
2. Chuyển giá trị `NaN` thành `0.0`.
3. Tính `ragas_score` bằng trung bình cộng các metric có sẵn trong test case đó.

Sau khi chạy hết dataset, script:

1. Tính trung bình theo từng metric trên toàn bộ test cases thành công.
2. Tính `average_ragas_score`.
3. In dashboard tổng hợp ra console.

## Output sinh ra

Mỗi lần chạy sẽ tạo 2 file trong thư mục `results/`:

- `results_YYYYMMDD_HHMMSS.json`
- `results_YYYYMMDD_HHMMSS.csv`

File JSON chứa:

- cấu hình evaluation
- điểm trung bình
- kết quả chi tiết từng test case

File CSV phù hợp để mở bằng Excel hoặc đưa vào phân tích nhanh.

## Cách chạy

Chạy với dataset mặc định:

```bash
python -m app.evaluation.eval_legal_rag
```

Chạy với dataset riêng:

```bash
python -m app.evaluation.eval_legal_rag --dataset path/to/dataset.json
```

Chạy thử vài câu đầu:

```bash
python -m app.evaluation.eval_legal_rag --limit 5
```

## Ghi chú quan trọng

1. Nếu không cấu hình đúng `LLM_BASE_URL` và `LLM_MODEL`, judge LLM có thể lỗi hoặc chấm sai.
2. Nếu embeddings không khởi tạo được, `Answer Relevancy` sẽ không được tính.
3. Nếu `LightRAGOrchestrator` không kết nối được tới database, toàn bộ test case sẽ fail ở bước sinh response.

## Khi nào quy trình này hữu ích

Quy trình này phù hợp khi bạn muốn:

- benchmark chất lượng RAG sau mỗi lần đổi model hoặc prompt
- so sánh nhiều cấu hình retrieval khác nhau
- kiểm tra hệ thống có hallucination hay không
- xuất báo cáo định kỳ để theo dõi chất lượng theo thời gian
