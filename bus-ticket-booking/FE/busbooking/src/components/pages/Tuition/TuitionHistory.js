import { Table, Typography, Tag } from 'antd';
import { formatCurrency } from '../../../utils/formatCurrencyUtil';
import { useEffect, useState } from 'react';
import { get } from '../../../utils/request';
import { formatVN } from '../../../utils/formatTime';
import { useOutletContext } from 'react-router-dom';
const { Text } = Typography;

// map màu theo status
const STATUS_MAP = {
    PENDING: { color: 'default', label: 'Đang chờ' },
    PAID: { color: 'success', label: 'Thành công' },
    OVERDUE: { color: 'error', label: 'Quá hạn' },
};

function TuitionHistory() {
    const { profile } = useOutletContext();
    const [tuitions, setTuitions] = useState([]);

    useEffect(() => {
        const fetchTuitionHistory = async () => {
            try {
                const rs = await get(
                    '/tuitions/student/' + profile.username + '/all'
                );

                console.log('Kết quả lấy lịch sử học phí:', rs);
                if (rs.data && Array.isArray(rs.data)) {
                    setTuitions(rs.data);
                } else {
                    setTuitions([]);
                }
            } catch (error) {
                console.error('Lỗi khi lấy lịch sử Tuition:', error);
                setTuitions([]);
            }
        };

        fetchTuitionHistory(); 
    }, [profile?.username]);

    const columns = [
        {
            title: 'Mã học phí',
            dataIndex: 'id',
            key: 'tuition_id',
            render: (id) => <Text code>{id}</Text>,
        },
        {
            title: 'Mã sinh viên',
            dataIndex: 'student_id',
            key: 'student_id',
        },
        {
            title: 'Họ tên',
            dataIndex: 'full_name',
            key: 'full_name',
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
            title: 'Đến hạn',
            dataIndex: 'due_at',
            key: 'due_at',
            render: (date) => formatVN(date),
        },
    ];

    return (
        <div style={{ padding: '10px', width: '100%', scrollbarWidth: 'thin' }}>
            <h2>Lịch sử học phí</h2>

            <div style={{ maxWidth: '95%', display:'flex', justifyContent: 'center', overflowX: 'auto' }}>
                <Table
                    rowKey="id"
                    columns={columns}
                    dataSource={tuitions}
                    pagination={{ pageSize: 5 }}
                    bordered
                    scroll={{ x: 1200 }} // hoặc 1000/1400 tuỳ tổng cột
                />
            </div>
        </div>
    );
}

export default TuitionHistory;
