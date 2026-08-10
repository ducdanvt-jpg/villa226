# -*- coding: utf-8 -*-
"""
Sinh HỆ THỐNG QUY TRÌNH SỐ HOÁ — VILLA 226  (một file SPA: quy-trinh.html)
=========================================================================
Cùng kiến trúc bản Ngọc Tước: đăng nhập bằng QR (#login=user~pass), header +
tabs theo vị trí, tab Tổng quan kèm Văn hoá & Tiêu chuẩn chung, trang Quản trị
tạo/in QR + bảng tài khoản. QR vẽ client-side bằng thư viện JS nhúng sẵn.

Nội dung lấy từ bộ SOP chính thức của Công ty CP Du lịch 226.
Sửa dữ liệu trong DATA bên dưới rồi chạy:  python3 quy-trinh/build_app.py
Xuất ra:  quy-trinh.html (thư mục gốc repo → https://villa226.com/quy-trinh.html)
"""
import os, json

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "quy-trinh", "_assets")
OUT    = os.path.join(ROOT, "quy-trinh.html")
QR_DARK = "#0F3F5C"
BASE_URL_DEFAULT = "https://villa226.com/quy-trinh.html"

QRLIB = open(os.path.join(ASSETS, "qrlib.js"), encoding="utf-8").read()
LOGO  = open(os.path.join(ASSETS, "logo226.datauri.txt"), encoding="utf-8").read().strip()

# =====================================================================================
# DỮ LIỆU
# =====================================================================================
COMMON = {
  "code": "CN-226", "title": "Văn hoá & Tiêu chuẩn 226",
  "intro": "Nền tảng chung cho mọi vị trí. Khách ở villa 226 nào cũng nhận cùng một trải nghiệm — bạn chính là trải nghiệm 226.",
  "blocks": [
    {"h": "Định vị & Nhận diện", "items": [
      "Định vị: “Resort thu nhỏ của riêng bạn” — riêng tư, sang trọng, gần gũi thiên nhiên.",
      "Màu thương hiệu: xanh navy #14547A + vàng đồng #C89A46.",
      "Giọng nói với khách: trang trọng, ấm áp — “kính chào quý khách”, “kính mong quý khách”.",
      "Giờ nhận phòng 14:00 · giờ trả phòng 12:00 (chuẩn toàn chuỗi)."]},
    {"h": "Nguyên tắc 3S", "items": [
      "Smile — luôn mỉm cười nhẹ, chân thành với khách và đồng đội.",
      "Speed — phản hồi khách ≤ 5 giây, tiếp cận xử lý ≤ 10 giây.",
      "Sincerity — quan tâm thật lòng, không giả tạo, không chiếu lệ."]},
    {"h": "Ba điều LUÔN NHỚ", "items": [
      "Quý khách không bao giờ sai — quan điểm của khách luôn được tôn trọng.",
      "Tranh luận với khách = mất khách và mất thương hiệu.",
      "Không có việc “không phải của tôi” — ai nhận yêu cầu, người đó chịu trách nhiệm."]},
    {"h": "Ba KHÔNG trong giao tiếp", "items": [
      "KHÔNG nói trống không, thiếu chủ ngữ (luôn có “dạ / thưa quý khách”).",
      "KHÔNG tranh luận hay biện minh với khách.",
      "KHÔNG từ chối thẳng — luôn tìm cách thay thế khéo léo."]},
    {"h": "Câu cứu nguy vạn năng", "items": [
      "“Dạ, em kiểm tra / hỗ trợ ngay cho quý khách ạ.” — rồi tìm người giúp, không để khách chờ trong im lặng."]},
    {"h": "Những điều BẮT BUỘC", "items": [
      "Tôn trọng riêng tư tuyệt đối — không camera trong phòng ngủ, nhà tắm và không gian riêng của khách.",
      "Giữ bí mật thông tin cá nhân của khách — không chia sẻ ra ngoài.",
      "Thay toàn bộ đồ vải sau mỗi lượt khách — không có ngoại lệ.",
      "Giữ trật tự sau 22:00 và tôn trọng giờ nghỉ của khách."]},
    {"h": "An toàn", "items": [
      "Biết vị trí cầu dao điện, van nước, bình cứu hoả tại villa mình làm.",
      "Trẻ em dưới 12 tuổi không dùng hồ bơi mà không có người lớn kèm.",
      "Báo ngay khi phát hiện sự cố an toàn — không tự xử lý nếu vượt khả năng."]},
  ]
}

DEPARTMENTS = []

# ------------------------------------------------------------------ QUẢN GIA
DEPARTMENTS.append({
 "id":"quan-gia","name":"Quản gia Villa","short":"Đón tiếp · Chăm sóc · Bàn giao","icon":"🛎️","sop":"SOP-226-QG-01",
 "tagline":"Bạn trực tiếp biến lời hứa 226 thành trải nghiệm thật — chuẩn bị, đón tiếp, chăm sóc và bàn giao villa, nhất quán ở mọi villa, mọi ca.",
 "role":"Quản gia villa (Villa Butler), báo cáo Quản lý Vận hành. Bạn xử lý yêu cầu thông thường của khách; KHÔNG báo giá đền bù, giảm giá, miễn phụ thu — việc tiền bạc do Quản lý quyết. Kênh làm việc chính: nhóm chat vận hành của villa.",
 "schedule":{
   "before":[
     {"t":"Nhận & xác nhận thông tin khách (T–1 ngày)","s":"Trước 20:00 hôm trước, nhắn xác nhận đủ: tên khách & SĐT; số người (người lớn/trẻ em/tài xế); giờ đến & số đêm; giá đã chốt/đã cọc/còn thu; yêu cầu đặc biệt."},
     {"t":"Nghiệm thu villa 6 khu vực (T–3 giờ)","s":"Sân vườn & lối vào · hồ bơi · phòng khách · phòng ngủ · nhà vệ sinh · bếp & kho giặt. Mỗi hạng mục Đạt/Chưa đạt; chưa đạt phải khắc phục xong trước giờ khách đến."},
     {"t":"Đủ bộ vật dụng bắt buộc","s":"Bàn chải – kem, dầu gội – sữa tắm – xà phòng, khăn, dép, bàn ủi, máy sấy, giấy vệ sinh, gia vị cơ bản, nước welcome, bao rác dự phòng. Thiếu → báo QL Vận hành cấp bổ sung."},
     {"t":"Xác nhận sẵn sàng (T–60 phút)","s":"Gửi nhóm: dòng “Villa [tên] đã sẵn sàng đón khách” + tối thiểu 06 ảnh (sân/hồ bơi, phòng khách, mỗi phòng ngủ, WC, bếp) làm bằng chứng nghiệm thu."}],
   "during":[
     {"t":"Đón & mời vào","s":"Có mặt trước 15 phút; chào: “Kính chào quý khách, em là [tên], quản gia của villa…”; mời ngồi, mời nước."},
     {"t":"Đối chiếu số khách","s":"Đếm người lớn/trẻ em/tài xế; vượt số lượng → báo QL Kinh doanh xác nhận phụ thu TRƯỚC khi nói con số với khách."},
     {"t":"Đăng ký lưu trú","s":"Chụp CCCD hai mặt khách người lớn, gửi nhóm để đăng ký; xoá ảnh khỏi máy cá nhân trong ngày."},
     {"t":"Tài sản bảo đảm","s":"Giữ 01 CCCD khách đại diện, hoặc thu cọc bảo đảm 2.000.000đ; ghi vào hợp đồng, báo nhóm."},
     {"t":"Thu tiền & ký hợp đồng","s":"Thu phần còn lại đúng số QL Kinh doanh xác nhận, không tự giảm/làm tròn/cho nợ; lập hợp đồng đủ thông tin; chụp ảnh gửi nhóm."},
     {"t":"Bàn giao villa","s":"Dẫn đi từng phòng; đếm cùng khách vật dụng dễ thất thoát; hướng dẫn thiết bị & WiFi; chỉ vị trí thiết bị an toàn."},
     {"t":"Hỗ trợ trong kỳ lưu trú","s":"Một đầu mối liên hệ; xử lý trong thẩm quyền; việc vượt quyền báo nhóm; ghi Sổ nhật ký villa mọi phát sinh."}],
   "after":[
     {"t":"Nghiệm thu trả phòng","s":"Khách báo trước ≥30 phút; có mặt trong 30 phút; kiểm 6 khu vực, đối chiếu bộ ảnh; đếm đủ đồ vải & vật dụng đã bàn giao."},
     {"t":"Xử lý thiếu/hỏng","s":"Chụp ảnh toàn cảnh + cận cảnh, gửi nhóm chờ Quản lý xác nhận mức đền bù; chỉ báo khách sau khi Quản lý duyệt — KHÔNG tự báo giá."},
     {"t":"Hoàn tất & tiễn khách","s":"Trả CCCD/hoàn cọc sau khi trừ khoản đã xác nhận; hỏi cảm nhận, mời đánh giá; tiễn khách ra tận xe."},
     {"t":"Dọn & báo cáo","s":"Tách đồ vải bẩn chuyển giặt (không tái sử dụng); tắt thiết bị, khoá cửa, kiểm an ninh; báo kết thúc lượt khách kèm ảnh & vật dụng cần bổ sung."}]},
 "golden":[
   "Khách luôn đúng về cảm nhận — không tranh cãi; ghi nhận, xin lỗi nếu thuộc trách nhiệm villa, chuyển Quản lý xử lý.",
   "Không tự ý quyết định về tiền — mọi đền bù, phụ thu, giảm trừ đều do Quản lý quyết.",
   "Riêng tư là sản phẩm — không quay phim/chụp ảnh khách, không đưa người ngoài vào villa khi có khách.",
   "Mọi việc phát sinh đều để lại dấu vết — ảnh, tin nhắn nhóm, biểu mẫu ký nhận; không xử lý “miệng”.",
   "Sạch là tiêu chuẩn, không phải cảm tính — villa nghiệm thu bằng checklist chấm điểm."],
 "phrases":[
   {"sit":"Đón khách","say":"Kính chào quý khách, em là [tên], quản gia của villa. Rất hân hạnh được đón quý khách tại 226 Villa."},
   {"sit":"Khi phát sinh phụ thu / việc về tiền","say":"Kính mong quý khách chờ em ít phút để xác nhận với bộ phận quản lý, em sẽ thông tin lại ngay."},
   {"sit":"Nhắc giữ trật tự sau 21:30","say":"Kính mong quý khách hỗ trợ giảm âm lượng sau 21:30 để không ảnh hưởng đến các hộ lân cận."},
   {"sit":"Tiễn khách","say":"Cảm ơn quý khách đã chọn 226 Villa, kính chúc quý khách thượng lộ bình an và hẹn gặp lại."}],
 "do":["Có mặt trước giờ khách đến ≥ 15 phút","Gửi dòng sẵn sàng + 6 ảnh nghiệm thu T–60 phút","Thay toàn bộ đồ vải sau mỗi lượt khách","Ghi mọi phát sinh vào nhóm & Sổ nhật ký villa","Giữ một đầu mối liên hệ duy nhất với khách"],
 "dont":["Tự báo giá đền bù / giảm giá / miễn phụ thu","Cãi nhau, tranh luận gay gắt với khách","Tái sử dụng đồ vải giữa hai lượt khách","Đưa người ngoài vào villa khi có khách","Dùng tiện ích villa (hồ bơi, bida, loa) cho mục đích cá nhân"],
 "exceptions":[
   {"sit":"Thiết bị hỏng, mất điện/nước, nghẹt cống","fix":"Xử lý sơ bộ trong khả năng; trấn an & báo khách thời gian khắc phục; báo nhóm ngay lập tức."},
   {"sit":"Khách xin giảm giá / bồi thường / miễn phụ thu","fix":"Không cam kết bất cứ điều gì; chuyển Quản lý quyết định."},
   {"sit":"Khách muốn nhận thêm người / ở thêm đêm","fix":"Không tự quyết; chuyển QL Kinh doanh xác nhận."},
   {"sit":"Sự cố an toàn, tai nạn, cháy nổ, đuối nước","fix":"Ưu tiên tuyệt đối cứu người; gọi 115 / 114; gọi trực tiếp Quản lý, không nhắn tin."},
   {"sit":"Trả phòng phát hiện hư hỏng / thất thoát","fix":"Chụp ảnh toàn cảnh + cận cảnh, gửi nhóm chờ Quản lý xác nhận mức đền; chỉ báo khách sau khi có xác nhận, đưa ảnh làm căn cứ, không tranh luận."}],
 "checklist":[
   {"item":"Xác nhận thông tin khách trước 20:00 hôm trước","when":"T–1 ngày"},
   {"item":"Nghiệm thu 6 khu vực đạt toàn bộ","when":"T–3 giờ"},
   {"item":"Đủ bộ vật dụng bắt buộc trong phòng","when":"T–3 giờ"},
   {"item":"Gửi dòng sẵn sàng + 6 ảnh vào nhóm","when":"T–60 phút"},
   {"item":"Đối chiếu số khách & thu đúng số tiền QL chốt","when":"Nhận phòng"},
   {"item":"Đăng ký lưu trú (CCCD) & tài sản bảo đảm","when":"Nhận phòng"},
   {"item":"Bàn giao villa, thiết bị & điểm an toàn","when":"Nhận phòng"},
   {"item":"Ghi Sổ nhật ký mọi phát sinh","when":"Trong kỳ"},
   {"item":"Nghiệm thu trả phòng, đối chiếu bộ ảnh","when":"Trả phòng"},
   {"item":"Tách đồ vải bẩn, báo kết thúc lượt khách","when":"Sau khách rời"}],
 "kpi":[
   {"group":"Chất lượng & trải nghiệm","name":"Điểm đánh giá của khách với villa phụ trách","good":"≥ 4,5/5"},
   {"group":"Chất lượng & trải nghiệm","name":"Số lượt phàn nàn về đón tiếp, vệ sinh","good":"≤ 1 lượt/tháng"},
   {"group":"Quy trình vận hành","name":"Nghiệm thu villa đúng hạn trước giờ khách đến","good":"≥ 95%"},
   {"group":"Quy trình vận hành","name":"Có mặt trong 30 phút khi khách báo trả phòng","good":"≥ 95%"},
   {"group":"Tài sản & kiểm kê","name":"Chênh lệch kiểm kê vật dụng cuối tháng","good":"≤ 2%"},
   {"group":"Tuân thủ thương hiệu","name":"Brand audit hạng mục thuộc quản gia","good":"100% CORE Đạt"}],
 "roadmap":[
   {"day":"Ngày 1","goal":"Học lời hứa dịch vụ 226, 5 nguyên tắc nghề, checklist nghiệm thu 6 khu vực","pass":"Đọc đúng checklist; thuộc 5 nguyên tắc"},
   {"day":"Ngày 2","goal":"Tập nghiệm thu villa & chụp bộ ảnh T–60 dưới giám sát","pass":"Nghiệm thu 1 villa đạt, gửi đủ 6 ảnh"},
   {"day":"Ngày 3","goal":"Tập quy trình đón & nhận phòng (7 bước)","pass":"Đón 1 lượt khách đúng chuẩn có giám sát"},
   {"day":"Ngày 4","goal":"Đăng ký lưu trú, thu tiền, hợp đồng, tài sản bảo đảm","pass":"Hoàn tất thủ tục 1 lượt không sai số"},
   {"day":"Ngày 5","goal":"Xử lý tình huống trong kỳ & bảng phân định báo nhóm","pass":"Xử lý đúng 1 tình huống thực tế"},
   {"day":"Ngày 6","goal":"Nghiệm thu trả phòng & xử lý hư hỏng","pass":"Nghiệm thu 1 lượt trả phòng đúng quy trình"},
   {"day":"Ngày 7","goal":"Trực độc lập trọn lượt khách","pass":"QL Vận hành xác nhận đủ tự tin đứng ca"}],
 "card":[
   {"k":"Trước khi đến","v":"Nghiệm thu 6 khu vực + đủ vật dụng; gửi 6 ảnh T–60 phút"},
   {"k":"Nhận phòng","v":"Đối chiếu số khách · thu đúng số QL chốt · CCCD/cọc bảo đảm"},
   {"k":"Tiền bạc","v":"KHÔNG tự báo phụ thu/đền bù — chuyển Quản lý"},
   {"k":"Trong kỳ","v":"Một đầu mối · ghi nhóm & sổ nhật ký mọi phát sinh"},
   {"k":"Trả phòng","v":"Có mặt ≤ 30 phút · đối chiếu ảnh · tách đồ vải bẩn"}]
})

