import os
import tempfile
import streamlit as st
from src.evaluator import evaluate_math_tutor_cv

# Cấu hình trang Web
st.set_page_config(
    page_title="AI Chấm Điểm CV Gia Sư Toán",
    page_icon="🎓",
    layout="wide"
)

# Tiêu đề ứng dụng
st.title("🎓 AI Assistant - Chấm Điểm CV Gia Sư Toán")
st.caption("Giải pháp giảm tải khối lượng công việc cho bộ phận HR sử dụng Gemini Pro API")

# Sidebar: Nhập Yêu cầu công việc (JD)
with st.sidebar:
    st.header("📋 Yêu cầu Công việc (JD)")
    default_jd = """Tuyển Gia sư môn Toán cấp 2 và cấp 3 (Luyện thi vào 10 & THPTQG):
- Học vấn: Sinh viên hoặc đã tốt nghiệp các trường ĐH Bách Khoa, Sư Phạm, KHTN, Ngoại Thương. Điểm thi ĐH môn Toán từ 8.5 trở lên.
- Kinh nghiệm: Có ít nhất 1 năm kinh nghiệm dạy kèm Toán hoặc dạy tại các trung tâm.
- Kỹ năng: Kiên nhẫn, có phương pháp dạy dễ hiểu, truyền cảm hứng. Ưu tiên từng đạt giải HSG Toán các cấp."""

    jd_input = st.text_area("Chỉnh sửa JD tuyển dụng tại đây:", value=default_jd, height=300)
    st.info("💡 Bạn có thể chỉnh sửa JD linh hoạt cho từng đợt tuyển dụng.")

# Khu vực chính: Upload file CV bằng Kéo-Thả
st.subheader("📁 Tải lên CV Ứng viên")
uploaded_file = st.file_uploader(
    label="Kéo và thả file CV (PDF, DOCX, TXT) vào đây",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=False
)

if uploaded_file is not None:
    # Hiển thị thông tin file đã tải
    st.success(f"Dữ liệu đã nhận: **{uploaded_file.name}** ({round(uploaded_file.size / 1024, 1)} KB)")

    # Nút bấm tiến hành đánh giá
    if st.button("🚀 Bắt đầu Phân tích & Chấm điểm", type="primary", use_container_width=True):
        with st.spinner("Gemini Pro đang đọc và phân tích CV... Vui lòng đợi trong giây lát..."):
            try:
                # Lưu tạm file uploader vào đĩa cứng để thư viện parsers.py đọc được
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # Gọi logic chấm điểm từ module evaluator
                result = evaluate_math_tutor_cv(tmp_file_path, jd_input)

                # Xóa file tạm sau khi xử lý xong
                os.remove(tmp_file_path)

                # -------------------------------------------------------------
                # TRÌNH BÀY KẾT QUẢ TRÊN GIAO DIỆN
                # -------------------------------------------------------------
                st.divider()
                st.header("📊 Kết Quả Đánh Giá")

                # Cột hiển thị Tổng quan
                col1, col2, col3 = st.columns([2, 2, 3])

                with col1:
                    st.metric(label="Ứng viên", value=result.candidate_name)

                with col2:
                    st.metric(label="Tổng điểm", value=f"{result.total_score} / 100")

                with col3:
                    if result.status == "ĐẠT":
                        st.success(f"### Kết luận: {result.status} ✅")
                    elif result.status == "CẦN PHỎNG VẤN THÊM":
                        st.warning(f"### Kết luận: {result.status} ⚠️")
                    else:
                        st.error(f"### Kết luận: {result.status} ❌")

                # Chi tiết điểm từng phần
                st.subheader("📈 Bảng Điểm Chi Tiết")
                score_col1, score_col2, score_col3, score_col4 = st.columns(4)
                
                with score_col1:
                    st.caption("Học vấn & Bằng cấp")
                    st.progress(result.score_breakdown.hoc_van / 30, text=f"{result.score_breakdown.hoc_van}/30")
                
                with score_col2:
                    st.caption("Kinh nghiệm giảng dạy")
                    st.progress(result.score_breakdown.kinh_nghiem / 40, text=f"{result.score_breakdown.kinh_nghiem}/40")
                
                with score_col3:
                    st.caption("Chuyên môn & Thi ĐH")
                    st.progress(result.score_breakdown.ky_nang_chuyen_mon / 20, text=f"{result.score_breakdown.ky_nang_chuyen_mon}/20")
                
                with score_col4:
                    st.caption("Hình thức & Kỹ năng mềm")
                    st.progress(result.score_breakdown.trinh_bay_cv / 10, text=f"{result.score_breakdown.trinh_bay_cv}/10")

                # Phân tích Ưu/Nhược điểm
                st.divider()
                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.subheader("👍 Điểm Mạnh")
                    for pro in result.pros:
                        st.write(f"- {pro}")

                with detail_col2:
                    st.subheader("👎 Điểm Hạn Chế")
                    for con in result.cons:
                        st.write(f"- {con}")

                # Khuyến nghị cho HR
                st.subheader("💡 Lời khuyên dành cho HR")
                st.info(result.recommendation_for_hr)

            except Exception as e:
                st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")