import { Outlet, useNavigate } from 'react-router-dom';
import './LayoutDefault.css'; 
import CustomerHeader from '../../partials/CustomerHeader';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';
import { fetchRoutes } from '../../../store/actions/tripsAction';
 
function LayoutDefault() { 
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { error } = useSelector((state) => state.trips);
  useEffect(() => {
    dispatch(fetchRoutes());
  }, [dispatch]);

  if (error) {
    navigate('/error?status=500&message=' + error);
  }


  return (
    <div className="layout-default">
      <header className="layout-default__header">
        <CustomerHeader />
      </header>

      <main className="layout-default__main">
        <Outlet />
      </main>

      <footer className="layout-default__footer">Tran Minh Thuyen</footer>
    </div>
  );
}

export default LayoutDefault;
