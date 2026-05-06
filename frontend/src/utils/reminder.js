export function requestNotificationPermission() {
  if (!("Notification" in window)) return;

  if (Notification.permission !== "granted") {
    Notification.requestPermission();
  }
}

export function sendNotification(title, body) {
  if (Notification.permission === "granted") {
    new Notification(title, { body });
  }
}