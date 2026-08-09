# -*- coding: utf-8 -*-
"""
Trình sinh CỔNG QUY TRÌNH SỐ HOÁ — VILLA 226
============================================
Sinh ra:
  - quy-trinh/index.html                (trang hub: lưới bộ phận + QR + bảng in)
  - quy-trinh/<slug>.html               (1 trang quy trình cho mỗi bộ phận)
  - img/qr/<slug>.svg                   (mã QR trỏ tới trang bộ phận)
  - img/qr/hub.svg                      (mã QR trỏ tới trang hub)

Cách chạy:  python3 quy-trinh/build.py
Yêu cầu:    pip install segno

Mọi nội dung quy trình nằm trong biến DEPTS bên dưới — sửa ở đây rồi chạy lại
để cập nhật toàn bộ cổng, giữ 100% đồng nhất giữa các bộ phận (chuẩn chuỗi 226).
"""
import os
import html
import segno

# ---------------------------------------------------------------------------
# Cấu hình chung
# ---------------------------------------------------------------------------
BASE_URL   = "https://villa226.com"          # tên miền chính thức (CNAME)
PORTAL_DIR = "quy-trinh"                       # thư mục cổng quy trình
QR_DIR     = "img/qr"                          # thư mục lưu QR
QR_DARK    = "#0F3F5C"                          # navy đậm — tương phản cao, dễ quét
BRAND      = "VILLA 226"
BRAND_SUB  = "COASTAL RETREAT"
COMPANY    = "Công ty Cổ phần Du lịch 226 · MST 3502546503"
HOTLINE    = "0387 979 797"
VERSION    = "Phiên bản 1.0 · 08/2026"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# DỮ LIỆU QUY TRÌNH — mỗi bộ phận là một dict
#   level: CORE = chuẩn lõi bất di bất dịch mọi villa | FLEX = linh hoạt địa phương
# ---------------------------------------------------------------------------
DEPTS = [
    {
        "slug": "quan-ly-villa", "code": "QL", "icon": "🧭",
        "name": "Quản lý Villa",
        "function": "Đầu mối vận hành tại chỗ của một villa — điều phối toàn bộ bộ phận, chịu trách nhiệm chất lượng dịch vụ, an toàn và số liệu Thu–Chi của cơ sở.",
        "reports": "Báo cáo: Ban điều hành chuỗi 226",
        "manages": "Quản lý: toàn bộ nhân sự tại villa",
        "target": "Villa vận hành trơn tru mỗi ngày, khách hài lòng, số liệu minh bạch và đúng hạn.",
        "standards": [
            ("CORE", "Luôn là MỘT đầu mối duy nhất với khách trong suốt kỳ lưu trú."),
            ("CORE", "Duy trì đủ 4 checklist bắt buộc tại cơ sở, lưu tối thiểu 3 tháng."),
            ("CORE", "Chốt báo cáo Thu–Chi trước ngày 05 hằng tháng theo mẫu chuẩn chuỗi."),
            ("CORE", "Villa mới/đổi mùa phải đạt brand audit trước khi mở bán."),
            ("FLEX", "Quy mô & phân ca nhân sự tuỳ số phòng và mùa cao/thấp điểm."),
        ],
        "steps": [
            ("Đầu ca — mở villa", "Kiểm tra checklist bàn giao ca trước; xác nhận lịch khách trong ngày (nhận/trả phòng), số khách, yêu cầu đặc biệt."),
            ("Điều phối trong ngày", "Phân công buồng phòng, bảo trì, hồ bơi theo lịch khách; theo dõi phản hồi khách qua đầu mối chung; xử lý phát sinh."),
            ("Nghiệm thu trước nhận phòng", "Cùng buồng phòng chạy checklist vệ sinh 14 dòng; một dòng Chưa đạt = chưa bàn giao phòng cho khách."),
            ("Trong kỳ lưu trú", "Giữ liên lạc một đầu mối; ghi nhật ký vận hành ngay khi phát sinh, không ghi dồn cuối ngày."),
            ("Cuối ca / cuối kỳ", "Nghiệm thu trả phòng, kiểm kê tài sản, đối chiếu chi phí phát sinh; bàn giao ca kèm nhật ký."),
            ("Nhịp định kỳ", "Tuần: kiểm tra kỹ thuật, kiểm kê, rà đánh giá. Tháng: chốt Thu–Chi, tổng hợp KPI, kiểm tra an toàn. Quý: brand audit, so sánh chéo, rà giá mùa, đào tạo."),
        ],
        "checklist": [
            "Checklist bàn giao ca & nhật ký vận hành đã ghi đầy đủ.",
            "4 checklist bắt buộc còn hiệu lực (vệ sinh, hồ bơi, an toàn tháng, bàn giao ca).",
            "Lịch khách hôm nay khớp với lịch OTA/kênh trực tiếp, không trùng.",
            "Không tồn sự cố Khẩn cấp/Nghiêm trọng chưa xử lý.",
            "Doanh thu & chi phí trong ngày đã ghi nhận.",
        ],
        "kpi": [
            ("Điểm đánh giá khách trung bình", "≥ 4.7/5"),
            ("Báo cáo Thu–Chi đúng hạn (trước ngày 05)", "100%"),
            ("Ngày có đủ nhật ký vận hành", "100%"),
            ("Sự cố an toàn nghiêm trọng", "0"),
        ],
        "exceptions": [
            ("Sự cố khẩn cấp (điện, nước, cháy nổ, an ninh)", "Bảo đảm an toàn khách trước tiên → gọi ứng cứu/hotline nội bộ → xử lý theo mức Khẩn cấp ≤2h → ghi nhật ký & báo Ban điều hành."),
            ("Khủng hoảng danh tiếng (khách doạ review xấu, tranh chấp)", "Chuyển ngay cho quy trình Xử lý ngoại lệ của bộ phận Đón tiếp & CSKH; Quản lý là người ra quyết định bồi hoàn trong hạn mức được duyệt."),
        ],
    },
    {
        "slug": "dat-phong-ota", "code": "OTA", "icon": "🗓️",
        "name": "Đặt phòng & OTA",
        "function": "Tiếp nhận và xử lý yêu cầu đặt phòng đa kênh (Zalo, Facebook/Messenger, form website, Booking/Agoda/Airbnb); quản lý lịch & giá; tuyệt đối chống trùng lịch.",
        "reports": "Báo cáo: Quản lý Villa / Điều hành chuỗi",
        "manages": "Phối hợp: Đón tiếp & CSKH, Tài chính",
        "target": "Không bỏ lỡ yêu cầu nào, phản hồi nhanh, chốt cọc gọn, lịch mọi kênh luôn khớp.",
        "standards": [
            ("CORE", "Phản hồi ≤ 30 phút trong giờ hành chính, ≤ 2 giờ ngoài giờ."),
            ("CORE", "Giá thống nhất mọi kênh (price parity) — ưu đãi đặt trực tiếp không phá giá công bố."),
            ("CORE", "Đồng bộ lịch mọi kênh ≤ 15 phút sau khi có thay đổi."),
            ("CORE", "Trùng lịch (overbooking) = 0."),
            ("FLEX", "Kênh OTA đang mở & tỷ trọng ngân sách quảng cáo theo từng villa/mùa."),
        ],
        "steps": [
            ("Tiếp nhận yêu cầu", "Ghi nhận mọi tin nhắn/inquiry vào một sổ đặt phòng chung (kênh, tên, SĐT/Zalo, villa, ngày, số khách). Không để tin nào ở trạng thái chưa phản hồi quá SLA."),
            ("Xác định nhu cầu", "Hỏi đủ: villa mong muốn, ngày nhận–trả, số khách (người lớn/trẻ em), nhu cầu đặc biệt (BBQ, đón đoàn, sự kiện)."),
            ("Kiểm tra phòng trống", "Đối chiếu lịch chung TẤT CẢ kênh. Nếu sát ngày/đoàn lớn, xác nhận lại tồn phòng thực tế trước khi báo còn phòng."),
            ("Báo giá", "Báo giá đúng bảng giá theo mùa (thường/cuối tuần/cao điểm) + phụ thu vượt khách; nêu rõ ưu đãi đặt trực tiếp. Không tự ý phá giá."),
            ("Chốt & thu cọc", "Chốt villa + ngày; gửi thông tin cọc (mức cọc & tài khoản 226 TRAVEL); xác nhận đã nhận cọc mới coi là giữ chỗ."),
            ("Xác nhận đặt phòng", "Gửi bản Xác nhận đặt phòng: villa, ngày nhận (14h)–trả (12h), số khách, tổng tiền, đã cọc/còn lại, chính sách huỷ."),
            ("Khoá lịch & đồng bộ", "Cập nhật lịch chung + đóng ngày trên mọi kênh OTA trong ≤15 phút để tránh trùng."),
            ("Bàn giao", "Chuyển thông tin khách cho Đón tiếp & CSKH để chăm sóc trước nhận phòng."),
        ],
        "checklist": [
            "Yêu cầu đã ghi vào sổ đặt phòng chung.",
            "Đã đối chiếu lịch tất cả kênh trước khi báo còn phòng.",
            "Báo giá đúng bảng giá mùa + phụ thu.",
            "Đã nhận cọc trước khi khoá giữ chỗ.",
            "Đã đóng ngày trên mọi kênh OTA ≤15 phút.",
            "Đã bàn giao khách cho Đón tiếp & CSKH.",
        ],
        "kpi": [
            ("Tỷ lệ phản hồi đúng SLA", "≥ 95%"),
            ("Trùng lịch / overbooking", "0"),
            ("Tỷ lệ chốt trên số inquiry", "≥ 30%"),
            ("Tỷ trọng booking đặt trực tiếp", "tăng theo quý"),
        ],
        "exceptions": [
            ("Trùng lịch / overbooking", "Xin lỗi ngay; ưu tiên chuyển khách sang villa 226 khác cùng phân khúc; nếu không được, hỗ trợ tìm chỗ tương đương + bù chênh lệch; ghi sự vụ và truy nguyên nguyên nhân đồng bộ."),
            ("Khách huỷ / đổi ngày", "Áp đúng chính sách huỷ đã công bố; đổi ngày tuỳ tồn phòng; mọi ngoại lệ do Quản lý duyệt."),
            ("No-show", "Giữ liên lạc đến hết giờ nhận phòng; áp chính sách cọc; mở lại ngày trên kênh nếu chắc chắn khách không đến."),
        ],
    },
    {
        "slug": "don-tiep-cham-soc", "code": "CS", "icon": "🤝",
        "name": "Đón tiếp & Chăm sóc khách",
        "function": "Là gương mặt của Villa 226 với khách: chăm sóc trước nhận phòng, đón – bàn giao villa, hỗ trợ trong kỳ lưu trú và tiễn khách. Một đầu mối duy nhất.",
        "reports": "Báo cáo: Quản lý Villa",
        "manages": "Phối hợp: Buồng phòng, Bảo trì, Dịch vụ tăng thêm",
        "target": "Khách được đón tiếp chu đáo, luôn biết liên hệ với ai, cảm nhận đúng chuẩn 4–5 sao.",
        "standards": [
            ("CORE", "Một đầu mối duy nhất chăm sóc khách suốt kỳ lưu trú."),
            ("CORE", "Villa sẵn sàng trước giờ nhận phòng ≥ 60 phút; nhận 14:00, trả 12:00."),
            ("CORE", "Gửi thông tin nhận phòng (địa chỉ, định vị, nội quy, WiFi) trước ngày đến."),
            ("CORE", "Văn phong trang trọng, tránh tiểu từ 'ạ' trong ngữ cảnh trang trọng."),
            ("FLEX", "Quà welcome, gợi ý ăn chơi địa phương tuỳ villa và đối tác tại chỗ."),
        ],
        "steps": [
            ("Chăm sóc trước nhận phòng (pre-arrival)", "Trước 1 ngày: gửi khách địa chỉ + Google Maps, giờ nhận/trả, nội quy chính, hướng dẫn đỗ xe, thông tin WiFi, đầu mối liên hệ; xác nhận giờ đến dự kiến."),
            ("Chuẩn bị đón", "Cùng buồng phòng nghiệm thu villa sạch sẽ, tiện nghi đủ; bật điện/nước/hồ bơi; đặt nước welcome; kiểm tra thẻ thông tin trong phòng."),
            ("Đón & bàn giao villa", "Chào đón, hướng dẫn phòng ốc, cách dùng bếp/BBQ/karaoke/hồ bơi, quy tắc an toàn hồ bơi & giờ giữ trật tự sau 22:00; bàn giao tài sản."),
            ("Trong kỳ lưu trú", "Chủ động hỏi thăm 1 lần; phản hồi yêu cầu nhanh; kết nối dịch vụ tăng thêm khi khách cần; ghi nhật ký các phát sinh."),
            ("Tiễn khách & trả phòng", "Nhắc giờ trả 12:00 (khách báo trước 30 phút); cùng kiểm tra tài sản; xử lý phụ thu/hư hỏng (nếu có) đúng bảng giá công bố."),
            ("Sau lưu trú", "Cảm ơn khách; mời đánh giá; chuyển thông tin cho bộ phận đánh giá & marketing để chăm sóc khách cũ."),
        ],
        "checklist": [
            "Đã gửi thông tin nhận phòng trước ngày đến.",
            "Villa sẵn sàng trước giờ nhận ≥60 phút, có nước welcome.",
            "Đã bàn giao hướng dẫn an toàn hồ bơi & nội quy trật tự.",
            "Đã hỏi thăm khách ít nhất 1 lần trong kỳ.",
            "Đã kiểm tra tài sản khi trả phòng.",
            "Đã mời khách đánh giá sau khi rời đi.",
        ],
        "kpi": [
            ("Điểm đánh giá khách", "≥ 4.7/5"),
            ("Tỷ lệ phàn nàn / lượt khách", "≤ 5%"),
            ("Tỷ lệ khách để lại đánh giá", "≥ 30%"),
            ("Thời gian phản hồi yêu cầu trong kỳ", "≤ 15 phút"),
        ],
        "exceptions": [
            ("Khách phàn nàn (quy trình 4 bước chung toàn chuỗi)", "1) Lắng nghe đầy đủ, không ngắt lời. 2) Xin lỗi về TRẢI NGHIỆM. 3) Đề xuất khắc phục kèm mốc thời gian; vượt thẩm quyền báo ngay & hẹn giờ trả lời. 4) Xác nhận lại sau khắc phục và ghi nhật ký."),
            ("Khách đến sớm khi villa chưa sẵn sàng", "Hỗ trợ nhận sớm nếu phòng trống & đã dọn; nếu chưa, mời khu chờ và cập nhật thời gian rõ ràng."),
            ("Hư hỏng tài sản do khách", "Ghi nhận có ảnh; áp bảng giá đền bù công bố; giữ thái độ tôn trọng, mọi khoản ngoài bảng do Quản lý quyết."),
        ],
    },
    {
        "slug": "buong-phong-ve-sinh", "code": "BP", "icon": "🧺",
        "name": "Buồng phòng & Vệ sinh",
        "function": "Bảo đảm villa sạch đúng chuẩn khách sạn cao cấp trước mỗi lượt khách: phòng ngủ, WC, khu bếp, không gian chung và đồ vải.",
        "reports": "Báo cáo: Quản lý Villa",
        "manages": "Phối hợp: Đón tiếp (nghiệm thu), Kho (đồ vải & vật tư)",
        "target": "Mỗi khách nhận villa sạch như mới — đạt nghiệm thu ngay lần đầu.",
        "standards": [
            ("CORE", "Thay TOÀN BỘ đồ vải (ga, gối, khăn) mỗi lượt khách."),
            ("CORE", "Nghiệm thu vệ sinh 14 dòng có ký; một dòng Chưa đạt = chưa bàn giao."),
            ("CORE", "Khăn tắm trắng, gấp đúng kiểu chuẩn, đủ số lượng theo giường."),
            ("CORE", "Tồn tối thiểu 3 bộ đồ vải mỗi vị trí để xoay ca."),
            ("FLEX", "Đơn vị giặt là & lịch tổng vệ sinh sâu tuỳ villa."),
        ],
        "steps": [
            ("Nhận lịch dọn", "Nhận lịch trả phòng/nhận phòng từ Quản lý; ưu tiên phòng có khách đến trong ngày."),
            ("Thu & thay đồ vải", "Thu toàn bộ ga/gối/khăn đã dùng; thay bộ sạch; đếm và ghi nhận số lượng."),
            ("Vệ sinh phòng & WC", "Lau bụi, hút/lau sàn, cọ WC, khử mùi, kiểm tra vòi/xả nước; bổ sung đồ dùng (dầu gội, sữa tắm, giấy, nước)."),
            ("Vệ sinh bếp & khu chung", "Dọn bếp, rửa dụng cụ, đổ rác, lau bàn ăn/khu BBQ, sắp xếp phòng khách gọn gàng."),
            ("Kiểm tra tiện nghi", "Bật thử đèn, điều hoà, TV, máy sấy, bàn ủi; báo Bảo trì nếu có lỗi."),
            ("Nghiệm thu & bàn giao", "Cùng Đón tiếp chạy checklist 14 dòng; ký nghiệm thu; chỉ bàn giao khi đạt toàn bộ."),
        ],
        "checklist": [
            "Đã thay toàn bộ đồ vải, số lượng đủ theo giường.",
            "WC sạch, không mùi, đủ đồ dùng bổ sung.",
            "Bếp & khu BBQ sạch, dụng cụ đủ.",
            "Sàn & bề mặt sạch, không bụi/tóc.",
            "Tiện nghi (đèn, điều hoà, TV) hoạt động.",
            "Checklist 14 dòng đạt toàn bộ, đã ký.",
        ],
        "kpi": [
            ("Nghiệm thu đạt ngay lần đầu", "≥ 95%"),
            ("Phàn nàn về vệ sinh / lượt khách", "≤ 3%"),
            ("Thời gian dọn chuẩn giữa 2 lượt khách", "đúng định mức villa"),
            ("Tồn đồ vải tối thiểu / vị trí", "≥ 3 bộ"),
        ],
        "exceptions": [
            ("Phát hiện hư hỏng khi dọn", "Ghi nhận có ảnh, báo Bảo trì (theo mức sự cố) và Quản lý; không bàn giao phòng lỗi trọng yếu."),
            ("Thiếu đồ vải/vật tư sạch", "Báo Kho ngay; dùng bộ tồn tối thiểu; nếu không đủ, Quản lý điều phối giữa villa trong chuỗi."),
        ],
    },
    {
        "slug": "bao-tri-ky-thuat", "code": "BT", "icon": "🔧",
        "name": "Bảo trì & Kỹ thuật",
        "function": "Giữ hạ tầng & thiết bị villa luôn hoạt động an toàn: điện, nước, điều hoà, thiết bị bếp, karaoke, hệ thống hồ bơi; xử lý sự cố theo mức độ.",
        "reports": "Báo cáo: Quản lý Villa",
        "manages": "Phối hợp: Buồng phòng, Hồ bơi & cảnh quan",
        "target": "Sự cố được xử lý đúng cam kết thời gian theo mức độ, không làm gián đoạn trải nghiệm khách.",
        "standards": [
            ("CORE", "4 mức sự cố: Khẩn cấp ≤2h · Nghiêm trọng ≤4h · Thông thường ≤24h · Định kỳ theo lịch."),
            ("CORE", "Thiết bị an toàn (điện, gas, hồ bơi) kiểm tra định kỳ và ghi nhật ký."),
            ("CORE", "Không bàn giao phòng có lỗi an toàn trọng yếu cho khách."),
            ("FLEX", "Nhà thầu kỹ thuật ngoài & chu kỳ bảo trì sâu tuỳ villa."),
        ],
        "steps": [
            ("Tiếp nhận báo sự cố", "Nhận từ Buồng phòng/Đón tiếp/khách; ghi: vị trí, mô tả, mức độ (Khẩn cấp/Nghiêm trọng/Thông thường/Định kỳ)."),
            ("Phân loại & cam kết thời gian", "Gán mức độ và mốc xử lý tương ứng; báo lại người liên quan mốc dự kiến."),
            ("Xử lý", "Khắc phục an toàn; nếu cần dừng thiết bị/khu vực, cô lập và cảnh báo rõ ràng."),
            ("Kiểm tra lại", "Chạy thử sau sửa; xác nhận an toàn trước khi đưa vào sử dụng."),
            ("Ghi nhật ký & báo cáo", "Ghi nhật ký kỹ thuật: sự cố, nguyên nhân, cách xử lý, vật tư dùng; báo Quản lý."),
            ("Bảo trì định kỳ", "Theo lịch tháng/quý: điện, nước, điều hoà, thiết bị bếp, bơm hồ bơi, PCCC."),
        ],
        "checklist": [
            "Sự cố đã được phân mức và gán mốc thời gian.",
            "Khu vực nguy hiểm đã cô lập & cảnh báo (nếu cần).",
            "Đã chạy thử lại sau khi sửa.",
            "Nhật ký kỹ thuật đã ghi đầy đủ.",
            "Hạng mục bảo trì định kỳ tháng này đã thực hiện.",
        ],
        "kpi": [
            ("Tỷ lệ sự cố xử lý đúng cam kết thời gian", "≥ 95%"),
            ("Sự cố lặp lại cùng hạng mục trong 30 ngày", "≤ 1"),
            ("Hạng mục bảo trì định kỳ hoàn thành đúng lịch", "100%"),
            ("Sự cố an toàn nghiêm trọng", "0"),
        ],
        "exceptions": [
            ("Sự cố khẩn cấp ảnh hưởng an toàn khách", "Bảo đảm an toàn trước; cô lập nguồn nguy hiểm; xử lý mức Khẩn cấp ≤2h; báo Quản lý & Ban điều hành."),
            ("Vượt năng lực xử lý tại chỗ", "Gọi nhà thầu đã duyệt; nếu ảnh hưởng lưu trú, phối hợp Đón tiếp phương án cho khách."),
        ],
    },
    {
        "slug": "ho-boi-canh-quan", "code": "HB", "icon": "🏊",
        "name": "Hồ bơi & Cảnh quan",
        "function": "Giữ hồ bơi sạch – an toàn và cảnh quan/sân vườn gọn đẹp; quản lý hoá chất và biển cảnh báo an toàn.",
        "reports": "Báo cáo: Quản lý Villa",
        "manages": "Phối hợp: Bảo trì (hệ thống bơm/lọc)",
        "target": "Hồ bơi luôn trong, an toàn, có nhật ký mỗi ngày; cảnh quan sạch đẹp đón khách.",
        "standards": [
            ("CORE", "Kiểm tra hồ bơi và ghi nhật ký MỖI NGÀY (chỉ số nước + hoá chất đã dùng)."),
            ("CORE", "Hoá chất khoá riêng, ngoài tầm với trẻ em; có phao cứu sinh."),
            ("CORE", "Biển cảnh báo độ sâu rõ ràng tại hồ bơi từng villa."),
            ("FLEX", "Loại cây cảnh, tần suất cắt tỉa, đối tác chăm sóc cảnh quan tuỳ villa."),
        ],
        "steps": [
            ("Kiểm tra đầu ngày", "Đo pH/clo, quan sát độ trong; vớt rác lá; kiểm tra phao cứu sinh & biển cảnh báo còn nguyên."),
            ("Xử lý nước", "Bổ sung hoá chất đúng liều; ghi lượng đã dùng; chờ đủ thời gian an toàn trước khi mở cho khách."),
            ("Ghi nhật ký hồ bơi", "Ghi chỉ số nước, hoá chất, giờ kiểm tra vào nhật ký hồ bơi hằng ngày."),
            ("Cảnh quan", "Quét sân, cắt tỉa cơ bản, dọn khu BBQ/sân vườn, kiểm tra đèn sân."),
            ("An toàn khi có khách", "Nhắc quy tắc an toàn hồ bơi khi bàn giao; giám sát biển độ sâu; tuyệt đối không để trẻ dùng hồ không giám sát."),
        ],
        "checklist": [
            "Đã đo pH/clo và ghi nhật ký hôm nay.",
            "Nước trong, không rác/lá.",
            "Phao cứu sinh & biển độ sâu đầy đủ.",
            "Hoá chất cất khoá an toàn.",
            "Sân vườn & khu BBQ sạch, đèn sân hoạt động.",
        ],
        "kpi": [
            ("Tỷ lệ ngày có nhật ký hồ bơi", "100%"),
            ("Sự cố an toàn hồ bơi", "0"),
            ("Phàn nàn về nước hồ bơi / lượt khách", "≤ 2%"),
            ("Cảnh quan đạt khi nghiệm thu", "≥ 95%"),
        ],
        "exceptions": [
            ("Nước đục / chỉ số bất thường", "Đóng tạm hồ, xử lý hoá chất, chỉ mở lại khi đạt chuẩn; thông báo khách lịch sự nếu ảnh hưởng."),
            ("Thiết bị bơm/lọc hỏng", "Báo Bảo trì (theo mức sự cố); che chắn khu vực nếu cần."),
        ],
    },
    {
        "slug": "an-ninh-an-toan", "code": "AN", "icon": "🛡️",
        "name": "An ninh & An toàn",
        "function": "Bảo đảm an toàn cho khách và tài sản villa: kiểm soát ra vào, phòng cháy, trật tự và quyền riêng tư của khách.",
        "reports": "Báo cáo: Quản lý Villa",
        "manages": "Phối hợp: Đón tiếp, Bảo trì",
        "target": "Khách an toàn và riêng tư tuyệt đối; sự vụ an ninh bằng 0.",
        "standards": [
            ("CORE", "Chỉ khách đã đăng ký mới được vào villa."),
            ("CORE", "CẤM TUYỆT ĐỐI camera trong không gian riêng tư của khách (trong nhà, khu hồ bơi kín)."),
            ("CORE", "Giữ trật tự sau 22:00; nhắc khách quy tắc âm thanh với hàng xóm."),
            ("CORE", "Thiết bị PCCC đủ, còn hạn, đặt đúng vị trí."),
            ("FLEX", "Camera an ninh chỉ đặt ở lối vào/ngoại vi tuỳ villa, không xâm phạm riêng tư."),
        ],
        "steps": [
            ("Kiểm soát ra vào", "Xác nhận đúng khách đã đăng ký; hướng dẫn đỗ xe đúng quy định từng villa; ghi nhận khách/đoàn lớn."),
            ("Tuần tra & quan sát", "Kiểm tra ngoại vi, khoá cổng/cửa khu chung ngoài giờ; quan sát an toàn hồ bơi khu vực chung."),
            ("Nhắc trật tự", "Nhắc lịch sự quy tắc giữ trật tự sau 22:00; xử lý sớm nếu ồn ảnh hưởng hàng xóm."),
            ("An toàn PCCC", "Kiểm tra bình chữa cháy, lối thoát, thiết bị điện quá tải; báo Bảo trì nếu bất thường."),
            ("Ghi nhận sự vụ", "Mọi sự vụ an ninh ghi nhật ký ngay: thời gian, diễn biến, cách xử lý; báo Quản lý."),
        ],
        "checklist": [
            "Chỉ khách đăng ký có mặt trong villa.",
            "Không có thiết bị ghi hình ở không gian riêng tư.",
            "Cổng/cửa khu chung khoá đúng giờ.",
            "Thiết bị PCCC đủ & còn hạn.",
            "Sự vụ (nếu có) đã ghi nhật ký.",
        ],
        "kpi": [
            ("Số sự vụ an ninh", "0"),
            ("Phàn nàn hàng xóm về trật tự", "≤ 1/quý"),
            ("Thiết bị PCCC đạt khi kiểm tra tháng", "100%"),
            ("Tuân thủ quy tắc riêng tư", "100%"),
        ],
        "exceptions": [
            ("Người lạ / tranh chấp / mất an ninh", "Bảo đảm an toàn khách; can thiệp trong thẩm quyền; gọi hỗ trợ/chính quyền nếu cần; ghi nhật ký & báo Quản lý ngay."),
            ("Sự cố cháy nổ", "Ưu tiên sơ tán an toàn; dùng PCCC nếu an toàn; gọi 114; báo Ban điều hành."),
        ],
    },
    {
        "slug": "dich-vu-tang-them", "code": "DV", "icon": "🍽️",
        "name": "Dịch vụ tăng thêm",
        "function": "Cung cấp và điều phối dịch vụ cộng thêm cho khách: đầu bếp/BBQ tại chỗ, trang trí sự kiện, tour, đưa đón — qua đối tác đã duyệt.",
        "reports": "Báo cáo: Quản lý Villa",
        "manages": "Phối hợp: Đón tiếp & CSKH",
        "target": "Tăng trải nghiệm và doanh thu dịch vụ mà không gây phiền cho khách.",
        "standards": [
            ("CORE", "Bảng giá dịch vụ công bố trước, minh bạch."),
            ("CORE", "Chỉ giới thiệu đối tác đã được duyệt về chất lượng & an toàn thực phẩm."),
            ("CORE", "Không chào bán gây phiền; chỉ tư vấn khi khách quan tâm."),
            ("FLEX", "Danh mục đối tác (đầu bếp, tour, trang trí) tuỳ địa phương từng villa."),
        ],
        "steps": [
            ("Giới thiệu dịch vụ", "Khi khách quan tâm, giới thiệu menu dịch vụ & bảng giá rõ ràng (BBQ, đầu bếp, trang trí sinh nhật, tour...)."),
            ("Chốt & xác nhận", "Chốt nội dung, thời gian, số lượng, giá; xác nhận với khách và với đối tác."),
            ("Điều phối thực hiện", "Sắp lịch với đối tác đã duyệt; chuẩn bị không gian (BBQ, bàn tiệc, karaoke); đảm bảo an toàn thực phẩm."),
            ("Giám sát chất lượng", "Theo dõi trong lúc phục vụ; xử lý phát sinh; giữ vệ sinh khu vực."),
            ("Chốt chi phí", "Ghi nhận doanh thu dịch vụ; chuyển Tài chính; thu dọn sau sự kiện."),
        ],
        "checklist": [
            "Đã báo bảng giá dịch vụ trước khi chốt.",
            "Đối tác sử dụng nằm trong danh sách đã duyệt.",
            "Đã xác nhận thời gian & số lượng với khách.",
            "An toàn thực phẩm & vệ sinh được đảm bảo.",
            "Doanh thu dịch vụ đã ghi nhận & bàn giao Tài chính.",
        ],
        "kpi": [
            ("Tỷ trọng doanh thu dịch vụ / doanh thu villa", "tăng theo quý"),
            ("Phàn nàn về dịch vụ tăng thêm", "≤ 3%"),
            ("Tỷ lệ đối tác đạt chuẩn khi rà soát", "100%"),
            ("Sự cố an toàn thực phẩm", "0"),
        ],
        "exceptions": [
            ("Đối tác trễ / không đạt", "Xin lỗi khách, tìm phương án thay thế trong hạn mức; loại đối tác không đạt khỏi danh sách."),
            ("Sự cố an toàn thực phẩm", "Ngừng phục vụ món liên quan; hỗ trợ khách; ghi sự vụ & rà lại đối tác."),
        ],
    },
    {
        "slug": "kho-vat-tu-mua-sam", "code": "KHO", "icon": "📦",
        "name": "Kho, Vật tư & Mua sắm",
        "function": "Quản lý vật tư tiêu hao và tài sản villa: đồ vải, đồ dùng khách, vật tư vệ sinh/hồ bơi; kiểm kê và bổ sung đúng định mức.",
        "reports": "Báo cáo: Quản lý Villa / Mua sắm chuỗi",
        "manages": "Phối hợp: Buồng phòng, Hồ bơi, Tài chính",
        "target": "Không bao giờ thiếu vật tư phục vụ khách; tồn kho gọn, đúng định mức, không thất thoát.",
        "standards": [
            ("CORE", "Vật tư mang thương hiệu (khăn thêu logo, ấn phẩm) mua tập trung cấp chuỗi."),
            ("CORE", "Kiểm kê hằng tuần; giữ định mức tồn tối thiểu từng loại."),
            ("CORE", "Nhập/xuất kho có ghi nhận, đối chiếu được."),
            ("FLEX", "Nhà cung cấp vật tư tiêu hao địa phương tuỳ villa."),
        ],
        "steps": [
            ("Theo dõi tồn", "Cập nhật tồn đồ vải, đồ dùng khách, vật tư vệ sinh/hồ bơi; đánh dấu mục dưới định mức tối thiểu."),
            ("Lập yêu cầu mua", "Gộp nhu cầu; ưu tiên hàng thương hiệu qua kênh mua tập trung; hàng địa phương qua NCC đã duyệt."),
            ("Nhập kho", "Kiểm số lượng & chất lượng khi nhận; ghi nhập kho; loại hàng lỗi."),
            ("Xuất kho", "Cấp phát theo yêu cầu bộ phận; ghi xuất kho; cập nhật tồn."),
            ("Kiểm kê tuần", "Đếm thực tế, đối chiếu sổ sách; báo chênh lệch & nguyên nhân cho Quản lý."),
        ],
        "checklist": [
            "Mục dưới định mức tối thiểu đã được đánh dấu.",
            "Hàng thương hiệu mua qua kênh tập trung.",
            "Nhập/xuất kho đã ghi nhận đầy đủ.",
            "Kiểm kê tuần đã thực hiện & đối chiếu.",
            "Chênh lệch (nếu có) đã báo cáo.",
        ],
        "kpi": [
            ("Số lần thiếu hàng phục vụ khách", "0"),
            ("Chênh lệch kiểm kê tuần", "≤ 2%"),
            ("Tồn tối thiểu duy trì đúng định mức", "100%"),
            ("Vật tư thương hiệu đúng chuẩn chuỗi", "100%"),
        ],
        "exceptions": [
            ("Thiếu hàng gấp phục vụ khách", "Điều phối giữa các villa trong chuỗi; mua khẩn tại chỗ trong hạn mức; báo Quản lý."),
            ("Chênh lệch kiểm kê lớn", "Truy nguyên (thất thoát/ghi sai/hư hỏng); báo Quản lý; điều chỉnh quy trình cấp phát."),
        ],
    },
    {
        "slug": "tai-chinh-bao-cao", "code": "TC", "icon": "📊",
        "name": "Tài chính & Báo cáo cơ sở",
        "function": "Ghi nhận doanh thu – chi phí của villa theo mẫu chuẩn chuỗi; theo dõi cọc, công nợ; chốt báo cáo Thu–Chi đúng hạn.",
        "reports": "Báo cáo: Kế toán chuỗi 226",
        "manages": "Phối hợp: mọi bộ phận phát sinh thu/chi",
        "target": "Số liệu minh bạch, đối chiếu được, báo cáo đúng hạn để so sánh chéo toàn chuỗi.",
        "standards": [
            ("CORE", "Dùng mẫu Thu–Chi thống nhất toàn chuỗi."),
            ("CORE", "Ghi doanh thu theo ngày lưu trú; tách chi phí đầu tư khỏi chi phí vận hành."),
            ("CORE", "Chốt báo cáo trước ngày 05 hằng tháng."),
            ("CORE", "Thu cọc/thanh toán qua tài khoản 226 TRAVEL, đối chiếu được."),
            ("FLEX", "Cơ cấu chi phí chi tiết tuỳ mô hình hợp tác từng villa."),
        ],
        "steps": [
            ("Ghi nhận doanh thu", "Ghi doanh thu phòng theo ngày lưu trú + doanh thu dịch vụ; đối chiếu với sổ đặt phòng."),
            ("Theo dõi cọc & công nợ", "Ghi cọc đã thu, số còn lại; nhắc khách/đối tác khoản đến hạn."),
            ("Ghi nhận chi phí", "Phân loại chi phí vận hành theo mẫu; tách riêng chi phí đầu tư; lưu chứng từ."),
            ("Đối chiếu", "Đối chiếu thu–chi với sao kê tài khoản 226 TRAVEL; xử lý lệch."),
            ("Chốt & báo cáo", "Chốt Thu–Chi trước ngày 05; gửi Kế toán chuỗi để tổng hợp & so sánh chéo."),
        ],
        "checklist": [
            "Doanh thu ghi theo ngày lưu trú, khớp sổ đặt phòng.",
            "Cọc & công nợ được theo dõi.",
            "Chi phí phân loại đúng mẫu, có chứng từ.",
            "Đã đối chiếu với sao kê tài khoản.",
            "Báo cáo chốt trước ngày 05.",
        ],
        "kpi": [
            ("Báo cáo Thu–Chi đúng hạn", "100%"),
            ("Chênh lệch đối chiếu chưa xử lý", "0"),
            ("Chứng từ đầy đủ cho khoản chi", "100%"),
            ("Công suất & doanh thu cập nhật kịp so sánh chéo", "hằng tháng"),
        ],
        "exceptions": [
            ("Lệch thu–chi khi đối chiếu", "Truy nguyên chứng từ & sao kê; không chốt khi còn khoản chưa rõ; báo Kế toán chuỗi."),
            ("Khách chậm thanh toán phần còn lại", "Áp chính sách thanh toán trước nhận phòng; phối hợp Đón tiếp nhắc khách."),
        ],
    },
]

