import { Button, Descriptions, Drawer, Spin } from 'antd';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { formatCurrency } from '../../../utils/formatCurrencyUtil';
import { get } from '../../../utils/request';

const Profile = ({ open, onClose, profile }) => {
    // console.log(profile);
    const username = profile?.username;
    const navigate = useNavigate();
    const [payer, setPayer] = useState(profile);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setTimeout(() => {
            setLoading(false);
        }, 1000);
    }, []);

    const showLoading = () => {
        setLoading(true);
        // Simple loading mock. You should add cleanup logic in real world.
        setTimeout(async() => {
            const user = await get(`/auth/users/${username}/`);
            if (user) {
                // profile = user;
                setPayer(user);
            } else{
                navigate('/login');
            }
            setLoading(false);
        }, 1000);
    };
    return (
        <>
            <Drawer
                closable
                title={<p>Thông tin hồ sơ</p>}
                placement="right"
                open={open}
                onClose={onClose}
                extra={
                    <Button onClick={showLoading} type="primary">
                        Tải lại
                    </Button>
                }
            >
                <Spin spinning={loading} tip="Đang tải...">
                    <Descriptions
                        bordered
                        column={1}
                        size="middle"
                        style={{ marginTop: 20 }}
                    >
                        <Descriptions.Item label="Họ tên">
                            {payer?.full_name}
                        </Descriptions.Item>
                        <Descriptions.Item label="Email">
                            {payer?.email}
                        </Descriptions.Item>
                        <Descriptions.Item label="Số điện thoại">
                            {payer?.phone}
                        </Descriptions.Item>
                        <Descriptions.Item label="Số dư">
                            {payer &&
                                payer.balance &&
                                formatCurrency(payer.balance)}
                        </Descriptions.Item>
                        <Descriptions.Item label="Mã sinh viên">
                            {payer?.username}
                        </Descriptions.Item>
                    </Descriptions>
                </Spin>
            </Drawer>
        </>
    );
};
export default Profile;
