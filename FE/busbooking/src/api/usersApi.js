// auth.ts
import axios from 'axios';
import api, { TOKEN_KEYS } from '../api/api.js';
import { API_DOMAIN } from '../constants/index.js';

const login = async (username, password) => {
  const body = new URLSearchParams();
  body.append('username', username);
  body.append('password', password);

  const response = await api.post('/users/auth/login', body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return {
    responseApi: response.data,
  };
};

const getMe = async () => {
  
  const response = await axios.get(API_DOMAIN + '/users/auth/me', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem(TOKEN_KEYS.BUS_ACCESS_TOKEN)}` }
  });
  return {
    responseApi: response.data,
  };
};

const register = async (
  full_name,
  email,
  phone,
  password,
  confirm_password
) => {
  const body = {
    full_name,
    email,
    phone,
    password,
    confirm_password,
  };
  const response = await api.post('/users/auth/register', body);
  return {
    responseApi: response.data,
  };
};

export { login, getMe, register };
