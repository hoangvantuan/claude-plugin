# KERNEL Framework — Chi tiết & Ví dụ

Mỗi letter đại diện cho một nguyên lý tách prompt hiệu quả khỏi prompt trung bình. Đọc file này khi cần tra cứu nguyên lý hoặc giải thích framework cho user.

## K — Keep It Simple

Một prompt nên có một mục tiêu rõ ràng ngay từ đầu. Phức tạp là kẻ thù của chính xác — khi prompt cố làm quá nhiều, AI phân tán attention và chất lượng giảm khắp nơi.

**The test**: Bạn có thể mô tả prompt này làm gì trong một câu? Nếu không → cần đơn giản hóa hoặc tách.

**Before**: "I need help writing something about Redis that covers caching strategies, includes performance benchmarks, discusses alternatives, and also mentions deployment best practices"

**After**: "Write a technical tutorial on Redis caching patterns for Python web applications"

## E — Easy to Verify

Mỗi prompt cần success criteria mà cả người và AI đều kiểm tra khách quan được. Từ mơ hồ ("make it engaging", "write something good") không cho AI mục tiêu — và không cho bạn cách đánh giá kết quả.

**The test**: Một người lạ có thể xác minh output đạt yêu cầu mà không cần hỏi thêm?

**Before**: "Write an engaging blog post about TypeScript"

**After**: "Write a 1500-word blog post about TypeScript generics. Include 3 working code examples, a comparison table with Java generics, and a 'Common Mistakes' section with at least 4 entries"

## R — Reproducible Results

Prompt nên cho chất lượng nhất quán bất kể khi nào chạy. Tham chiếu thời gian ("current trends", "latest best practices") và thuật ngữ mơ hồ tạo drift — cùng prompt cho kết quả khác nhau tuần sau.

**The test**: Prompt này có cho kết quả tốt ngang nhau nếu chạy 30 ngày sau?

**Before**: "Summarize the latest developments in AI"

**After**: "Summarize the key architectural changes introduced in Transformer models between 2017 (Vaswani et al.) and 2024 (Mixture of Experts). Focus on attention mechanisms, training efficiency, and inference optimization"

## N — Narrow Scope

Một prompt = một mục tiêu. Prompt nhiều mục tiêu có tỷ lệ hài lòng 41% vs 89% cho prompt đơn mục tiêu. Khi cần nhiều thứ, chain các prompt riêng — mỗi prompt làm tốt một việc rồi feed vào prompt tiếp theo.

**The test**: Prompt này yêu cầu đúng một deliverable?

**Before**: "Create the API endpoint, write tests, update the docs, and add error handling"

**After**: Chain of 4 prompts:

1. "Design the REST API endpoint for user registration with input validation"
2. "Write pytest test cases for the user registration endpoint covering happy path, validation errors, and duplicate emails"
3. "Write API documentation for the user registration endpoint in OpenAPI 3.0 format"
4. "Add error handling to the user registration endpoint: rate limiting, malformed JSON, and database connection failures"

## E — Explicit Constraints

Nói cho AI biết KHÔNG làm gì. Prompt không constraints cho output generic, thiếu focus. Constraints là guardrails — loại bỏ nguyên nhóm kết quả không mong muốn.

**The test**: Bạn đã chỉ rõ ít nhất 2-3 thứ output KHÔNG nên include hoặc làm?

**Before**: "Write Python code for data processing"

**After**: "Write Python code to merge CSV files by date column. Constraints: pandas only, no external libraries beyond stdlib+pandas, no functions longer than 20 lines, no global variables, include type hints, handle missing values with forward-fill"

## L — Logical Structure

Mọi prompt hiệu quả theo cấu trúc nhất quán: Context → Task → Constraints → Format. Cấu trúc này map tự nhiên với cách AI xử lý instruction — context đặt frame, task định goal, constraints thu hẹp space, format chỉ rõ deliverable.

**The test**: Prompt có theo thứ tự Context → Task → Constraints → Format?

**Before**: "I want Python code. It should be clean. The task is parsing JSON. Use requests library. Output should be a CSV. Don't use pandas. The JSON comes from an API endpoint."

**After**:

```
Context: Fetching JSON data from a REST API endpoint
Task: Write a Python script that parses the JSON response and converts it to CSV
Constraints: Use requests library only, no pandas, handle pagination
Output Format: Single .csv file with headers matching JSON keys
```

## Common Transformations

Quick fixes cho các prompt problems phổ biến nhất:

| Problem | Before | After |
|---|---|---|
| Vague virtue | "Write a good summary" | "Write a 3-sentence summary covering: finding, impact, recommendation" |
| Overloaded | "Code + test + document this" | Split into 3 chained prompts |
| Temporal drift | "Current best practices for..." | "Best practices as of Python 3.12 for..." |
| No constraints | "Write Python code" | "Python 3.12+, no external libs, type hints, <50 lines per function" |
| Unclear format | "Analyze this data" | "Output: markdown table with columns [Metric, Value, Trend, Action]" |
| Unverifiable | "Make it production-ready" | "Include: error handling, input validation, logging, retry logic with exponential backoff" |
