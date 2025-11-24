import { Box, Grid } from '@mui/material';
import { Button, Input, Modal } from 'antd';
// import { useState } from 'react';

const ModalConfirm = ({
  errorMessage = null,
  isModalOpen,
  setIsModalOpen,
  onSubmit,
  otp,
  setOtp,
  onResend,
  resendLoading,
}) => {
  const handleCancel = () => {
    // setIsModalOpen(false);
    // onCancel
  };

  const handleInput = (value) => {
    // value là string, VD: "1a3" → lọc chỉ giữ số
    if (value.length > 6) {
      setOtp(value.slice(0, 6));
      return; // giới hạn độ dài tối đa 6
    }
    if (!value) {
      setOtp('');
      return;
    }
    console.log('Raw input:', value);
    setOtp(value?.join(''));
  };

  const handleChange = (text) => {
    // text là string, khi điền đủ length (6) sẽ gọi
    console.log('OTP complete:', text);
    // có thể setOtp(text); nhưng ở đây mình đã set trong onInput rồi
  };

  return (
    <Modal
      title="Xác nhận OTP với thông tin đặt vé"
      open={isModalOpen}
      closable={false} // ẩn nút X góc trên
      footer={[
        <Button key="resend" onClick={onResend} loading={resendLoading}>
          Gửi lại mã
        </Button>,
        <Button
          key="submit"
          type="primary"
          onClick={onSubmit}
          // loading={loading}
        >
          Xác nhận
        </Button>,
      ]}
    >
      <Grid container justify="center" align="middle">
        <Grid size={12} sx={{ width: '100%' }}>
          <Input.OTP
            length={6} // 6 số OTP
            value={otp} // controlled string
            formatter={(str) => str.replace(/\D/g, '')}
            onInput={handleInput} // lọc chỉ số
            onChange={handleChange}
            inputMode="numeric" // gợi ý bàn phím số trên mobile
            pattern="[0-9]*" // hint form
            // separator nếu thích thêm dấu gạch giữa các ô:
            separator={<span style={{ margin: '0 4px' }}>-</span>}
            className="otp-input-custom"
          />
        </Grid>
        <Grid
          size={12}
          sx={{ marginTop: '10px', fontSize: '14px', color: '#555' }}
        >
          Vui lòng nhập mã OTP đã được gửi đến email của bạn để xác nhận đặt vé.
        </Grid>
        <Box sx={{ fontSize: '12px', color: '#888', marginTop: '8px' }}>
          (Nếu không nhận được email, vui lòng kiểm tra trong mục Spam hoặc
          Quảng cáo)
        </Box>
        {/* err msg */}
        {errorMessage && (
          <Box sx={{ color: 'red', marginTop: '10px', fontSize: '14px' }}>
            {errorMessage}
          </Box>
        )}
      </Grid>
    </Modal>
  );
};

export default ModalConfirm;
