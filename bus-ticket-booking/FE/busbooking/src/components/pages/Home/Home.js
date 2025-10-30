import { Tabs } from 'antd';
import Payment from '../Payment/Payment';
import PaymentHistory from '../Payment/PaymentHistory';
import TuitionPaymentHistory from '../Payment/TuitionPaymentHistory';
import TuitionHistory from '../Tuition/TuitionHistory';
import { useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';

function Home() {
    const location = useLocation();
    const [activeKey, setActiveKey] = useState('1');

    useEffect(() => {

        const k = location.state?.tabKey;
        if (k) setActiveKey(k);
    }, [location.state]);

    const items = [
        {
            key: '1',
            label: 'Thanh toán học phí',
            children: <Payment />,
        },
        {
            key: '2',
            label: 'Lịch sử thanh toán',
            children: <PaymentHistory />,
        },
        {
            key: '3',
            label: 'Danh sách học phí đã thanh toán',
            children: <TuitionPaymentHistory />,
        },
        {
            key: '4',
            label: 'Lịch sử học phí',
            children: <TuitionHistory />,
        },
    ];

    const onChange = (key) => {
        setActiveKey(key);
    };

    return (
        <>
            <div
                style={{
                    width: '97%',
                    minHeight: '100vh',
                    display: 'flex',
                    justifyContent: 'center',
                }}
            >
                <Tabs
                    defaultActiveKey={activeKey || '1'}
                    items={items}
                    onChange={onChange}
                    style={{ width: '100%' }}
                />
            </div>
        </>
    );
}

export default Home;
