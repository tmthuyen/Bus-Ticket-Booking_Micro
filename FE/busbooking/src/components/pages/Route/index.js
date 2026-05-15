import { Container, Typography } from "@mui/material"
import RouteList from "./RouteList"
import { useNavigate } from "react-router-dom"

const RoutePage = () => {
  const navigate = useNavigate();

  const handleRouteClick = (route) => {
    // console.log('Selected route:', route, new Date().toISOString().split('T'));
    // Sau này có thể navigate tới /trips?origin=... ở đây luôn
    navigate(`/trips?origin=${route.origin_code}&destination=${route.destination_code}&from_date=${new Date().toISOString().split('T')[0]}`);
  }
  return (
    <>
      <Container maxWidth="lg" sx={{ mt: 2, mb: 2}}>
        <Typography variant="h5" component="h1" gutterBottom textAlign={'center'}> 
          Available Routes
        </Typography>
        <RouteList onRouteClick={handleRouteClick}/>
      </Container>
    </>
  )
}

export default RoutePage;