# ------------------------------------------------------------------ QUẢN LÝ VẬN HÀNH
DEPARTMENTS.append({
 "id":"van-hanh","name":"Quản lý Vận hành","short":"Chất lượng · Bảo trì · Nhân sự quản gia","icon":"🧭","sop":"SOP-226-VH-01",
 "tagline":"Giữ mọi villa luôn sẵn sàng đón khách, chất lượng đồng nhất giữa các cơ sở, và điều phối toàn bộ đội ngũ quản gia.",
 "role":"Quản lý Vận hành, báo cáo Giám đốc, phối hợp ngang cấp Quản lý Kinh doanh, quản lý trực tiếp đội quản gia. Quyết định về CHẤT LƯỢNG và NHÂN SỰ; KHÔNG quyết về giá, phụ thu, đền bù (thuộc Quản lý Kinh doanh).",
 "schedule":{
   "before":[
     {"t":"08:00–08:30","s":"Nhận danh sách khách trong ngày từ QL Kinh doanh; rà soát yêu cầu đặc biệt & cam kết đã hứa với khách."},
     {"t":"08:30–09:30","s":"Liên hệ khách xác nhận giờ đến; phân công & báo quản gia đón; xác nhận villa đã đủ vật tư."}],
   "during":[
     {"t":"09:30–12:00","s":"Giám sát công tác chuẩn bị villa; xử lý các yêu cầu bảo trì tồn đọng."},
     {"t":"12:00–14:00","s":"Theo dõi trả phòng & nhận phòng; xử lý hư hỏng, thất thoát cùng QL Kinh doanh."},
     {"t":"14:00–17:00","s":"Kiểm tra villa theo lịch tuần (ưu tiên đột xuất); cấp phát vật tư; làm việc với thợ & nhà cung cấp."}],
   "after":[
     {"t":"17:00–18:00","s":"Kiểm tra ảnh nghiệm thu villa của các quản gia trong ngày; nhắc việc còn tồn."},
     {"t":"21:30","s":"Kiểm soát trật tự các villa đang có khách; hỗ trợ quản gia khi khách không hợp tác."}]},
 "golden":[
   "Quản lý Vận hành giữ CHẤT LƯỢNG; không quyết định về giá, phụ thu, đền bù.",
   "Villa chưa đạt hạng mục CORE về vệ sinh/an toàn thì KHÔNG nhận khách.",
   "Ưu tiên kiểm tra đột xuất, không báo trước, để thấy đúng thực trạng.",
   "Sự cố cùng loại lặp ở nhiều villa = vấn đề hệ thống, cần giải pháp cấp hệ thống (đổi NCC, đổi định kỳ bảo dưỡng)."],
 "phrases":[],
 "do":["Kiểm tra mỗi villa ≥ 1 lần/tuần, chấm checklist 6 khu vực","Phản hồi quản gia trong 10 phút khi có sự cố ảnh hưởng khách","Cấp phát vật tư có phiếu ký nhận","Chấm KPI quản gia hằng tháng có dẫn chứng","Brand audit định kỳ, gửi Giám đốc"],
 "dont":["Chấm checklist khống hoặc bỏ tần suất kiểm tra","Để villa nhận khách khi chưa đạt CORE vệ sinh/an toàn","Tự quyết giá, phụ thu, mức đền bù","Cấp phát vật tư không ghi chép","Tiết lộ thông tin giấy tờ, hình ảnh của khách"],
 "exceptions":[
   {"sit":"Sự cố Cấp 1 — Khẩn cấp (mất điện/nước, cháy nổ, rò rỉ điện, an toàn hồ bơi, hỏng khoá khi có khách)","fix":"Có mặt & xử lý ngay ≤ 2 giờ; gọi báo Giám đốc bằng cuộc gọi."},
   {"sit":"Sự cố Cấp 2 — Ảnh hưởng trải nghiệm (điều hoà, nóng lạnh, nghẹt cống, bơm hồ bơi, WiFi)","fix":"Xử lý trong ngày; nếu chưa xong phải có phương án thay thế cho khách."},
   {"sit":"Vượt năng lực xử lý tại chỗ","fix":"Gọi nhà thầu đã duyệt; nếu vượt hạn mức, lập phiếu đề nghị chi gửi KD/Giám đốc; phối hợp Đón tiếp phương án cho khách."},
   {"sit":"Khách gây ồn sau 21:30, không hợp tác","fix":"Quản gia nhắc lần 1 → QL Vận hành trao đổi trực tiếp → tái diễn có phản ánh hàng xóm thì báo Giám đốc; không tranh cãi với khách."}],
 "checklist":[
   {"item":"Nhận & rà soát danh sách khách trong ngày","when":"Đầu ngày"},
   {"item":"Phân công quản gia & xác nhận villa đủ vật tư","when":"Đầu ngày"},
   {"item":"Kiểm tra villa theo lịch tuần (chấm 6 khu vực)","when":"Trong ngày"},
   {"item":"Xử lý & phân cấp sự cố bảo trì đúng thời hạn","when":"Trong ngày"},
   {"item":"Kiểm ảnh nghiệm thu của quản gia","when":"Cuối ngày"},
   {"item":"Kiểm soát trật tự villa có khách lúc 21:30","when":"Cuối ngày"},
   {"item":"Rà tồn kho & lập đề nghị mua bổ sung","when":"Hằng tuần"},
   {"item":"Chấm KPI quản gia & brand audit","when":"Hằng tháng"}],
 "kpi":[
   {"group":"Chất lượng & trải nghiệm","name":"Điểm đánh giá TB các villa phụ trách","good":"≥ 4,5/5"},
   {"group":"Chất lượng & trải nghiệm","name":"Phàn nàn vệ sinh, thiết bị, tiếng ồn","good":"≤ 2 lượt/tháng"},
   {"group":"Quy trình vận hành","name":"Villa được kiểm tra đủ tần suất tuần","good":"100%"},
   {"group":"Quy trình vận hành","name":"Sự cố xử lý đúng thời hạn theo phân cấp","good":"≥ 90%"},
   {"group":"Tài sản & vật tư","name":"Villa thiếu vật tư bắt buộc khi khách nhận phòng","good":"0 lần"},
   {"group":"Tuân thủ thương hiệu","name":"Brand audit định kỳ","good":"100% CORE Đạt"}],
 "roadmap":[
   {"day":"Ngày 1–2","goal":"Nắm hệ thống 226, checklist 6 khu vực & thang đánh giá villa","pass":"Chấm thử 1 villa khớp với người kèm"},
   {"day":"Ngày 3","goal":"Quy trình điều phối khách & bàn giao quản gia","pass":"Điều phối 1 ngày khách không sai sót"},
   {"day":"Ngày 4","goal":"Phân cấp & điều phối sự cố bảo trì","pass":"Xử lý đúng 1 sự cố theo phân cấp"},
   {"day":"Ngày 5","goal":"Cấp phát vật tư, tồn tối thiểu, kiểm kê","pass":"Lập phiếu cấp phát & rà tồn đúng mẫu"},
   {"day":"Ngày 6","goal":"Quản lý trật tự 21:30 & xử lý khách khó","pass":"Xử lý đúng 1 tình huống trật tự"},
   {"day":"Ngày 7","goal":"Điều hành độc lập cụm villa","pass":"Giám đốc xác nhận đủ năng lực điều hành"}],
 "card":[
   {"k":"Vai trò","v":"Chất lượng & nhân sự — KHÔNG quyết giá/phụ thu/đền bù"},
   {"k":"Kiểm tra villa","v":"≥ 1 lần/tuần, ưu tiên đột xuất, chấm 6 khu vực"},
   {"k":"Sự cố","v":"Cấp 1 ≤ 2h · Cấp 2 trong ngày · Cấp 3 ≤ 7 ngày"},
   {"k":"Hỗ trợ quản gia","v":"Phản hồi ≤ 10 phút khi ảnh hưởng khách đang ở"},
   {"k":"Định kỳ","v":"Tuần: kiểm kê · Tháng: KPI quản gia + brand audit"}]
})

