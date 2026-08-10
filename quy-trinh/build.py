# -*- coding: utf-8 -*-
"""
Trình sinh CỔNG QUY TRÌNH SỐ HOÁ — VILLA 226
============================================
Nội dung lấy nguyên văn từ bộ tài liệu SOP chính thức của Công ty CP Du lịch 226:
  - Cẩm nang Nhập việc                         -> trang "nhap-viec"
  - Cẩm nang SOP Các Bộ Phận (9 bộ phận)       -> 9 trang bộ phận chức năng
  - SOP-226-KD-01 Quản lý Kinh doanh           -> trang "kinh-doanh"
  - SOP-226-VH-01 Quản lý Vận hành             -> trang "van-hanh"
  - SOP-226-QG-01 Quản gia Villa               -> trang "quan-gia"

Sinh ra:
  - quy-trinh/index.html                (hub: 2 nhóm — Vị trí & vai trò · 9 bộ phận)
  - quy-trinh/<slug>.html               (mỗi vị trí / bộ phận 1 trang)
  - img/qr/<slug>.svg + img/qr/hub.svg  (mã QR trỏ tới từng trang)

Chạy:  python3 quy-trinh/build.py     (cần: pip install segno)
Sửa nội dung ngay trong biến PAGES bên dưới rồi chạy lại để đồng bộ toàn hệ thống.
"""
import os, io, html, glob
import segno

# --------------------------------------------------------------------------- cfg
BASE_URL   = "https://villa226.com"
PORTAL_DIR = "quy-trinh"
QR_DIR     = "img/qr"
QR_DARK    = "#0F3F5C"
COMPANY    = "Công ty Cổ phần Du lịch 226 · MST 3502546503"
ADDRESS    = "226 Huyền Trân Công Chúa, Phường Tam Thắng, TP. Hồ Chí Minh"
EMAIL      = "226villa.travel@gmail.com"
HOTLINE    = "0387 979 797"
VERSION    = "Phiên bản 1.0 · 2026"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------- block helpers
def roleinfo(rows):      return {"k": "roleinfo", "rows": rows}
def selfqr():            return {"k": "selfqr"}
def lead(t):             return {"k": "lead", "text": t}
def p(t):                return {"k": "p", "text": t}
def h(t):                return {"k": "h", "text": t}
def std(items):          return {"k": "std", "items": items}        # [(LEVEL|None, text)]
def steps(items):        return {"k": "steps", "items": items}      # [str] hoặc [(title,detail)]
def ul(items):           return {"k": "ul", "items": items}
def table(head, rows):   return {"k": "table", "head": head, "rows": rows}
def kpi(rows):           return {"k": "kpi", "rows": rows}          # [(truc,chi tieu,cach do,nguong)]
def callout(v, t, b):    return {"k": "callout", "variant": v, "title": t, "body": b}  # v: day|never|note|script
def card(t, blocks, no=None): return {"t": t, "no": no, "blocks": blocks}

# =====================================================================================
# NỘI DUNG
# =====================================================================================
PAGES = []

# ---------------------------------------------------------------- CẨM NANG NHẬP VIỆC
PAGES.append({
 "slug":"nhap-viec","code":"HR","icon":"🎓","group":"chung",
 "name":"Cẩm nang Nhập việc","doc":"Dùng chung mọi nhân viên",
 "function":"Chào mừng bạn gia nhập gia đình 226 — thương hiệu, giá trị, tác phong, quy định chung và lộ trình hội nhập 4 tuần dành cho mọi vị trí.",
 "cards":[
   card("Vị trí & Chức năng",[
     roleinfo([("Áp dụng cho","Mọi nhân viên, mọi bộ phận, mọi villa 226"),
               ("Đọc khi","Ngày đầu nhập việc — trước khi đọc SOP bộ phận"),
               ("Đọc tiếp theo","Cẩm nang Tiêu chuẩn Dịch vụ · SOP bộ phận của bạn")]),
     selfqr(),
   ]),
   card("Về Villa 226",[
     lead("Villa 226 là thương hiệu villa nghỉ dưỡng cao cấp tại Vũng Tàu, thuộc Công ty Cổ phần Du lịch 226 — cho thuê villa riêng tư theo tiêu chuẩn 4–5 sao và đang phát triển thành chuỗi nhiều cơ sở."),
     p("Điều làm 226 khác biệt: khách ở villa 226 nào cũng nhận CÙNG một trải nghiệm và CÙNG một mức chất lượng. Đó là lý do có những tiêu chuẩn thống nhất — để dù bạn làm ở villa nào, khách vẫn nhận ra \"đây là 226\"."),
     table(["Ghi nhớ 4 điều về 226","Nội dung"],[
       ["1. Định vị","\"Resort thu nhỏ của riêng bạn\""],
       ["2. Phong cách","Sang trọng, tinh tế, hiện đại, gần gũi thiên nhiên"],
       ["3. Khách mục tiêu","Gia đình, nhóm bạn, khách doanh nghiệp, nghỉ dưỡng cao cấp"],
       ["4. Trải nghiệm cốt lõi","Riêng tư, dịch vụ chuyên nghiệp, không gian đẹp, tiện nghi đầy đủ"],
     ]),
     table(["Nhận diện","Chuẩn 226"],[
       ["Tên thương hiệu","Villa 226 — Coastal Retreat"],
       ["Màu chủ đạo","Xanh navy biển #14547A + vàng đồng #C89A46"],
       ["Giọng nói với khách","Trang trọng, ấm áp: \"kính chào quý khách\", \"kính mong quý khách\""],
       ["Giờ trả phòng","12:00 trưa (chuẩn toàn chuỗi)"],
     ]),
   ]),
   card("Văn hoá & Tác phong",[
     h("Ba giá trị cốt lõi — quy tắc 3S"),
     table(["Yếu tố","Ý nghĩa"],[
       ["Smile — Nụ cười","Luôn mỉm cười nhẹ, chân thành với khách và đồng đội"],
       ["Speed — Tốc độ","Phản hồi khách ≤ 5 giây, tiếp cận xử lý ≤ 10 giây"],
       ["Sincerity — Chân thành","Quan tâm thật lòng, không giả tạo, không chiếu lệ"],
     ]),
     h("Ba điều LUÔN NHỚ"),
     ul(["Quý khách không bao giờ sai — quan điểm của khách luôn được tôn trọng.",
         "Tranh luận với khách = mất khách và mất thương hiệu.",
         "Không có việc \"không phải của tôi\" — ai nhận yêu cầu, người đó chịu trách nhiệm."]),
     h("Ba KHÔNG trong giao tiếp"),
     ul(["KHÔNG nói trống không, thiếu chủ ngữ (luôn có \"dạ / thưa quý khách\").",
         "KHÔNG tranh luận hay biện minh với khách.",
         "KHÔNG từ chối thẳng — luôn tìm cách thay thế khéo léo."]),
     callout("script","Câu cứu nguy vạn năng",
       "\"Dạ, em kiểm tra / hỗ trợ ngay cho quý khách ạ.\" Sau đó tìm người có thể giúp — không bao giờ để khách chờ trong im lặng."),
   ]),
   card("Quy định chung",[
     h("Giờ giấc & ca làm việc"),
     ul(["Có mặt trước giờ vào ca ít nhất 10–15 phút để dự họp đầu ca.",
         "Báo trước cho quản lý nếu nghỉ hoặc đến muộn — càng sớm càng tốt.",
         "Bàn giao ca đầy đủ trước khi rời đi, không để việc dở cho ca sau tự đoán."]),
     h("Đồng phục & ngoại hình"),
     table(["Hạng mục","Tiêu chuẩn"],[
       ["Đồng phục","Đúng đồng phục 226 theo ca — sạch, phẳng, không nhàu"],
       ["Thẻ nhân viên","Đeo rõ ràng ở ngực trái trong suốt ca làm"],
       ["Tóc & móng","Gọn gàng, sạch sẽ; nữ buộc tóc gọn khi làm việc"],
       ["Mùi cơ thể","Trung tính, sạch sẽ; không dùng nước hoa nồng"],
       ["Giày","Tối màu, sạch, phù hợp công việc"],
     ]),
     callout("never","Quy tắc không bao giờ được phá vỡ",
       "Tuyệt đối tôn trọng sự riêng tư của khách — không có camera trong phòng ngủ, nhà tắm và không gian riêng tư. Đây là lời hứa thương hiệu của 226."),
     h("An toàn"),
     ul(["Biết vị trí cầu dao điện, van nước, bình cứu hoả tại villa mình làm.",
         "Trẻ em dưới 12 tuổi không dùng hồ bơi mà không có người lớn kèm.",
         "Báo ngay khi phát hiện sự cố an toàn — không tự xử lý nếu vượt khả năng."]),
   ]),
   card("Lộ trình hội nhập 4 tuần",[
     table(["Tuần","Mục tiêu","Nội dung chính"],[
       ["1 — Định hướng","Hiểu thương hiệu & giao tiếp cơ bản","Đọc cẩm nang; học 3S và 10-5; học script cơ bản; đi một vòng villa"],
       ["2 — Kỹ năng","Nắm quy trình & SOP bộ phận","Quy trình phục vụ 5 bước; SOP bộ phận mình; thực hành ô \"Ngày đầu tiên\""],
       ["3 — Thực hành kèm cặp","Làm việc thật cùng người senior","Xử lý tình huống thực tế có giám sát; nhận phản hồi mỗi cuối ca"],
       ["4 — Đánh giá & phân cấp","Xác định cấp độ & hướng phát triển","Thi role-play; quản lý chấm điểm; xác định Level"],
     ]),
     table(["Cấp độ","Năng lực"],[
       ["Level 1 — Cơ bản","Việc cơ bản, cần giám sát trực tiếp. Điểm khởi đầu của mọi người mới"],
       ["Level 2 — Thành thục","Đón tiếp và xử lý yêu cầu độc lập, biết gợi ý dịch vụ"],
       ["Level 3 — Chuyên nghiệp","Tiếp khách VIP, xử lý tình huống khó, kèm cặp Level 1"],
     ]),
     callout("note","Lời khuyên cho người mới",
       "Đừng ngại hỏi. Ở 226, người hỏi nhiều là người học nhanh. Không ai kỳ vọng bạn hoàn hảo ngay — chỉ cần chân thành, chịu học và luôn đặt khách lên trước."),
   ]),
 ],
})

