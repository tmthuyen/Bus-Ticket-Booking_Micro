// utils/timeVN.js
// Nhận chuỗi ISO. Nếu KHÔNG có 'Z' hay offset, hiểu là UTC và thêm 'Z'
export function parseAsUTC(iso) {
  if (!iso) return null;
  const looksNaive = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$/.test(iso);
  return new Date(looksNaive ? iso + "Z" : iso);
}

export function formatVN(isoLike) {
  if (!isoLike) return "—";
  const d = parseAsUTC(isoLike);
  if (Number.isNaN(d.getTime())) return String(isoLike);
  return new Intl.DateTimeFormat("vi-VN", {
    timeZone: "Asia/Ho_Chi_Minh",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(d);
}