# ------------------------------------------------------------------ QUẢN LÝ KINH DOANH
DEPARTMENTS.append({
 "id":"kinh-doanh","name":"Quản lý Kinh doanh","short":"Lịch bán · Giá · Thu–chi · Báo cáo","icon":"💼","sop":"SOP-226-KD-01",
 "tagline":"Giữ lịch bán không sai sót, dòng tiền minh bạch, số liệu báo cáo thống nhất và so sánh chéo được giữa các villa.",
 "role":"Quản lý Kinh doanh, báo cáo Giám đốc, phối hợp ngang cấp Quản lý Vận hành, là đầu mối duy nhất làm việc với chủ nhà về số liệu. Quyết định về TIỀN và LỊCH; mọi đền bù, phụ thu, giảm giá thuộc thẩm quyền vị trí này.",
 "schedule":{
   "before":[
     {"t":"Trước 08:00 — Bàn giao khách cho vận hành","s":"Gửi nhóm vận hành danh sách khách hôm nay & ngày kế theo mẫu chuẩn: villa, tên, SĐT, ngày nhận–trả, số người, giá/đã cọc/còn thu, hình thức bảo đảm, yêu cầu & cam kết đã hứa."}],
   "during":[
     {"t":"Tiếp nhận & chốt đơn","s":"Phản hồi ≤30' giờ HC / ≤2h ngoài giờ; kiểm lịch trống toàn hệ thống; báo giá đúng bảng giá; giữ tạm tối đa 24 giờ."},
     {"t":"Nhận cọc & khoá lịch","s":"Khách cọc xong → khoá ngày trên lịch bán & lịch cộng đồng trong ≤ 15 phút; chuyển trạng thái “đã chốt”; cập nhật nhóm chủ nhà."},
     {"t":"Theo dõi nhận/trả phòng","s":"Cùng đội vận hành theo dõi trong ngày; xác nhận số tiền quản gia đã thu; quyết định các việc về tiền (phụ thu, đền bù, nhận sớm/trả muộn)."},
     {"t":"Cập nhật thu–chi","s":"Ghi thu/chi liên tục kèm chứng từ; duyệt chi theo hạn mức; không dồn cuối tháng."}],
   "after":[
     {"t":"Cuối ngày — Đối soát lịch","s":"Đối soát lịch bán với lịch cộng đồng & các kênh; trước kỳ cao điểm đối soát toàn kỳ trước ≥ 7 ngày."},
     {"t":"Cuối tháng — Báo cáo","s":"Chốt & gửi bộ 4 báo cáo trước ngày 03: tổng hợp hệ thống, lẻ từng căn, chi tiết thu–chi, tồn kho; kiểm kê cùng QL Vận hành."}]},
 "golden":[
   "Một nguồn lịch duy nhất — mọi kênh phản chiếu về đây; không có lịch riêng cá nhân.",
   "Chốt là khoá — khách cọc xong khoá ngày trong ≤ 15 phút; không giữ chỗ miệng quá 24 giờ.",
   "Mọi khoản thu/chi phải có chứng từ; thu và chi ghi riêng, đối chiếu được.",
   "Phần chia lợi nhuận luôn tính trên LỢI NHUẬN RÒNG; chủ đất chỉ nhận một trong hai: tiền thuê HOẶC phần chia."],
 "phrases":[],
 "do":["Gửi danh sách khách cho vận hành trước 08:00","Báo giá đúng bảng giá mùa + nêu cọc & huỷ","Khoá lịch ≤ 15 phút sau khi có cọc","Duyệt chi đúng hạn mức, lưu chứng từ","Nộp đủ bộ 4 báo cáo trước ngày 03"],
 "dont":["Nhận đặt phòng nhưng không khoá lịch (gây trùng lịch)","Giảm giá công khai dưới mức sàn đã thống nhất","Thu tiền khách không có chứng từ/không ghi nhận","Chi vượt hạn mức khi chưa được duyệt","Sửa số liệu báo cáo không đúng thực tế"],
 "exceptions":[
   {"sit":"Phát hiện trùng lịch (double booking)","fix":"Báo Giám đốc ngay; ưu tiên giữ khách đã cọc trước; chủ động đổi villa trong hệ thống + phương án bù đắp trước khi khách phát hiện."},
   {"sit":"Khách huỷ / đổi ngày","fix":"Áp đúng chính sách cọc & huỷ đã công bố; mọi ngoại lệ phải có phê duyệt Giám đốc."},
   {"sit":"Chi khẩn cấp ảnh hưởng khách đang ở","fix":"Cho thực hiện ngay, báo cáo trong 24 giờ kèm ảnh hiện trạng & chứng từ bổ sung."},
   {"sit":"Quản gia báo hư hỏng khi trả phòng","fix":"Phản hồi mức đền bù trong 15 phút để không giữ khách chờ lâu."}],
 "checklist":[
   {"item":"Gửi danh sách khách cho vận hành trước 08:00","when":"Đầu ngày"},
   {"item":"Phản hồi yêu cầu đặt phòng đúng SLA","when":"Trong ngày"},
   {"item":"Khoá lịch ≤ 15 phút sau khi có cọc","when":"Trong ngày"},
   {"item":"Ghi thu–chi kèm chứng từ, duyệt chi đúng hạn mức","when":"Trong ngày"},
   {"item":"Đối soát lịch bán với lịch cộng đồng","when":"Cuối ngày"},
   {"item":"Kiểm kê tồn kho cùng QL Vận hành","when":"Cuối tháng"},
   {"item":"Nộp đủ bộ 4 báo cáo trước ngày 03","when":"Cuối tháng"}],
 "kpi":[
   {"group":"Hiệu quả kinh tế","name":"Công suất phòng toàn hệ thống","good":"Đạt mục tiêu kỳ"},
   {"group":"Hiệu quả kinh tế","name":"Biên lợi nhuận toàn hệ thống","good":"Không giảm so cùng kỳ"},
   {"group":"Chất lượng dữ liệu","name":"Nộp đủ bộ 4 báo cáo đúng hạn","good":"100% trước ngày 03"},
   {"group":"Quy trình bán hàng","name":"Số lần trùng lịch trong tháng","good":"0 lần"},
   {"group":"Quy trình bán hàng","name":"Phản hồi yêu cầu đặt phòng","good":"≥ 90% trong 30'"},
   {"group":"Phối hợp & tuân thủ","name":"Chênh lệch kiểm kê cuối tháng","good":"≤ 2%"}],
 "roadmap":[
   {"day":"Ngày 1–2","goal":"Nắm bảng giá, chính sách cọc–huỷ, quy trình chốt đơn 8 bước","pass":"Chốt thử 1 đơn đúng quy trình"},
   {"day":"Ngày 3","goal":"Quản lý một nguồn lịch & phòng ngừa trùng lịch","pass":"Đối soát lịch 1 kỳ không lỗi"},
   {"day":"Ngày 4","goal":"Mẫu bàn giao khách cho vận hành","pass":"Gửi danh sách đúng mẫu, đủ trường"},
   {"day":"Ngày 5","goal":"Thu–chi, hạn mức duyệt chi, chứng từ","pass":"Lập & duyệt 1 phiếu chi đúng hạn mức"},
   {"day":"Ngày 6","goal":"Bộ 4 báo cáo & nguyên tắc trình bày số liệu","pass":"Dựng nháp báo cáo lẻ 1 căn"},
   {"day":"Ngày 7","goal":"Vận hành độc lập lịch & dòng tiền","pass":"Giám đốc xác nhận đủ năng lực"}],
 "card":[
   {"k":"Vai trò","v":"Tiền & Lịch — quyết phụ thu/đền bù/giảm giá"},
   {"k":"Lịch","v":"Một nguồn duy nhất · cọc xong khoá ≤ 15 phút"},
   {"k":"Bàn giao khách","v":"Gửi vận hành trước 08:00 theo mẫu chuẩn"},
   {"k":"Thu–chi","v":"Có chứng từ · duyệt đúng hạn mức · không dồn"},
   {"k":"Báo cáo","v":"Bộ 4 báo cáo trước ngày 03 · chia trên lợi nhuận ròng"}]
})

# =====================================================================================
# 9 BỘ PHẬN CHỨC NĂNG  (Cẩm nang SOP Các Bộ Phận)
# =====================================================================================
def fdept(id, name, short, icon, tagline, role, day_one, standards, steps, controls,
          do, dont, exceptions, phrases=None, before=None, after=None, card=None, roadmap=None):
    """standards: [(CORE|FLEX, text)] · steps/controls: [str] · exceptions: [(sit,fix)]"""
    golden = [t for lv,t in standards if lv=="CORE"][:4]
    during = [{"t": s.split(":")[0] if ":" in s[:40] else s, "s": s.split(":",1)[1].strip() if ":" in s[:40] else ""} for s in steps]
    before = before or [{"t":"Nhận lịch & bàn giao ca","s":"Nắm lịch khách trong ngày, việc còn tồn từ ca trước; chuẩn bị dụng cụ/vật tư cần cho ca."}]
    after  = after  or [{"t":"Ghi nhật ký & bàn giao","s":"Ghi các phát sinh vào nhật ký vận hành; bàn giao ca kèm việc chưa xong."}]
    chk = ([{"item":"Ngày đầu: "+day_one.split(".")[0].strip(), "when":"Ngày đầu"}] if day_one else []) + \
          [{"item":s if ":" not in s[:40] else s.split(":",1)[1].strip(), "when":"Trong ca"} for s in steps] + \
          [{"item":c, "when":"Điểm kiểm soát"} for c in controls]
    kpi = [{"group":"Điểm kiểm soát","name":c, "good":"Đạt"} for c in controls]
    rm = roadmap or [
      {"day":"Ngày 1","goal":day_one,"pass":"Làm đúng phần “Ngày đầu tiên”"},
      {"day":"Ngày 2","goal":"Học tiêu chuẩn CORE của bộ phận","pass":"Đọc đúng các tiêu chuẩn CORE"},
      {"day":"Ngày 3–4","goal":"Thực hành các bước dưới giám sát","pass":"Hoàn thành 1 lượt đạt điểm kiểm soát"},
      {"day":"Ngày 5","goal":"Xử lý tình huống phát sinh","pass":"Xử lý đúng 1 tình huống thực tế"},
      {"day":"Ngày 6–7","goal":"Trực độc lập dưới quan sát","pass":"Người kèm xác nhận đủ tự tin"}]
    cd = card or ([{"k":"Tiêu chuẩn CORE", "v":g} for g in golden[:3]] +
                  [{"k":"Điểm kiểm soát", "v":" · ".join(controls[:2])}])
    return {"id":id,"name":name,"short":short,"icon":icon,"sop":"Cẩm nang SOP · "+name,
            "tagline":tagline,"role":role,
            "schedule":{"before":before,"during":during,"after":after},
            "golden":golden,
            "phrases":[{"sit":p[0],"say":p[1]} for p in (phrases or [])],
            "do":do,"dont":dont,
            "exceptions":[{"sit":s,"fix":f} for s,f in exceptions],
            "checklist":chk,"kpi":kpi,"roadmap":rm,"card":cd}

DEPARTMENTS.append(fdept(
 "dat-phong-ota","Đặt phòng & OTA","Tuyến đầu trên internet","🗓️",
 "Bộ phận tuyến đầu trên internet — nơi khách gặp Villa 226 lần đầu tiên.",
 "Tiếp nhận & xử lý đặt phòng đa kênh (Zalo, Facebook, website, Booking/Agoda/Airbnb); giữ giá thống nhất; tuyệt đối chống trùng lịch.",
 "Đăng nhập cả 3 kênh OTA và xem lịch phòng hôm nay; học trả lời tin nhắn theo mẫu, đúng tên villa; ghi nhớ mọi kênh cùng một giá; chưa chắc thì hỏi quản lý.",
 [("CORE","Phản hồi khách ≤ 30 phút giờ hành chính; ngoài giờ ≤ 2 giờ."),
  ("CORE","Giá phòng thống nhất trên tất cả các kênh — không có giá riêng lẻ."),
  ("CORE","Đồng bộ lịch giữa các kênh trong ≤ 15 phút sau mỗi lượt đặt."),
  ("CORE","Văn phong trả lời trang trọng, đúng brand voice 226."),
  ("FLEX","Chương trình khuyến mãi theo mùa/địa bàn do cấp chuỗi duyệt.")],
 ["Đầu ca: mở cả 3 kênh OTA, kiểm tra đơn mới / tin nhắn chưa trả lời.",
  "Với mỗi đơn mới: xác nhận ngày nhận–trả, số khách, ghi vào lịch chung ngay.",
  "Trả lời mọi tin nhắn theo mẫu chuẩn, đúng thời gian cam kết.",
  "Chặn ngay ngày đã có khách trên tất cả kênh còn lại để tránh trùng lịch.",
  "Chuyển thông tin khách sắp đến cho bộ phận Đón tiếp trước ít nhất 1 ngày.",
  "Cuối ca: rà lại toàn bộ lịch tuần tới, xác nhận không có xung đột."],
 ["Số lần trùng lịch = 0 (bắt buộc tuyệt đối)","Tỷ lệ tin nhắn trả lời đúng hạn ≥ 95%","Không chênh lệch giá giữa các kênh khi kiểm tra ngẫu nhiên"],
 ["Trả lời đúng SLA & đúng brand voice","Đồng bộ / chặn lịch mọi kênh ≤ 15 phút","Chuyển khách cho Đón tiếp trước 1 ngày"],
 ["Tự ý báo giá khác giữa các kênh","Hứa phòng khi chưa kiểm lịch","Để tin nhắn khách quá hạn SLA"],
 [("Trùng lịch/overbooking","Xin lỗi ngay; ưu tiên chuyển sang villa 226 khác cùng phân khúc; nếu không được, tìm chỗ tương đương + bù chênh lệch; truy nguyên đồng bộ."),
  ("Khách huỷ/đổi ngày","Áp đúng chính sách huỷ đã công bố; đổi ngày tuỳ tồn phòng; ngoại lệ do Quản lý duyệt."),
  ("No-show","Giữ liên lạc đến hết giờ nhận phòng; áp chính sách cọc; mở lại ngày nếu chắc khách không đến.")],
 phrases=[("Phản hồi khách hỏi phòng","Kính chào quý khách, cảm ơn quý khách đã quan tâm đến Villa 226. Villa còn trống trong ngày quý khách chọn. Em xin phép gửi thông tin chi tiết và hỗ trợ quý khách đặt phòng ạ.")],
))