# ---------------------------------------------------------------------------
# CSS dùng chung (đồng bộ nhận diện với index.html)
# ---------------------------------------------------------------------------
CSS = """
:root{--navy:#14547A;--navy-d:#0F3F5C;--copper:#C89A46;--copper-l:#DDB86A;
--bg:#EEF3F6;--ink:#222;--muted:#5C6B75;--line:#D6E0E6;--white:#fff;
--core:#0F7A4E;--core-bg:#E4F3EC;--flex:#B07A16;--flex-bg:#FBF1DC;}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Be Vietnam Pro',system-ui,-apple-system,sans-serif;color:var(--ink);
background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3,.display{font-family:'Playfair Display',serif;font-weight:600;line-height:1.18}
a{color:inherit;text-decoration:none}
img,svg{max-width:100%;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.muted{color:var(--muted)}
/* top bar */
.topbar{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid var(--line)}
.topbar .in{display:flex;align-items:center;justify-content:space-between;height:64px}
.brand{display:flex;align-items:center;gap:10px}
.brand img{height:44px;width:auto;mix-blend-mode:multiply}
.brand b{font-family:'Playfair Display';color:var(--navy);font-size:19px;font-weight:700}
.back{font-size:14px;font-weight:600;color:var(--navy);border:1.5px solid var(--line);
padding:8px 14px;border-radius:10px}
.back:hover{border-color:var(--navy)}
/* hero */
.phero{background:linear-gradient(150deg,var(--navy),var(--navy-d));color:#fff;padding:46px 0 40px;position:relative;overflow:hidden}
.phero::after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 85% 15%,rgba(200,154,70,.22),transparent 45%)}
.phero .wrap{position:relative}
.eyebrow{font-weight:600;letter-spacing:.16em;text-transform:uppercase;font-size:12px;color:var(--copper-l)}
.phero h1{font-size:clamp(26px,4vw,40px);margin:10px 0 8px;color:#fff}
.phero p{color:#d3e2ec;max-width:60ch;font-weight:300}
.tagcode{display:inline-block;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);
color:#fff;font-weight:600;font-size:13px;padding:5px 13px;border-radius:100px;margin-bottom:6px}
/* section */
.section{padding:40px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:26px 26px;
margin-bottom:20px;box-shadow:0 4px 16px rgba(20,84,122,.05)}
.card h2{color:var(--navy);font-size:22px;margin-bottom:14px;display:flex;align-items:center;gap:10px}
.card h2 .no{width:30px;height:30px;border-radius:8px;background:var(--navy);color:var(--copper-l);
font-family:'Be Vietnam Pro';font-weight:700;font-size:15px;display:grid;place-items:center;flex:none}
.role{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:640px){.role{grid-template-columns:1fr}}
.role .box{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.role .box .lb{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--copper)}
.role .box .vl{font-size:15px;color:var(--ink);margin-top:3px}
ul.clean{list-style:none;display:flex;flex-direction:column;gap:11px}
ul.clean li{padding-left:28px;position:relative;font-size:15.3px}
ul.clean li::before{content:"✓";position:absolute;left:0;top:0;color:var(--copper);font-weight:700}
.tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.03em;padding:2px 8px;
border-radius:6px;margin-right:8px;vertical-align:middle}
.tag.core{background:var(--core-bg);color:var(--core)}
.tag.flex{background:var(--flex-bg);color:var(--flex)}
ol.steps{list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:14px}
ol.steps li{counter-increment:s;position:relative;padding:14px 16px 14px 56px;background:var(--bg);
border:1px solid var(--line);border-radius:12px}
ol.steps li::before{content:counter(s);position:absolute;left:14px;top:14px;width:30px;height:30px;
border-radius:8px;background:var(--copper);color:#fff;font-weight:700;display:grid;place-items:center}
ol.steps li b{color:var(--navy);display:block;margin-bottom:2px}
ol.steps li span{font-size:14.6px;color:#33434d}
.chk{display:flex;flex-direction:column;gap:10px}
.chk .row{display:flex;align-items:flex-start;gap:11px;font-size:15px;background:var(--bg);
border:1px solid var(--line);border-radius:10px;padding:11px 14px}
.chk .bx{width:20px;height:20px;border:2px solid var(--copper);border-radius:5px;flex:none;margin-top:1px}
table{width:100%;border-collapse:collapse;font-size:14.6px}
table th,table td{text-align:left;padding:11px 13px;border-bottom:1px solid var(--line)}
table th{background:var(--navy);color:#fff;font-weight:600;font-size:13.5px}
table tr:last-child td{border-bottom:none}
table td.t{font-weight:600;color:var(--navy)}
.exc{display:flex;flex-direction:column;gap:14px}
.exc .e{border-left:4px solid var(--copper);background:var(--bg);border-radius:0 12px 12px 0;padding:13px 16px}
.exc .e b{color:var(--navy)}
.exc .e p{font-size:14.6px;color:#33434d;margin-top:3px}
/* self qr */
.selfqr{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:#fff;border:1px dashed var(--copper);
border-radius:14px;padding:16px 18px;margin-top:20px}
.selfqr svg{width:96px;height:96px}
.selfqr .t{font-size:13.5px;color:var(--muted)}
.selfqr .t b{color:var(--navy);display:block;font-size:15px}
footer{background:var(--navy-d);color:#bcd2df;padding:30px 0;font-size:13px;text-align:center;margin-top:20px}
footer a:hover{color:var(--copper-l)}
""".strip()

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700'
             '&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">')

