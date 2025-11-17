import LayoutDefault from '../components/layout/LayoutDefault/LayoutDefault';
import Login from '../components/pages/Login';
import Logout from '../components/pages/Logout';
import ErrorPage from '../components/pages/ErrorPage';
import Home from '../components/pages/Home/Home';
import Register from '../components/pages/Register';
import ProtectedRoute from './ProtectedRoute';
import TripList from '../components/pages/Trip/TripList';
import RouteList from '../components/pages/Route/RouteList'; 

export const routes = [
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/register',
    element: <Register />,
  },
  {
    path: '/logout',
    element: <Logout />,
  },
  {
    path: '/protected',
    element: <ProtectedRoute />, // 🔒 Bọc lại
    children: [],
  },
  {
    path: '/',
    element: <LayoutDefault />, // layout
    children: [
      {
        path: '',
        element: <Home />,
      },
      {
        path: 'routes',
        element: <RouteList />,
      },
      {
        path: 'trips',
        element: <TripList />,
      },
      {
        path: 'bookings',
        element: <div>Bookings</div>,
      },
      {
        path:'profile',
        element:<div>Profile</div>,
      },
      {
        path: 'contact',
        element: <div>Contact</div>,
      } 
    ],
  },
  {
    path: '/error?status=:status&message=:message',
    element: <ErrorPage />,
  },
  {
    path: '*',
    element: <ErrorPage status={404} message={'Page Not Found'} />,
  },
];