DEPARTMENTS.append(fdept(
 "don-tiep-cham-soc","Đón tiếp & Chăm sóc khách","Gương mặt của villa","🤝",
 "Bộ phận “gương mặt” của villa — người khách tiếp xúc nhiều nhất.",
 "Đón tiếp chu đáo, một đầu mối duy nhất, mang lại trải nghiệm như một resort thu nhỏ riêng tư.",
 "Học thuộc quy trình 5 bước phục vụ; đi một vòng villa nắm vị trí; chuẩn bị welcome drink & Welcome Book trước giờ khách; ghi số hotline & tên quản lý ca.",
 [("CORE","Giờ trả phòng 12:00; villa sẵn sàng trước giờ nhận phòng 60 phút."),
  ("CORE","Mỗi đoàn khách có MỘT đầu mối chăm sóc duy nhất suốt kỳ lưu trú."),
  ("CORE","Khách cần hỗ trợ báo trước 30 phút — nhân viên xác nhận lại ngay."),
  ("CORE","Giao tiếp theo chuẩn dịch vụ 226 (3S, quy tắc 10-5, script chuẩn)."),
  ("FLEX","Đối tác dịch vụ tại chỗ (đầu bếp, tour) tuỳ theo từng villa.")],
 ["Trước khi khách đến: kiểm tra villa sẵn sàng, chuẩn bị welcome drink.",
  "Đón khách tại cổng, cúi chào 30°, giới thiệu tên mình.",
  "Làm thủ tục check-in nhanh gọn, trao Welcome Book và số hotline.",
  "Dẫn khách tham quan villa, hướng dẫn thiết bị (điều hoà, hồ bơi, bếp).",
  "Trong kỳ: chủ động hỏi thăm, hỗ trợ, ghi nhớ nhu cầu đặc biệt của khách.",
  "Check-out: hỗ trợ hành lý, kiểm tra phòng, tiễn khách tận cổng, mời đánh giá."],
 ["Điểm đánh giá khách ≥ 4.7/5","Tỷ lệ phàn nàn về đón tiếp ≤ 2%","Villa sẵn sàng trước nhận phòng 60 phút"],
 ["Giữ một đầu mối duy nhất với khách","Chuẩn bị villa sẵn sàng trước 60 phút","Chủ động hỏi thăm trong kỳ lưu trú"],
 ["Để khách không biết liên hệ với ai","Bỏ bước hướng dẫn an toàn hồ bơi & nội quy","Dùng tiểu từ “ạ” sai trong ngữ cảnh trang trọng theo hướng dẫn brand voice"],
 [("Khách phàn nàn (4 bước)","Lắng nghe đầy đủ → xin lỗi về TRẢI NGHIỆM → đề xuất khắc phục kèm mốc thời gian (vượt quyền báo ngay) → xác nhận lại sau khắc phục & ghi nhật ký."),
  ("Khách đến sớm khi villa chưa sẵn sàng","Hỗ trợ nhận sớm nếu phòng trống & đã dọn; nếu chưa, mời khu chờ và cập nhật thời gian rõ ràng."),
  ("Hư hỏng tài sản do khách","Ghi nhận có ảnh; áp bảng giá đền bù công bố; giữ thái độ tôn trọng, khoản ngoài bảng do Quản lý quyết.")],
 phrases=[("Đón khách nhận phòng","Kính chào quý khách, chào mừng đến với Villa 226. Em là [tên], sẽ đồng hành cùng quý khách suốt kỳ nghỉ. Bất cứ điều gì quý khách cần, xin gọi em qua số hotline trong Welcome Book ạ.")],
))

DEPARTMENTS.append(fdept(
 "buong-phong-ve-sinh","Buồng phòng & Vệ sinh","Ấn tượng sạch sẽ","🧺",
 "Bộ phận quyết định ấn tượng “sạch sẽ” — điều khách cảm nhận đầu tiên khi mở cửa phòng.",
 "Bảo đảm mỗi khách bước vào không gian sạch tuyệt đối, thơm, gọn — đạt chuẩn 4–5 sao ngay lần đầu nghiệm thu.",
 "Học gấp khăn & trải ga theo chuẩn 226; nhớ nguyên tắc vàng thay TOÀN BỘ đồ vải sau MỖI lượt khách; xem phiếu nghiệm thu 14 dòng; biết kho đồ vải & tồn tối thiểu 3 bộ/vị trí.",
 [("CORE","Thay toàn bộ đồ vải (ga, gối, khăn) sau mỗi lượt khách — bắt buộc."),
  ("CORE","Mỗi phòng phải qua phiếu nghiệm thu có ký trước khi bàn giao."),
  ("CORE","Một dòng “Chưa đạt” trên phiếu = CHƯA được bàn giao phòng."),
  ("CORE","Tồn tối thiểu 3 bộ đồ vải mỗi vị trí để luôn có đồ thay."),
  ("FLEX","Loại nước lau sàn / tinh dầu thơm có thể khác theo villa.")],
 ["Thu gom toàn bộ đồ vải bẩn, rác; mở cửa thông thoáng phòng.",
  "Lau bụi từ trên xuống dưới: đèn, kệ, bàn, rồi mới đến sàn.",
  "Vệ sinh nhà tắm: bồn cầu, lavabo, vòi sen, gương — không để vết nước.",
  "Trải ga giường mới, gấp khăn đúng chuẩn, bổ sung amenities đầy đủ.",
  "Kiểm tra mùi phòng, xịt tinh dầu nhẹ; kiểm tra thiết bị điện hoạt động.",
  "Hoàn thành phiếu nghiệm thu 14 dòng, ký tên, báo quản lý bàn giao."],
 ["Nghiệm thu đạt ngay lần đầu ≥ 90%","Không phàn nàn về vệ sinh phòng","Kho đồ vải đủ định mức tồn tối thiểu"],
 ["Thay toàn bộ đồ vải mỗi lượt khách","Chạy đủ phiếu nghiệm thu 14 dòng","Bổ sung amenities đầy đủ"],
 ["Bàn giao phòng khi còn dòng Chưa đạt","Tái sử dụng đồ vải cũ","Bỏ sót vệ sinh nhà tắm/khu bếp"],
 [("Phát hiện hư hỏng khi dọn","Ghi nhận có ảnh, báo Bảo trì (theo mức sự cố) và Quản lý; không bàn giao phòng lỗi trọng yếu."),
  ("Thiếu đồ vải/vật tư sạch","Báo Kho ngay; dùng bộ tồn tối thiểu; không đủ thì Quản lý điều phối giữa villa.")],
))

DEPARTMENTS.append(fdept(
 "bao-tri-ky-thuat","Bảo trì & Kỹ thuật","Điện · nước · thiết bị","🔧",
 "Bộ phận giữ cho mọi thứ luôn hoạt động — điện, nước, điều hoà, thiết bị.",
 "Bảo đảm mọi thiết bị & hạ tầng hoạt động tốt; sự cố xử lý đúng thời gian cam kết theo mức độ khẩn cấp.",
 "Đi một vòng ghi vị trí cầu dao, van nước tổng, máy bơm hồ bơi, bình cứu hoả; học 4 mức sự cố & thời gian xử lý; lưu số thợ; biết cách ghi nhật ký + báo quản lý.",
 [("CORE","4 mức sự cố với thời gian xử lý cố định — tuân thủ nghiêm."),
  ("CORE","Mọi sự cố phải ghi vào nhật ký vận hành ngay khi phát sinh."),
  ("CORE","Kiểm tra kỹ thuật định kỳ hằng tuần theo checklist."),
  ("FLEX","Danh sách nhà thầu/thợ tại chỗ do từng villa tự lập.")],
 ["Nhận báo sự cố: xác định mức độ (Khẩn cấp/Nghiêm trọng/Thông thường/Định kỳ).",
  "Ghi vào nhật ký: thời gian, vị trí, mô tả sự cố.",
  "Xử lý ngay nếu trong khả năng; nếu không, gọi thợ theo cam kết thời gian.",
  "Nếu ảnh hưởng khách, báo Đón tiếp để thông báo và xin lỗi khách.",
  "Sau khắc phục: kiểm tra lại, ghi kết quả vào nhật ký, đóng sự cố.",
  "Hằng tuần: chạy checklist kiểm tra phòng ngừa toàn bộ thiết bị."],
 ["Sự cố xử lý đúng thời gian cam kết ≥ 95%","Không sự cố lặp lại do bỏ bảo trì định kỳ","Nhật ký kỹ thuật ghi đầy đủ, không ghi dồn"],
 ["Phân đúng mức & gán mốc thời gian","Cô lập & cảnh báo khu vực nguy hiểm","Ghi nhật ký kỹ thuật đầy đủ"],
 ["Bỏ qua bảo trì định kỳ hằng tuần","Để khách tự phát hiện sự cố rồi mới xử lý","Đưa thiết bị vào dùng khi chưa chạy thử lại"],
 [("Sự cố Khẩn cấp (mất điện/nước, rò gas, an toàn)","Bảo đảm an toàn trước; cô lập nguồn nguy hiểm; xử lý ≤ 2 giờ; báo Quản lý & Ban điều hành."),
  ("Vượt năng lực xử lý tại chỗ","Gọi nhà thầu đã duyệt; nếu ảnh hưởng lưu trú, phối hợp Đón tiếp phương án cho khách.")],
))

DEPARTMENTS.append(fdept(
 "ho-boi-canh-quan","Hồ bơi & Cảnh quan","Điểm nhấn đẹp nhất","🏊",
 "Bộ phận giữ điểm nhấn đẹp nhất của villa — hồ bơi và sân vườn.",
 "Bảo đảm hồ bơi luôn trong, an toàn, đạt chuẩn vệ sinh; sân vườn gọn đẹp — tạo cảm giác resort nghỉ dưỡng.",
 "Học đo pH & clo (nhờ người cũ chỉ bộ test); biết kho hoá chất luôn khoá riêng; mỗi ngày kiểm tra hồ bơi VÀ ghi nhật ký; kiểm biển cảnh báo độ sâu & phao/sào cứu hộ.",
 [("CORE","Kiểm tra hồ bơi và ghi nhật ký MỖI ngày (pH, clo, hoá chất đã dùng)."),
  ("CORE","Hoá chất hồ bơi khoá riêng, tuyệt đối cách ly khỏi khách và trẻ em."),
  ("CORE","Biển cảnh báo độ sâu và thiết bị cứu hộ luôn sẵn sàng tại hồ bơi."),
  ("FLEX","Loại cây cảnh, phong cách sân vườn linh hoạt theo địa phương.")],
 ["Mỗi sáng: đo pH và clo, ghi chỉ số vào nhật ký hồ bơi.",
  "Vớt lá, rác trên mặt nước; kiểm tra hệ thống lọc hoạt động.",
  "Điều chỉnh hoá chất nếu chỉ số ngoài ngưỡng; ghi lượng đã dùng.",
  "Kiểm tra biển cảnh báo, phao cứu hộ còn nguyên vị trí.",
  "Chăm sóc sân vườn: tưới cây, cắt tỉa, dọn lá theo lịch.",
  "Nếu nước đục/bẩn: tạm dừng hồ bơi, thông báo khách, xử lý trong 2 giờ."],
 ["Tỷ lệ ngày có ghi nhật ký hồ bơi = 100%","pH/clo luôn trong ngưỡng an toàn","Không sự cố an toàn liên quan hồ bơi"],
 ["Ghi nhật ký hồ bơi mỗi ngày","Khoá hoá chất, cách ly khỏi trẻ em","Giữ biển cảnh báo & phao cứu hộ đủ"],
 ["Bỏ ngày không ghi nhật ký","Để hoá chất trong tầm với của khách","Mở hồ khi nước chưa đạt chuẩn"],
 [("Nước đục / chỉ số bất thường","Đóng tạm hồ, xử lý hoá chất, chỉ mở lại khi đạt chuẩn; thông báo khách lịch sự nếu ảnh hưởng."),
  ("Thiết bị bơm/lọc hỏng","Báo Bảo trì theo mức sự cố; che chắn khu vực nếu cần.")],
))

DEPARTMENTS.append(fdept(
 "an-ninh-an-toan","An ninh & An toàn","Riêng tư · An toàn","🛡️",
 "Bộ phận bảo vệ sự riêng tư và an toàn — giá trị cốt lõi của Villa 226.",
 "Bảo đảm an toàn và riêng tư tuyệt đối cho khách; kiểm soát người ra vào; giữ trật tự và xử lý khẩn cấp.",
 "Nhớ quy tắc tối quan trọng: TUYỆT ĐỐI không có camera trong không gian riêng tư; chỉ khách đã đăng ký được vào villa; giữ trật tự sau 22:00; ghi số công an/y tế khẩn cấp.",
 [("CORE","CẤM TUYỆT ĐỐI camera trong phòng ngủ, nhà tắm và không gian riêng tư của khách."),
  ("CORE","Chỉ khách đã đăng ký mới được vào villa — kiểm soát chặt người lạ."),
  ("CORE","Giữ trật tự sau 22:00, nhắc nhở lịch sự nếu có tiếng ồn lớn."),
  ("FLEX","Danh sách liên hệ khẩn cấp địa phương theo từng villa.")],
 ["Đầu ca: kiểm tra khoá cổng, camera khu vực chung, đèn an ninh.",
  "Xác nhận danh sách khách đang lưu trú; cảnh giác người lạ tiếp cận.",
  "Tuần tra định kỳ khu vực ngoài villa theo lịch.",
  "Sau 22:00: nhắc nhở nhẹ nhàng nếu khách gây ồn ảnh hưởng xung quanh.",
  "Sự cố an ninh: bảo đảm an toàn khách trước, báo quản lý & cơ quan chức năng.",
  "Ghi mọi sự vụ vào nhật ký, kể cả sự việc nhỏ."],
 ["Số sự vụ an ninh = 0 hoặc xử lý kịp thời","Không vi phạm camera không gian riêng tư","Không có người lạ (không đăng ký) vào villa"],
 ["Chỉ cho khách đã đăng ký vào villa","Kiểm tra thiết bị PCCC & lối thoát","Ghi nhật ký mọi sự vụ, kể cả nhỏ"],
 ["Đặt camera ở không gian riêng tư của khách","Rời vị trí kiểm soát khi chưa bàn giao","Tiết lộ khách đến/đi cho người ngoài"],
 [("Người lạ / tranh chấp / mất an ninh","Bảo đảm an toàn khách; can thiệp trong thẩm quyền; gọi hỗ trợ/chính quyền nếu cần; ghi nhật ký & báo Quản lý ngay."),
  ("Sự cố cháy nổ","Ưu tiên sơ tán an toàn; dùng PCCC nếu an toàn; gọi 114; báo Ban điều hành.")],
))

