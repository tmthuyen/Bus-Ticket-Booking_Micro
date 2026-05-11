const validateOtp = (otp='') => {
  if (!otp) {
      return {
        isValid: false,
        message: 'Mã OTP không được để trống.'
      }
    }

    if (otp.length !== 6) {
      
      return {
        isValid: false,
        message: 'Mã OTP phải gồm 6 chữ số.'
      }
    }

    if (!/^\d{6}$/.test(otp)) {
      return {
        isValid: false,
        message: 'Mã OTP chỉ được chứa chữ số.'
      }
    }

    return {
      isValid: true,
      message: ''
    }
}

export {
  validateOtp
}