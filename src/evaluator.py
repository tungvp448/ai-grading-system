from google.genai import types
from src.config import get_genai_client, DEFAULT_MODEL
from src.schemas import CVAssessmentResult
from src.parsers import extract_text_from_file

SYSTEM_INSTRUCTION = """
Bạn là một Chuyên viên Tuyển dụng (HR Assessment Specialist) cao cấp chuyên đánh giá ứng viên vị trí Gia sư môn Toán.
Nhiệm vụ của bạn là phân tích CV của ứng viên dựa trên Yêu cầu công việc (JD) và trả về kết quả chấm điểm khách quan, chính xác.

Thang điểm 100 bao gồm:
1. Học vấn & Bằng cấp (Tối đa 30 điểm): Ưu tiên sinh viên/cựu sinh viên các trường ĐH TOP đầu (Bách Khoa, Sư Phạm, Tự Nhiên, Ngoại Thương...) hoặc đạt giải HSG Toán.
2. Kinh nghiệm gia sư/giảng dạy (Tối đa 40 điểm): Đã từng dạy Toán các cấp, luyện thi vào 10, luyện thi Đại học, hiểu tâm lý học sinh.
3. Điểm thi & Kỹ năng chuyên môn (Tối đa 20 điểm): Điểm thi ĐH môn Toán cao (>= 8.5/10), có chứng chỉ sư phạm hoặc phương pháp dạy học tốt.
4. Trình bày CV & Kỹ năng mềm (Tối đa 10 điểm): CV rõ ràng, không lỗi chính tả, thể hiện sự trách nhiệm và kiên nhẫn.

Quy tắc đánh giá:
- Tổng điểm >= 80: Status = 'ĐẠT'
- Tổng điểm từ 60 - 79: Status = 'CẦN PHỎNG VẤN THÊM'
- Tổng điểm < 60: Status = 'LOẠI'
"""

def evaluate_math_tutor_cv(cv_path: str, jd_text: str, model_name: str = DEFAULT_MODEL) -> CVAssessmentResult:
    """Gửi dữ liệu CV và JD lên Gemini API để xử lý chấm điểm."""
    client = get_genai_client()
    cv_content = extract_text_from_file(cv_path)

    user_prompt = f"""
    --- YÊU CẦU CÔNG VIỆC (JD) ---
    {jd_text}

    --- NỘI DUNG CV ỨNG VIÊN ---
    {cv_content}
    """

    response = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=CVAssessmentResult,
            temperature=0.2
        ),
    )

    return response.parsed