DEPARTMENTS.append(fdept(
 "dich-vu-tang-them","Dịch vụ tăng thêm","BBQ · đầu bếp · tour · spa","🍽️",
 "Bộ phận tạo thêm doanh thu và trải nghiệm — BBQ, đầu bếp, tour, spa, đưa đón.",
 "Tăng doanh thu & làm phong phú trải nghiệm qua dịch vụ bổ sung, giới thiệu tinh tế, minh bạch về giá.",
 "Xem bảng giá dịch vụ đã công bố; biết danh sách đối tác đã duyệt (đầu bếp, tour, spa) và chỉ giới thiệu đối tác này; gợi ý nhẹ nhàng đúng lúc, không ép, không lan man.",
 [("CORE","Mọi dịch vụ có bảng giá công bố trước — không phát sinh giá bất ngờ."),
  ("CORE","Chỉ giới thiệu đối tác đã được duyệt về chất lượng và an toàn."),
  ("CORE","Không chào bán gây áp lực hoặc làm phiền khách."),
  ("FLEX","Danh mục dịch vụ và đối tác cụ thể linh hoạt theo từng villa.")],
 ["Giới thiệu dịch vụ ngay khi check-in (qua Welcome Book), không ép.",
  "Quan sát nhu cầu khách (gia đình → BBQ; cặp đôi → spa) để gợi ý đúng.",
  "Báo giá rõ ràng, minh bạch trước khi khách quyết định.",
  "Khách đồng ý: đặt dịch vụ với đối tác đã duyệt, xác nhận thời gian.",
  "Theo dõi chất lượng đối tác cung cấp, ghi nhận phản hồi khách.",
  "Ghi doanh thu dịch vụ vào báo cáo Thu–Chi của villa."],
 ["Tỷ trọng doanh thu dịch vụ theo mục tiêu","Không phàn nàn bị chào bán gây phiền","Đối tác giữ chất lượng ổn định"],
 ["Báo bảng giá trước khi chốt","Chỉ dùng đối tác đã duyệt","Ghi doanh thu dịch vụ vào Thu–Chi"],
 ["Chào bán gây áp lực, làm phiền khách","Giới thiệu đối tác chưa được duyệt","Phát sinh giá bất ngờ với khách"],
 [("Đối tác trễ / không đạt","Xin lỗi khách, tìm phương án thay thế trong hạn mức; loại đối tác không đạt khỏi danh sách."),
  ("Sự cố an toàn thực phẩm","Ngừng phục vụ món liên quan; hỗ trợ khách; ghi sự vụ & rà lại đối tác.")],
 phrases=[("Gợi ý dịch vụ","Dạ, villa bên em có dịch vụ đầu bếp nấu tại chỗ và tiệc BBQ ngoài trời, rất phù hợp cho nhóm của quý khách. Em xin phép gửi quý khách bảng giá để tham khảo, quý khách cần thì báo em sắp xếp ạ.")],
))

DEPARTMENTS.append(fdept(
 "kho-vat-tu-mua-sam","Kho, Vật tư & Mua sắm","Không bao giờ thiếu đồ","📦",
 "Bộ phận bảo đảm không bao giờ thiếu đồ — từ khăn tắm đến amenities.",
 "Villa luôn đủ vật tư để vận hành liên tục; kiểm soát tồn kho chặt; vật tư thương hiệu đồng nhất toàn chuỗi.",
 "Đi một vòng kho nắm vị trí từng loại vật tư; xem định mức tồn tối thiểu — dưới mức phải báo đặt thêm; biết mặt hàng nào mua tập trung cấp chuỗi; học ghi phiếu kiểm kê tuần.",
 [("CORE","Vật tư mang thương hiệu 226 (đồ vải, amenities in logo) mua tập trung cấp chuỗi."),
  ("CORE","Kiểm kê kho hằng tuần theo phiếu chuẩn."),
  ("CORE","Luôn giữ định mức tồn tối thiểu — không để thiếu hàng khi có khách."),
  ("FLEX","Nhà cung cấp vật tư tiêu hao thông thường linh hoạt theo villa.")],
 ["Nhận và kiểm đếm hàng khi nhập kho, đối chiếu phiếu đặt.",
  "Sắp xếp vật tư theo khu vực, dán nhãn rõ ràng, hàng cũ dùng trước.",
  "Cấp phát vật tư cho các bộ phận, ghi vào sổ xuất kho.",
  "Kiểm kê hằng tuần: đếm tồn thực tế, so với định mức tối thiểu.",
  "Mặt hàng dưới định mức: lập đề nghị mua, gửi đúng kênh (chuỗi hoặc tại chỗ).",
  "Báo cáo tồn kho và đề xuất mua sắm cho quản lý villa."],
 ["Số lần thiếu hàng khi cần = 0","Chênh lệch kiểm kê trong ngưỡng cho phép","Vật tư thương hiệu đồng nhất giữa các villa"],
 ["Ghi nhập/xuất kho đầy đủ","Giữ định mức tồn tối thiểu","Mua hàng thương hiệu qua kênh tập trung"],
 ["Cấp phát vật tư không ghi chép","Để thiếu hàng khi có khách","Mua hàng thương hiệu ngoài kênh chuỗi"],
 [("Thiếu hàng gấp phục vụ khách","Điều phối giữa các villa trong chuỗi; mua khẩn tại chỗ trong hạn mức; báo Quản lý."),
  ("Chênh lệch kiểm kê lớn","Truy nguyên (thất thoát/ghi sai/hư hỏng); báo Quản lý; điều chỉnh quy trình cấp phát.")],
))

DEPARTMENTS.append(fdept(
 "tai-chinh-bao-cao","Tài chính & Báo cáo cơ sở","Dòng tiền của villa","📊",
 "Bộ phận ghi lại dòng tiền của villa — nền tảng để chuỗi so sánh và ra quyết định.",
 "Ghi chép trung thực, thống nhất mọi khoản thu–chi; cung cấp số liệu chuẩn để chuỗi so sánh chéo.",
 "Xem mẫu báo cáo Thu–Chi chuẩn của chuỗi; nhớ ghi doanh thu theo NGÀY LƯU TRÚ (không phải ngày nhận tiền); tách chi phí đầu tư khỏi vận hành; hạn chốt trước ngày 05 tháng sau.",
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
  "Lưu chứng từ tối thiểu để phục vụ kiểm tra và brand audit."],
 ["Báo cáo nộp đúng hạn (trước ngày 05) = 100%","Số liệu khớp OTA – tiền thực nhận – báo cáo","Phân loại chi phí đúng, không lẫn đầu tư vào vận hành"],
 ["Ghi doanh thu theo ngày lưu trú","Lưu đủ chứng từ cho mọi khoản chi","Chốt & nộp báo cáo trước ngày 05"],
 ["Tự tạo mẫu báo cáo riêng","Lẫn chi phí đầu tư vào vận hành","Ghi doanh thu theo ngày nhận tiền"],
 [("Lệch thu–chi khi đối chiếu","Truy nguyên chứng từ & sao kê; không chốt khi còn khoản chưa rõ; báo Kế toán chuỗi."),
  ("Khách chậm thanh toán phần còn lại","Áp chính sách thanh toán trước nhận phòng; phối hợp Đón tiếp nhắc khách.")],
))

# tài khoản: id bỏ gạch + "226"
ACCOUNTS = {d["id"]: d["id"].replace("-", "") + "226" for d in DEPARTMENTS}
ADMIN = {"user": "admin", "pass": "admin226"}

DATA = {"common": COMMON, "departments": DEPARTMENTS}