def esc(s):
    return html.escape(str(s), quote=True)

def page_head(title, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<link rel="icon" type="image/png" href="../img/logo-226.png">
{FONT_LINK}
<style>{CSS}
{extra_css}</style>
</head>
<body>"""

TOPBAR = """<header class="topbar"><div class="wrap in">
<a class="brand" href="index.html"><img src="../img/logo-226.png" alt="Villa 226"><b>Villa 226</b></a>
<a class="back" href="index.html">← Tất cả bộ phận</a>
</div></header>"""

FOOTER = f"""<footer><div class="wrap">
{esc(BRAND)} — {esc(BRAND_SUB)} · {esc(COMPANY)}<br>
Hotline/Zalo {esc(HOTLINE)} · Hệ thống quy trình số hoá nội bộ · {esc(VERSION)}
</div></footer>"""

# ---------------------------------------------------------------------------
# Sinh trang bộ phận
# ---------------------------------------------------------------------------
def render_dept(d, qr_svg):
    std_rows = "".join(
        f'<li><span class="tag {lvl.lower()}">{lvl}</span>{esc(txt)}</li>'
        for lvl, txt in d["standards"])
    step_rows = "".join(
        f'<li><b>{esc(t)}</b><span>{esc(det)}</span></li>' for t, det in d["steps"])
    chk_rows = "".join(
        f'<div class="row"><div class="bx"></div><div>{esc(c)}</div></div>' for c in d["checklist"])
    kpi_rows = "".join(
        f'<tr><td class="t">{esc(m)}</td><td>{esc(v)}</td></tr>' for m, v in d["kpi"])
    exc_rows = "".join(
        f'<div class="e"><b>{esc(s)}</b><p>{esc(h)}</p></div>' for s, h in d["exceptions"])

    return f"""{page_head(f'{d["name"]} — Quy trình Villa 226')}
{TOPBAR}
<section class="phero"><div class="wrap">
  <span class="tagcode">{esc(d["icon"])} Mã bộ phận: {esc(d["code"])}</span>
  <div class="eyebrow">Quy trình vận hành số hoá</div>
  <h1>{esc(d["name"])}</h1>
  <p>{esc(d["function"])}</p>
</div></section>

<div class="wrap section">

  <div class="card">
    <h2><span class="no">i</span> Vị trí &amp; Chức năng</h2>
    <div class="role">
      <div class="box"><div class="lb">Chức năng chính</div><div class="vl">{esc(d["function"])}</div></div>
      <div class="box"><div class="lb">Tuyến báo cáo</div><div class="vl">{esc(d["reports"])}</div></div>
      <div class="box"><div class="lb">Phối hợp / Quản lý</div><div class="vl">{esc(d["manages"])}</div></div>
      <div class="box"><div class="lb">Mục tiêu</div><div class="vl">{esc(d["target"])}</div></div>
    </div>
    <div class="selfqr">
      {qr_svg}
      <div class="t"><b>Mã QR bộ phận {esc(d["code"])}</b>Dán mã này tại vị trí làm việc. Nhân viên quét để mở đúng quy trình của mình bất cứ lúc nào.</div>
    </div>
  </div>

  <div class="card">
    <h2><span class="no">1</span> Tiêu chuẩn bắt buộc</h2>
    <ul class="clean">{std_rows}</ul>
    <p class="muted" style="margin-top:14px;font-size:13px"><span class="tag core">CORE</span> chuẩn lõi — giống hệt mọi villa 226. &nbsp; <span class="tag flex">FLEX</span> linh hoạt theo từng cơ sở.</p>
  </div>

  <div class="card">
    <h2><span class="no">2</span> Quy trình thực hiện</h2>
    <ol class="steps">{step_rows}</ol>
  </div>

  <div class="card">
    <h2><span class="no">3</span> Checklist / Biểu mẫu</h2>
    <div class="chk">{chk_rows}</div>
  </div>

  <div class="card">
    <h2><span class="no">4</span> Điểm kiểm soát &amp; KPI</h2>
    <table><thead><tr><th>Chỉ số</th><th>Mục tiêu</th></tr></thead><tbody>{kpi_rows}</tbody></table>
  </div>

  <div class="card">
    <h2><span class="no">5</span> Xử lý ngoại lệ</h2>
    <div class="exc">{exc_rows}</div>
  </div>

</div>
{FOOTER}
</body></html>"""

# ---------------------------------------------------------------------------
# Sinh trang hub
# ---------------------------------------------------------------------------
HUB_CSS = """
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
.dept{background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;
display:flex;flex-direction:column;transition:.25s;box-shadow:0 4px 16px rgba(20,84,122,.05)}
.dept:hover{transform:translateY(-5px);box-shadow:0 16px 36px rgba(20,84,122,.14)}
.dept .top{padding:18px 20px 14px;display:flex;align-items:center;gap:12px;border-bottom:1px solid var(--line)}
.dept .ic{width:46px;height:46px;border-radius:12px;background:var(--navy);color:var(--copper-l);
display:grid;place-items:center;font-size:24px;flex:none}
.dept .code{font-size:12px;font-weight:700;color:var(--copper);letter-spacing:.05em}
.dept .nm{font-family:'Playfair Display';font-weight:700;color:var(--navy);font-size:18px;line-height:1.2}
.dept .body{padding:14px 20px 18px;display:flex;flex-direction:column;gap:14px;flex:1}
.dept .fn{font-size:13.6px;color:var(--muted);flex:1}
.dept .qrbox{display:flex;align-items:center;gap:14px;border-top:1px dashed var(--line);padding-top:14px}
.dept .qrbox svg{width:74px;height:74px;flex:none}
.dept .qrbox .hint{font-size:12px;color:var(--muted)}
.dept .open{display:block;text-align:center;background:var(--navy);color:#fff;font-weight:600;
font-size:14.5px;padding:12px;border-radius:0}
.dept .open:hover{background:var(--navy-d)}
.howto{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin-bottom:26px}
.howto h3{color:var(--navy);font-size:18px;margin-bottom:8px}
.howto ol{margin:0;padding-left:20px;color:#33434d;font-size:14.6px;display:flex;flex-direction:column;gap:5px}
.masterqr{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:linear-gradient(150deg,var(--navy),var(--navy-d));
color:#fff;border-radius:16px;padding:20px 22px;margin-bottom:26px}
.masterqr svg{width:104px;height:104px;background:#fff;padding:7px;border-radius:10px}
.masterqr .t b{display:block;font-size:16px}
.masterqr .t{font-size:13.5px;color:#d3e2ec}
/* print sheet */
.printbar{text-align:center;margin:10px 0 26px}
.printbtn{display:inline-flex;gap:9px;background:var(--copper);color:#fff;font-weight:600;
padding:13px 24px;border-radius:12px;border:none;cursor:pointer;font-size:15px;font-family:inherit}
.printbtn:hover{background:var(--copper-l)}
.sheet{display:none}
@media print{
  .topbar,.phero,.howto,.masterqr,.printbar,.grid,footer{display:none!important}
  body{background:#fff}
  .sheet{display:grid!important;grid-template-columns:repeat(2,1fr);gap:16px;padding:14px 0}
  .sheet .qc{border:1.5px dashed #999;border-radius:12px;padding:16px;text-align:center;page-break-inside:avoid}
  .sheet .qc svg{width:150px;height:150px;margin:0 auto 8px}
  .sheet .qc .nm{font-family:'Playfair Display';font-weight:700;color:#0F3F5C;font-size:16px}
  .sheet .qc .code{font-size:12px;color:#B07A16;font-weight:700;letter-spacing:.05em}
  .sheet .qc .u{font-size:10px;color:#666;margin-top:4px;word-break:break-all}
}
"""

def render_hub(cards_html, sheet_html, master_qr):
    return f"""{page_head('Hệ thống Quy trình số hoá — Villa 226', HUB_CSS)}
<header class="topbar"><div class="wrap in">
<a class="brand" href="../index.html"><img src="../img/logo-226.png" alt="Villa 226"><b>Villa 226</b></a>
<a class="back" href="../index.html">← Trang chủ</a>
</div></header>

<section class="phero"><div class="wrap">
  <div class="eyebrow">Vận hành chuỗi · Nội bộ</div>
  <h1>Hệ thống Quy trình số hoá</h1>
  <p>Mỗi bộ phận của Villa 226 có một trang quy trình riêng và một mã QR. Dán QR tại vị trí làm việc — nhân viên quét là mở ngay vị trí – chức năng, quy trình, checklist và KPI của mình.</p>
</div></section>

<div class="wrap section">

  <div class="masterqr">
    {master_qr}
    <div class="t"><b>QR tổng — mở toàn bộ hệ thống</b>Dán tại khu nhân sự / bảng tin. Quét để vào danh mục tất cả bộ phận.</div>
  </div>

  <div class="howto">
    <h3>Cách dùng</h3>
    <ol>
      <li>In bảng QR (nút bên dưới) và dán mã của từng bộ phận tại đúng vị trí làm việc.</li>
      <li>Nhân viên dùng điện thoại quét QR để mở trang quy trình của bộ phận mình.</li>
      <li>Làm theo các bước, tick checklist, đối chiếu KPI; xem mục Xử lý ngoại lệ khi phát sinh.</li>
      <li>Cập nhật nội dung tại <code>quy-trinh/build.py</code> rồi chạy lại để đồng bộ toàn hệ thống.</li>
    </ol>
  </div>

  <div class="printbar">
    <button class="printbtn" onclick="window.print()">🖨️ In bảng QR để dán</button>
  </div>

  <div class="grid">{cards_html}</div>

  <div class="sheet">{sheet_html}</div>

</div>
{FOOTER}
</body></html>"""

def render_card(d, qr_svg):
    return f"""<div class="dept">
  <div class="top"><div class="ic">{esc(d["icon"])}</div>
    <div><div class="code">MÃ {esc(d["code"])}</div><div class="nm">{esc(d["name"])}</div></div>
  </div>
  <div class="body">
    <div class="fn">{esc(d["function"])}</div>
    <div class="qrbox">{qr_svg}<div class="hint">Quét để mở<br>quy trình bộ phận</div></div>
  </div>
  <a class="open" href="{esc(d["slug"])}.html">Mở quy trình →</a>
</div>"""

def render_sheet_cell(d, qr_svg, url):
    return f"""<div class="qc">{qr_svg}<div class="code">MÃ {esc(d["code"])}</div>
<div class="nm">{esc(d["name"])}</div><div class="u">{esc(url)}</div></div>"""

# ---------------------------------------------------------------------------
# Tạo QR SVG (inline, không phụ thuộc file ngoài) + lưu file .svg
# ---------------------------------------------------------------------------
def qr_svg_inline(data):
    qr = segno.make(data, error="q")
    import io
    buf = io.BytesIO()
    qr.save(buf, kind="svg", border=2, dark=QR_DARK,
            omitsize=True, xmldecl=False, svgns=True)
    return buf.getvalue().decode("utf-8")

def qr_save_file(data, path):
    qr = segno.make(data, error="q")
    qr.save(path, scale=8, border=2, dark=QR_DARK)

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def main():
    portal_path = os.path.join(ROOT, PORTAL_DIR)
    qr_path = os.path.join(ROOT, QR_DIR)
    os.makedirs(portal_path, exist_ok=True)
    os.makedirs(qr_path, exist_ok=True)

    hub_url = f"{BASE_URL}/{PORTAL_DIR}/"
    master_qr = qr_svg_inline(hub_url)
    qr_save_file(hub_url, os.path.join(qr_path, "hub.svg"))

    cards, cells = [], []
    for d in DEPTS:
        url = f"{BASE_URL}/{PORTAL_DIR}/{d['slug']}.html"
        inline = qr_svg_inline(url)
        qr_save_file(url, os.path.join(qr_path, f"{d['slug']}.svg"))
        # trang bộ phận
        with open(os.path.join(portal_path, f"{d['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(render_dept(d, inline))
        cards.append(render_card(d, inline))
        cells.append(render_sheet_cell(d, inline, url))
        print(f"  ✓ {d['code']:>3}  {d['name']}  →  {d['slug']}.html")

    with open(os.path.join(portal_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_hub("\n".join(cards), "\n".join(cells), master_qr))
    print(f"\n  ✓ Hub: {PORTAL_DIR}/index.html  ({len(DEPTS)} bộ phận)")
    print(f"  ✓ QR SVG: {QR_DIR}/  (hub + {len(DEPTS)} bộ phận)")

if __name__ == "__main__":
    print("Đang sinh cổng quy trình số hoá Villa 226...\n")
    main()
    print("\nHoàn tất.")
