import { useNavigate } from 'react-router-dom';
import { API_DOMAIN } from '../constants';

export const useRequest = () => {
  const navigate = useNavigate();

  const getToken = () => localStorage.getItem('access_token') || null;

  const request = async (method, path, body = null) => {
    const headers = { Accept: 'application/json' };
    const token = getToken();

    if (!token) {
      navigate('/login');
      return;
    }

    headers.Authorization = `Bearer ${token}`;
    if (body) headers['Content-Type'] = 'application/json';

    const res = await fetch(API_DOMAIN + path, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (res.status === 401) {
      localStorage.removeItem('access_token');
      navigate('/login');
      return;
    }

    if (!res.ok) {
      const errorBody = await res.text();
      throw new Error(`HTTP error! status: ${res.status}, body: ${errorBody}`);
    }

    return res.json();
  };

  return {
    get: (path) => request('GET', path),
    post: (path, body) => request('POST', path, body),
    edit: (path, body) => request('PUT', path, body),
    del: (path) => request('DELETE', path),
  };
};
