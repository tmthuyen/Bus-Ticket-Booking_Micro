import { SearchOutlined } from '@ant-design/icons';
import {
    Form,
    Input,
    Typography,
    Row,
    Col,
    Card,
    Spin,
    Descriptions,
    message,
} from 'antd';
import { DEBT_STATUS } from '../../../constants/debtStatus';
import { formatCurrency } from '../../../utils/formatCurrencyUtil';
import { useEffect, useState } from 'react';
import { API_DOMAIN } from '../../../constants';
import { useNavigate } from 'react-router-dom';
const { Text, Title } = Typography;

function FormInfo({ receiverData, setReceiverData }) {
    const navigate = useNavigate();
    const [formReceiver] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [errMsg, setErrMsg] = useState('');
    const [oldVal, setOldVal] = useState('');

    useEffect(() => {
        if (receiverData) {
            formReceiver.setFieldsValue({
                receiver_name: receiverData.full_name || '', // Tên người nộp
                receiver_tuition: receiverData.amount || '', // Số tiền học phí
                receiver_term: receiverData.term || '', // Học kỳ
                receiver_status: receiverData.status ? (
                    <Text
                        style={{
                            color: DEBT_STATUS[receiverData.status].color,
                        }}
                    >
                        DEBT_STATUS[receiverData.status].label
                    </Text>
                ) : (
                    ''
                ),
            });
        } else {
            formReceiver.resetFields();
        }
    }, [receiverData, formReceiver]);

    const handleSearchTuitionSt = async () => {
        const receiverId = formReceiver.getFieldValue('receiver_id');
        if (!receiverId) {
            message.warning('Nhập id sinh viên nộp học phí');
            return;
        }
        setLoading(true);
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            setErrMsg('Bạn cần đăng nhập để thực hiện chức năng này');

            setTimeout(() => {
                navigate('/logout');
            }, 1000);
            setLoading(false);
            return;
        }
        try {
            const res = await fetch(
                API_DOMAIN + '/tuitions/student/' + receiverId,
                {
                    headers: {
                        Authorization: 'Bearer ' + accessToken,
                    },
                }
            );
            const data = await res.json();
            // if (res.ok) {
            //   if (data.status === "failed") {
            //     message.error("Không tìm thấy sinh viên với id đã nhập");
            //     setReceiverData(null);
            //   }else{
            //     console.log("DATA TUITION API:", data);
            //     setReceiverData(data);
            //   }
            // }
            if (res.status === 401) {
                setErrMsg('Bạn cần đăng nhập để thực hiện chức năng này');

                setTimeout(() => {
                    navigate('/logout');
                }, 1000);
            }
            if (!res.ok) {
                // message.error("Không tìm thấy sinh viên với id đã nhập");
                setErrMsg('Không tìm thấy sinh viên với id đã nhập');
                setReceiverData(null);
            } else {
                console.log('DATA TUITION API:', data);
                setErrMsg('');
                setReceiverData(data);
            }
        } catch (error) {
            // message.error("Đã xảy ra lỗi khi tìm kiếm thông tin sinh viên");
            setErrMsg('Đã xảy ra lỗi khi tìm kiếm thông tin sinh viên');
            setReceiverData(null);
        } finally {
            setLoading(false);
        }
    };

    const handleInputReceiverChange = (values) => {
        setErrMsg('');
        setOldVal(values);
        setReceiverData(null);
    };

    return (
        <>
            <Row gutter={16} justify={'center'}>
                <Col xs={20} md={12}>
                    <Card
                        title={<Title level={4}>Thông tin nộp học phí</Title>}
                        variant="borderless"
                    >
                        <Form
                            layout={'vertical'}
                            form={formReceiver}
                            onValuesChange={handleInputReceiverChange}
                            initialValues={{ layout: 'vertical' }}
                            // style={{ maxWidth: "1000px", minWidth: "700px" }}
                        >
                            <Form.Item
                                rules={[
                                    {
                                        required: true,
                                        message:
                                            'Hãy nhập mã sinh viên đóng học phí!',
                                    },
                                ]}
                                name="receiver_id"
                                label="Mã sinh viên"
                            >
                                <Input
                                    placeholder="Hãy nhập mã sinh viên đóng học phí"
                                    suffix={
                                        <SearchOutlined
                                            onClick={handleSearchTuitionSt}
                                            style={{
                                                cursor: 'pointer',
                                                color: '#1677ff',
                                            }}
                                        />
                                    }
                                    value={oldVal}
                                />
                            </Form.Item>
                        </Form>

                        {/* Hiển thị thông tin học phí */}
                        {receiverData ? (
                            <Descriptions
                                bordered
                                column={1}
                                size="middle"
                                style={{ marginTop: '20px' }}
                            >
                                <Descriptions.Item label="Tên sinh viên">
                                    {receiverData.full_name}
                                </Descriptions.Item>
                                <Descriptions.Item label="Học kỳ">
                                    {receiverData.term}
                                </Descriptions.Item>
                                <Descriptions.Item label="Số tiền học phí">
                                    {receiverData.amount &&
                                        formatCurrency(receiverData.amount)}
                                </Descriptions.Item>
                                <Descriptions.Item label="Trạng thái">
                                    <Text
                                        style={{
                                            color: DEBT_STATUS[
                                                receiverData.status
                                            ].color,
                                        }}
                                    >
                                        {DEBT_STATUS[receiverData.status].label}
                                    </Text>
                                </Descriptions.Item>
                            </Descriptions>
                        ) : (
                            <Text type="danger" style={{ marginTop: '20px' }}>
                                {errMsg}
                            </Text>
                        )}
                    </Card>

                    <Spin
                        size="large"
                        fullscreen
                        delay={100}
                        spinning={loading}
                        tip={'Đang tìm kiếm'}
                    />
                </Col>
            </Row>
        </>
    );
}

export default FormInfo;
