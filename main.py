import sys
from src.evaluator import evaluate_math_tutor_cv

SAMPLE_JD = """
Tuyển Gia sư môn Toán cấp 2 và cấp 3 (Luyện thi vào 10 & THPTQG):
- Học vấn: Sinh viên hoặc đã tốt nghiệp các trường ĐH Bách Khoa, Sư Phạm, KHTN, Ngoại Thương. Điểm thi ĐH môn Toán từ 8.5 trở lên.
- Kinh nghiệm: Có ít nhất 1 năm kinh nghiệm dạy kèm Toán hoặc dạy tại các trung tâm.
- Kỹ năng: Kiên nhẫn, có phương pháp dạy dễ hiểu, truyền cảm hứng. Ưu tiên từng đạt giải HSG Toán các cấp.
"""

def main():
    # Lấy đường dẫn file CV từ tham số dòng lệnh hoặc dùng mặc định
    cv_file = sys.argv[1] if len(sys.argv) > 1 else "CV_NguyenVanA.pdf"

    print(f"🔄 Đang phân tích CV: {cv_file}...")

    try:
        result = evaluate_math_tutor_cv(cv_file, SAMPLE_JD)

        print("\n" + "="*20 + " KẾT QUẢ ĐÁNH GIÁ CV " + "="*20)
        print(f"Ứng viên       : {result.candidate_name}")
        print(f"Kết luận       : [{result.status}] (Tổng điểm: {result.total_score}/100)")
        print("-" * 61)
        print("Chi tiết điểm số:")
        print(f"  • Học vấn         : {result.score_breakdown.hoc_van}/30")
        print(f"  • Kinh nghiệm     : {result.score_breakdown.kinh_nghiem}/40")
        print(f"  • Chuyên môn Toán : {result.score_breakdown.ky_nang_chuyen_mon}/20")
        print(f"  • Hình thức CV    : {result.score_breakdown.trinh_bay_cv}/10")
        print("-" * 61)
        print("👍 Điểm mạnh:")
        for pro in result.pros:
            print(f"  - {pro}")

        print("\n👎 Điểm hạn chế:")
        for con in result.cons:
            print(f"  - {con}")

        print("\n💡 Khuyến nghị cho HR:")
        print(f"  {result.recommendation_for_hr}")
        print("="*61)

    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()