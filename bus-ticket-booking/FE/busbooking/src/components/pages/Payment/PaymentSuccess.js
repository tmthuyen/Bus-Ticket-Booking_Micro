import { Container, Typography } from "@mui/material";

const PaymentSuccess = () => {
  return (
    <>
      <Container maxWidth="lg" sx={{ mt: 1, mb: 4 }}>
        <Typography variant="h4" style={{ textAlign: 'center', marginBottom: '20px' }}>Payment Success Page</Typography>
      </Container>
    </>
  );
}
export default PaymentSuccess;