# =====================================================================================
# CSS  (bảng màu navy/đồng 226, cấu trúc thành phần theo bản Ngọc Tước)
# =====================================================================================
CSS = r"""
:root{
  --gold:#C89A46; --gold-lt:#DDB86A; --gold-dk:#8F6B22; --gold-soft:#F4EAD3;
  --navy:#14547A; --navy-lt:#1B6A94; --navy-dp:#0F3F5C;
  --bg:#EEF3F6; --paper:#FFFFFF; --panel:#F6FAFC;
  --ink:#1F2A30; --muted:#5C6B75; --faint:#93A2AC;
  --line:#D6E0E6; --line-2:#E6EDF1;
  --ok:#0F7A4E; --ok-bg:rgba(15,122,78,.12); --bad:#B0472F; --warn:#A9702A;
  --shadow-s:0 2px 10px rgba(20,84,122,.07); --shadow:0 14px 40px rgba(20,84,122,.14); --shadow-l:0 26px 70px rgba(15,63,92,.32);
  --radius:18px;
  --serif:"Playfair Display","Iowan Old Style",Palatino,Georgia,serif;
  --sans:"Be Vietnam Pro",-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,Roboto,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0E1A20; --paper:#152229; --panel:#18262E; --ink:#E7EEF2; --muted:#9DB0BB; --faint:#6C808B;
  --line:#243642; --line-2:#1E2E38; --navy:#0F3F5C; --navy-lt:#1B6A94; --gold-soft:rgba(200,154,70,.14); --ok-bg:rgba(15,122,78,.2);
  --shadow:0 14px 40px rgba(0,0,0,.45); --shadow-l:0 26px 70px rgba(0,0,0,.6); --shadow-s:0 2px 10px rgba(0,0,0,.35);
}}
:root[data-theme="dark"]{--bg:#0E1A20;--paper:#152229;--panel:#18262E;--ink:#E7EEF2;--muted:#9DB0BB;--faint:#6C808B;--line:#243642;--line-2:#1E2E38;--navy:#0F3F5C;--navy-lt:#1B6A94;--gold-soft:rgba(200,154,70,.14);--ok-bg:rgba(15,122,78,.2);--shadow:0 14px 40px rgba(0,0,0,.45);--shadow-l:0 26px 70px rgba(0,0,0,.6);--shadow-s:0 2px 10px rgba(0,0,0,.35);}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.58;-webkit-text-size-adjust:100%;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{margin:0;line-height:1.22;font-weight:600}
.serif{font-family:var(--serif)}
a{color:var(--gold-dk)}
.hidden{display:none !important}
.wrap{max-width:940px;margin:0 auto;padding:0 18px}
.eyebrow{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold-dk);font-weight:700}
img{max-width:100%}
@media (prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important}}

#login{min-height:100dvh;display:flex;align-items:center;justify-content:center;padding:24px;position:relative;overflow:hidden;
  background:radial-gradient(1100px 620px at 50% -12%,rgba(200,154,70,.30),transparent 62%),radial-gradient(900px 700px at 50% 120%,rgba(200,154,70,.10),transparent 60%),linear-gradient(160deg,var(--navy-lt),var(--navy) 55%,var(--navy-dp))}
#login .watermark{position:absolute;inset:auto -8% -18% auto;width:min(70vw,540px);opacity:.06;filter:brightness(0) invert(1);pointer-events:none;transform:rotate(-6deg)}
.card-login{position:relative;width:100%;max-width:410px;background:var(--paper);border-radius:26px;box-shadow:var(--shadow-l);padding:34px 30px 24px;text-align:center;border:1px solid rgba(200,154,70,.28);animation:rise .6s cubic-bezier(.2,.7,.2,1) both}
.card-login::before{content:"";position:absolute;inset:7px;border-radius:20px;border:1px solid var(--line-2);pointer-events:none}
.card-login .lotus{width:120px;height:auto;margin:0 auto 4px;display:block;mix-blend-mode:multiply}
.card-login .brand{font-size:11px;letter-spacing:.32em;color:var(--gold-dk);font-weight:700;text-transform:uppercase;margin-top:2px}
.card-login .rule{width:46px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:13px auto}
.card-login h1{font-family:var(--serif);font-size:25px;font-weight:600;color:var(--ink)}
.card-login .sub{color:var(--muted);font-size:13px;margin:5px 0 22px}
.field{text-align:left;margin-bottom:14px}
.field label{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted);margin-bottom:6px}
.field input,.field select{width:100%;padding:13px 14px;border:1.5px solid var(--line);border-radius:13px;font-size:15px;font-family:var(--sans);background:var(--panel);color:var(--ink);outline:none;transition:border-color .18s,box-shadow .18s}
.field input:focus,.field select:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(200,154,70,.16)}
.btn{width:100%;padding:14px;border:none;border-radius:13px;font-size:15.5px;font-weight:700;cursor:pointer;font-family:var(--sans);color:#3a2c0c;background:linear-gradient(150deg,var(--gold-lt),var(--gold));box-shadow:0 8px 20px rgba(200,154,70,.35);transition:transform .1s,filter .18s,box-shadow .18s}
.btn:hover{filter:brightness(1.05)}.btn:active{transform:translateY(1px)}
.btn.ghost{background:transparent;border:1.5px solid var(--line);color:var(--ink);box-shadow:none}
.err{color:var(--bad);font-size:13px;margin:11px 0 0;min-height:18px;font-weight:600}
.card-login .hint{margin-top:16px;padding-top:14px;border-top:1px solid var(--line-2);font-size:12px;color:var(--muted);line-height:1.5}

#app{min-height:100dvh}
header.top{position:sticky;top:0;z-index:40;color:#EAF2F6;background:linear-gradient(120deg,var(--navy-lt),var(--navy) 62%);border-bottom:1px solid rgba(200,154,70,.5);box-shadow:0 2px 20px rgba(15,63,92,.35)}
header.top::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.75}
.top .wrap{display:flex;align-items:center;gap:13px;padding:11px 18px}
.dept-ic{width:46px;height:46px;border-radius:13px;display:grid;place-items:center;font-size:23px;flex:none;background:linear-gradient(150deg,var(--gold-lt),var(--gold));box-shadow:0 4px 14px rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.35)}
.top .eyebrow{color:var(--gold-lt);opacity:.95;font-size:9.5px;letter-spacing:.18em}
.top h2{font-family:var(--serif);font-size:18.5px;color:#fff;font-weight:600;line-height:1.15;margin-top:1px}
.top .role{font-size:11.5px;color:#CFE0EA;margin-top:1px}
.top .spacer{flex:1}
.iconbtn{background:rgba(255,255,255,.12);color:#EAF2F6;border:1px solid rgba(255,255,255,.16);border-radius:11px;padding:8px 12px;font-size:12.5px;cursor:pointer;font-weight:600;white-space:nowrap;transition:background .16s}
.iconbtn:hover{background:rgba(255,255,255,.22)}
nav.tabs{position:sticky;top:68px;z-index:30;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.tabs-scroll{display:flex;gap:7px;overflow-x:auto;padding:10px 18px;max-width:940px;margin:0 auto;scrollbar-width:none}
.tabs-scroll::-webkit-scrollbar{display:none}
.tab{flex:none;padding:7px 15px;border-radius:999px;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap;background:var(--paper);border:1.5px solid var(--line);color:var(--muted);transition:all .18s}
.tab:hover{border-color:var(--gold);color:var(--ink)}
.tab.active{background:linear-gradient(150deg,var(--navy-lt),var(--navy));color:#fff;border-color:var(--navy);box-shadow:var(--shadow-s)}
main{padding:20px 0 70px}
#content{animation:fadeUp .34s cubic-bezier(.2,.7,.2,1)}
.hero{position:relative;overflow:hidden;border-radius:var(--radius);padding:26px 24px;margin-bottom:20px;color:#EFF5F9;background:linear-gradient(145deg,var(--navy-lt),var(--navy) 70%);box-shadow:var(--shadow);border:1px solid rgba(200,154,70,.4)}
.hero::before{content:"";position:absolute;inset:8px;border-radius:12px;border:1px solid rgba(200,154,70,.28);pointer-events:none}
.hero .wm{position:absolute;right:-30px;bottom:-40px;width:220px;opacity:.10;filter:brightness(0) invert(1);pointer-events:none;transform:rotate(-8deg)}
.hero .eyebrow{color:var(--gold-lt);position:relative}
.hero .tl{font-family:var(--serif);font-size:22px;font-weight:600;color:#fff;margin-top:9px;position:relative;max-width:40ch}
.hero .rl{font-size:14px;margin-top:11px;color:#DCE8F0;position:relative;max-width:66ch}
.hero .code{display:inline-block;margin-top:15px;font-size:10.5px;letter-spacing:.16em;background:rgba(0,0,0,.28);padding:5px 12px;border-radius:999px;color:var(--gold-lt);font-weight:700;position:relative;border:1px solid rgba(200,154,70,.35)}
.sec-h{display:flex;align-items:center;gap:12px;margin:26px 2px 13px}
.sec-h .mark{width:12px;height:12px;flex:none;background:linear-gradient(135deg,var(--gold-lt),var(--gold));transform:rotate(45deg);border-radius:3px;box-shadow:0 2px 6px rgba(200,154,70,.4)}
.sec-h h3{font-family:var(--serif);font-size:19px;font-weight:600}
.sec-h .line{flex:1;height:1px;background:linear-gradient(90deg,var(--line),transparent)}
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow-s);overflow:hidden}
.card+.card{margin-top:13px}
.card-b{padding:17px 18px}
.note-b{font-size:13px;color:var(--muted);border-bottom:1px solid var(--line);padding:13px 18px;background:var(--panel)}
.shift{margin-bottom:8px}.shift+.shift{margin-top:20px;padding-top:18px;border-top:1px dashed var(--line)}
.shift-t{display:flex;align-items:center;gap:9px;font-size:11.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-dk);margin:0 0 12px}
.shift-t .dot{width:8px;height:8px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 4px var(--gold-soft)}
.step{display:flex;gap:13px;padding:12px 0;border-top:1px solid var(--line-2)}
.step:first-of-type{border-top:none}
.step .k{flex:none;width:27px;height:27px;border-radius:9px;background:linear-gradient(150deg,var(--navy-lt),var(--navy));color:#EFF5F9;font-size:12.5px;display:grid;place-items:center;font-weight:700;margin-top:2px;border:1px solid rgba(200,154,70,.3)}
.step .t{font-weight:700;font-size:14.5px}.step .s{color:var(--muted);font-size:13.5px;margin-top:3px}
.golden{background:linear-gradient(150deg,var(--gold-soft),transparent);border:1px solid rgba(200,154,70,.4);border-left:3px solid var(--gold);border-radius:12px;padding:13px 15px;margin:11px 0;font-size:13.8px;color:var(--ink);display:flex;gap:11px}
.golden .i{flex:none;color:var(--gold-dk)}.golden:first-child{margin-top:0}
.phrase{border-top:1px solid var(--line-2);padding:13px 0}.phrase:first-child{border-top:none}
.phrase .sit{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--gold-dk);font-weight:700;margin-bottom:5px}
.phrase .say{font-family:var(--serif);font-size:16.5px;font-style:italic;color:var(--ink);padding-left:14px;border-left:2px solid var(--gold)}
.dd{display:grid;grid-template-columns:1fr 1fr;gap:13px}@media(max-width:560px){.dd{grid-template-columns:1fr}}
.dd .col{background:var(--paper);border:1px solid var(--line);border-radius:15px;padding:15px;box-shadow:var(--shadow-s)}
.dd .col h4{font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;display:flex;gap:8px;align-items:center}
.dd .do h4{color:var(--ok)}.dd .dont h4{color:var(--bad)}
.dd li{list-style:none;font-size:13.6px;padding:7px 0 7px 24px;position:relative;border-top:1px dashed var(--line-2)}
.dd li:first-child{border-top:none}
.dd .do li::before{content:"✓";position:absolute;left:0;color:var(--ok);font-weight:800}
.dd .dont li::before{content:"✕";position:absolute;left:0;color:var(--bad);font-weight:800}
ul{margin:0;padding:0}
.quicknav{display:grid;grid-template-columns:1fr 1fr;gap:13px}
.quicknav button{cursor:pointer;text-align:left;font-weight:700;font-size:14.5px;font-family:var(--sans);color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:15px;padding:16px 15px;box-shadow:var(--shadow-s);transition:transform .12s,border-color .16s}
.quicknav button:hover{transform:translateY(-2px);border-color:var(--gold)}
.quicknav .qsub{display:block;font-weight:500;font-size:12px;color:var(--muted);margin-top:3px}
.chk{display:flex;gap:12px;padding:13px 0;border-top:1px solid var(--line-2);cursor:pointer;align-items:flex-start}
.chk:first-child{border-top:none}
.box{flex:none;width:23px;height:23px;border-radius:8px;border:2px solid var(--gold);display:grid;place-items:center;margin-top:1px;color:#fff;font-size:14px;transition:background .14s,transform .14s;background:transparent}
.chk.on .box{background:linear-gradient(150deg,var(--gold-lt),var(--gold))}
.chk:active .box{transform:scale(.9)}
.chk .ci{font-size:14.2px;font-weight:600}.chk.on .ci{text-decoration:line-through;color:var(--faint)}
.chk .cw{font-size:11px;color:var(--gold-dk);background:var(--gold-soft);border:1px solid rgba(200,154,70,.3);padding:2px 9px;border-radius:999px;margin-left:auto;flex:none;white-space:nowrap;font-weight:700}
.progress{height:9px;background:var(--line);border-radius:999px;overflow:hidden;margin:3px 0 5px}
.progress>i{display:block;height:100%;background:linear-gradient(90deg,var(--gold-lt),var(--gold));width:0;transition:width .35s}
.progress-lbl{font-size:12px;color:var(--muted);margin-bottom:14px;font-weight:700;font-variant-numeric:tabular-nums}
.kpi{border-top:1px solid var(--line-2);padding:13px 0;display:flex;gap:13px;align-items:baseline;flex-wrap:wrap}
.kpi:first-child{border-top:none}
.kpi .g{font-size:10.5px;font-weight:800;letter-spacing:.06em;color:var(--gold-dk);text-transform:uppercase;flex:none;width:158px}
@media(max-width:560px){.kpi .g{width:100%}}
.kpi .nm{flex:1;font-size:14px;min-width:150px}
.kpi .gd{font-size:12.5px;font-weight:700;color:var(--ok);background:var(--ok-bg);padding:3px 11px;border-radius:999px;white-space:nowrap}
.exc{border-top:1px solid var(--line-2);padding:14px 0}.exc:first-child{border-top:none}
.exc .q{font-weight:700;font-size:14px;display:flex;gap:9px}.exc .q .i{color:var(--warn);flex:none}
.exc .a{font-size:13.6px;color:var(--muted);margin-top:5px;padding-left:26px}
.day{border-top:1px solid var(--line-2);padding:14px 0;display:flex;gap:13px;cursor:pointer;align-items:flex-start}
.day:first-child{border-top:none}
.day .dn{flex:none;width:64px;font-family:var(--serif);font-size:14px;color:var(--navy);font-weight:700}
.day .dbody{flex:1}.day .goal{font-size:14px;font-weight:600}.day .pass{font-size:12.5px;color:var(--ok);margin-top:3px}
.day .dcheck{flex:none;width:24px;height:24px;border-radius:7px;border:2px solid var(--gold);display:grid;place-items:center;color:#fff;font-size:14px;background:transparent}
.day.on .dcheck{background:var(--ok);border-color:var(--ok)}.day.on .goal{color:var(--faint)}
.tcard{position:relative;overflow:hidden;background:linear-gradient(160deg,var(--navy-lt),var(--navy) 75%);color:#EFF5F9;border-radius:20px;padding:8px 20px 20px;box-shadow:var(--shadow);border:1px solid rgba(200,154,70,.4)}
.tcard .wm{position:absolute;right:-24px;top:-30px;width:170px;opacity:.10;filter:brightness(0) invert(1);pointer-events:none;transform:rotate(8deg)}
.tcard .tk{border-top:1px solid rgba(200,154,70,.28);padding:14px 0;position:relative}.tcard .tk:first-of-type{border-top:none}
.tcard .tk .k{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-lt);font-weight:800}
.tcard .tk .v{font-size:14.2px;margin-top:4px;color:#EAF2F6}
.tcard .note{font-size:11.5px;color:#CFE0EA;text-align:center;padding-top:14px;position:relative}
.cblk{margin-bottom:4px}
.cblk h4{font-family:var(--serif);font-size:16px;font-weight:600;color:var(--gold-dk);margin:18px 0 9px}.cblk:first-of-type h4{margin-top:4px}
.cblk li{list-style:none;font-size:13.8px;padding:6px 0 6px 22px;position:relative;border-top:1px dashed var(--line-2)}.cblk li:first-child{border-top:none}
.cblk li::before{content:"";position:absolute;left:2px;top:13px;width:7px;height:7px;background:var(--gold);transform:rotate(45deg);border-radius:1px}
.footer{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;padding:22px 18px 34px;color:var(--muted);font-size:12px;text-align:center}
.footer img{height:26px;opacity:.85;mix-blend-mode:multiply}.footer .fdiv{width:1px;height:16px;background:var(--line)}
#admin{min-height:100dvh;background:var(--bg)}
.adm-h{color:#EAF2F6;background:linear-gradient(120deg,var(--navy-lt),var(--navy) 62%);border-bottom:1px solid rgba(200,154,70,.5)}
.adm-h .wrap{display:flex;align-items:center;gap:13px;padding:13px 18px}
.adm-h h2{color:#fff}
.adm-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:720px){.adm-grid{grid-template-columns:1fr}}
.qrframe{display:flex;flex-direction:column;align-items:center;gap:8px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}
.qrframe .lotus{height:34px;mix-blend-mode:multiply}
.qrframe canvas{width:224px;height:224px;background:#fff;border-radius:12px;padding:10px;image-rendering:pixelated}
.cred{margin-top:12px;font-size:14px}.cred code{background:var(--gold-soft);color:var(--gold-dk);padding:2px 8px;border-radius:6px;font-weight:700}
.printgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:720px){.printgrid{grid-template-columns:repeat(2,1fr)}}
.print-card{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:18px 14px;text-align:center;position:relative}
.print-card::before{content:"";position:absolute;inset:6px;border-radius:11px;border:1px solid var(--line-2);pointer-events:none}
.print-card>*{position:relative;max-width:100%}
.print-card .plotus{height:34px;width:auto;opacity:.95;display:block;margin:0 auto 12px;mix-blend-mode:multiply}
.print-card canvas{display:block;width:150px;height:150px;background:#fff;padding:9px;border-radius:11px;image-rendering:pixelated;margin:0 auto}
.print-card .pn{font-family:var(--serif);font-weight:600;font-size:15px;margin-top:12px}
.print-card .pc{font-size:11.5px;color:var(--muted);margin-top:5px}.print-card .pc code{background:var(--gold-soft);color:var(--gold-dk);padding:1px 6px;border-radius:5px}
.print-card .pscan{font-size:11px;color:var(--gold-dk);margin-top:8px;font-weight:700}
table.acc{width:100%;border-collapse:collapse;font-size:14px}
table.acc th,table.acc td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}
table.acc th{background:var(--navy);color:#fff}
table.acc code{background:var(--gold-soft);color:var(--gold-dk);padding:1px 7px;border-radius:5px;font-weight:700}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media print{
  nav.tabs,header.top,.iconbtn,.noprint,.footer{display:none !important}
  body{background:#fff}
  .printgrid{grid-template-columns:repeat(2,1fr);gap:12px}
  .print-card{break-inside:avoid;border:1.5px dashed #999}
}
"""