# ---------------------------------------------------------------- QUẢN LÝ KINH DOANH
PAGES.append({
 "slug":"kinh-doanh","code":"KD","icon":"💼","group":"role","docid":"SOP-226-KD-01",
 "name":"Quản lý Kinh doanh","doc":"SOP-226-KD-01",
 "function":"Chịu trách nhiệm về doanh thu, lịch bán hàng, dòng tiền thu–chi và toàn bộ báo cáo kinh doanh của hệ thống. Quyết định về TIỀN và LỊCH.",
 "cards":[
   card("Vị trí & Chức năng",[
     roleinfo([("Chức danh","Quản lý Kinh doanh"),
               ("Báo cáo trực tiếp","Giám đốc"),
               ("Phối hợp ngang cấp","Quản lý Vận hành"),
               ("Đầu mối","Duy nhất làm việc với chủ nhà về số liệu kinh doanh")]),
     selfqr(),
     callout("note","Nguyên tắc phân vai",
       "Quản lý Kinh doanh quyết định về TIỀN và LỊCH; Quản lý Vận hành quyết định về CHẤT LƯỢNG và NHÂN SỰ. Mọi quyết định đền bù, phụ thu, giảm giá đều thuộc thẩm quyền Quản lý Kinh doanh."),
     table(["Nhóm công việc","Nội dung trách nhiệm"],[
       ["Quản lý lịch bán hàng","Tư vấn bán khách lẻ & kênh sale/CTV; khoá lịch khi chốt; cập nhật nhóm chủ nhà; chịu trách nhiệm tính chính xác của lịch"],
       ["Chính sách giá & doanh thu","Xây & áp bảng giá theo mùa/lễ/cuối tuần; quy định chiết khấu, phụ thu, cọc và huỷ"],
       ["Quản lý thu – chi","Thu doanh thu; thanh toán chi phí cố định & vận hành; trả lương quản gia, thợ"],
       ["Báo cáo kinh doanh","Lập bộ báo cáo cuối tháng gửi Giám đốc và chủ nhà"],
       ["Kiểm kê","Kiểm kê tồn kho cuối tháng; đối chiếu file đồ dùng trong căn"],
       ["Hỗ trợ vận hành","Chuyển thông tin khách cho vận hành mỗi sáng; theo dõi nhận/trả phòng"],
     ]),
   ]),
   card("Quản lý lịch bán hàng",[
     std([("CORE","Một nguồn lịch duy nhất — mọi kênh phản chiếu về nguồn này, không có lịch riêng cá nhân."),
          ("CORE","Chốt là khoá — khách cọc xong, khoá ngày trên lịch bán & lịch cộng đồng trong ≤15 phút."),
          ("CORE","Không giữ chỗ miệng — giữ tạm chưa cọc tối đa 24 giờ, ghi rõ giờ hết hạn."),
          ("CORE","Trách nhiệm cuối cùng — Quản lý Kinh doanh chịu toàn bộ trách nhiệm nếu trùng lịch.")]),
     h("Quy trình chốt một đơn đặt phòng"),
     table(["Bước","Nội dung","Thời hạn chuẩn"],[
       ["1. Tiếp nhận yêu cầu","Từ khách lẻ, OTA, sale/CTV. Ghi: ngày ở, số đêm, số người, nhu cầu đặc biệt","≤30' giờ HC, ≤2h ngoài giờ"],
       ["2. Kiểm tra lịch trống","Đối chiếu lịch toàn hệ thống; ưu tiên villa phù hợp sức chứa & ngân sách","Ngay khi tiếp nhận"],
       ["3. Báo giá","Giá phòng, số người tối đa, phụ thu vượt người, chính sách cọc & huỷ","Cùng lượt phản hồi"],
       ["4. Giữ chỗ","Đánh dấu \"giữ tạm\" kèm giờ hết hạn 24 giờ","Ngay sau báo giá"],
       ["5. Nhận cọc","Xác nhận cọc theo mức quy định; không giữ quá hạn nếu chưa cọc","Trong 24 giờ"],
       ["6. Khoá lịch","Khoá ngày trên lịch bán & lịch cộng đồng; chuyển \"đã chốt\"","≤15' sau khi có cọc"],
       ["7. Cập nhật chủ nhà","Cập nhật lịch vào nhóm chủ nhà tương ứng","Trong ngày"],
       ["8. Chuyển vận hành","Chuyển thông tin khách theo mẫu chuẩn","Chậm nhất 08:00 ngày trước ngày khách đến"],
     ]),
     callout("note","Mẫu bàn giao khách cho vận hành (trước 08:00 mỗi sáng) [CORE]",
       "Villa · Tên khách đại diện · SĐT · Ngày nhận–trả · Số đêm · Số người (người lớn/trẻ em/tài xế) · Giá đã chốt · Đã cọc · Còn phải thu · Hình thức bảo đảm · Yêu cầu đặc biệt và các cam kết đã hứa. Cam kết không ghi lại là nguyên nhân phổ biến nhất gây phàn nàn khi khách nhận phòng."),
   ]),
   card("Chính sách giá & Quản trị doanh thu",[
     table(["Loại giá","Nguyên tắc áp dụng"],[
       ["Giá ngày thường","Giá nền từng villa theo sức chứa & cấu hình phòng"],
       ["Giá cuối tuần","Đêm thứ Sáu & thứ Bảy, cao hơn giá nền theo tỷ lệ quy định"],
       ["Giá cao điểm","Lễ, tết, hè; kèm điều kiện số đêm tối thiểu"],
       ["Phụ thu vượt người","Trên số người vượt mức bao gồm, theo bảng phụ thu công bố tại villa"],
       ["Phụ thu nhận sớm/trả muộn","Chỉ khi còn lịch trống & Quản lý KD xác nhận; mức theo bảng giá"],
       ["Chiết khấu sale/CTV","Theo mức thống nhất từng kênh; ghi rõ trong đơn để tính doanh thu thuần"],
     ]),
     ul(["Rà soát giá hằng tháng theo công suất thực tế tháng trước & lịch đặt tháng tới.",
         "Công suất thấp: ưu tiên kích cầu KHÔNG phá giá (tặng dịch vụ, ưu đãi số đêm, gói khách quay lại).",
         "Không giảm giá công khai dưới mức sàn đã thống nhất với Giám đốc.",
         "Chính sách cọc & huỷ công bố rõ khi báo giá, ghi trong xác nhận đặt phòng & hợp đồng; mọi ngoại lệ do Giám đốc duyệt."]),
   ]),
   card("Quản lý Thu – Chi",[
     std([("CORE","Mọi khoản thu/chi đều phải có chứng từ (biên nhận, ảnh chuyển khoản, hoá đơn, phiếu chi ký nhận)."),
          ("CORE","Không dùng tiền mặt thu của khách để chi trực tiếp mà không ghi nhận; thu và chi ghi riêng, đối chiếu được."),
          ("CORE","Chi ngoài định mức phải được duyệt trước khi thực hiện."),
          ("CORE","Số liệu thu–chi cập nhật liên tục, không dồn cuối tháng.")]),
     h("Hạn mức phê duyệt chi [FLEX — Giám đốc ấn định]"),
     table(["Giá trị khoản chi","Thẩm quyền","Chứng từ"],[
       ["Dưới 1.000.000đ","QL Vận hành đề xuất, QL Kinh doanh duyệt","Hoá đơn/ảnh chứng từ"],
       ["1–5.000.000đ","QL Kinh doanh duyệt, báo Giám đốc","Phiếu đề nghị chi + báo giá"],
       ["Trên 5.000.000đ","Giám đốc phê duyệt trước khi thực hiện","Phiếu đề nghị chi + ≥2 báo giá"],
       ["Chi khẩn cấp ảnh hưởng khách đang ở","Thực hiện ngay, báo cáo trong 24 giờ","Ảnh hiện trạng + chứng từ bổ sung"],
     ]),
   ]),
   card("Báo cáo kinh doanh",[
     callout("note","Bộ báo cáo cuối tháng [CORE] — chậm nhất ngày 03 tháng kế tiếp",
       "Thống nhất cấu trúc, đơn vị và cách tính giữa mọi villa để so sánh chéo được."),
     table(["Báo cáo","Nội dung bắt buộc","Người nhận"],[
       ["1. Tổng hợp hệ thống","Doanh thu, chi phí, lợi nhuận toàn hệ thống; công suất từng villa; so sánh kỳ trước","Giám đốc"],
       ["2. Lẻ từng căn","Doanh thu, chi phí, lợi nhuận ròng của villa; phần chia theo mô hình hợp tác","Giám đốc & chủ nhà"],
       ["3. Chi tiết thu–chi","Từng khoản theo ngày, phân loại nhóm, kèm chứng từ đối chiếu","Giám đốc"],
       ["4. Vật dụng tồn kho","Tồn đầu kỳ, nhập, xuất, tồn cuối kỳ; chênh lệch & giải trình","Giám đốc"],
     ]),
     ul(["Phần chia lợi nhuận luôn tính trên LỢI NHUẬN RÒNG, không trên doanh thu.",
         "Villa đồng đầu tư: tiền thuê đất là chi phí trước khi chia; chủ đất chỉ nhận MỘT trong hai — tiền thuê HOẶC phần chia, không cả hai.",
         "Mọi con số truy được về chứng từ gốc; không có dòng \"chi phí khác\" lớn mà không diễn giải."]),
     h("Chỉ số theo dõi hằng tháng"),
     table(["Chỉ số","Cách tính"],[
       ["Công suất phòng","Số đêm đã bán / số đêm khả dụng"],
       ["Doanh thu BQ mỗi đêm bán","Tổng doanh thu phòng / số đêm đã bán"],
       ["Doanh thu / đêm khả dụng","Tổng doanh thu phòng / số đêm khả dụng"],
       ["Biên lợi nhuận","Lợi nhuận ròng / doanh thu"],
       ["Tỷ lệ khách quay lại","Số lượt khách cũ / tổng số lượt khách"],
     ]),
   ]),
   card("Chỉ tiêu đánh giá (KPI)",[
     kpi([("1. Hiệu quả kinh tế","Công suất phòng toàn hệ thống","Báo cáo tổng hợp tháng","Đạt mục tiêu kỳ do Giám đốc giao"),
          ("","Biên lợi nhuận toàn hệ thống","Báo cáo tổng hợp tháng","Không giảm so với cùng kỳ"),
          ("2. Chất lượng dữ liệu","Nộp đủ bộ 04 báo cáo đúng hạn","Ngày gửi thực tế","100% trước ngày 03"),
          ("","Tỷ lệ khoản chi có chứng từ đầy đủ","Đối chiếu chứng từ","100%"),
          ("3. Quy trình bán hàng","Số lần trùng lịch trong tháng","Ghi nhận sự cố","0 lần"),
          ("","Thời gian phản hồi yêu cầu đặt phòng","Ghi nhận trên kênh","≥90% trong 30' giờ HC"),
          ("4. Phối hợp & tuân thủ","Gửi danh sách khách trước 08:00 hằng ngày","Nhóm vận hành","≥95% số ngày"),
          ("","Chênh lệch kiểm kê cuối tháng","Biên bản kiểm kê","≤2% giá trị")]),
   ]),
   card("Các điều cấm",[
     table(["Hành vi vi phạm","Mức xử lý"],[
       ["Nhận đặt phòng nhưng không khoá lịch, gây trùng lịch","Nhắc nhở bằng văn bản & chịu chi phí khắc phục"],
       ["Chi tiêu vượt hạn mức mà không có phê duyệt","Bồi hoàn & xử lý kỷ luật"],
       ["Thu tiền khách không có chứng từ/không ghi nhận","Kỷ luật cao nhất, chấm dứt hợp đồng"],
       ["Sửa số liệu báo cáo không đúng thực tế","Chấm dứt hợp đồng"],
       ["Cam kết với khách/chủ nhà ngoài chính sách đã duyệt","Nhắc nhở, chịu phần chênh lệch"],
       ["Nộp báo cáo cuối tháng trễ hạn không lý do","Trừ KPI · Tái phạm: nhắc nhở bằng văn bản"],
     ]),
     h("Biểu mẫu kèm theo"),
     ul(["BM-KD-01: Bảng lịch bán hàng hệ thống (trống / giữ tạm / đã chốt).",
         "BM-KD-02: Mẫu bàn giao thông tin khách cho vận hành.",
         "BM-KD-03: Phiếu đề nghị chi và phê duyệt.",
         "BM-KD-04: Bảng theo dõi thu–chi chi tiết theo ngày.",
         "BM-KD-05: Mẫu báo cáo tổng hợp & báo cáo lẻ từng căn.",
         "BM-KD-06: Biên bản kiểm kê tồn kho cuối tháng."]),
   ]),
 ],
})

