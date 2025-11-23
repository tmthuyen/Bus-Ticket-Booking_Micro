import './App.css';
import AllRoute from '../src/components/AllRoutes/AllRoute'
import api, { TOKEN_KEYS } from './api/api';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    const initToken = async() => {
      const anonymousToken = localStorage.getItem(TOKEN_KEYS.BUS_ANONYMOUS_TOKEN);
      if (anonymousToken) return;

      try {
        const resp = await api.post('/users/auth/anonymous');
        console.log('Anonymous token response:', resp.data);
        const token = resp.data?.data.bus_anonymous_token;
        if (token) {
          localStorage.setItem(TOKEN_KEYS.BUS_ANONYMOUS_TOKEN, token);
        } else{
          throw new Error('Token not found in response');
        }
      } catch (error) {
        console.error('Error fetching anonymous token:', error);
      }
    }
    initToken();
  }, []);

  return (
    <div className="App">
      <AllRoute />
    </div>
  );
}

export default App;
