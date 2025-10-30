const formatDate = (v) => {
  if (!v) return '-';
  const d = new Date(v); // v nên là ISO (có hoặc không có timezone)
  if (Number.isNaN(d.getTime())) return v; // fallback nếu không parse được
  return d.toLocaleString('vi-VN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false
  });
};

export {
    formatDate
}