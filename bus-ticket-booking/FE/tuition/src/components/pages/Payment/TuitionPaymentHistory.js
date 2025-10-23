import { Table, Typography, Tag } from 'antd';
import { formatCurrency } from '../../../utils/formatCurrencyUtil';
import { useEffect, useState } from 'react';
import { get } from '../../../utils/request';
import { formatVN } from '../../../utils/formatTime';
import { useOutletContext } from 'react-router-dom';
const { Text } = Typography;

// map màu theo status
const STATUS_MAP = {
    INTENDED: { color: 'default', label: 'Khởi tạo' },
    PROCESSING: { color: 'processing', label: 'Đang xử lý' },
    SUCCESS: { color: 'success', label: 'Thành công' },
    FAILED: { color: 'error', label: 'Thất bại' },
    EXPIRED: { color: 'warning', label: 'Hết hạn' },
};

function TuitionPaymentHistory() {
    const { profile } = useOutletContext();
    const [payments, setPayments] = useState([]);
 
    useEffect(() => {
        const fetchTuitionPaymentHistory = async () => {
            try {
                const rs = await get(
                    '/payment/payments/student/' + profile.username
                );

                console.log('Kết quả lấy lịch sử payment:', rs);
                if (rs.status === 'ok' && rs.data && Array.isArray(rs.data)) {
                    setPayments(rs.data);
                } else {
                    setPayments([]);
                }
            } catch (error) {
                console.error('Lỗi khi lấy lịch sử payment:', error);
                setPayments([]);
            }
        };

        fetchTuitionPaymentHistory(); 
    }, [profile]);

    const columns = [
        {
            title: 'Mã giao dịch',
            dataIndex: 'payment_id',
            key: 'payment_id',
            render: (id) => <Text code>{id}</Text>,
        },
        {
            title: 'Mã người nộp',
            dataIndex: 'payer_id',
            key: 'payer_id',
        },
        {
            title: 'Kỳ học',
            dataIndex: 'term',
            key: 'term',
        },
        {
            title: 'Số tiền',
            dataIndex: 'amount',
            key: 'amount',
            align: 'right',
            render: (amount) => formatCurrency(amount),
        },
        {
            title: 'Trạng thái',
            dataIndex: 'status',
            key: 'status',
            render: (status) => {
                const info = STATUS_MAP[status] || {
                    color: 'default',
                    label: status,
                };
                return <Tag color={info.color}>{info.label}</Tag>;
            },
        },
        {
            title: 'Ngày tạo',
            dataIndex: 'created_at',
            key: 'created_at',
            render: (date) => formatVN(date),
        },
        {
            title: 'Ngày cập nhật',
            dataIndex: 'updated_at',
            key: 'updated_at',
            render: (date) => formatVN(date),
        },
    ];

    return (
        <div style={{ padding: '10px', width: '100%', scrollbarWidth: 'thin' }}>
            <h2>Danh sách học phí đã thanh toán</h2>

            <div
                style={{
                    maxWidth: '95%',
                    display: 'flex',
                    justifyContent: 'center',
                    overflowX: 'auto',
                }}
            >
                <Table
                    rowKey="id"
                    columns={columns}
                    dataSource={payments}
                    pagination={{ pageSize: 5 }}
                    bordered
                    scroll={{ x: 1200 }} // hoặc 1000/1400 tuỳ tổng cột
                />
            </div>
        </div>
    );
}

export default TuitionPaymentHistory;