# ---------------------------------------------------------------- QUẢN LÝ VẬN HÀNH
PAGES.append({
 "slug":"van-hanh","code":"VH","icon":"🧭","group":"role","docid":"SOP-226-VH-01",
 "name":"Quản lý Vận hành","doc":"SOP-226-VH-01",
 "function":"Giữ mọi villa luôn sẵn sàng đón khách, bảo đảm chất lượng đồng nhất giữa các cơ sở và điều phối toàn bộ đội ngũ quản gia. Quyết định về CHẤT LƯỢNG và NHÂN SỰ.",
 "cards":[
   card("Vị trí & Chức năng",[
     roleinfo([("Chức danh","Quản lý Vận hành"),
               ("Báo cáo trực tiếp","Giám đốc"),
               ("Phối hợp ngang cấp","Quản lý Kinh doanh"),
               ("Quản lý trực tiếp","Đội ngũ quản gia tại các villa")]),
     selfqr(),
     callout("note","Giới hạn thẩm quyền",
       "Quản lý Vận hành KHÔNG quyết định về giá, phụ thu và mức đền bù — các nội dung này thuộc Quản lý Kinh doanh."),
     table(["Nhóm công việc","Nội dung trách nhiệm"],[
       ["Điều phối khách lưu trú","Nhận thông tin khách từ KD; hẹn giờ & báo quản gia đón; đăng ký lưu trú; xử lý phát sinh"],
       ["Kiểm tra villa định kỳ","Tối thiểu 01 lần/tuần mỗi villa; chấm theo checklist chuẩn"],
       ["Bảo trì & sự cố","Tiếp nhận, phân cấp, điều phối xử lý; quản lý đội thợ & nhà cung cấp"],
       ["Vật tư & kho","Phân phát cho quản gia; duy trì tồn tối thiểu; kiểm kê cuối tháng"],
       ["Nhân sự quản gia","Phân ca, giám sát, đào tạo, đánh giá quản gia"],
       ["Trật tự & an toàn","Nhắc trật tự sau 21:30; bảo đảm điều kiện an toàn tại villa"],
     ]),
   ]),
   card("Nhịp làm việc chuẩn",[
     h("Công việc hằng ngày"),
     table(["Mốc giờ","Công việc"],[
       ["08:00–08:30","Nhận danh sách khách trong ngày từ QL Kinh doanh; rà soát yêu cầu đặc biệt & cam kết đã hứa"],
       ["08:30–09:30","Liên hệ khách xác nhận giờ đến; phân công & báo quản gia đón; xác nhận villa đủ vật tư"],
       ["09:30–12:00","Giám sát chuẩn bị villa; xử lý yêu cầu bảo trì tồn đọng"],
       ["12:00–14:00","Theo dõi trả/nhận phòng; xử lý hư hỏng, thất thoát cùng QL Kinh doanh"],
       ["14:00–17:00","Kiểm tra villa theo lịch tuần; cấp phát vật tư; làm việc với thợ & NCC"],
       ["17:00–18:00","Kiểm tra ảnh nghiệm thu villa của quản gia; nhắc việc tồn"],
       ["21:30","Kiểm soát trật tự villa đang có khách; hỗ trợ quản gia khi khách không hợp tác"],
     ]),
     h("Hằng tuần / hằng tháng"),
     ul(["Tuần: kiểm tra thực địa ≥1 lần/villa (ưu tiên đột xuất); rà sự cố bảo trì; rà tồn kho; họp ngắn đội quản gia.",
         "Tháng: kiểm kê tồn kho cùng KD; kiểm kê đồ dùng trong căn cùng quản gia; chấm KPI quản gia; brand audit từng villa gửi Giám đốc."]),
   ]),
   card("Kiểm tra villa định kỳ",[
     ul(["Tần suất tối thiểu 01 lần/tuần mỗi villa; villa có khách liên tục hoặc mới bị phản hồi tiêu cực thì tăng tần suất.",
         "Ưu tiên kiểm tra đột xuất, không báo trước, để thấy đúng thực trạng.",
         "Chấm theo checklist, chụp ảnh minh chứng, gửi nhóm vận hành trong ngày.",
         "Mỗi hạng mục chưa đạt phải có: người chịu trách nhiệm, cách khắc phục, thời hạn cụ thể."]),
     h("Checklist kiểm tra sáu khu vực [CORE]"),
     table(["Khu vực","Tiêu chí Đạt (tóm tắt)"],[
       ["1. Ngoài sân","Sân sạch; cây được tưới; nước hồ trong, không rong rêu/rác; biển hiệu 226 sạch & đủ sáng; đèn hoạt động"],
       ["2. Phòng khách","Bàn bida không bụi, đủ cơ & bi; quạt/điều hoà không bám bụi; nội thất không hư; TV/loa/remote hoạt động"],
       ["3. Phòng bếp","Gia vị còn hạn; dụng cụ đủ, sạch, gọn; tủ lạnh sạch không mùi; bồn rửa khô sạch; thùng rác có bọc"],
       ["4. Phòng ngủ","Tủ không bụi; đồ vải trắng sạch, không ố/mùi, gấp đúng chuẩn; sàn không tóc; đèn/ổ điện hoạt động; điều hoà mát trong 5'"],
       ["5. Nhà vệ sinh","Không đọng nước, không mùi; bồn cầu/lavabo/gương sạch; đủ khăn & đồ dùng; máy sấy hoạt động"],
       ["6. Kho giặt","Đồ sạch & bẩn tách riêng; xếp gọn theo loại; kho khô ráo; có sổ xuất nhập đồ vải"],
     ]),
     h("Thang đánh giá villa"),
     table(["Mức","Điều kiện","Hành động"],[
       ["Xuất sắc","Toàn bộ Đạt, không ghi chú khắc phục","Ghi nhận, làm hình mẫu cho villa khác"],
       ["Tốt","Toàn bộ [CORE] Đạt, ≤2 ghi chú nhỏ","Khắc phục trong 48 giờ"],
       ["Đạt","Toàn bộ [CORE] Đạt, nhiều ghi chú nhỏ","Khắc phục trong 48 giờ & kiểm tra lại trong tuần"],
       ["Chưa đạt","≥1 hạng mục [CORE] không đạt","Khắc phục trước lượt khách kế; báo Giám đốc; không nhận khách nếu liên quan an toàn/vệ sinh nghiêm trọng"],
     ]),
   ]),
   card("Quản lý bảo trì & sự cố",[
     h("Phân cấp sự cố & thời hạn xử lý [CORE]"),
     table(["Cấp","Loại sự cố","Thời hạn"],[
       ["Cấp 1 — Khẩn cấp","Mất điện/nước, cháy nổ, rò rỉ điện, sự cố an toàn hồ bơi, hỏng khoá khi có khách","Xử lý ngay ≤2 giờ; gọi báo Giám đốc"],
       ["Cấp 2 — Ảnh hưởng trải nghiệm","Hỏng điều hoà, nóng lạnh, nghẹt cống, bơm hồ bơi hỏng, mất WiFi","Trong ngày; nếu chưa xong phải có phương án thay thế cho khách"],
       ["Cấp 3 — Không ảnh hưởng khách","Trầy nội thất, bóng đèn phụ, sơn bong, thiết bị dự phòng hỏng","Trong 07 ngày, gộp vào lịch bảo trì định kỳ"],
     ]),
     steps(["Tiếp nhận từ quản gia / đợt kiểm tra, kèm ảnh hiện trạng.",
            "Phân cấp theo bảng và ghi vào sổ theo dõi bảo trì.",
            "Liên hệ thợ/NCC; nếu vượt hạn mức, lập phiếu đề nghị chi gửi KD hoặc Giám đốc.",
            "Trong lúc chờ, chủ động thông báo & trấn an khách với thời gian dự kiến cụ thể.",
            "Nghiệm thu, chụp ảnh kết quả, xác nhận làm cơ sở thanh toán.",
            "Đóng sự cố, ghi rõ nguyên nhân để phân tích hỏng hóc lặp lại."]),
     callout("note","Sự cố lặp lại nhiều villa = vấn đề hệ thống",
       "Nếu cùng một loại sự cố lặp lại ở nhiều villa, đó là vấn đề hệ thống chứ không phải lỗi một cơ sở — cần giải pháp cấp hệ thống (đổi NCC thiết bị, thay đổi định kỳ bảo dưỡng)."),
   ]),
   card("Quản lý & đào tạo đội ngũ quản gia",[
     ul(["Lập lịch trực quản gia theo tuần dựa trên lịch khách; công bố chậm nhất Chủ nhật tuần liền trước.",
         "Mỗi lượt nhận/trả phòng đều có quản gia phụ trách xác định, không để trống nhân sự.",
         "Kiểm tra ảnh nghiệm thu villa của quản gia mỗi ngày; nhắc ngay khi thiếu hoặc chưa đạt."]),
     h("Lộ trình đào tạo"),
     table(["Giai đoạn","Nội dung","Thời lượng"],[
       ["Nhập việc","Hệ thống 226 & lời hứa dịch vụ; quy trình đón/trả phòng; checklist nghiệm thu; các điều cấm","02 ngày kèm cặp trực tiếp"],
       ["Thực hành có giám sát","≥3 lượt khách dưới giám sát của quản gia kinh nghiệm/QL Vận hành","01 tuần đầu"],
       ["Đánh giá thử việc","Chấm theo checklist & phản hồi khách; chỉ giao độc lập khi đạt toàn bộ [CORE]","Cuối tuần thứ hai"],
       ["Đào tạo định kỳ","Họp tuần điểm lại phản hồi khách & nhắc một chuẩn dịch vụ; đào tạo lại khi có chuẩn mới","Hằng tuần"],
     ]),
   ]),
   card("Chỉ tiêu đánh giá (KPI)",[
     kpi([("1. Chất lượng & trải nghiệm","Điểm đánh giá TB các villa phụ trách","Kênh đặt phòng","≥4,5/5"),
          ("","Số phàn nàn vệ sinh, thiết bị, tiếng ồn","Nhóm vận hành","≤2 lượt/tháng toàn hệ thống"),
          ("2. Quy trình vận hành","Tỷ lệ villa được kiểm tra đủ tần suất tuần","Biên bản kiểm tra","100%"),
          ("","Tỷ lệ sự cố xử lý đúng thời hạn theo phân cấp","Sổ theo dõi bảo trì","≥90%"),
          ("3. Tài sản & vật tư","Số lần villa thiếu vật tư bắt buộc khi khách nhận phòng","Ghi nhận từ quản gia & khách","0 lần"),
          ("","Chênh lệch kiểm kê cuối tháng","Biên bản kiểm kê","≤2% giá trị"),
          ("4. Tuân thủ chuẩn thương hiệu","Kết quả brand audit định kỳ","Phiếu brand audit","100% hạng mục [CORE] Đạt"),
          ("","Tỷ lệ quản gia hoàn thành đào tạo nhập việc đúng lộ trình","Hồ sơ đào tạo","100%")]),
   ]),
   card("Các điều cấm",[
     table(["Hành vi vi phạm","Mức xử lý"],[
       ["Không kiểm tra villa đủ tần suất, hoặc chấm checklist khống","Nhắc nhở văn bản · Tái phạm: kỷ luật"],
       ["Để villa nhận khách khi chưa đạt [CORE] về vệ sinh/an toàn","Nhắc nhở văn bản & chịu trách nhiệm hậu quả"],
       ["Tự quyết về giá, phụ thu, mức đền bù với khách","Nhắc nhở bằng văn bản"],
       ["Cấp phát vật tư không ghi chép, gây thất thoát","Bồi hoàn & xử lý kỷ luật"],
       ["Không phản hồi quản gia khi có sự cố ảnh hưởng khách đang ở","Trừ KPI · Tái phạm: nhắc nhở văn bản"],
       ["Tiết lộ thông tin giấy tờ, hình ảnh của khách","Chấm dứt hợp đồng & chịu trách nhiệm pháp luật"],
     ]),
     h("Biểu mẫu kèm theo"),
     ul(["BM-VH-01: Checklist kiểm tra villa định kỳ (6 khu vực, thang 4 mức).",
         "BM-VH-02: Sổ theo dõi sự cố và bảo trì.",
         "BM-VH-03: Phiếu cấp phát vật tư cho quản gia.",
         "BM-VH-04: Biên bản kiểm kê đồ dùng trong căn.",
         "BM-VH-05: Lịch trực quản gia theo tuần.",
         "BM-VH-06: Phiếu đánh giá KPI quản gia hằng tháng."]),
   ]),
 ],
})