# =====================================================================================
# APP JS  (namespace VL)
# =====================================================================================
APP_JS = r"""
var VL = (function(){
  var D = window.VILLA_DATA, L = window.VILLA_LOGOS||{}, ACC = window.VILLA_ACCOUNTS, ADM = window.VILLA_ADMIN;
  var cur=null, curTab="overview", adminMode=false;
  var TABS = [
    ["overview","Tổng quan"],["day","Một ngày làm việc"],["phrases","Câu nói chuẩn"],
    ["rules","Nên & Cấm"],["process","Quy trình chi tiết"],["checklist","Checklist"],
    ["kpi","KPI đánh giá"],["exc","Xử lý tình huống"],["road","Lộ trình 7 ngày"],["card","Thẻ tóm tắt"]
  ];
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
  function dept(id){return D.departments.find(function(x){return x.id===id})}
  function fillLogos(root){(root||document).querySelectorAll("img[data-logo]").forEach(function(im){var k=im.getAttribute("data-logo");if(L[k])im.src=L[k];});}

  function applyTheme(t){document.documentElement.setAttribute("data-theme",t);try{localStorage.setItem("v226-theme",t)}catch(e){}}
  function toggleTheme(){var c=document.documentElement.getAttribute("data-theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");applyTheme(c==="dark"?"light":"dark")}
  (function(){try{var t=localStorage.getItem("v226-theme");if(t)applyTheme(t)}catch(e){}})();

  function doLogin(ev){ev.preventDefault();
    var u=document.getElementById("u").value.trim().toLowerCase(),p=document.getElementById("p").value;
    authenticate(u,p,function(ok,msg){if(!ok)document.getElementById("loginErr").textContent=msg;});return false;}
  function authenticate(u,p,cb){
    if(u===ADM.user&&p===ADM.pass){session("admin");openAdmin();return cb&&cb(true);}
    if(ACC[u]&&ACC[u]===p){session(u);openApp(u);return cb&&cb(true);}
    cb&&cb(false,"Sai tài khoản hoặc mật khẩu. Vui lòng kiểm tra lại.");}
  function session(u){try{sessionStorage.setItem("v226-user",u)}catch(e){}}
  function logout(){try{sessionStorage.removeItem("v226-user")}catch(e){}location.hash="";location.reload();}
  function show(id){["login","app","admin"].forEach(function(s){document.getElementById(s).classList.toggle("hidden",s!==id)});}

  function openApp(id){cur=dept(id);if(!cur){logout();return;}
    document.getElementById("hIc").textContent=cur.icon;
    document.getElementById("hName").textContent=cur.name;
    document.getElementById("hRole").textContent=cur.short;
    var t=document.getElementById("tabs");t.innerHTML="";
    TABS.forEach(function(tb){var d=document.createElement("div");d.className="tab";d.textContent=tb[1];d.tabIndex=0;
      d.onclick=function(){setTab(tb[0])};d.onkeydown=function(e){if(e.key==="Enter")setTab(tb[0])};d.dataset.id=tb[0];t.appendChild(d);});
    document.getElementById("btnAdmin").classList.toggle("hidden",!adminMode);
    document.getElementById("btnLogout").classList.toggle("hidden",adminMode);
    show("app");setTab("overview");window.scrollTo(0,0);}
  function adminView(id){openApp(id);}
  function backToAdmin(){openAdmin();window.scrollTo(0,0);}
  function setTab(id){curTab=id;
    Array.prototype.forEach.call(document.querySelectorAll("#tabs .tab"),function(el){el.classList.toggle("active",el.dataset.id===id)});
    var host=document.getElementById("content");host.innerHTML=render(id);
    host.style.animation="none";void host.offsetWidth;host.style.animation="";
    var at=document.querySelector('#tabs .tab[data-id="'+id+'"]');if(at&&at.scrollIntoView)at.scrollIntoView({inline:"center",block:"nearest"});
    window.scrollTo({top:0});bindInteractive();}

  function heroHtml(){return '<div class="hero"><img class="wm" data-logo="v226" alt="">'+
    '<div class="eyebrow">Vai trò của bạn</div><div class="tl serif">'+esc(cur.tagline)+'</div>'+
    '<div class="rl">'+esc(cur.role)+'</div><span class="code">'+esc(cur.sop)+'</span></div>';}
  function secH(t){return '<div class="sec-h"><span class="mark"></span><h3 class="serif">'+esc(t)+'</h3><span class="line"></span></div>';}
  function render(id){var f={overview:renderOverview,day:renderDay,phrases:renderPhrases,rules:renderRules,process:renderProcess,
    checklist:renderChecklist,kpi:renderKpi,exc:renderExc,road:renderRoad,card:renderCard};
    var out=(f[id]||function(){return""})();fillLogosSoon();return out;}
  function fillLogosSoon(){setTimeout(function(){fillLogos(document.getElementById("content"))},0);}

  function renderOverview(){var h=heroHtml()+secH("Quy tắc Vàng của bạn");
    h+='<div class="card"><div class="card-b">'+cur.golden.map(function(g){return '<div class="golden"><span class="i">◆</span><div>'+esc(g)+'</div></div>';}).join("")+'</div></div>';
    var c=D.common;h+=secH(c.title+" — áp dụng chung cho mọi vị trí");
    h+='<div class="card"><div class="card-b"><div style="font-size:13.8px;color:var(--muted);margin-bottom:4px">'+esc(c.intro)+'</div>';
    c.blocks.forEach(function(b){h+='<div class="cblk"><h4 class="serif">'+esc(b.h)+'</h4><ul>'+b.items.map(function(it){return '<li>'+esc(it)+'</li>';}).join("")+'</ul></div>';});
    h+='</div></div>'+secH("Xem nhanh");
    var q=[["day","Một ngày làm việc","Nhật trình đầu–trong–cuối ca"],["card","Thẻ tóm tắt","Mang theo trong ca"],["checklist","Checklist ca","Tự chấm, có tiến độ"],["road","Lộ trình 7 ngày","Mục tiêu từng ngày"]];
    h+='<div class="quicknav">'+q.map(function(x){return '<button onclick="VL.setTab(\''+x[0]+'\')">'+esc(x[1])+'<span class="qsub">'+esc(x[2])+'</span></button>';}).join("")+'</div>';
    return h;}
  function shiftBlock(title,arr){var s='<div class="shift"><div class="shift-t"><span class="dot"></span>'+title+'</div>';
    arr.forEach(function(it,i){s+='<div class="step"><div class="k">'+(i+1)+'</div><div><div class="t">'+esc(it.t)+'</div>'+(it.s?'<div class="s">'+esc(it.s)+'</div>':'')+'</div></div>';});return s+'</div>';}
  function renderDay(){var s=cur.schedule;return secH("Nhật trình chuẩn một ngày")+'<div class="card"><div class="card-b">'+
    shiftBlock("Đầu ca — Chuẩn bị",s.before)+shiftBlock("Trong ca — Vận hành",s.during)+shiftBlock("Cuối ca — Tổng kết &amp; bàn giao",s.after)+'</div></div>';}
  function renderPhrases(){var h=secH("Câu nói chuẩn phải thuộc");
    if(!cur.phrases||!cur.phrases.length)return h+'<div class="card"><div class="card-b" style="color:var(--muted);font-size:14px">Vị trí này chủ yếu làm việc nội bộ / không giao tiếp khách theo kịch bản cố định — áp dụng chuẩn giao tiếp chung trong <b>Văn hoá &amp; Tiêu chuẩn 226</b> (tab Tổng quan).</div></div>';
    return h+'<div class="card"><div class="card-b">'+cur.phrases.map(function(p){return '<div class="phrase"><div class="sit">'+esc(p.sit)+'</div><div class="say">“'+esc(p.say)+'”</div></div>';}).join("")+'</div></div>';}
  function renderRules(){return secH("Những điều tuyệt đối")+'<div class="dd"><div class="col do"><h4>✓ Nên / Bắt buộc</h4><ul>'+
    cur.do.map(function(x){return '<li>'+esc(x)+'</li>';}).join("")+'</ul></div><div class="col dont"><h4>✕ Cấm / Tránh</h4><ul>'+
    cur.dont.map(function(x){return '<li>'+esc(x)+'</li>';}).join("")+'</ul></div></div>';}
  function renderProcess(){var s=cur.schedule,h=secH("Quy trình chi tiết &amp; Quy tắc vàng")+'<div class="card"><div class="card-b">';
    cur.golden.forEach(function(g){h+='<div class="golden"><span class="i">◆</span><div>'+esc(g)+'</div></div>';});
    h+='</div></div><div class="card"><div class="card-b">'+shiftBlock("Đầu ca",s.before)+shiftBlock("Trong ca",s.during)+shiftBlock("Cuối ca",s.after)+'</div></div>';return h;}
  function stateKey(k){return "v226-"+k+"-"+cur.id;}
  function getState(k){try{return JSON.parse(localStorage.getItem(stateKey(k))||"[]")}catch(e){return[]}}
  function setState(k,a){try{localStorage.setItem(stateKey(k),JSON.stringify(a))}catch(e){}}
  function renderChecklist(){var st=getState("chk"),tot=cur.checklist.length,done=st.length;
    var h=secH("Checklist ca của bạn")+'<div class="card"><div class="card-b"><div class="progress-lbl" id="chkLbl">Hoàn thành '+done+'/'+tot+'</div><div class="progress"><i id="chkBar" style="width:'+(tot?done/tot*100:0)+'%"></i></div>';
    cur.checklist.forEach(function(c,i){h+='<div class="chk'+(st.indexOf(i)>=0?" on":"")+'" data-i="'+i+'" data-kind="chk"><div class="box">✓</div><div class="ci">'+esc(c.item)+'</div><div class="cw">'+esc(c.when)+'</div></div>';});
    return h+'<div style="text-align:center;margin-top:14px"><button class="btn ghost" style="width:auto;padding:9px 18px;font-size:13px" onclick="VL.resetChk()">Bỏ chọn tất cả</button></div></div></div>';}
  function renderRoad(){var st=getState("road"),h=secH("Lộ trình 7 ngày đầu")+'<div class="card"><div class="note-b">Người kèm cặp (Quản lý Vận hành) đánh giá bạn theo lộ trình này. Đạt hết mục tiêu → đứng ca độc lập. Bấm để đánh dấu ngày đã đạt.</div><div class="card-b">';
    cur.roadmap.forEach(function(r,i){h+='<div class="day'+(st.indexOf(i)>=0?" on":"")+'" data-i="'+i+'" data-kind="road"><div class="dn serif">'+esc(r.day)+'</div><div class="dbody"><div class="goal">'+esc(r.goal)+'</div><div class="pass">✔ Đạt khi: '+esc(r.pass)+'</div></div><div class="dcheck">✓</div></div>';});
    return h+'</div></div>';}
  function renderKpi(){var h=secH("KPI đánh giá")+'<div class="card"><div class="note-b">Chu kỳ đánh giá hằng tháng. Cột phải là ngưỡng <b>mục tiêu</b>. Ngưỡng khởi điểm điều chỉnh sau 3 tháng vận hành thực tế.</div><div class="card-b">';
    cur.kpi.forEach(function(k){h+='<div class="kpi"><div class="g">'+esc(k.group)+'</div><div class="nm">'+esc(k.name)+'</div><div class="gd">'+esc(k.good)+'</div></div>';});
    return h+'</div></div>';}
  function renderExc(){return secH("Xử lý tình huống phát sinh")+'<div class="card"><div class="card-b">'+cur.exceptions.map(function(e){return '<div class="exc"><div class="q"><span class="i">▲</span>'+esc(e.sit)+'</div><div class="a">→ '+esc(e.fix)+'</div></div>';}).join("")+'</div></div>';}
  function renderCard(){return secH("Thẻ tóm tắt — mang theo trong ca")+'<div class="tcard"><img class="wm" data-logo="v226" alt="">'+
    cur.card.map(function(c){return '<div class="tk"><div class="k">'+esc(c.k)+'</div><div class="v">'+esc(c.v)+'</div></div>';}).join("")+'<div class="note">Lưu màn hình này, mang theo trong ca cho đến khi thuộc.</div></div>';}

  function bindInteractive(){Array.prototype.forEach.call(document.querySelectorAll(".chk,.day"),function(el){
    el.onclick=function(){var kind=el.dataset.kind,i=parseInt(el.dataset.i,10),st=getState(kind),pos=st.indexOf(i);
      if(pos>=0)st.splice(pos,1);else st.push(i);setState(kind,st);el.classList.toggle("on");
      if(kind==="chk"){var done=getState("chk").length,tot=cur.checklist.length,bar=document.getElementById("chkBar"),lbl=document.getElementById("chkLbl");
        if(bar)bar.style.width=(tot?done/tot*100:0)+"%";if(lbl)lbl.textContent="Hoàn thành "+done+"/"+tot;}};});}
  function resetChk(){setState("chk",[]);setTab("checklist");}

  function drawQR(canvas,text){var q=QRCode.generate(text),n=q.size,quiet=4,total=n+quiet*2;
    var px=Math.floor(canvas.width/total),size=px*total,off=Math.floor((canvas.width-size)/2),ctx=canvas.getContext("2d");
    ctx.fillStyle="#fff";ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle=QR_DARK;
    for(var r=0;r<n;r++)for(var c=0;c<n;c++)if(q.modules[r][c])ctx.fillRect(off+(c+quiet)*px,off+(r+quiet)*px,px,px);}
  function loginUrl(user){var base=(document.getElementById("baseUrl")&&document.getElementById("baseUrl").value.trim())||(location.origin+location.pathname);
    return base+"#login="+encodeURIComponent(user)+"~"+encodeURIComponent(ACC[user]);}

  function openAdmin(){adminMode=true;show("admin");var sel=document.getElementById("admDept");sel.innerHTML="";
    D.departments.forEach(function(d){var o=document.createElement("option");o.value=d.id;o.textContent=d.icon+"  "+d.name;sel.appendChild(o);});
    var g=document.getElementById("admDeptGrid");g.innerHTML="";
    D.departments.forEach(function(d){var b=document.createElement("button");b.onclick=function(){adminView(d.id)};b.innerHTML=esc(d.icon+"  "+d.name)+'<span class="qsub">'+esc(d.short)+'</span>';g.appendChild(b);});
    fillLogos(document);renderAdmin();renderAccTable();admTab("main");}
  function admTab(name){["main","qr","acc"].forEach(function(n){var el=document.getElementById("adm_"+n);if(el)el.classList.toggle("hidden",n!==name);});
    Array.prototype.forEach.call(document.querySelectorAll("#admTabs .tab"),function(el){el.classList.toggle("active",el.dataset.at===name);});window.scrollTo(0,0);}
  function renderAdmin(){var id=document.getElementById("admDept").value,d=dept(id);
    drawQR(document.getElementById("admQr"),loginUrl(id));
    document.getElementById("admCred").innerHTML='<div><b>'+esc(d.icon+" "+d.name)+'</b></div><div style="margin-top:6px">Tài khoản <code>'+esc(id)+'</code> &nbsp; Mật khẩu <code>'+esc(ACC[id])+'</code></div><div style="font-size:12px;color:var(--muted);margin-top:9px">Quét QR = đăng nhập thẳng. Hoặc gõ tài khoản/mật khẩu trên.</div>';
    renderPrintGrid();}
  function renderPrintGrid(){var g=document.getElementById("printGrid");g.innerHTML="";
    D.departments.forEach(function(d){var card=document.createElement("div");card.className="print-card";
      var lg=document.createElement("img");lg.className="plotus";if(L.v226)lg.src=L.v226;lg.alt="";card.appendChild(lg);
      var cv=document.createElement("canvas");cv.width=300;cv.height=300;card.appendChild(cv);
      var nm=document.createElement("div");nm.className="pn serif";nm.textContent=d.icon+" "+d.name;card.appendChild(nm);
      var pc=document.createElement("div");pc.className="pc";pc.innerHTML="TK <code>"+esc(d.id)+"</code> · MK <code>"+esc(ACC[d.id])+"</code>";card.appendChild(pc);
      var ps=document.createElement("div");ps.className="pscan";ps.textContent="Quét để vào ca";card.appendChild(ps);
      g.appendChild(card);drawQR(cv,loginUrl(d.id));});}
  function renderAccTable(){var t=document.getElementById("accTable"),h="<tr><th>Vị trí / Bộ phận</th><th>Tài khoản</th><th>Mật khẩu</th></tr>";
    D.departments.forEach(function(d){h+="<tr><td>"+esc(d.icon+" "+d.name)+"</td><td><code>"+esc(d.id)+"</code></td><td><code>"+esc(ACC[d.id])+"</code></td></tr>";});
    h+='<tr><td>⚙️ Quản trị (Nhân sự)</td><td><code>'+esc(ADM.user)+'</code></td><td><code>'+esc(ADM.pass)+'</code></td></tr>';t.innerHTML=h;}
  function copyCred(){var lines=D.departments.map(function(d){return d.name+"\t"+d.id+"\t"+ACC[d.id];});
    lines.unshift("Vị trí\tTài khoản\tMật khẩu");var txt=lines.join("\n");
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(function(){alert("Đã sao chép danh sách tài khoản.")});else prompt("Sao chép danh sách:",txt);}

  function boot(){fillLogos(document);
    var m=location.hash.match(/login=([^~&]+)~([^&]+)/);
    if(m){var u=decodeURIComponent(m[1]),p=decodeURIComponent(m[2]);history.replaceState(null,"",location.pathname+location.search);
      authenticate(u,p,function(ok){if(!ok){show("login");document.getElementById("loginErr").textContent="Mã QR không hợp lệ hoặc đã đổi mật khẩu.";}});return;}
    var s;try{s=sessionStorage.getItem("v226-user")}catch(e){}
    if(s==="admin"){openAdmin();return;}
    if(s&&ACC[s]){openApp(s);return;}
    show("login");}
  return {doLogin:doLogin,logout:logout,toggleTheme:toggleTheme,setTab:setTab,resetChk:resetChk,renderAdmin:renderAdmin,copyCred:copyCred,boot:boot,adminView:adminView,backToAdmin:backToAdmin,admTab:admTab};
})();
window.addEventListener("DOMContentLoaded",VL.boot);
"""

