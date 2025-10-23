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
import { post } from '../../../utils/request';
import { useNavigate, useOutletContext } from 'react-router-dom';

const { Title } = Typography;

function FormPayment({ receiverData, onReset }) {
    const navigate = useNavigate();
    const { profile, refreshProfile } = useOutletContext();
    const [messageApi, contextHolder] = message.useMessage();
    const [loadingPayment, setLoadingPayment] = useState(false);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [paymentResult, setPaymentResult] = useState({});

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
        setSendingOtp(true);

        // Tạo intent thanh toán
        const paymentApiResult = await handlePaymentForStudent(
            profile,
            receiverData
        );
        if (!paymentApiResult || paymentApiResult.status !== 'ok') {
            messageApi.error(
                paymentApiResult?.message || 'Thanh toán thất bại!'
            );
            setSendingOtp(false);
            refreshProfile?.();
            return;
        } 
        setPaymentResult(paymentApiResult);
        try {
            const response = await fetch(
                `${API_DOMAIN}/notify/generateOTP/${profile.username}`,
                {
                    method: 'POST',
                    headers: {
                        Authorization: 'Bearer ' + accessToken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: profile.username,
                        email: profile.email,
                    }),
                }
            );
            const data = await response.json();
            
            if (response.ok) {
                messageApi.success(
                    data?.message ||
                        'OTP đã được gửi, vui lòng kiểm tra email/SMS'
                );
                setIsModalVisible(true);
                setOtp('');
                // set status
                // Thuyen doi API URL set status tuition
                // const resp = await fetch(`${API_DOMAIN}/tuitions/set_open_to_pending/${receiverData.student_id}`, {
                //     method: 'POST',
                //     headers: {
                //         Authorization: 'Bearer ' + accessToken,
                //         'Content-Type': 'application/json',
                //     },
                // });
                const resp = await fetch(`${API_DOMAIN}/tuitions/${receiverData.id}`, {
                    method: 'PUT',
                    headers: {
                        Authorization: 'Bearer ' + accessToken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ status: DEBT_STATUS.PENDING.value }),
                });

                if (!resp.ok) {
                    messageApi.error('Không thể cập nhật trạng thái học phí');
                }

            } else {
                messageApi.error(data?.message || 'Không thể gửi OTP');
            }
        } catch (error) {
            console.error(error);
            messageApi.error('Lỗi kết nối server');
        } finally {
            setSendingOtp(false);
            refreshProfile?.();
        }
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
            setLoadingPayment(false);
            return;
        }

        try {
            // console.log(receiverData);
            const res = await fetch(`${API_DOMAIN}/notify/verifyOTP`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: 'Bearer ' + accessToken,
                },
                body: JSON.stringify({
                    username: profile.username,
                    code: otp.trim(),
                    email: profile.email,
                }),
            });
            /// >= 400 lỗi

            const data = await res.json(); // <— dùng safeJson // de handle lỗi JSON

            // console.log(data);
            if (!res.ok) {
                // console.log(data);

                messageApi.error(data?.message || 'Xác thực OTP thất bại');
                return;
            }

            if (data.status !== 'ok') {
                // console.log(data);

                messageApi.error(
                    data?.message || 'Mã OTP không đúng hoặc đã hết hạn'
                );
                return;
            }

            
            // console.log(data);
            messageApi.success(data?.message || 'Xác thực OTP thành công!'); 

            // Tạo intent thanh toán
            const paymentApiResult = await handlePaymentForStudent(
                profile,
                receiverData
            );

            if (!paymentApiResult || paymentApiResult.status !== 'ok') {
                messageApi.error(
                    paymentApiResult?.message || 'Thanh toán thất bại!'
                );
                return;
            }

            // Xử lý thanh toán (nếu có id)
            const pid = paymentResult.data?.payment_id; 
            let redirect = '/payment-success';
            if (pid) {
                const processResult = await handleProcessPayment(pid);

                if(!processResult || processResult.status !== 'ok') {
                    messageApi.error(
                        processResult?.message || 'Xử lý thanh toán thất bại!'
                    );
                     
                }
                 
                redirect = processResult.redirect || '/payment-success';
                messageApi.success(
                    processResult?.message || 'Thanh toán thành công!'
                ); 
            } else{
                messageApi.error('Không tìm thấy thông tin thanh toán');
            }

            navigateToPaymentSuccess(redirect, pid);

            // Done
            setOtp('');
            setIsModalVisible(false);
            onReset?.();
        } catch (err) {
            console.error('Lỗi khi gọi API verify OTP:', err);
            messageApi.error('Lỗi khi gọi API verify OTP');
        } finally {
            setLoadingPayment(false); // <— luôn tắt
            refreshProfile?.();
        }
    };

    const handleCancel = () => {
        setIsModalVisible(false);
        setOtp('');
        // refreshProfile?.();
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

    const handleProcessPayment = async (payment_id) => {
        try {
            // Kiểm tra đúng đường dẫn backend, ví dụ: /payments/{id}/intent
            const rs = await post(
                `/payment/payments/${payment_id}/process`,
                null
            );
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

    const navigateToPaymentSuccess = (redirect, payment_id) => {
        // Sử dụng react-router-dom để chuyển hướng và truyền thông tin thanh toán
        navigate(`/payment-success/${payment_id}`);
    }

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
                            receiverData.status ===
                                DEBT_STATUS.OPEN.value && (
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
                                                receiverData.amount || receiverData.gate === "CLOSED" ||
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
                            receiverData.status === DEBT_STATUS.PENDING.value && (
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

export default FormPayment;
