from pydantic import BaseModel, Field

class ScoreBreakdown(BaseModel):
    hoc_van: int = Field(description="Điểm học vấn và bằng cấp (thang 30)")
    kinh_nghiem: int = Field(description="Điểm kinh nghiệm dạy học/gia sư (thang 40)")
    ky_nang_chuyen_mon: int = Field(description="Điểm kiến thức Toán và chứng chỉ (thang 20)")
    trinh_bay_cv: int = Field(description="Điểm hình thức và thái độ qua CV (thang 10)")

class CVAssessmentResult(BaseModel):
    candidate_name: str = Field(description="Họ tên ứng viên trích xuất từ CV")
    total_score: int = Field(description="Tổng điểm trên thang 100")
    score_breakdown: ScoreBreakdown
    status: str = Field(description="Kết luận: 'ĐẠT', 'CẦN PHỎNG VẤN THÊM', hoặc 'LOẠI'")
    pros: list[str] = Field(description="Danh sách các điểm mạnh nổi bật")
    cons: list[str] = Field(description="Danh sách các điểm yếu hoặc thiếu sót")
    recommendation_for_hr: str = Field(description="Lời khuyên chi tiết cho HR khi phỏng vấn")