# =====================================================================================
# HTML skeleton
# =====================================================================================
BODY = r"""
<section id="login">
  <img class="watermark" data-logo="v226" alt="">
  <form class="card-login" onsubmit="return VL.doLogin(event)">
    <img class="lotus" data-logo="v226" alt="Villa 226">
    <div class="brand">Hệ thống Vận hành</div>
    <div class="rule"></div>
    <h1 class="serif">Quy trình &amp; Cẩm nang</h1>
    <div class="sub">Quy trình số hoá theo từng vị trí</div>
    <div class="field"><label>Tài khoản (vị trí)</label>
      <div class="ip"><input id="u" type="text" autocomplete="username" autocapitalize="none" spellcheck="false" placeholder="vd: quan-gia"></div></div>
    <div class="field"><label>Mật khẩu</label>
      <div class="ip"><input id="p" type="password" autocomplete="current-password" placeholder="Mật khẩu được cấp"></div></div>
    <button class="btn" type="submit">Đăng nhập</button>
    <div class="err" id="loginErr"></div>
    <div class="hint">Nhân viên: <b>quét mã QR</b> được cấp là vào thẳng phần việc của mình. Quên mật khẩu? Liên hệ Quản lý / Nhân sự.<br><a href="index.html" style="color:var(--gold-dk);font-weight:600">← Về villa226.com</a></div>
  </form>
</section>

<section id="app" class="hidden">
  <header class="top"><div class="wrap">
    <div class="dept-ic" id="hIc">🏝️</div>
    <div><div class="eyebrow">Villa 226 · Vị trí</div><h2 id="hName">—</h2><div class="role" id="hRole">—</div></div>
    <div class="spacer"></div>
    <button class="iconbtn hidden" id="btnAdmin" onclick="VL.backToAdmin()" title="Về trang quản trị">← Quản trị</button>
    <button class="iconbtn" onclick="VL.toggleTheme()" title="Đổi giao diện sáng/tối" aria-label="Đổi giao diện">◐</button>
    <button class="iconbtn" id="btnLogout" onclick="VL.logout()">Đăng xuất</button>
  </div></header>
  <nav class="tabs"><div class="tabs-scroll" id="tabs"></div></nav>
  <main><div class="wrap" id="content"></div></main>
  <div class="footer"><img data-logo="v226" alt="Villa 226"><span class="fdiv"></span><span>Hệ thống Quy trình số hoá · <b>Công ty CP Du lịch 226</b> · Tài liệu nội bộ</span></div>
</section>

<section id="admin" class="hidden">
  <div class="adm-h noprint"><div class="wrap">
    <div class="dept-ic">⚙️</div>
    <div><div class="eyebrow" style="color:var(--gold-lt)">Villa 226</div><h2 class="serif">Quản trị · Tạo mã QR đăng nhập</h2></div>
    <div class="spacer" style="flex:1"></div>
    <button class="iconbtn noprint" onclick="VL.toggleTheme()" title="Đổi giao diện">◐</button>
    <button class="iconbtn noprint" onclick="VL.logout()">Đăng xuất</button>
  </div></div>
  <div class="wrap noprint"><div class="tabs-scroll" id="admTabs" style="padding:12px 0">
    <div class="tab active" data-at="main" onclick="VL.admTab('main')">⚙️ Trang chính</div>
    <div class="tab" data-at="qr" onclick="VL.admTab('qr')">🖨️ Thẻ QR để in</div>
    <div class="tab" data-at="acc" onclick="VL.admTab('acc')">🔑 Danh sách tài khoản</div>
  </div></div>
  <div class="wrap" style="padding-bottom:20px">
    <div id="adm_main">
      <div class="card noprint"><div class="card-b">
        <div class="field" style="margin-bottom:10px"><label>Đường dẫn (URL) nơi đăng tải app — để mã QR mở đúng trang</label>
          <input id="baseUrl" type="text" value="__BASEURL__" oninput="VL.renderAdmin()"></div>
        <div style="font-size:12.5px;color:var(--muted)">Để trống nếu chỉ dùng nội bộ. Xem tất cả thẻ QR ở tab <b>Thẻ QR để in</b>, mật khẩu ở tab <b>Danh sách tài khoản</b>.</div>
      </div></div>
      <div class="adm-grid" style="margin-top:14px">
        <div class="card"><div class="card-b">
          <div class="field"><label>Xem/tạo mã QR một vị trí</label><select id="admDept" onchange="VL.renderAdmin()"></select></div>
          <div class="qrframe" style="margin-top:12px"><img class="lotus" data-logo="v226" alt="Villa 226"><div><canvas id="admQr" width="224" height="224"></canvas></div></div>
          <div class="cred" id="admCred"></div>
        </div></div>
        <div class="card"><div class="card-b">
          <h3 class="serif" style="font-size:17px;margin-bottom:8px">Hướng dẫn phát hành</h3>
          <ol style="font-size:13.5px;color:var(--muted);padding-left:18px;line-height:1.75;margin:0">
            <li>Nhập URL nơi đăng tải file này (nếu có).</li>
            <li>Sang tab <b>Thẻ QR để in</b> → bấm In → phát cho nhân viên.</li>
            <li>Nhân viên quét QR là vào thẳng phần việc của mình.</li>
            <li>Xem nội dung từng vị trí ở lưới bên dưới.</li>
          </ol>
        </div></div>
      </div>
      <div class="sec-h"><span class="mark"></span><h3 class="serif">Xem nội dung từng vị trí</h3><span class="line"></span></div>
      <div class="note-b" style="border:1px solid var(--line);border-radius:14px;margin-bottom:12px">Bấm một vị trí để xem đúng nội dung nhân viên vị trí đó nhìn thấy. Xem xong bấm <b>← Quản trị</b> ở góc trên để quay lại.</div>
      <div class="quicknav" id="admDeptGrid" style="grid-template-columns:repeat(3,1fr)"></div>
    </div>
    <div id="adm_qr" class="hidden">
      <div class="sec-h"><span class="mark"></span><h3 class="serif">Toàn bộ thẻ QR — để in &amp; phát</h3><span class="line"></span></div>
      <div class="note-b noprint" style="border:1px solid var(--line);border-radius:14px;margin-bottom:12px">Mỗi thẻ gồm logo + mã QR + tài khoản. Bấm nút để in, cắt và phát cho từng vị trí. Nhân viên quét QR là đăng nhập thẳng.</div>
      <button class="btn noprint" style="margin-bottom:14px" onclick="window.print()">🖨️  In toàn bộ thẻ QR</button>
      <div class="printgrid" id="printGrid"></div>
    </div>
    <div id="adm_acc" class="hidden">
      <div class="sec-h"><span class="mark"></span><h3 class="serif">Danh sách tài khoản</h3><span class="line"></span></div>
      <div class="card noprint"><div class="card-b">
        <button class="btn ghost" style="width:auto;padding:9px 16px;font-size:13px;margin-bottom:12px" onclick="VL.copyCred()">📋  Sao chép danh sách</button>
        <div style="overflow-x:auto"><table class="acc" id="accTable"></table></div>
        <div style="font-size:12px;color:var(--muted);margin-top:12px">⚠️ Tài liệu nội bộ. Giữ danh sách này bảo mật.</div>
      </div></div>
    </div>
  </div>
  <div class="footer noprint"><img data-logo="v226" alt="Villa 226"><span class="fdiv"></span><span><b>Công ty CP Du lịch 226</b> — Villa 226 · Tài liệu nội bộ</span></div>
</section>
"""

# =====================================================================================
# GHÉP FILE
# =====================================================================================
def build():
    data_js = ("window.VILLA_DATA=" + json.dumps(DATA, ensure_ascii=False) + ";\n"
               "window.VILLA_ACCOUNTS=" + json.dumps(ACCOUNTS, ensure_ascii=False) + ";\n"
               "window.VILLA_ADMIN=" + json.dumps(ADMIN, ensure_ascii=False) + ";\n"
               "window.VILLA_LOGOS={v226:\"" + LOGO + "\"};\n"
               "var QR_DARK=\"" + QR_DARK + "\";\n")
    body = BODY.replace("__BASEURL__", BASE_URL_DEFAULT)
    html = (
      "<!doctype html>\n<html lang=\"vi\">\n<head>\n<meta charset=\"utf-8\">\n"
      "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
      "<meta name=\"theme-color\" content=\"#14547A\">\n"
      "<title>Villa 226 — Quy trình &amp; Cẩm nang</title>\n"
      "<link rel=\"icon\" type=\"image/png\" href=\"img/logo-226.png\">\n"
      "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
      "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
      "<link href=\"https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap\" rel=\"stylesheet\">\n"
      "<style>\n" + CSS.strip() + "\n</style>\n</head>\n<body>\n"
      + body +
      "\n<script>\n" + QRLIB.strip() + "\n</script>\n"
      "<script>\n" + data_js + "</script>\n"
      "<script>\n" + APP_JS.strip() + "\n</script>\n"
      "</body>\n</html>\n"
    )
    open(OUT, "w", encoding="utf-8").write(html)
    print("✓ Đã sinh:", OUT)
    print("  Vị trí/bộ phận:", len(DEPARTMENTS), "· Kích thước:", round(len(html)/1024), "KB")
    print("  Tài khoản mẫu: quan-gia /", ACCOUNTS["quan-gia"], "· admin /", ADMIN["pass"])

if __name__ == "__main__":
    build()
