import { Table, Typography, Tag } from 'antd';
import { formatCurrency } from '../../../utils/formatCurrencyUtil';
import { useEffect, useState } from 'react';
import { get } from '../../../utils/request';
import { formatVN } from '../../../utils/formatTime';
import { useOutletContext } from 'react-router-dom';
const { Text } = Typography;

const STATUS_MAP = {
  INTENDED: { color: 'default', label: 'Khởi tạo' },
  PROCESSING: { color: 'processing', label: 'Đang xử lý' },
  SUCCESS: { color: 'success', label: 'Thành công' },
  FAILED: { color: 'error', label: 'Thất bại' },
  EXPIRED: { color: 'warning', label: 'Hết hạn' },
};

function PaymentHistory() {
  const { profile } = useOutletContext(); // ❌ đừng gọi refreshProfile ở đây
  const [payments, setPayments] = useState([]);

  useEffect(() => {
    if (!profile?.username) return;

    const ac = new AbortController();
    (async () => {
      try {
        const rs = await get(`/payment/payments/user/${profile.username}`, { signal: ac.signal });
        if (rs?.status === 'ok' && Array.isArray(rs.data)) {
          setPayments(rs.data);
        } else {
          setPayments([]);
        }
      } catch (e) {
        if (e?.name !== 'AbortError') {
          console.error('Lỗi khi lấy lịch sử payment:', e);
          setPayments([]);
        }
      }
    })();

    return () => ac.abort();
  }, [profile?.username]); // ✅ chỉ chạy khi username đổi

  const columns = [
    { title: 'Mã giao dịch', dataIndex: 'payment_id', key: 'payment_id', render: (id) => <Text code>{id}</Text>, width: 150, ellipsis: true },
    { title: 'Mã sinh viên', dataIndex: 'student_id', key: 'student_id', width: 120, ellipsis: true },
    { title: 'Tên sinh viên', dataIndex: 'student_name', key: 'student_name', width: 120, ellipsis: true },
    { title: 'Kỳ học', dataIndex: 'term', key: 'term', width: 100, ellipsis: true },
    { title: 'Số tiền', dataIndex: 'amount', key: 'amount', align: 'right', render: (v) => formatCurrency(v), width: 140 },
    { title: 'Trạng thái', dataIndex: 'status', key: 'status', width: 130, render: (s) => <Tag color={(STATUS_MAP[s]||{}).color || 'default'}>{(STATUS_MAP[s]||{}).label || s}</Tag> },
    { title: 'Ngày tạo', dataIndex: 'created_at', key: 'created_at', render: formatVN, width: 180, ellipsis: true },
    { title: 'Ngày cập nhật', dataIndex: 'updated_at', key: 'updated_at', render: formatVN, width: 180, ellipsis: true },
  ];

  return (
    <div style={{ padding: 10, width: '100%', scrollbarWidth: 'thin' }}>
      <h2>Lịch sử thanh toán</h2>
      <div style={{ maxWidth: '95%', display: 'flex', justifyContent: 'center', overflowX: 'auto' }}>
        <Table
          rowKey="payment_id"        
          columns={columns}
          dataSource={payments}
          pagination={{ pageSize: 5 }}
          bordered
          tableLayout="fixed"
          scroll={{ x: 'max-content' }}
        />
      </div>
    </div>
  );
}

export default PaymentHistory;