# ---------------------------------------------------------------- QUẢN GIA
PAGES.append({
 "slug":"quan-gia","code":"QG","icon":"🛎️","group":"role","docid":"SOP-226-QG-01",
 "name":"Quản gia Villa","doc":"SOP-226-QG-01",
 "function":"Người trực tiếp biến lời hứa dịch vụ 226 thành trải nghiệm thật: chuẩn bị, đón tiếp, chăm sóc và bàn giao — nhất quán ở mọi villa, mọi ca trực.",
 "cards":[
   card("Vị trí & Chức năng",[
     roleinfo([("Chức danh","Quản gia villa (Villa Butler)"),
               ("Báo cáo trực tiếp","Quản lý Vận hành"),
               ("Phối hợp","QL Kinh doanh (lịch, thu tiền, hợp đồng) · Bảo trì · Giặt là"),
               ("Kênh làm việc chính","Nhóm chat vận hành của villa — mọi việc phát sinh phải hiện diện tại đây")]),
     selfqr(),
     callout("never","Quyền quyết định — giới hạn cứng",
       "Quản gia xử lý các yêu cầu thông thường của khách trong phạm vi được giao. KHÔNG có quyền báo giá đền bù, giảm giá, miễn phụ thu, hoặc cam kết dịch vụ ngoài hợp đồng."),
     h("Năm nguyên tắc nghề nghiệp"),
     ul(["Khách luôn đúng về cảm nhận — không tranh cãi; ghi nhận, xin lỗi nếu thuộc trách nhiệm villa, chuyển Quản lý xử lý.",
         "Mọi việc phát sinh đều để lại dấu vết — ảnh, tin nhắn nhóm, biểu mẫu ký nhận; không xử lý \"miệng\".",
         "Không tự ý quyết định về tiền — mọi đền bù, phụ thu, giảm trừ do Quản lý quyết.",
         "Riêng tư là sản phẩm — không quay phim/chụp ảnh khách, không đưa người ngoài vào villa khi có khách.",
         "Sạch là tiêu chuẩn, không phải cảm tính — nghiệm thu bằng checklist chấm điểm."]),
   ]),
   card("Tác phong & Ca làm việc",[
     h("Tác phong cá nhân [CORE]"),
     table(["Hạng mục","Tiêu chuẩn bắt buộc"],[
       ["Trang phục","Đồng phục 226 (hoặc áo tối màu lịch sự), sạch, phẳng; giày/dép kín gọn"],
       ["Vệ sinh cá nhân","Tóc gọn, móng cắt ngắn sạch, không mùi cơ thể/thuốc lá khi tiếp khách"],
       ["Thái độ","Chủ động chào khách trước; luôn mỉm cười; xưng \"anh/chị – em\"; nói câu hoàn chỉnh"],
       ["Điện thoại","Luôn mở máy, còn pin, còn dung lượng ảnh; nhận cuộc gọi Quản lý trong 03 phút giờ làm"],
       ["Cấm tuyệt đối","Uống rượu bia trong ca; ngủ khu vực khách; dùng tiện ích villa cho mục đích cá nhân"],
     ]),
     h("Khung giờ làm việc chuẩn [FLEX theo villa]"),
     table(["Mốc giờ","Công việc"],[
       ["08:00–09:00","Nhận lịch khách trong ngày; xác nhận số khách, giờ đến, yêu cầu đặc biệt"],
       ["09:00–13:00","Kiểm tra – dọn – nghiệm thu villa trước khi khách đến; nhận đồ vải sạch, bổ sung vật dụng"],
       ["12:00","Giờ trả phòng chuẩn — có mặt nhận bàn giao từ khách rời"],
       ["14:00 trở đi","Giờ nhận phòng chuẩn — đón khách, làm thủ tục, bàn giao villa"],
       ["Trong lưu trú","Trực điện thoại, hỗ trợ khách, kiểm tra hồ bơi & khu vực chung"],
       ["21:30","Nhắc khách giữ trật tự; phối hợp QL Vận hành nếu khách không hợp tác"],
     ]),
   ]),
   card("Quy trình A — Chuẩn bị trước khi khách đến",[
     h("Tiếp nhận thông tin khách (T–1 ngày)"),
     p("Trước 20:00 ngày hôm trước, xác nhận lại bằng tin nhắn đủ: tên khách đại diện & SĐT; số người (người lớn/trẻ em/tài xế tách riêng); giờ đến & số đêm; giá đã chốt, đã cọc, còn phải thu; yêu cầu đặc biệt (sinh nhật, BBQ, thêm nệm, thú cưng, đón muộn). Nếu 20:00 chưa có thông tin, chủ động hỏi trong nhóm — không chờ đến sáng."),
     h("Nghiệm thu villa (T–3 giờ) — sáu khu vực"),
     table(["Khu vực","Hạng mục nghiệm thu bắt buộc"],[
       ["1. Sân vườn & lối vào","Sân sạch không rác/lá tồn; cây được tưới; biển hiệu 226 sạch, đủ sáng; đèn lối đi hoạt động; chỗ để xe thông thoáng"],
       ["2. Hồ bơi","Nước trong, không rác/rong rêu; đã xử lý hoá chất theo lịch; phao/ghế sạch gọn; biển cảnh báo độ sâu & nội quy còn nguyên"],
       ["3. Phòng khách","Sàn sạch; bàn bida sạch, đủ cơ & bi; quạt/điều hoà chạy tốt; nội thất không hư; loa/TV/remote hoạt động đủ pin"],
       ["4. Phòng ngủ","Ga–gối–chăn mới hoàn toàn, không ố/mùi, gấp đúng chuẩn; tủ sạch bụi; sàn sạch; đèn/ổ điện hoạt động; điều hoà mát trong 5'"],
       ["5. Nhà vệ sinh","Bồn rửa/cầu/sàn khô sạch; thoát nước không đọng, không mùi; đủ khăn theo số khách +1 dự phòng; đủ dầu gội/sữa tắm/giấy; máy sấy hoạt động"],
       ["6. Bếp & kho giặt","Bếp/bồn rửa/tủ lạnh sạch khô; đủ chén đũa ly xoong nồi theo số khách; gia vị còn hạn; thùng rác bọc mới; kho giặt gọn, đồ sạch tách đồ bẩn"],
     ]),
     callout("note","Bộ vật dụng bắt buộc trước giờ khách đến [CORE]",
       "Bàn chải – kem đánh răng · dầu gội – sữa tắm – xà phòng · khăn tắm, khăn mặt · dép trong nhà · bàn ủi · máy sấy · giấy vệ sinh · gia vị nấu ăn cơ bản · nước uống chào mừng · bao rác dự phòng. Thiếu bất kỳ hạng mục nào phải báo QL Vận hành cấp bổ sung — không để khách phát hiện thiếu."),
     callout("script","Xác nhận sẵn sàng (T–60 phút)",
       "Gửi nhóm vận hành: (1) dòng \"Villa [tên] đã sẵn sàng đón khách\", (2) tối thiểu 06 ảnh — sân/hồ bơi, phòng khách, mỗi phòng ngủ, nhà vệ sinh, bếp. Đây là bằng chứng nghiệm thu & căn cứ đối chiếu nếu tranh chấp hư hỏng khi trả phòng."),
   ]),
   card("Quy trình B — Đón khách & Nhận phòng",[
     p("Có mặt tại villa trước giờ khách đến ít nhất 15 phút. Ấn tượng trong 5 phút đầu quyết định phần lớn đánh giá của khách."),
     steps([("Chào đón & mời vào","\"Kính chào quý khách, em là [tên], quản gia của villa. Rất hân hạnh được đón quý khách tại 226 Villa.\" Mời khách ngồi, mời nước."),
            ("Đối chiếu số lượng khách","Đếm chính xác người lớn/trẻ em/tài xế; đối chiếu đặt phòng. Vượt số lượng: báo lịch sự sẽ có phụ thu & báo ngay QL Kinh doanh xác nhận mức thu TRƯỚC khi nói con số với khách."),
            ("Đăng ký lưu trú","Chụp CCCD hai mặt của khách người lớn, gửi nhóm vận hành để đăng ký; xoá ảnh khỏi điện thoại cá nhân trong ngày."),
            ("Tài sản bảo đảm","Giữ 01 CCCD khách đại diện suốt kỳ, hoặc thu cọc bảo đảm 2.000.000đ nếu khách không gửi giấy tờ; ghi rõ vào hợp đồng & báo nhóm."),
            ("Thu tiền & ký hợp đồng","Thu phần còn lại đúng số QL Kinh doanh xác nhận, không tự giảm/làm tròn/cho nợ. Lập hợp đồng đủ thông tin; chụp ảnh gửi nhóm."),
            ("Bàn giao villa","Dẫn khách đi từng phòng; đếm cùng khách vật dụng dễ thất thoát; hướng dẫn thiết bị & WiFi; chỉ vị trí thiết bị an toàn."),
            ("Dặn dò trước khi rời","Cung cấp số quản gia trực; nhắc trật tự sau 21:30; nhắc gọi trước ≥30 phút khi trả phòng; chúc khách kỳ nghỉ vui vẻ.")]),
     callout("script","Khi phát sinh phụ thu / việc về tiền",
       "\"Kính mong quý khách chờ em ít phút để xác nhận với bộ phận quản lý về mức phụ thu, em sẽ thông tin lại ngay.\" Quản gia không tự đưa ra con số."),
   ]),
   card("Quy trình C — Phục vụ trong kỳ lưu trú",[
     p("Khách luôn có một đầu mối liên hệ duy nhất và liên hệ được. Việc vượt thẩm quyền phải báo nhóm vận hành, không tự ý xử lý."),
     table(["Tình huống","Quản gia xử lý","Báo nhóm"],[
       ["Khách hỏi cách dùng thiết bị","Hướng dẫn trực tiếp","Không"],
       ["Bật/tắt thác nước, hỗ trợ hồ bơi","Thực hiện ngay","Không"],
       ["Khách nhờ mua đồ","Hỗ trợ mua & tính công theo quy định, hoặc cung cấp số shipper","Có — ghi khoản chi hộ"],
       ["Thiết bị hỏng, mất điện/nước, nghẹt cống","Xử lý sơ bộ; trấn an & báo thời gian khắc phục","Có — ngay lập tức"],
       ["Xin thêm khăn, ga, vật dụng","Cấp từ kho dự phòng","Có — để bổ sung kho"],
       ["Nhận thêm người / ở thêm đêm","Không tự quyết","Có — chuyển QL Kinh doanh"],
       ["Phàn nàn chất lượng dịch vụ","Lắng nghe, ghi nhận, xin lỗi nếu thuộc trách nhiệm villa","Có — ngay lập tức"],
       ["Gây ồn sau 21:30","Nhắc nhở lịch sự một lần","Có nếu khách không hợp tác"],
       ["Đề nghị giảm giá, bồi thường, miễn phụ thu","Không cam kết bất cứ điều gì","Có — chuyển Quản lý"],
       ["Sự cố an toàn, tai nạn, cháy nổ, đuối nước","Ưu tiên tuyệt đối cứu người; gọi 115/114","Gọi trực tiếp Quản lý, không nhắn tin"],
     ]),
     callout("script","Nhắc giờ yên tĩnh (21:30)",
       "Đến trực tiếp, nói nhỏ nhẹ, không làm khách mất mặt trước đám đông: \"Kính mong quý khách hỗ trợ giảm âm lượng sau 21:30 để không ảnh hưởng đến các hộ lân cận.\" Nếu tiếp diễn, báo QL Vận hành — tuyệt đối không tranh luận."),
   ]),
   card("Quy trình D — Trả phòng & Nghiệm thu",[
     ul(["Khách báo trả phòng trước ≥30 phút; quản gia có mặt trong 30 phút kể từ khi nhận thông báo. Không thể kịp thì gọi ngay QL Vận hành bố trí người thay.",
         "Kiểm tra lần lượt sáu khu vực, đối chiếu bộ ảnh chụp trước khi khách nhận phòng.",
         "Đếm đủ ga/gối/chăn/khăn từng phòng & vật dụng đã bàn giao (máy sấy, bàn ủi, remote, chén đũa, cơ bida, phao hồ bơi)."]),
     callout("never","Khi phát hiện thiếu / hỏng / dơ bẩn",
       "Chụp ảnh toàn cảnh & cận cảnh, gửi nhóm & chờ Quản lý xác nhận mức đền bù. Chỉ thông báo khách SAU khi Quản lý xác nhận. Quản gia tuyệt đối KHÔNG tự báo giá đền bù — đây là lỗi nghiêm trọng gây tranh chấp."),
     h("Hoàn tất & sau khi khách rời"),
     ul(["Trả CCCD hoặc hoàn cọc sau khi trừ các khoản đã được khách xác nhận; hỏi thăm cảm nhận & mời đánh giá; tiễn khách ra tận xe.",
         "Tắt thiết bị điện không cần thiết, khoá cửa, kiểm tra an ninh.",
         "Tách toàn bộ đồ vải bẩn chuyển giặt là — KHÔNG tái sử dụng đồ vải giữa hai lượt khách trong bất kỳ trường hợp nào.",
         "Báo cáo kết thúc lượt khách vào nhóm, kèm ảnh hiện trạng & danh sách vật dụng cần bổ sung."]),
   ]),
   card("KPI & Các điều cấm",[
     kpi([("1. Chất lượng & trải nghiệm","Điểm đánh giá của khách với villa phụ trách","Điểm TB trên kênh đặt phòng","≥4,5/5"),
          ("","Số lượt phàn nàn về đón tiếp, vệ sinh","Nhóm vận hành","≤1 lượt/tháng"),
          ("2. Quy trình vận hành","Tỷ lệ nghiệm thu villa đúng hạn trước giờ khách đến","Ảnh xác nhận T–60'","≥95%"),
          ("","Tỷ lệ có mặt trong 30' khi khách báo trả phòng","Ghi nhận thời gian nhóm","≥95%"),
          ("3. Tài sản & kiểm kê","Chênh lệch kiểm kê vật dụng cuối tháng","Biên bản cùng QL Vận hành","≤2% giá trị"),
          ("4. Tuân thủ thương hiệu","Điểm brand audit hạng mục thuộc quản gia","Phiếu brand audit","100% [CORE] Đạt")]),
     h("Các điều cấm (trích)"),
     table(["Hành vi vi phạm","Mức xử lý"],[
       ["Cãi nhau, tranh luận gay gắt với khách","Nhắc nhở văn bản · Tái phạm: đình chỉ"],
       ["Tự ý báo giá đền bù, giảm giá, miễn phụ thu","Nhắc nhở & bồi hoàn chênh lệch nếu gây thiệt hại"],
       ["Thu tiền khách nhưng không báo/không nộp đúng quy định","Kỷ luật cao nhất, chấm dứt hợp đồng"],
       ["Để đồ vải cũ chưa thay cho lượt khách mới","Nhắc nhở bằng văn bản"],
       ["Phát tán hình ảnh, thông tin của khách","Chấm dứt hợp đồng & chịu trách nhiệm pháp luật"],
     ]),
   ]),
 ],
})

