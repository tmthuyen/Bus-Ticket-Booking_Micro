// api.ts
import axios from 'axios';
import { API_DOMAIN } from '../constants';
import { message } from 'antd';

export const TOKEN_KEYS = {
  BUS_ANONYMOUS_TOKEN: 'bus_anonymous_token',
  BUS_ACCESS_TOKEN: 'bus_access_token',
  BUS_REFRESH_TOKEN: 'bus_refresh_token',
}

const api = axios.create({
  baseURL: API_DOMAIN,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // để cookie refresh/CSRF tự đi kèm khi bạn dùng /token/refresh
});

let accessToken = null;
const setAccessToken = (t) => {
  accessToken = t;
};

api.interceptors.request.use((cfg) => {
  const token = accessToken || localStorage.getItem(TOKEN_KEYS.BUS_ANONYMOUS_TOKEN);
  if (token) {
    cfg.headers = cfg.headers ?? {};
    cfg.headers.Authorization = `Bearer ${token}`;
  }
  return cfg;
});

let isRefreshing = false;
let hasShown401 = false;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalConfig = error.config;

    if (error.response?.status === 401 && !isRefreshing) {
      isRefreshing = true;
      if (!hasShown401) {
        hasShown401 = true;
        // 📢 Thông báo global
        message.error('Phiên làm việc đã hết hạn, hệ thống sẽ tải lại.', 2);
      }
      try {
        // xoá token cũ
        localStorage.removeItem(TOKEN_KEYS.BUS_ANONYMOUS_TOKEN);

        // gọi lấy token anonymous mới (dùng axios gốc để tránh loop interceptor)
        const res = await axios.post(`${API_DOMAIN}/users/auth/anonymous`);
        const token = res.data?.data.bus_anonymous_token;
        console.log('Anonymous token response during refresh:', res.data?.data.bus_access_token);
        if (token) {
          console.log('Refreshed anonymous token response:', token);
          localStorage.setItem(TOKEN_KEYS.BUS_ANONYMOUS_TOKEN, token);
        }

      } catch (err) {
        console.error('Failed to refresh anonymous token', err);
        return Promise.reject(error);
      } finally {
        isRefreshing = false;
        hasShown401 = false;
        // setTimeout(() => {
        //     if (window.location.pathname !== '/') {
        //       window.location.href = '/';
        //     } else {
        //       // nếu đã ở / rồi thì chỉ reload lại
        //       window.location.reload();
        //     }
        //   }, 1500); 
      }

      const newToken = localStorage.getItem(TOKEN_KEYS.BUS_ANONYMOUS_TOKEN);
      if (newToken) {
        // console.log('Retrying original request with new token', newToken);
        originalConfig.headers = originalConfig.headers ?? {};
        originalConfig.headers.Authorization = `Bearer ${newToken}`;
        //window.location.reload(); // reload lại trang sau khi có token mới
        return api(originalConfig); // ✅ retry request cũ
      }
    }

    return Promise.reject(error);
  }
);

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
      'Có lỗi xảy ra. Vui lòng thử lại.',
  };
};

// map lỗi Pydantic 422 => set vào field AntD
const setPydanticErrorsToForm = (form, detail) => {
  if (!Array.isArray(detail)) return;
  const fields = detail
    .map((d) => {
      // pydantic: {"loc": ["body","email"], "msg": "..."}
      const loc = d.loc || [];
      const name = loc[loc.length - 1]; // "email", "password", ...
      if (typeof name !== 'string') return null;
      return { name, errors: [d.msg || 'Giá trị không hợp lệ'] };
    })
    .filter(Boolean);
  if (fields.length) form.setFields(fields);
};

export { setAccessToken, parseAxiosError, setPydanticErrorsToForm };

export default api;
