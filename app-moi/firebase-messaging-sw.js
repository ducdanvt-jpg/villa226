/* Nhận thông báo việc khi app đang đóng (Web Push qua Firebase Cloud Messaging).
   Thông báo do bot gửi kèm tiêu đề và nội dung nên trình duyệt tự hiện, bấm vào thì mở villa226.com/app. */
importScripts(
  "https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js",
  "https://www.gstatic.com/firebasejs/10.14.1/firebase-messaging-compat.js",
  "firebase-config.js"
);
firebase.initializeApp(self.FB_CONFIG);
firebase.messaging();