# =====================================================================================
# 9 BỘ PHẬN CHỨC NĂNG  (Cẩm nang SOP Các Bộ Phận)
# =====================================================================================
def dept_page(slug, code, icon, name, tagline, function, day_one, target, standards,
              steps_list, controls, script=None, note=None, extra_cards=None):
    cards=[
      card("Vị trí & Chức năng",[
        roleinfo([("Chức năng","Bộ phận chức năng — "+tagline),
                  ("Mục tiêu", target),
                  ("Nhãn tiêu chuẩn","CORE = giống hệt mọi villa · FLEX = linh hoạt theo cơ sở")]),
        selfqr(),
        callout("day","Ngày đầu tiên — Bắt đầu từ đây", day_one),
      ]),
      card("Tiêu chuẩn bắt buộc",[ std(standards) ]),
      card("Các bước thực hiện",[ steps(steps_list) ]),
      card("Điểm kiểm soát (làm đúng = biết ngay)",[ ul(controls) ]),
    ]
    if script: cards.append(card("Script chuẩn",[ callout("script","Câu mẫu với khách", script) ]))
    if note:   cards[-1]["blocks"].append(callout("note", note[0], note[1]))
    if extra_cards: cards.extend(extra_cards)
    return {"slug":slug,"code":code,"icon":icon,"group":"dept","name":name,
            "doc":"Cẩm nang SOP Các Bộ Phận","function":function,"cards":cards}

PAGES.append(dept_page(
 "dat-phong-ota","OTA","🗓️","Đặt phòng & OTA",
 "tuyến đầu trên internet, nơi khách gặp Villa 226 lần đầu tiên",
 "Bảo đảm khách đặt phòng dễ dàng, phản hồi nhanh, giá thống nhất mọi kênh và không bao giờ trùng lịch.",
 "1) Đăng nhập tất cả kênh OTA (Booking, Agoda, Airbnb), xem lịch phòng hôm nay. 2) Học trả lời tin nhắn theo mẫu — lịch sự, đúng tên villa. 3) Ghi nhớ: mọi kênh cùng một giá, không tự báo giá khác. 4) Chưa chắc thì hỏi quản lý ngay.",
 "Khách đặt phòng dễ dàng, phản hồi nhanh, giá thống nhất mọi kênh, không trùng lịch.",
 [("CORE","Phản hồi khách ≤ 30 phút giờ hành chính; ngoài giờ ≤ 2 giờ."),
  ("CORE","Giá phòng thống nhất trên tất cả các kênh — không có giá riêng lẻ."),
  ("CORE","Đồng bộ lịch giữa các kênh trong ≤ 15 phút sau mỗi lượt đặt."),
  ("CORE","Văn phong trả lời trang trọng, đúng brand voice 226 (\"kính chào quý khách\")."),
  ("FLEX","Chương trình khuyến mãi theo mùa/địa bàn do cấp chuỗi duyệt.")],
 ["Đầu ca: mở cả 3 kênh OTA, kiểm tra đơn đặt mới / tin nhắn chưa trả lời.",
  "Với mỗi đơn mới: xác nhận ngày nhận–trả, số khách, ghi vào lịch chung ngay.",
  "Trả lời mọi tin nhắn theo mẫu chuẩn, đúng thời gian cam kết.",
  "Chặn (block) ngay ngày đã có khách trên tất cả kênh còn lại để tránh trùng lịch.",
  "Chuyển thông tin khách sắp đến cho bộ phận Đón tiếp trước ít nhất 1 ngày.",
  "Cuối ca: rà lại toàn bộ lịch tuần tới, xác nhận không có xung đột."],
 ["Số lần trùng lịch = 0 (bắt buộc tuyệt đối).",
  "Tỷ lệ tin nhắn được trả lời đúng hạn ≥ 95%.",
  "Không có chênh lệch giá giữa các kênh khi kiểm tra ngẫu nhiên."],
 script="\"Kính chào quý khách, cảm ơn quý khách đã quan tâm đến Villa 226. Villa còn trống trong ngày quý khách chọn. Em xin phép gửi thông tin chi tiết và hỗ trợ quý khách đặt phòng ạ.\"",
))

PAGES.append(dept_page(
 "don-tiep-cham-soc","CS","🤝","Đón tiếp & Chăm sóc khách",
 "\"gương mặt\" của villa — người khách tiếp xúc nhiều nhất",
 "Đón tiếp chu đáo, một đầu mối duy nhất, mang lại trải nghiệm như một resort thu nhỏ riêng tư.",
 "1) Học thuộc quy trình 5 bước phục vụ (Cẩm nang Tiêu chuẩn Dịch vụ). 2) Đi một vòng villa: phòng ngủ, bếp, hồ bơi, cầu dao, bình cứu hoả. 3) Chuẩn bị welcome drink & Welcome Book trước giờ khách đến. 4) Ghi số hotline & tên quản lý ca vào điện thoại.",
 "Khách được đón tiếp chu đáo, luôn có một đầu mối liên hệ, trải nghiệm resort thu nhỏ riêng tư.",
 [("CORE","Giờ trả phòng chuẩn 12:00; villa sẵn sàng trước giờ nhận phòng 60 phút."),
  ("CORE","Mỗi đoàn khách có MỘT đầu mối chăm sóc duy nhất trong suốt kỳ lưu trú."),
  ("CORE","Khách cần hỗ trợ báo trước 30 phút — nhân viên xác nhận lại ngay."),
  ("CORE","Giao tiếp theo chuẩn dịch vụ 226 (3S, quy tắc 10-5, script chuẩn)."),
  ("FLEX","Đối tác dịch vụ tại chỗ (đầu bếp, tour) tuỳ theo từng villa.")],
 ["Trước khi khách đến: kiểm tra villa sẵn sàng, chuẩn bị welcome drink.",
  "Đón khách tại cổng, cúi chào 30°, giới thiệu tên mình.",
  "Làm thủ tục check-in nhanh gọn, trao Welcome Book và số hotline.",
  "Dẫn khách tham quan villa, hướng dẫn sử dụng thiết bị (điều hoà, hồ bơi, bếp).",
  "Trong kỳ lưu trú: chủ động hỏi thăm, hỗ trợ, ghi nhớ nhu cầu đặc biệt.",
  "Check-out: hỗ trợ hành lý, kiểm tra phòng, tiễn khách tận cổng, mời đánh giá."],
 ["Điểm đánh giá khách (OTA + trực tiếp) ≥ 4.7/5.",
  "Tỷ lệ phàn nàn về đón tiếp ≤ 2% số lượt khách.",
  "Villa luôn sẵn sàng đúng mốc \"trước nhận phòng 60 phút\"."],
 script="\"Kính chào quý khách, chào mừng đến với Villa 226. Em là [tên], sẽ đồng hành cùng quý khách suốt kỳ nghỉ. Bất cứ điều gì quý khách cần, xin gọi em qua số hotline trong Welcome Book ạ.\"",
))

PAGES.append(dept_page(
 "buong-phong-ve-sinh","BP","🧺","Buồng phòng & Vệ sinh",
 "quyết định ấn tượng \"sạch sẽ\" — điều khách cảm nhận đầu tiên khi mở cửa phòng",
 "Mỗi khách bước vào không gian sạch tuyệt đối, thơm, gọn gàng — đạt chuẩn 4–5 sao ngay lần đầu nghiệm thu.",
 "1) Học gấp khăn & trải ga theo chuẩn 226 (nhờ nhân viên cũ hướng dẫn). 2) Nguyên tắc vàng: thay TOÀN BỘ đồ vải sau MỖI lượt khách — không ngoại lệ. 3) Xem phiếu nghiệm thu vệ sinh 14 dòng. 4) Biết vị trí kho đồ vải & định mức tồn tối thiểu 3 bộ/vị trí.",
 "Mỗi khách nhận không gian sạch tuyệt đối, đạt nghiệm thu ngay lần đầu.",
 [("CORE","Thay toàn bộ đồ vải (ga, gối, khăn) sau mỗi lượt khách — bắt buộc."),
  ("CORE","Mỗi phòng phải qua phiếu nghiệm thu có ký trước khi bàn giao cho khách."),
  ("CORE","Một dòng \"Chưa đạt\" trên phiếu = CHƯA được bàn giao phòng."),
  ("CORE","Tồn tối thiểu 3 bộ đồ vải mỗi vị trí để luôn có đồ thay."),
  ("FLEX","Loại nước lau sàn / tinh dầu thơm có thể khác theo villa.")],
 ["Thu gom toàn bộ đồ vải bẩn, rác; mở cửa thông thoáng phòng.",
  "Lau bụi từ trên xuống dưới: đèn, kệ, bàn, rồi mới đến sàn.",
  "Vệ sinh nhà tắm: bồn cầu, lavabo, vòi sen, gương — không để vết nước.",
  "Trải ga giường mới, gấp khăn đúng chuẩn, bổ sung amenities đầy đủ.",
  "Kiểm tra mùi phòng, xịt tinh dầu nhẹ; kiểm tra thiết bị điện hoạt động.",
  "Hoàn thành phiếu nghiệm thu 14 dòng, ký tên, báo quản lý bàn giao."],
 ["Tỷ lệ nghiệm thu đạt ngay lần đầu ≥ 90%.",
  "Không có phàn nàn của khách về vệ sinh phòng.",
  "Kho đồ vải luôn đủ định mức tồn tối thiểu."],
))

