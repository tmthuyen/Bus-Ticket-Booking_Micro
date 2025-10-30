// auth.ts
import api, { setAccessToken } from "../api/api.js";

export async function login(username, password) {
  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const { data } = await api.post("/users/auth/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  // Nếu backend trả bọc successResponse:
  // const token = data.data?.access_token;
  const token = data.access_token ?? data?.data?.access_token;
  setAccessToken(token);
  return token;
}

export async function getMe() {
  const { data } = await api.get("/users/auth/me");
  return data;
}

export async function register(full_name, email, phone, password, confirm_password) {
  const body = {
    full_name,
    email,
    phone,
    password,
    confirm_password,
  };
  const { data } = await api.post("/users/auth/register", body);
  return data;
}
