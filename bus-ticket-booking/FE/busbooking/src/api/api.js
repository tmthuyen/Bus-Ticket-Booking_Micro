// api.ts
import axios from "axios";
import { API_DOMAIN } from "../constants";
const api = axios.create({
  baseURL: API_DOMAIN,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // để cookie refresh/CSRF tự đi kèm khi bạn dùng /token/refresh
});

let accessToken = null;
const setAccessToken = (t) => { 
  accessToken = t; 
}

api.interceptors.request.use((cfg) => {
  const token = accessToken || localStorage.getItem("access_token");
  if (token) {
    cfg.headers = cfg.headers ?? {};
    cfg.headers.Authorization = `Bearer ${token}`;
  }
  return cfg;
});

// api error helper: bóc tách lỗi axios
const parseAxiosError = (err) => {
  const resp = err?.response;
  return {
    success: resp?.success,
    data: resp?.data,
    message:
      resp?.data?.message ||
      resp?.data?.detail ||
      err?.message ||
      "Có lỗi xảy ra. Vui lòng thử lại.",
  };
}

// map lỗi Pydantic 422 => set vào field AntD
const setPydanticErrorsToForm = (form, detail) => {
  if (!Array.isArray(detail)) return;
  const fields = detail
    .map((d) => {
      // pydantic: {"loc": ["body","email"], "msg": "..."}
      const loc = d.loc || [];
      const name = loc[loc.length - 1]; // "email", "password", ...
      if (typeof name !== "string") return null;
      return { name, errors: [d.msg || "Giá trị không hợp lệ"] };
    })
    .filter(Boolean);
  if (fields.length) form.setFields(fields);
}

export { 
  setAccessToken,
  parseAxiosError, 
  setPydanticErrorsToForm 
};

export default api;
