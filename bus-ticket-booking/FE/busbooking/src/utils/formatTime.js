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

// Múi giờ VN
const VN_TZ = "Asia/Ho_Chi_Minh";
const VN_LOCALE = "vi-VN";

/**
 * Nhận vào chuỗi ISO (YYYY-MM-DD hoặc ISO có giờ),
 * trả ra chuỗi ngày kiểu Việt.
 */
export function formatVNDate(
  dateInput,
  { withWeekday = true, withTime = false, timeZone = VN_TZ } = {}
) {
  if (!dateInput) return "—";

  let d;

  if (typeof dateInput === "string") {
    // YYYY-MM-DD
    if (/^\d{4}-\d{2}-\d{2}$/.test(dateInput)) {
      // nếu coi ngày này là UTC:
      d = new Date(dateInput + "T00:00:00Z");
      // nếu muốn coi là 00:00 giờ VN: new Date(dateInput + "T00:00:00+07:00")
    } else {
      // ISO có giờ: dùng parseAsUTC (thêm Z nếu thiếu)
      d = parseAsUTC(dateInput);
    }
  } else {
    d = new Date(dateInput);
  }

  if (Number.isNaN(d.getTime())) return String(dateInput);

  const baseOpts = {
    timeZone,
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    ...(withWeekday ? { weekday: "long" } : {}),
  };

  const fmtDate = new Intl.DateTimeFormat(VN_LOCALE, baseOpts).format(d);

  if (!withTime) return fmtDate;

  const time = new Intl.DateTimeFormat(VN_LOCALE, {
    timeZone,
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(d);

  return `${fmtDate}, ${time}`;
}


/** Hiển thị khoảng ngày kiểu Việt (tự gọn khi cùng tháng/năm) */
export function formatVNDateRange(startISO, endISO, { timeZone = VN_TZ } = {}) {
  const start = new Date(startISO);
  const end = new Date(endISO);
  const sameYear  = start.getUTCFullYear() === end.getUTCFullYear();
  const sameMonth = sameYear && (start.getUTCMonth() === end.getUTCMonth());

  const d = (opts) => new Intl.DateTimeFormat("vi-VN", { timeZone, ...opts }).format;
  const short = { day: "2-digit", month: "2-digit", year: "numeric" };
  const noYear = { day: "2-digit", month: "2-digit" };

  if (sameYear && sameMonth) {
    // "13–15/12/2025"
    return `${d("vi-VN", { timeZone, day: "2-digit" }).call(null, start)}–${d("vi-VN", { timeZone, day: "2-digit" }).call(null, end)}/${String(end.getUTCMonth()+1).padStart(2,"0")}/${end.getUTCFullYear()}`;
  }
  // Khác tháng/năm: "13/12/2025 – 02/01/2026"
  return `${d(short)(start)} – ${d(short)(end)}`;
}


export function formatHM(totalMinutes) {
  if (!totalMinutes && totalMinutes !== 0) return "--";
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return `${h}g ${m}p`;
}

export function diffMinutes(a, b) {
  const start = new Date(a).getTime();
  const end = new Date(b).getTime();
  return Math.max(0, Math.round((end - start) / 60000));
}
