import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { App as AntApp } from "antd";
import { CssBaseline, ThemeProvider } from '@mui/material';
import './index.css';
import App from './App';
import theme from './config/themeMui';
import store from './store/store';
import { LoadingProvider } from './context/LoadingContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AntApp>
          <LoadingProvider>
            <App />
          </LoadingProvider>
        </AntApp>
      </ThemeProvider>
    </Provider>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
