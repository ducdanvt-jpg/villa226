/* Thông tin dự án Firebase của 226 Villa (dự án villa226-69510).
   Những giá trị này không phải mật khẩu, để công khai được: quyền truy cập do firestore.rules quyết định. */
self.FB_CONFIG = {
  apiKey: "AIzaSyAvJ3rS8u8q5gVsOTPi88TSwVu4jClZbBk",
  authDomain: "villa226-69510.firebaseapp.com",
  projectId: "villa226-69510",
  storageBucket: "villa226-69510.firebasestorage.app",
  messagingSenderId: "939040704242",
  appId: "1:939040704242:web:6dce964fcdcc9b1833f26b"
};
/* Email chủ app: có toàn quyền. Phải giống email trong firestore.rules. */
self.FB_OWNERS = ["ducdanvt@gmail.com"];
/* Khóa Web Push (VAPID) để bật thông báo trên điện thoại: Firebase console, Project settings, tab Cloud Messaging,
   mục Web Push certificates, Generate key pair, chép khóa công khai (chuỗi dài bắt đầu bằng chữ B). Để trống thì ẩn nút bật thông báo. */
self.FB_VAPID = "BEQblF7Hre7fIV0GaZ-DJfLRUQQTkWexYuIg22QtUy4P3Gah_9hYTABp3U9o2GbLTsrcoTCoODPm9twznuRhzFE";
