import LayoutDefault from '../components/layout/LayoutDefault/LayoutDefault';
import Login from '../components/pages/Login';
import Logout from '../components/pages/Logout';
import ErrorPage from '../components/pages/ErrorPage';
import Home from '../components/pages/Home/Home';
import Register from '../components/pages/Register';
import ProtectedRoute from './ProtectedRoute';
import TripPage from '../components/pages/Trip/TripPage';  
import RoutePage from '../components/pages/Route';
import LookupTicketPage from '../components/pages/Ticket/LookupTicketPage';
import BookingPage from '../components/pages/Booking/BookingPage';
import PaymentPage from '../components/pages/Payment/PaymentPage';
import BookingSuccess from '../components/pages/Booking/BookingSuccess';
import PaymentReturn from '../components/pages/Payment/PaymentReturn';

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
        element: <RoutePage />,
      },
      {
        path: 'trips',
        element: <TripPage />,
      },
      {
        path: 'bookings/:tripId',
        element: <BookingPage />,
      },
      {
        path: 'payments',
        element: <PaymentPage />,
      },
      {
        path: 'payment-return',
        element: <PaymentReturn />
      },
      {
        path: 'booking-success',
        element: <BookingSuccess />,
      },
      {
        path: 'lookup-ticket',
        element: <LookupTicketPage />,
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
