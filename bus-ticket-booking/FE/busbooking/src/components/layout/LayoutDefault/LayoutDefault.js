import { Outlet, useNavigate } from 'react-router-dom';
import './LayoutDefault.css'; 
import CustomerHeader from '../../partials/CustomerHeader';
import { useDispatch } from 'react-redux';
import { useEffect } from 'react';
import { fetchRoutes } from '../../../store/actions/tripsAction';
 
function LayoutDefault() { 
  const dispatch = useDispatch(); 

  useEffect(() => {
    dispatch(fetchRoutes());
  }, [dispatch]);
 

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
