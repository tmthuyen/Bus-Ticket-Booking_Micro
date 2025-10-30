import { useNavigate, useParams } from 'react-router-dom';
import {
    Result,
    Button,
    Card,
    Descriptions,
    Typography,
    Space,
    Tag,
    Spin,
    message,
} from 'antd';
import {
    CheckCircleTwoTone,
    HomeOutlined,
    ProfileOutlined,
} from '@ant-design/icons';
import { useEffect, useState } from 'react';
import { get } from '../../../utils/request';
import { formatVN } from '../../../utils/formatTime';

const { Text } = Typography;

const STATUS = {
    SUCCESS: { color: 'success', label: 'Thành công' },
    PROCESSING: { color: 'processing', label: 'Đang xử lý' },
    FAILED: { color: 'error', label: 'Thất bại' },
    INTENDED: { color: 'default', label: 'Khởi tạo' },
    EXPIRED: { color: 'warning', label: 'Hết hạn' },
};

function formatVND(v) {
    const n = Number(v ?? 0);
    try {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND',
        }).format(n);
    } catch {
        return `${n} VND`;
    }
}
// function formatVN(dt) {
//     if (!dt) return '—';
//     const d = new Date(dt);
//     return Number.isNaN(d.getTime())
//         ? dt
//         : d.toLocaleString('vi-VN', { hour12: false });
// }

export default function PaymentSuccess() {
    const { payment_id } = useParams(); // route: /payment-success/:payment_id
    const navigate = useNavigate();

    const [paymentInfo, setPaymentInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [notFound, setNotFound] = useState(false);

    useEffect(() => {
        let ignore = false;

        async function fetchPaymentInfo(id) {
            setLoading(true);
            setNotFound(false);
            try {
                const rs = await get(`/payment/payments/${id}/history`);
                // Tùy backend: nếu trả {status: 'ok', data: {...}}
                const ok = rs?.status === 'ok';
                const data = ok ? rs.data : rs;

                if (!ok) {
                    // Nếu 404 hoặc lỗi khác
                    if (rs?.status_code === 404 || rs?.detail === 'Not Found') {
                        if (!ignore) setNotFound(true);
                    } else {
                        message.error(
                            rs?.message || 'Không lấy được thông tin giao dịch'
                        );
                    }
                    if (!ignore) setPaymentInfo(null);
                    return;
                }

                if (!ignore) setPaymentInfo(data.payment_info);
            } catch (e) {
                console.error('fetchPaymentInfo error:', e);
                message.error('Lỗi kết nối máy chủ');
                if (!ignore) setPaymentInfo(null);
            } finally {
                if (!ignore) setLoading(false);
            }
        }

        if (payment_id) fetchPaymentInfo(payment_id);
        else {
            setLoading(false);
            setNotFound(true);
        }

        return () => {
            ignore = true;
        };
    }, [payment_id]);

    if (loading) {
        return (
            <div
                style={{
                    minHeight: '60vh',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Spin size="large" tip="Đang tải biên lai..." />
            </div>
        );
    }

    if (notFound || !paymentInfo) {
        return (
            <div
                style={{
                    minHeight: '75vh',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: 16,
                }}
            >
                <Result
                    status="404"
                    title="Không tìm thấy giao dịch"
                    subTitle="Vui lòng kiểm tra lại mã giao dịch hoặc quay về trang chủ."
                    extra={
                        <Button type="primary" onClick={() => navigate('/')}>
                            Về trang chủ
                        </Button>
                    }
                />
            </div>
        );
    }

    const st = STATUS[paymentInfo.status] || {
        color: 'default',
        label: paymentInfo.status || '—',
    };

    return (
        <div
            style={{
                minHeight: '75vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 16,
                background: 'linear-gradient(180deg,#f8fffb,#ffffff)',
            }}
        >
            <Card
                style={{
                    width: 'min(880px,94vw)',
                    borderRadius: 16,
                    boxShadow: '0 10px 30px rgba(0,0,0,.06)',
                }}
            >
                <Result
                    status="success"
                    icon={<CheckCircleTwoTone twoToneColor="#52c41a" />}
                    title="Thanh toán thành công!"
                    subTitle="Cảm ơn bạn đã sử dụng cổng thanh toán TDTU."
                    extra={
                        <Space wrap>
                            <Button
                                icon={<HomeOutlined />}
                                onClick={() => navigate('/')}
                            >
                                Về trang chủ
                            </Button>
                            {/* <Button
                                type="primary"
                                icon={<ProfileOutlined />}
                                onClick={() =>
                                    navigate("/", { state: { tabKey: "2" } })
                                }
                            >
                                Xem lịch sử thanh toán
                            </Button> */}
                        </Space>
                    }
                />

                <Card
                    size="small"
                    style={{ borderRadius: 12, overflow: 'hidden' }}
                >
                    <Descriptions
                        bordered
                        column={1}
                        size="middle" 
                    >
                        <Descriptions.Item label="Mã giao dịch">
                            <Space>
                                <Text code>
                                    {paymentInfo.payment_id || '—'}
                                </Text>
                                <Tag color={st.color}>{st.label}</Tag>
                            </Space>
                        </Descriptions.Item>
                        <Descriptions.Item label="Người thanh toán">
                            {paymentInfo.payer_name ||
                                paymentInfo.payer_id ||
                                '—'}
                        </Descriptions.Item>
                        <Descriptions.Item label="Sinh viên">
                            {paymentInfo.full_name
                                ? `${paymentInfo.full_name} (${paymentInfo.student_id})`
                                : paymentInfo.student_id || '—'}
                        </Descriptions.Item>
                        <Descriptions.Item label="Kỳ học">
                            {paymentInfo.term || '—'}
                        </Descriptions.Item>
                        <Descriptions.Item label="Số tiền">
                            <Text strong>{formatVND(paymentInfo.amount)}</Text>
                        </Descriptions.Item>
                        <Descriptions.Item label="Thời gian tạo">
                            {formatVN(paymentInfo.created_at)}
                        </Descriptions.Item>
                        <Descriptions.Item label="Cập nhật">
                            {formatVN(paymentInfo.updated_at)}
                        </Descriptions.Item>
                    </Descriptions>
                </Card>
            </Card>
        </div>
    );
}
