import { API_DOMAIN } from '../constants';

const getToken = () => localStorage.getItem('access_token') || null;

const request = async (method, path, body = null) => {
  const headers = {
    Accept: 'application/json',
  };
  const token = getToken();
  // console.log('Token:', token);
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body) headers['Content-Type'] = 'application/json';

  const res = await fetch(API_DOMAIN + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  // ⚡ Nếu API trả về 401 → token sai/hết hạn
  if (res.status === 401) {
    console.log(localStorage.getItem('access_token'));
    localStorage.removeItem('access_token'); // xoá token
    window.location.href = '/login';         // redirect về login
    return;
  }

  if (!res.ok) {
    const errorBody = await res.text(); 
    console.error('API error body:', JSON.parse(errorBody));
    return {
      status: res.status,
      message: `HTTP error! status: ${res.status}, body: ${errorBody}` || res.statusText,
      data: null,
    }; 
  }

  // 204 No Content
  if (res.status === 204) {
    return { status: 'ok', message: 'No content', data: null, status_code: 204 };
  }

  const data = await res.json();

  return data;
};

export const get = (path) => request('GET', path);
export const post = (path, body) => request('POST', path, body);
export const edit = (path, body) => request('PUT', path, body);
export const del = (path) => request('DELETE', path);