PAGES.append(dept_page(
 "bao-tri-ky-thuat","BT","🔧","Bảo trì & Kỹ thuật",
 "giữ cho mọi thứ luôn hoạt động — điện, nước, điều hoà, thiết bị",
 "Mọi thiết bị & hạ tầng hoạt động tốt; sự cố xử lý đúng thời gian cam kết theo mức độ khẩn cấp.",
 "1) Đi một vòng ghi vị trí: cầu dao điện, van nước tổng, máy bơm hồ bơi, bình cứu hoả. 2) Học 4 mức độ ưu tiên sự cố & thời gian xử lý. 3) Lưu số thợ điện/nước/điều hoà villa hay dùng. 4) Biết cách báo sự cố: ghi nhật ký + báo quản lý ngay.",
 "Thiết bị & hạ tầng luôn hoạt động; sự cố xử lý đúng cam kết thời gian.",
 [("CORE","4 mức sự cố với thời gian xử lý cố định (bảng dưới) — tuân thủ nghiêm."),
  ("CORE","Mọi sự cố phải ghi vào nhật ký vận hành ngay khi phát sinh."),
  ("CORE","Kiểm tra kỹ thuật định kỳ hằng tuần theo checklist."),
  ("FLEX","Danh sách nhà thầu/thợ tại chỗ do từng villa tự lập.")],
 ["Khi nhận báo sự cố: xác định mức độ (Khẩn cấp / Nghiêm trọng / Thông thường / Định kỳ).",
  "Ghi vào nhật ký: thời gian, vị trí, mô tả sự cố.",
  "Xử lý ngay nếu trong khả năng; nếu không, gọi thợ theo cam kết thời gian.",
  "Nếu ảnh hưởng khách, báo bộ phận Đón tiếp để thông báo và xin lỗi khách.",
  "Sau khắc phục: kiểm tra lại, ghi kết quả vào nhật ký, đóng sự cố.",
  "Hằng tuần: chạy checklist kiểm tra phòng ngừa toàn bộ thiết bị."],
 ["Tỷ lệ sự cố xử lý đúng thời gian cam kết ≥ 95%.",
  "Không có sự cố lặp lại do bỏ qua bảo trì định kỳ.",
  "Nhật ký kỹ thuật được ghi đầy đủ, không ghi dồn."],
 extra_cards=[ card("Bảng phân mức sự cố",[ table(["Mức độ","Thời gian xử lý"],[
    ["Khẩn cấp","≤ 2 giờ (mất điện, mất nước, rò rỉ gas, sự cố an toàn)"],
    ["Nghiêm trọng","≤ 4 giờ (điều hoà hỏng, nóng lạnh không hoạt động)"],
    ["Thông thường","≤ 24 giờ (bóng đèn, vòi nước nhỏ giọt, ổ cắm lỏng)"],
    ["Định kỳ","Theo lịch phòng ngừa hằng tuần/tháng"],
 ]) ]) ],
))

PAGES.append(dept_page(
 "ho-boi-canh-quan","HB","🏊","Hồ bơi & Cảnh quan",
 "giữ điểm nhấn đẹp nhất của villa — hồ bơi và sân vườn",
 "Hồ bơi luôn trong, an toàn, đạt chuẩn vệ sinh; sân vườn gọn đẹp — tạo cảm giác resort nghỉ dưỡng.",
 "1) Học đo pH & mức clo (nhờ người cũ chỉ bộ test). 2) Biết vị trí kho hoá chất — LUÔN khoá riêng, không để trẻ em tiếp cận. 3) Mỗi ngày kiểm tra hồ bơi VÀ ghi nhật ký — không bỏ ngày nào. 4) Kiểm tra biển cảnh báo độ sâu & thiết bị cứu hộ (phao, sào).",
 "Hồ bơi trong, an toàn, có nhật ký mỗi ngày; sân vườn sạch đẹp.",
 [("CORE","Kiểm tra hồ bơi và ghi nhật ký MỖI ngày (chỉ số pH, clo, hoá chất đã dùng)."),
  ("CORE","Hoá chất hồ bơi khoá riêng, tuyệt đối cách ly khỏi khách và trẻ em."),
  ("CORE","Biển cảnh báo độ sâu và thiết bị cứu hộ luôn sẵn sàng tại hồ bơi."),
  ("FLEX","Loại cây cảnh, phong cách sân vườn linh hoạt theo địa phương.")],
 ["Mỗi sáng: đo pH và clo, ghi chỉ số vào nhật ký hồ bơi.",
  "Vớt lá, rác trên mặt nước; kiểm tra hệ thống lọc hoạt động.",
  "Điều chỉnh hoá chất nếu chỉ số ngoài ngưỡng an toàn; ghi lượng đã dùng.",
  "Kiểm tra biển cảnh báo, phao cứu hộ còn nguyên vị trí.",
  "Chăm sóc sân vườn: tưới cây, cắt tỉa, dọn lá theo lịch.",
  "Nếu nước đục/bẩn: tạm dừng hồ bơi, thông báo khách, xử lý trong 2 giờ."],
 ["Tỷ lệ ngày có ghi nhật ký hồ bơi = 100%.",
  "Chỉ số pH/clo luôn trong ngưỡng an toàn khi kiểm tra.",
  "Không có sự cố an toàn liên quan đến hồ bơi."],
))

PAGES.append(dept_page(
 "an-ninh-an-toan","AN","🛡️","An ninh & An toàn",
 "bảo vệ sự riêng tư và an toàn — giá trị cốt lõi của Villa 226",
 "An toàn và riêng tư tuyệt đối cho khách; kiểm soát người ra vào; giữ trật tự và xử lý khẩn cấp.",
 "1) Quy tắc tối quan trọng: TUYỆT ĐỐI không có camera trong không gian riêng tư của khách. 2) Chỉ khách đã đăng ký mới được vào villa. 3) Giờ giữ trật tự: sau 22:00 hạn chế tiếng ồn. 4) Ghi số công an/y tế khẩn cấp địa phương vào điện thoại.",
 "An toàn & riêng tư tuyệt đối cho khách; sự vụ an ninh bằng 0.",
 [("CORE","CẤM TUYỆT ĐỐI camera trong phòng ngủ, nhà tắm và không gian riêng tư của khách."),
  ("CORE","Chỉ khách đã đăng ký mới được vào villa — kiểm soát chặt người lạ."),
  ("CORE","Giữ trật tự sau 22:00, nhắc nhở lịch sự nếu có tiếng ồn lớn."),
  ("FLEX","Danh sách liên hệ khẩn cấp địa phương theo từng villa.")],
 ["Đầu ca: kiểm tra khoá cổng, camera khu vực chung (chỉ khu chung), đèn an ninh.",
  "Xác nhận danh sách khách đang lưu trú; cảnh giác với người lạ tiếp cận.",
  "Tuần tra định kỳ khu vực ngoài villa theo lịch.",
  "Sau 22:00: nhắc nhở nhẹ nhàng nếu khách gây ồn ảnh hưởng xung quanh.",
  "Khi có sự cố an ninh: bảo đảm an toàn khách trước, báo quản lý và cơ quan chức năng.",
  "Ghi mọi sự vụ vào nhật ký, kể cả sự việc nhỏ."],
 ["Số sự vụ an ninh = 0 hoặc được xử lý kịp thời không gây hậu quả.",
  "Không có vi phạm về camera trong không gian riêng tư.",
  "Không có người lạ (không đăng ký) vào được villa."],
 note=("Quy tắc không bao giờ được phá vỡ",
   "Sự riêng tư của khách là lời hứa thương hiệu của Villa 226. Không camera, không quan sát, không xâm phạm không gian riêng của khách trong bất kỳ hoàn cảnh nào."),
))

PAGES.append(dept_page(
 "dich-vu-tang-them","DV","🍽️","Dịch vụ tăng thêm",
 "tạo thêm doanh thu và trải nghiệm — BBQ, đầu bếp, tour, spa, đưa đón",
 "Tăng doanh thu & làm phong phú trải nghiệm qua dịch vụ bổ sung, giới thiệu tinh tế, minh bạch giá.",
 "1) Xem bảng giá dịch vụ đã công bố của villa — học thuộc mức giá. 2) Biết danh sách đối tác đã duyệt (đầu bếp, tour, spa) — chỉ giới thiệu đối tác này. 3) Học gợi ý dịch vụ nhẹ nhàng, đúng lúc — không ép. 4) Gợi ý theo nhu cầu & dịp của khách, không chào bán lan man.",
 "Tăng doanh thu & trải nghiệm với cách giới thiệu tinh tế, minh bạch về giá.",
 [("CORE","Mọi dịch vụ có bảng giá công bố trước — không phát sinh giá bất ngờ."),
  ("CORE","Chỉ giới thiệu đối tác đã được duyệt về chất lượng và an toàn."),
  ("CORE","Không chào bán gây áp lực hoặc làm phiền khách."),
  ("FLEX","Danh mục dịch vụ và đối tác cụ thể linh hoạt theo từng villa.")],
 ["Giới thiệu dịch vụ ngay khi check-in (qua Welcome Book), không ép.",
  "Quan sát nhu cầu khách (gia đình → BBQ; cặp đôi → spa) để gợi ý đúng.",
  "Báo giá rõ ràng, minh bạch trước khi khách quyết định.",
  "Khi khách đồng ý: đặt dịch vụ với đối tác đã duyệt, xác nhận thời gian.",
  "Theo dõi chất lượng dịch vụ đối tác cung cấp, ghi nhận phản hồi khách.",
  "Ghi doanh thu dịch vụ vào báo cáo Thu–Chi của villa."],
 ["Tỷ trọng doanh thu dịch vụ tăng thêm trên tổng doanh thu (theo mục tiêu).",
  "Không có phàn nàn về việc bị chào bán gây phiền.",
  "Đối tác dịch vụ giữ được chất lượng ổn định."],
 script="\"Dạ, villa bên em có dịch vụ đầu bếp nấu tại chỗ và tiệc BBQ ngoài trời, rất phù hợp cho nhóm của quý khách. Em xin phép gửi quý khách bảng giá để tham khảo, quý khách cần thì báo em sắp xếp ạ.\"",
))

PAGES.append(dept_page(
 "kho-vat-tu-mua-sam","KHO","📦","Kho, Vật tư & Mua sắm",
 "bảo đảm không bao giờ thiếu đồ — từ khăn tắm đến amenities",
 "Villa luôn đủ vật tư để vận hành liên tục; kiểm soát tồn kho chặt; vật tư thương hiệu đồng nhất toàn chuỗi.",
 "1) Đi một vòng kho, nắm vị trí từng loại vật tư (đồ vải, amenities, hoá chất, đồ dùng). 2) Xem định mức tồn tối thiểu — dưới mức phải báo đặt thêm. 3) Biết mặt hàng nào mua tập trung cấp chuỗi (đồ có logo). 4) Học cách ghi phiếu kiểm kê hằng tuần.",
 "Villa luôn đủ vật tư; tồn kho kiểm soát chặt; vật tư thương hiệu đồng nhất.",
 [("CORE","Vật tư mang thương hiệu 226 (đồ vải, amenities in logo) mua tập trung cấp chuỗi."),
  ("CORE","Kiểm kê kho hằng tuần theo phiếu chuẩn."),
  ("CORE","Luôn giữ định mức tồn tối thiểu — không để thiếu hàng khi có khách."),
  ("FLEX","Nhà cung cấp vật tư tiêu hao thông thường (rau củ, đồ tươi) linh hoạt theo villa.")],
 ["Nhận và kiểm đếm hàng khi nhập kho, đối chiếu với phiếu đặt.",
  "Sắp xếp vật tư theo khu vực, dán nhãn rõ ràng, hàng cũ dùng trước.",
  "Cấp phát vật tư cho các bộ phận, ghi vào sổ xuất kho.",
  "Kiểm kê hằng tuần: đếm tồn thực tế, so với định mức tối thiểu.",
  "Mặt hàng dưới định mức: lập đề nghị mua, gửi đúng kênh (chuỗi hoặc tại chỗ).",
  "Báo cáo tồn kho và đề xuất mua sắm cho quản lý villa."],
 ["Số lần thiếu hàng khi cần = 0.",
  "Chênh lệch kiểm kê (thực tế vs sổ sách) trong ngưỡng cho phép.",
  "Vật tư thương hiệu đồng nhất giữa các villa."],
))

