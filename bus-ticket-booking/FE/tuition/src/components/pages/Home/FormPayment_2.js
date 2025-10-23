import { useState } from 'react';
import {
    Input,
    Button,
    Typography,
    Row,
    Col,
    Card,
    Spin,
    Descriptions,
    Tag,
    Modal,
    message,
} from 'antd';
import { DEBT_STATUS } from '../../../constants/debtStatus';
import { formatCurrency } from '../../../utils/formatCurrencyUtil';
import { API_DOMAIN } from '../../../constants';
import { edit, get, post } from '../../../utils/request';
import { useNavigate, useOutletContext } from 'react-router-dom';
import { sleep } from '../../../utils/waitingResponse';

const { Title } = Typography;

function FormPayment2({ receiverData, onReset }) {
    const navigate = useNavigate();
    const { profile, refreshProfile } = useOutletContext();
    const [messageApi, contextHolder] = message.useMessage();
    const [loadingPayment, setLoadingPayment] = useState(false);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [paymentIntent, setPaymentIntent] = useState({});

    // Thêm state mới để theo dõi trạng thái gửi OTP
    const [sendingOtp, setSendingOtp] = useState(false);

    const [otp, setOtp] = useState('');

    const handlePayClick = async () => {
        if (profile.balance < receiverData.amount) {
            messageApi.error('Số dư không đủ để thực hiện giao dịch');
            return;
        }
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            messageApi.error('Bạn cần đăng nhập để thực hiện chức năng này');
            return;
        }

        // bật trạng thái gửi OTP va tao intent thanh toan
        setSendingOtp(true);

        // Tạo intent thanh toán
        const paymentIntentResult = await handlePaymentForStudent(
            profile,
            receiverData
        );
        if (!paymentIntentResult || paymentIntentResult.status !== 'ok') {
            messageApi.error(
                paymentIntentResult?.message ||
                    'Tạo ý định thanh toán thất bại!'
            );
            setSendingOtp(false);
            refreshProfile?.();
            return;
        }

        // tao intent thanh toan thanh cong, thi set pending tuition
        setPaymentIntent(paymentIntentResult);

        const bodyEditTuition = { status: DEBT_STATUS.PENDING.value };
        const rs = await edit(`/tuitions/${receiverData.id}`, bodyEditTuition);

        if (!rs || rs.status !== 'ok') {
            messageApi.error(
                rs.message || 'Không thể cập nhật trạng thái học phí'
            );

            setSendingOtp(false);
            refreshProfile?.();
            return;
        }

        await sleep(3000);
        setSendingOtp(false); // tắt trạng thái gửi OTP
        setIsModalVisible(true); // Hiển thị modal nhập OTP
        setOtp(''); // Reset ô nhập OTP
    };

    const handleVerifyOTP = async () => {
        if (!otp?.trim()) {
            messageApi.warning('Vui lòng nhập mã OTP');
            return;
        }

        setLoadingPayment(true);
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            messageApi.error('Bạn cần đăng nhập để thực hiện chức năng này');
            updateStatusTuition(receiverData.id, DEBT_STATUS.OPEN.value);
            navigate('/login');
            setLoadingPayment(false);
            return;
        }

        // Xử lý thanh toán với mã OTP
        let payment_id = paymentIntent.data?.payment_id;
        if (!payment_id) {
            messageApi.error('Không tìm thấy thông tin thanh toán');
            setLoadingPayment(false);
            return;
        }
        const paymentProcessResult = await handleProcessPayment(
            payment_id,
            profile.username,
            profile.email,
            otp.trim()
        );

        if (!paymentProcessResult || paymentProcessResult.status !== 'ok') {
            messageApi.error(
                paymentProcessResult?.message || 'Xử lý thanh toán thất bại!'
            );
            setLoadingPayment(false);
            // updateStatusTuition(receiverData.id, DEBT_STATUS.OPEN.value);
            const rsUpdateTuition = await updateStatusTuitionByStudentAndTerm(
                receiverData.student_id,
                receiverData.term
            );
            console.log('rsUpdateTuition', rsUpdateTuition);
            return;
        }

        const redirect = paymentProcessResult.redirect || '/payment-success';
        messageApi.success(
            paymentProcessResult?.message || 'Thanh toán thành công!'
        );

        navigateToPaymentSuccess(redirect, payment_id);

        // Done
        setOtp('');
        setIsModalVisible(false);
        onReset?.();
        setLoadingPayment(false); // <— luôn tắt
        refreshProfile?.();
    };

    const handleCancel = async () => {
        // updateStatusTuition(receiverData.id, DEBT_STATUS.OPEN.value);
        await updateStatusTuitionByStudentAndTerm(
                receiverData.student_id,
                receiverData.term
            );
        setIsModalVisible(false);
        setOtp('');
        // refreshProfile?.();
    };

    const updateStatusTuition = async (tuitionId, status) => {
        const bodyEditTuition = { status: status };
        const rs = await edit(`/tuitions/${tuitionId}`, bodyEditTuition);
        return rs;
    };

    const handlePaymentForStudent = async (profile, receiverData) => {
        try {
            const body = {
                student_id: receiverData.student_id,
                payer_id: profile.username,
                term: receiverData.term,
                amount: receiverData.amount,
                description: `${profile.full_name} thanh toán cho ${receiverData.full_name} - Học kỳ ${receiverData.term}`,
            };
            // Đảm bảo base URL/post() đúng domain: /payments/intent (không thừa /payment)
            const rs = await post('/payment/payments/intent', body);
            return rs; // expected: { status: 'ok' | 'failed', message, data }
        } catch (error) {
            console.error('Lỗi khi gọi API thanh toán:', error);
            // messageApi.error('Lỗi khi gọi API thanh toán');
            return {
                status: 'failed',
                message: 'Lỗi khi gọi API thanh toán',
                error,
            };
        }
    };

    const handleProcessPayment = async (
        payment_id,
        payer_id,
        payer_email,
        otp_code
    ) => {
        try {
            // Kiểm tra đúng đường dẫn backend, ví dụ: /payments/{id}/intent
            const rs = await post(`/payment/payments/${payment_id}/process`, {
                payer_id,
                payer_email,
                otp_code,
            });
            return rs;
        } catch (error) {
            console.error('Lỗi khi xử lý thanh toán:', error);
            // messageApi.error('Lỗi khi xử lý thanh toán');
            return {
                status: 'failed',
                message: 'Lỗi khi gọi API xử lý thanh toán',
                error,
            };
        }
    };

    const updateStatusTuitionByStudentAndTerm = async (student_id, term) => {
        // neu dang Processing thi return Processing

        // neu SUCCESS thi return SUCCESS
        try {
            // Kiểm tra đúng đường dẫn backend, ví dụ: /payments/{id}/intent
            const rs = await get(`/payment/payments/student/${student_id}`);
            console.log('rs payments', rs);
            let isUpdateTuitionStatus = false;
            if (rs.status === 'ok') {
                const payments = rs.data;
                for (let payment of payments) {
                    if (payment.term === term) {
                        // if (payment.status === 'PROCESSING') {
                        //     updateStatusTuition(
                        //         receiverData.id,
                        //         DEBT_STATUS.PENDING.value
                        //     );

                        // } 
                        if (payment.status === 'SUCCESS') {
                            updateStatusTuition(
                                receiverData.id,
                                DEBT_STATUS.PAID.value
                            );
                            isUpdateTuitionStatus = true;
                        }
                    }
                }
            }
            if (!isUpdateTuitionStatus){
                updateStatusTuition(
                    receiverData.id,
                    DEBT_STATUS.OPEN.value
                );
            }

            return rs;
        } catch (error) {
            console.error('Lỗi khi xử lý thanh toán:', error);
            // messageApi.error('Lỗi khi xử lý thanh toán');
            return {
                status: 'failed',
                message: 'Lỗi khi gọi API lấy dữ liệu thanh toán',
                error,
            };
        }
    };

    const navigateToPaymentSuccess = (redirect, payment_id) => {
        // Sử dụng react-router-dom để chuyển hướng và truyền thông tin thanh toán
        navigate(`/payment-success/${payment_id}`);
    };

    return (
        <>
            {contextHolder}
            <Spin
                size="large"
                spinning={loadingPayment}
                delay={200}
                tip={
                    <span
                        style={{
                            fontSize: '16px',
                            marginTop: '15px',
                        }}
                    >
                        Đang xử lý thanh toán...
                    </span>
                }
                style={{
                    display: loadingPayment ? 'flex' : 'none',
                    userSelect: 'none',
                    width: '100%',
                    height: '100%',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    zIndex: 9999,
                    backgroundColor: 'rgba(255,255,255,0.6)', // overlay mờ nền
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            />
            <Row gutter={16} justify={'center'}>
                <Col xs={20} md={12}>
                    <Card
                        title={<Title level={4}>Thông tin thanh toán</Title>}
                        variant="borderless"
                    >
                        {/* Hiển thị thông tin thanh toan */}
                        {receiverData &&
                            receiverData.status === DEBT_STATUS.OPEN.value && (
                                <>
                                    <Descriptions
                                        bordered
                                        column={1}
                                        size="middle"
                                        style={{ marginTop: '20px' }}
                                    >
                                        <Descriptions.Item label="Nguời nộp">
                                            {profile.full_name}
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Số dư">
                                            {formatCurrency(profile.balance)}
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Nộp cho">
                                            {receiverData.full_name}
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Số tiền thanh toán">
                                            {receiverData &&
                                                receiverData.amount &&
                                                formatCurrency(
                                                    receiverData.amount
                                                )}
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Hướng dẫn">
                                            {
                                                <Tag
                                                    color={
                                                        profile.balance >=
                                                        receiverData.amount
                                                            ? 'blue'
                                                            : 'orange'
                                                    }
                                                >
                                                    {profile.balance >=
                                                    receiverData.amount
                                                        ? 'Nhấn nút để thanh toán'
                                                        : 'Số dư không đủ để thanh toán'}
                                                </Tag>
                                            }
                                        </Descriptions.Item>
                                    </Descriptions>

                                    <Button
                                        type="primary"
                                        disabled={
                                            profile.balance <
                                                receiverData.amount ||
                                            receiverData.gate === 'CLOSED' ||
                                            sendingOtp
                                        }
                                        onClick={handlePayClick}
                                        loading={sendingOtp} // Thêm hiệu ứng loading khi đang gửi OTP
                                    >
                                        {sendingOtp
                                            ? 'Đang gửi OTP...'
                                            : 'Thanh toán'}
                                    </Button>
                                    <Modal
                                        title="Xác thực OTP"
                                        open={isModalVisible}
                                        onOk={handleVerifyOTP}
                                        onCancel={handleCancel}
                                        okText="Xác nhận"
                                        cancelText="Hủy"
                                    >
                                        <p>
                                            Vui lòng nhập mã OTP để hoàn tất
                                            thanh toán:
                                        </p>
                                        <Input
                                            placeholder="Nhập OTP"
                                            value={otp}
                                            onChange={(e) =>
                                                setOtp(e.target.value)
                                            }
                                            maxLength={6}
                                        />
                                    </Modal>
                                </>
                            )}

                        {receiverData &&
                            receiverData.status === DEBT_STATUS.PAID.value && (
                                <Descriptions
                                    bordered
                                    column={1}
                                    size="middle"
                                    style={{ marginTop: '10px' }}
                                >
                                    <Descriptions.Item label="Chú thích">
                                        {
                                            <Tag color="success">
                                                Sinh viên đã hoàn thành học phí
                                            </Tag>
                                        }
                                    </Descriptions.Item>
                                </Descriptions>
                            )}

                        {receiverData &&
                            receiverData.status ===
                                DEBT_STATUS.OVERDUE.value && (
                                <Descriptions
                                    bordered
                                    column={1}
                                    size="middle"
                                    style={{ marginTop: '10px' }}
                                >
                                    <Descriptions.Item label="Chú thích">
                                        {
                                            <Tag color="warning">
                                                Học phí sinh viên đang quá hạn
                                                thanh toán{' '}
                                            </Tag>
                                        }
                                    </Descriptions.Item>
                                </Descriptions>
                            )}

                        {receiverData &&
                            receiverData.status ===
                                DEBT_STATUS.PENDING.value && (
                                <Descriptions
                                    bordered
                                    column={1}
                                    size="middle"
                                    style={{ marginTop: '10px' }}
                                >
                                    <Descriptions.Item label="Chú thích">
                                        {
                                            <Tag color="default">
                                                Học phí đang được xử lý
                                            </Tag>
                                        }
                                    </Descriptions.Item>
                                </Descriptions>
                            )}
                    </Card>
                </Col>
            </Row>
        </>
    );
}

export default FormPayment2;