PAGES.append(dept_page(
 "tai-chinh-bao-cao","TC","📊","Tài chính & Báo cáo cơ sở",
 "ghi lại dòng tiền của villa — nền tảng để chuỗi so sánh và ra quyết định",
 "Ghi chép trung thực, thống nhất mọi khoản thu–chi; cung cấp số liệu chuẩn để chuỗi so sánh chéo.",
 "1) Xem mẫu báo cáo Thu–Chi chuẩn của chuỗi — mọi villa dùng cùng một mẫu. 2) Nguyên tắc: ghi doanh thu theo NGÀY LƯU TRÚ, không phải ngày nhận tiền. 3) Tách riêng chi phí đầu tư (một lần) & chi phí vận hành (hằng tháng). 4) Hạn chốt: báo cáo tháng trước ngày 05 tháng sau.",
 "Số liệu minh bạch, đối chiếu được, báo cáo đúng hạn để so sánh chéo toàn chuỗi.",
 [("CORE","Dùng đúng mẫu Thu–Chi thống nhất của chuỗi — không tự tạo mẫu riêng."),
  ("CORE","Ghi doanh thu theo ngày lưu trú của khách (không theo ngày nhận tiền)."),
  ("CORE","Tách bạch chi phí đầu tư (một lần) khỏi chi phí vận hành (định kỳ)."),
  ("CORE","Chốt sổ và nộp báo cáo trước ngày 05 hằng tháng."),
  ("FLEX","Nhà cung cấp/đối tác thanh toán tại chỗ linh hoạt theo villa.")],
 ["Ghi mọi khoản thu (tiền phòng, dịch vụ) vào mẫu Thu–Chi ngay khi phát sinh.",
  "Ghi mọi khoản chi kèm chứng từ; phân loại đúng nhóm (vận hành / đầu tư).",
  "Đối chiếu số tiền thực nhận với đơn đặt phòng OTA.",
  "Cuối tháng: tổng hợp thu–chi, tính lợi nhuận ròng của villa.",
  "Chốt sổ trước ngày 05, gửi báo cáo cho kế toán chuỗi.",
  "Lưu chứng từ tối thiểu theo quy định để phục vụ kiểm tra và brand audit."],
 ["Báo cáo nộp đúng hạn (trước ngày 05) = 100%.",
  "Số liệu khớp giữa OTA, tiền thực nhận và báo cáo.",
  "Phân loại chi phí đúng, không lẫn đầu tư vào vận hành."],
 note=("Lưu ý quan trọng",
   "Ghi doanh thu theo ngày lưu trú và tách chi phí đầu tư khỏi vận hành là hai nguyên tắc giúp so sánh công bằng giữa các villa. Ghi sai hai điểm này sẽ làm sai lệch toàn bộ đánh giá hiệu quả của cơ sở."),
))

# =====================================================================================
# RENDER
# =====================================================================================
CSS = """
:root{--navy:#14547A;--navy-d:#0F3F5C;--copper:#C89A46;--copper-l:#DDB86A;
--bg:#EEF3F6;--ink:#222;--muted:#5C6B75;--line:#D6E0E6;--white:#fff;
--core:#0F7A4E;--core-bg:#E4F3EC;--flex:#B07A16;--flex-bg:#FBF1DC;}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Be Vietnam Pro',system-ui,-apple-system,sans-serif;color:var(--ink);
background:var(--bg);line-height:1.62;-webkit-font-smoothing:antialiased}
h1,h2,h3,.display{font-family:'Playfair Display',serif;font-weight:600;line-height:1.18}
a{color:inherit;text-decoration:none}
img,svg{max-width:100%;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.muted{color:var(--muted)}
.topbar{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid var(--line)}
.topbar .in{display:flex;align-items:center;justify-content:space-between;height:62px}
.brand{display:flex;align-items:center;gap:10px}
.brand img{height:42px;width:auto;mix-blend-mode:multiply}
.brand b{font-family:'Playfair Display';color:var(--navy);font-size:19px;font-weight:700}
.back{font-size:14px;font-weight:600;color:var(--navy);border:1.5px solid var(--line);padding:8px 14px;border-radius:10px}
.back:hover{border-color:var(--navy)}
.phero{background:linear-gradient(150deg,var(--navy),var(--navy-d));color:#fff;padding:42px 0 38px;position:relative;overflow:hidden}
.phero::after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 85% 15%,rgba(200,154,70,.22),transparent 45%)}
.phero .wrap{position:relative}
.eyebrow{font-weight:600;letter-spacing:.16em;text-transform:uppercase;font-size:12px;color:var(--copper-l)}
.phero h1{font-size:clamp(25px,4vw,38px);margin:9px 0 8px;color:#fff}
.phero p{color:#d3e2ec;max-width:64ch;font-weight:300}
.tagcode{display:inline-flex;gap:8px;align-items:center;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);
color:#fff;font-weight:600;font-size:13px;padding:5px 13px;border-radius:100px;margin-bottom:8px}
.section{padding:36px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px 26px;margin-bottom:18px;box-shadow:0 4px 16px rgba(20,84,122,.05)}
.card>h2{color:var(--navy);font-size:21px;margin-bottom:15px;display:flex;align-items:center;gap:11px}
.card>h2 .no{width:30px;height:30px;border-radius:8px;background:var(--navy);color:var(--copper-l);
font-family:'Be Vietnam Pro';font-weight:700;font-size:14px;display:grid;place-items:center;flex:none}
.card h3.sub{color:var(--navy);font-size:16.5px;font-family:'Be Vietnam Pro';font-weight:700;margin:18px 0 10px}
.card h3.sub:first-child{margin-top:0}
.card p{margin:0 0 4px;font-size:15.2px}
.card p.lead{font-size:16px;color:#33434d}
.role{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:4px}
@media(max-width:640px){.role{grid-template-columns:1fr}}
.role .box{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:13px 15px}
.role .box .lb{font-size:11.5px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--copper)}
.role .box .vl{font-size:14.6px;color:var(--ink);margin-top:3px}
ul.clean{list-style:none;display:flex;flex-direction:column;gap:9px;margin:2px 0}
ul.clean li{padding-left:26px;position:relative;font-size:15px}
ul.clean li::before{content:"✓";position:absolute;left:0;top:0;color:var(--copper);font-weight:700}
.tag{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.03em;padding:2px 7px;border-radius:6px;margin-right:7px;vertical-align:middle}
.tag.core{background:var(--core-bg);color:var(--core)}
.tag.flex{background:var(--flex-bg);color:var(--flex)}
ol.steps{list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:12px;margin:0}
ol.steps li{counter-increment:s;position:relative;padding:13px 15px 13px 54px;background:var(--bg);border:1px solid var(--line);border-radius:12px}
ol.steps li::before{content:counter(s);position:absolute;left:13px;top:13px;width:29px;height:29px;border-radius:8px;background:var(--copper);color:#fff;font-weight:700;display:grid;place-items:center}
ol.steps li b{color:var(--navy);display:block;margin-bottom:2px}
ol.steps li span{font-size:14.4px;color:#33434d}
.tbl{overflow-x:auto;margin:4px 0}
table{width:100%;border-collapse:collapse;font-size:14.3px;min-width:440px}
table th,table td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
table th{background:var(--navy);color:#fff;font-weight:600;font-size:13px}
table tr:last-child td{border-bottom:none}
table td:first-child{font-weight:600;color:var(--navy)}
table.kpi td:nth-child(2),table.kpi td:nth-child(3){font-weight:400;color:var(--ink)}
.co{border-radius:0 12px 12px 0;padding:14px 16px 14px 17px;margin:12px 0 2px;border-left:4px solid}
.co .ct{font-weight:700;margin-bottom:3px;font-size:14.5px}
.co .cb{font-size:14.4px;color:#33434d}
.co.day{background:var(--flex-bg);border-color:var(--copper)}.co.day .ct{color:#8a5e12}
.co.never{background:#FBEBE7;border-color:#C0492E}.co.never .ct{color:#A33A22}
.co.note{background:#EAF1F6;border-color:var(--navy)}.co.note .ct{color:var(--navy-d)}
.co.script{background:#EFF6F1;border-color:var(--core)}.co.script .ct{color:var(--core)}
.co.script .cb{font-style:italic}
.selfqr{display:flex;align-items:center;gap:16px;flex-wrap:wrap;background:#fff;border:1px dashed var(--copper);border-radius:14px;padding:14px 16px;margin:14px 0 2px}
.selfqr svg{width:88px;height:88px}
.selfqr .t{font-size:13px;color:var(--muted)}.selfqr .t b{color:var(--navy);display:block;font-size:14.5px}
footer{background:var(--navy-d);color:#bcd2df;padding:28px 0;font-size:13px;text-align:center;margin-top:16px}
footer a:hover{color:var(--copper-l)}
"""

HUB_CSS = """
.howto{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin-bottom:22px}
.howto h3{color:var(--navy);font-size:17px;margin-bottom:8px}
.howto ol{margin:0;padding-left:18px;color:#33434d;font-size:14.4px;display:flex;flex-direction:column;gap:5px}
.howto .note2{margin-top:12px;font-size:13.4px;color:var(--muted);border-top:1px dashed var(--line);padding-top:10px}
.masterqr{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:linear-gradient(150deg,var(--navy),var(--navy-d));color:#fff;border-radius:16px;padding:18px 20px;margin-bottom:22px}
.masterqr svg{width:100px;height:100px;background:#fff;padding:7px;border-radius:10px}
.masterqr .t b{display:block;font-size:16px}.masterqr .t{font-size:13.3px;color:#d3e2ec}
.grouphd{display:flex;align-items:baseline;gap:12px;margin:26px 0 16px}
.grouphd h2{color:var(--navy);font-size:22px}
.grouphd .cnt{font-size:13px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
.dept{background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;transition:.25s;box-shadow:0 4px 16px rgba(20,84,122,.05)}
.dept:hover{transform:translateY(-5px);box-shadow:0 16px 36px rgba(20,84,122,.14)}
.dept.role{border-color:#cfe0d8}
.dept .top{padding:16px 18px 12px;display:flex;align-items:center;gap:12px;border-bottom:1px solid var(--line)}
.dept .ic{width:44px;height:44px;border-radius:12px;background:var(--navy);color:var(--copper-l);display:grid;place-items:center;font-size:23px;flex:none}
.dept.role .ic{background:var(--copper)}
.dept .code{font-size:11.5px;font-weight:700;color:var(--copper);letter-spacing:.05em}
.dept .nm{font-family:'Playfair Display';font-weight:700;color:var(--navy);font-size:17.5px;line-height:1.2}
.dept .body{padding:13px 18px 16px;display:flex;flex-direction:column;gap:12px;flex:1}
.dept .fn{font-size:13.3px;color:var(--muted);flex:1}
.dept .docid{font-size:11px;color:var(--copper);font-weight:600}
.dept .qrbox{display:flex;align-items:center;gap:13px;border-top:1px dashed var(--line);padding-top:12px}
.dept .qrbox svg{width:70px;height:70px;flex:none}
.dept .qrbox .hint{font-size:11.5px;color:var(--muted)}
.dept .open{display:block;text-align:center;background:var(--navy);color:#fff;font-weight:600;font-size:14px;padding:11px}
.dept.role .open{background:var(--navy-d)}
.dept .open:hover{background:var(--copper)}
.printbar{text-align:center;margin:8px 0 22px}
.printbtn{display:inline-flex;gap:9px;background:var(--copper);color:#fff;font-weight:600;padding:12px 24px;border-radius:12px;border:none;cursor:pointer;font-size:15px;font-family:inherit}
.printbtn:hover{background:var(--copper-l)}
.sheet{display:none}
@media print{
  .topbar,.phero,.howto,.masterqr,.printbar,.grid,.grouphd,footer{display:none!important}
  body{background:#fff}
  .sheet{display:grid!important;grid-template-columns:repeat(2,1fr);gap:14px;padding:12px 0}
  .sheet .qc{border:1.5px dashed #999;border-radius:12px;padding:14px;text-align:center;page-break-inside:avoid}
  .sheet .qc svg{width:150px;height:150px;margin:0 auto 8px}
  .sheet .qc .nm{font-family:'Playfair Display';font-weight:700;color:#0F3F5C;font-size:15px}
  .sheet .qc .code{font-size:11px;color:#B07A16;font-weight:700;letter-spacing:.05em}
  .sheet .qc .u{font-size:9.5px;color:#666;margin-top:4px;word-break:break-all}
}
"""

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700'
 '&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">')

def esc(s): return html.escape(str(s), quote=True)

def head(title, extra=""):
    return (f'<!DOCTYPE html>\n<html lang="vi">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{esc(title)}</title>\n<link rel="icon" type="image/png" href="../img/logo-226.png">\n'
            f'{FONT_LINK}\n<style>{CSS}{extra}</style>\n</head>\n<body>')

FOOTER = (f'<footer><div class="wrap">226 VILLA — COASTAL RETREAT · {esc(COMPANY)}<br>'
          f'{esc(ADDRESS)} · {esc(EMAIL)} · Hotline/Zalo {esc(HOTLINE)}<br>'
          f'Hệ thống quy trình số hoá nội bộ · {esc(VERSION)}</div></footer>')

# ---- block renderer ----
def r_block(b, qr_svg):
    k=b["k"]
    if k=="lead":  return f'<p class="lead">{esc(b["text"])}</p>'
    if k=="p":     return f'<p>{esc(b["text"])}</p>'
    if k=="h":     return f'<h3 class="sub">{esc(b["text"])}</h3>'
    if k=="ul":    return '<ul class="clean">'+"".join(f'<li>{esc(x)}</li>' for x in b["items"])+'</ul>'
    if k=="std":
        out=[]
        for lvl,txt in b["items"]:
            tag=f'<span class="tag {lvl.lower()}">{lvl}</span>' if lvl else ""
            out.append(f'<li>{tag}{esc(txt)}</li>')
        return '<ul class="clean">'+"".join(out)+'</ul>'
    if k=="steps":
        out=[]
        for it in b["items"]:
            if isinstance(it,tuple): out.append(f'<li><b>{esc(it[0])}</b><span>{esc(it[1])}</span></li>')
            else: out.append(f'<li><span>{esc(it)}</span></li>')
        return '<ol class="steps">'+"".join(out)+'</ol>'
    if k=="table":
        th="".join(f'<th>{esc(x)}</th>' for x in b["head"])
        tr="".join('<tr>'+"".join(f'<td>{esc(c)}</td>' for c in row)+'</tr>' for row in b["rows"])
        return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    if k=="kpi":
        th='<th>Trục</th><th>Chỉ tiêu</th><th>Cách đo</th><th>Ngưỡng Đạt</th>'
        tr="".join('<tr>'+"".join(f'<td>{esc(c)}</td>' for c in row)+'</tr>' for row in b["rows"])
        return f'<div class="tbl"><table class="kpi"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    if k=="callout":
        return f'<div class="co {b["variant"]}"><div class="ct">{esc(b["title"])}</div><div class="cb">{esc(b["body"])}</div></div>'
    if k=="roleinfo":
        boxes="".join(f'<div class="box"><div class="lb">{esc(l)}</div><div class="vl">{esc(v)}</div></div>' for l,v in b["rows"])
        return f'<div class="role">{boxes}</div>'
    if k=="selfqr":
        return (f'<div class="selfqr">{qr_svg}<div class="t"><b>Mã QR quy trình này</b>'
                f'Dán tại vị trí làm việc. Nhân viên quét để mở đúng quy trình bất cứ lúc nào.</div></div>')
    return ""

def render_page(pg, qr_svg):
    doc_line = pg.get("doc","")
    hero_code = f'{pg["icon"]} Mã: {pg["code"]}' + (f' · {doc_line}' if doc_line else "")
    cards_html=[]
    for i,c in enumerate(pg["cards"]):
        no = c["no"] if c["no"] is not None else ("i" if i==0 else i)
        blocks="".join(r_block(b, qr_svg) for b in c["blocks"])
        cards_html.append(f'<div class="card"><h2><span class="no">{esc(no)}</span> {esc(c["t"])}</h2>{blocks}</div>')
    return f"""{head(pg["name"]+' — Quy trình Villa 226')}
<header class="topbar"><div class="wrap in">
<a class="brand" href="index.html"><img src="../img/logo-226.png" alt="Villa 226"><b>Villa 226</b></a>
<a class="back" href="index.html">← Tất cả quy trình</a>
</div></header>
<section class="phero"><div class="wrap">
  <span class="tagcode">{esc(hero_code)}</span>
  <div class="eyebrow">Quy trình vận hành số hoá</div>
  <h1>{esc(pg["name"])}</h1>
  <p>{esc(pg["function"])}</p>
</div></section>
<div class="wrap section">
{"".join(cards_html)}
</div>
{FOOTER}
</body></html>"""

# ---- hub ----
def render_card(pg, qr_svg):
    role = "role" if pg["group"] in ("role","chung") else ""
    docid = f'<div class="docid">{esc(pg["doc"])}</div>' if pg.get("doc") else ""
    return (f'<div class="dept {role}"><div class="top"><div class="ic">{esc(pg["icon"])}</div>'
            f'<div><div class="code">MÃ {esc(pg["code"])}</div><div class="nm">{esc(pg["name"])}</div></div></div>'
            f'<div class="body">{docid}<div class="fn">{esc(pg["function"])}</div>'
            f'<div class="qrbox">{qr_svg}<div class="hint">Quét để mở<br>quy trình</div></div></div>'
            f'<a class="open" href="{esc(pg["slug"])}.html">Mở quy trình →</a></div>')

def render_cell(pg, qr_svg, url):
    return (f'<div class="qc">{qr_svg}<div class="code">MÃ {esc(pg["code"])}</div>'
            f'<div class="nm">{esc(pg["name"])}</div><div class="u">{esc(url)}</div></div>')

def render_hub(groups, sheet_html, master_qr):
    body=[]
    labels={"role":"Vị trí quản lý & Quản gia","chung":"Tài liệu chung","dept":"9 Bộ phận chức năng"}
    order=["role","chung","dept"]
    for g in order:
        items=groups.get(g,[])
        if not items: continue
        body.append(f'<div class="grouphd"><h2>{esc(labels[g])}</h2><span class="cnt">{len(items)} trang</span></div>')
        body.append('<div class="grid">'+"".join(items)+'</div>')
    return f"""{head('Hệ thống Quy trình số hoá — Villa 226', HUB_CSS)}
<header class="topbar"><div class="wrap in">
<a class="brand" href="../index.html"><img src="../img/logo-226.png" alt="Villa 226"><b>Villa 226</b></a>
<a class="back" href="../index.html">← Trang chủ</a>
</div></header>
<section class="phero"><div class="wrap">
  <div class="eyebrow">Vận hành chuỗi · Nội bộ</div>
  <h1>Hệ thống Quy trình số hoá</h1>
  <p>Toàn bộ SOP của Villa 226 theo từng vị trí và bộ phận. Mỗi trang có một mã QR — dán tại nơi làm việc, nhân viên quét là mở ngay quy trình của mình.</p>
</div></section>
<div class="wrap section">
  <div class="masterqr">{master_qr}
    <div class="t"><b>QR tổng — mở toàn bộ hệ thống</b>Dán tại khu nhân sự / bảng tin. Quét để vào danh mục tất cả quy trình.</div>
  </div>
  <div class="howto">
    <h3>Cách dùng</h3>
    <ol>
      <li>In bảng QR (nút bên dưới) và dán mã của từng vị trí/bộ phận tại đúng nơi làm việc.</li>
      <li>Nhân viên dùng điện thoại quét QR để mở trang quy trình tương ứng.</li>
      <li>Làm theo các bước, đối chiếu tiêu chuẩn CORE/FLEX, KPI và mục điều cấm.</li>
    </ol>
    <div class="note2"><b>Phân biệt:</b> nhóm <b>Vị trí</b> là con người (Quản lý Kinh doanh, Quản lý Vận hành, Quản gia); nhóm <b>Bộ phận</b> là nhóm công việc. Một quản gia có thể đảm nhận nhiều bộ phận chức năng tại villa nhỏ.</div>
  </div>
  <div class="printbar"><button class="printbtn" onclick="window.print()">🖨️ In bảng QR để dán</button></div>
  {"".join(body)}
  <div class="sheet">{sheet_html}</div>
</div>
{FOOTER}
</body></html>"""

# ---- QR ----
def qr_inline(data):
    qr=segno.make(data, error="q"); buf=io.BytesIO()
    qr.save(buf, kind="svg", border=2, dark=QR_DARK, omitsize=True, xmldecl=False, svgns=True)
    return buf.getvalue().decode("utf-8")

def qr_file(data, path):
    segno.make(data, error="q").save(path, scale=8, border=2, dark=QR_DARK)

# ---- main ----
def main():
    portal=os.path.join(ROOT,PORTAL_DIR); qrp=os.path.join(ROOT,QR_DIR)
    os.makedirs(portal,exist_ok=True); os.makedirs(qrp,exist_ok=True)
    # dọn QR & html cũ không còn dùng
    valid_slugs={pg["slug"] for pg in PAGES}
    for f in glob.glob(os.path.join(qrp,"*.svg")):
        b=os.path.splitext(os.path.basename(f))[0]
        if b!="hub" and b not in valid_slugs: os.remove(f); print("  - gỡ QR cũ:",b)
    for f in glob.glob(os.path.join(portal,"*.html")):
        b=os.path.splitext(os.path.basename(f))[0]
        if b!="index" and b not in valid_slugs: os.remove(f); print("  - gỡ trang cũ:",b)

    hub_url=f"{BASE_URL}/{PORTAL_DIR}/"
    master=qr_inline(hub_url); qr_file(hub_url, os.path.join(qrp,"hub.svg"))
    groups={}; cells=[]
    for pg in PAGES:
        url=f"{BASE_URL}/{PORTAL_DIR}/{pg['slug']}.html"
        inl=qr_inline(url); qr_file(url, os.path.join(qrp,f"{pg['slug']}.svg"))
        open(os.path.join(portal,f"{pg['slug']}.html"),"w",encoding="utf-8").write(render_page(pg,inl))
        groups.setdefault(pg["group"],[]).append(render_card(pg,inl))
        cells.append(render_cell(pg,inl,url))
        print(f"  ✓ {pg['code']:>3}  {pg['name']}")
    open(os.path.join(portal,"index.html"),"w",encoding="utf-8").write(render_hub(groups,"".join(cells),master))
    print(f"\n  ✓ Hub: {PORTAL_DIR}/index.html  ({len(PAGES)} trang)")

if __name__=="__main__":
    print("Đang sinh cổng quy trình số hoá Villa 226...\n")
    main()
    print("\nHoàn tất.")
