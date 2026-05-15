import { useMemo, useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
  Autocomplete,
  Button,
  Container,
  Grid,
  Skeleton,
  TextField,
  Box,
  Typography,
  IconButton,
} from '@mui/material';
import { LocationOn, Search, ArrowBackIosNew, ArrowForwardIos } from '@mui/icons-material';
import useMessage from 'antd/es/message/useMessage';
import RouteList from '../Route/RouteList';

const todayVN = () => {
  const today = new Date();
  const day = String(today.getDate()).padStart(2, '0');
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const year = today.getFullYear();
  return `${year}-${month}-${day}`;
};

const today = todayVN();

// slide demo – bạn có thể đổi link ảnh sau
const HERO_SLIDES = [
  {
    title: 'Đặt vé xe khách dễ dàng',
    subtitle: 'So sánh tuyến, chọn ghế, thanh toán chỉ trong vài bước.',
    image:
      'https://images.pexels.com/photos/460672/pexels-photo-460672.jpeg?auto=compress&cs=tinysrgb&w=1200',
  },
  {
    title: 'Khám phá mọi miền đất nước',
    subtitle: 'Từ Sài Gòn đến Hà Nội, đi đâu cũng có vé trên hệ thống của bạn.',
    image:
      'https://images.pexels.com/photos/210182/pexels-photo-210182.jpeg?auto=compress&cs=tinysrgb&w=1200',
  },
  {
    title: 'An tâm trên mọi hành trình',
    subtitle: 'Thông tin minh bạch, hỗ trợ khách hàng 24/7 (tùy bạn ghi 😄).',
    image:
      'https://images.pexels.com/photos/1287460/pexels-photo-1287460.jpeg?auto=compress&cs=tinysrgb&w=1200',
  },
];

const Home = () => {
  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);
  const [fromDate, setFromDate] = useState(today);
  const [errors, setErrors] = useState({
    origin: false,
    destination: false,
    fromDate: false,
  });

  const [currentSlide, setCurrentSlide] = useState(0);

  const navigate = useNavigate();
  const [messageApi, contextHolder] = useMessage();

  const { routes, loading } = useSelector((state) => state.trips);

  // build danh sách bến/tỉnh từ routes
  const places = useMemo(() => {
    const map = new Map();
    if (routes && routes.length > 0) {
      routes.forEach((route) => {
        if (route.origin && route.origin_code && !map.has(route.origin_code)) {
          map.set(route.origin_code, {
            label: route.origin,
            code: route.origin_code,
          });
        }
        if (
          route.destination &&
          route.destination_code &&
          !map.has(route.destination_code)
        ) {
          map.set(route.destination_code, {
            label: route.destination,
            code: route.destination_code,
          });
        }
      });
    }
    return Array.from(map.values());
  }, [routes]);

  const handleSearchRoute = () => {
    const newErrors = {
      origin: !origin,
      destination: !destination,
      fromDate: !fromDate,
    };
    setErrors(newErrors);
    if (newErrors.origin || newErrors.destination || newErrors.fromDate) return;

    if (origin.code === destination.code) {
      messageApi.error('Điểm đi và điểm đến không được trùng nhau!');
      setDestination(null);
      return;
    }

    const payload = {
      origin_code: origin.code,
      destination_code: destination.code,
      from_date: fromDate,
    };

    console.log('Search payload: ', payload);

    navigate(
      `/trips?origin=${payload.origin_code}&destination=${payload.destination_code}&from_date=${payload.from_date}`
    );
  };

  // auto slide hero
  useEffect(() => {
    const id = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % HERO_SLIDES.length);
    }, 5000);
    return () => clearInterval(id);
  }, []);

  const goPrev = () => {
    setCurrentSlide((prev) =>
      prev === 0 ? HERO_SLIDES.length - 1 : prev - 1
    );
  };

  const goNext = () => {
    setCurrentSlide((prev) => (prev + 1) % HERO_SLIDES.length);
  };

  const slide = HERO_SLIDES[currentSlide];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #e6fbff 0%, #ffffff 60%, #f0ffff 100%)',
        py: 4,
      }}
    >
      <Container maxWidth="lg">
        {contextHolder}

        {/* Hero + Search */}
        {loading ? (
          <Box
            sx={{
              height: '60vh',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-around',
            }}
          >
            <Skeleton variant="rounded" width={'100%'} height={160} />
            <Skeleton variant="rounded" width={'100%'} height={320} />
          </Box>
        ) : (
          <>
            <Grid container spacing={3} alignItems="stretch">
              {/* Hero Carousel */}
              <Grid size={{ xs: 12, md: 7 }}>
                <Box
                  sx={{
                    position: 'relative',
                    height: { xs: 260, md: 340 },
                    borderRadius: 4,
                    overflow: 'hidden',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.18)',
                    backgroundColor: '#000',
                  }}
                >
                  <Box
                    sx={{
                      position: 'absolute',
                      inset: 0,
                      backgroundImage: `url(${slide.image})`,
                      backgroundSize: 'cover',
                      backgroundPosition: 'center',
                      filter: 'brightness(0.65)',
                      transition: 'background-image 0.6s ease-in-out',
                    }}
                  />
                  <Box
                    sx={{
                      position: 'absolute',
                      inset: 0,
                      p: { xs: 3, md: 4 },
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      color: 'white',
                    }}
                  >
                    <Box>
                      <Typography variant="h4" fontWeight={700} gutterBottom>
                        {slide.title}
                      </Typography>
                      <Typography variant="body1" sx={{ maxWidth: 420 }}>
                        {slide.subtitle}
                      </Typography>
                    </Box>

                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                      }}
                    >
                      <Box>
                        <Typography variant="caption" sx={{ opacity: 0.85 }}>
                          An tâm với hệ thống đặt vé trực tuyến
                        </Typography>
                      </Box>
                      <Box>
                        <IconButton
                          size="small"
                          onClick={goPrev}
                          sx={{ color: 'white', mr: 1 }}
                        >
                          <ArrowBackIosNew fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={goNext}
                          sx={{ color: 'white' }}
                        >
                          <ArrowForwardIos fontSize="small" />
                        </IconButton>
                      </Box>
                    </Box>

                    <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                      {HERO_SLIDES.map((_, idx) => (
                        <Box
                          key={idx}
                          sx={{
                            width: idx === currentSlide ? 18 : 8,
                            height: 8,
                            borderRadius: 999,
                            bgcolor:
                              idx === currentSlide
                                ? 'var(--color-primary, #2bddf4)'
                                : 'rgba(255,255,255,0.5)',
                            transition: 'all 0.3s',
                            cursor: 'pointer',
                          }}
                          onClick={() => setCurrentSlide(idx)}
                        />
                      ))}
                    </Box>
                  </Box>
                </Box>
              </Grid>

              {/* Search Card */}
              <Grid size={{ xs: 12, md: 5 }}>
                <Box
                  sx={{
                    backgroundColor: 'var(--color-white, #ffffff)',
                    borderRadius: 4,
                    p: 3,
                    boxShadow: '0 6px 20px rgba(0,0,0,0.12)',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                  }}
                >
                  <Box sx={{ mb: 2 }}>
                    <Typography
                      variant="h6"
                      fontWeight={700}
                      sx={{ color: 'var(--color-text, #023039)' }}
                    >
                      Tìm chuyến xe
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#555', mt: 0.5 }}>
                      Chọn điểm đi, điểm đến và ngày khởi hành
                    </Typography>
                  </Box>

                  <Grid container spacing={2}>
                    <Grid size={{ xs: 12 }}>
                      <Autocomplete
                        disablePortal
                        options={places}
                        getOptionLabel={(option) => option.label}
                        sx={{ width: '100%' }}
                        value={origin}
                        onChange={(e, newValue) => setOrigin(newValue)}
                        renderInput={(params) => (
                          <TextField
                            {...params}
                            label="Điểm đi"
                            error={errors.origin}
                            helperText={
                              errors.origin ? 'Vui lòng chọn điểm đi' : ''
                            }
                            InputProps={{
                              ...params.InputProps,
                              startAdornment: (
                                <>
                                  <LocationOn
                                    sx={{ mr: 1, color: 'primary.main' }}
                                  />
                                  {params.InputProps.startAdornment}
                                </>
                              ),
                            }}
                          />
                        )}
                      />
                    </Grid>

                    <Grid size={{ xs: 12 }}>
                      <Autocomplete
                        disablePortal
                        options={places}
                        getOptionLabel={(option) => option.label}
                        sx={{ width: '100%' }}
                        value={destination}
                        onChange={(e, newValue) => setDestination(newValue)}
                        renderInput={(params) => (
                          <TextField
                            {...params}
                            label="Điểm đến"
                            error={errors.destination}
                            helperText={
                              errors.destination
                                ? 'Vui lòng chọn điểm đến'
                                : ''
                            }
                            InputProps={{
                              ...params.InputProps,
                              startAdornment: (
                                <>
                                  <LocationOn
                                    sx={{ mr: 1, color: 'primary.main' }}
                                  />
                                  {params.InputProps.startAdornment}
                                </>
                              ),
                            }}
                          />
                        )}
                      />
                    </Grid>

                    <Grid size={{ xs: 12 }}>
                      <TextField
                        fullWidth
                        label="Ngày khởi hành"
                        type="date"
                        value={fromDate}
                        onChange={(e) => setFromDate(e.target.value)}
                        error={errors.fromDate}
                        helperText={
                          errors.fromDate ? 'Vui lòng chọn ngày' : ''
                        }
                        InputLabelProps={{ shrink: true }}
                        inputProps={{
                          min: today, // chỉ cho chọn từ hôm nay trở đi
                        }}
                      />
                    </Grid>
                  </Grid>

                  <Button
                    variant="contained"
                    startIcon={<Search />}
                    onClick={handleSearchRoute}
                    sx={{
                      width: '100%',
                      mt: 3,
                      py: 1.2,
                      borderRadius: 999,
                      textTransform: 'none',
                      fontWeight: 600,
                    }}
                  >
                    Tìm chuyến xe
                  </Button>
                </Box>
              </Grid>
            </Grid>

            {/* Routes section */}
            <Box sx={{ mt: 5 }}>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  mb: 2,
                }}
              >
                <Typography variant="h5" fontWeight={700}>
                  Tuyến xe phổ biến
                </Typography>
                <Typography variant="body2" sx={{ color: '#666' }}>
                  Có {routes.length} tuyến đang hoạt động
                </Typography>
              </Box>

              <RouteList
                routes={routes}
                onRouteClick={(route) =>
                  navigate(
                    `/trips?origin=${route.origin_code}&destination=${route.destination_code}&from_date=${today}`
                  )
                }
              />
            </Box>
          </>
        )}
      </Container>
    </Box>
  );
};

export default Home;


// import { useMemo, useState } from 'react';
// import { useSelector } from 'react-redux';
// import { useNavigate } from 'react-router-dom';
// import {
//   Autocomplete,
//   Button,
//   Container,
//   Grid,
//   Skeleton,
//   TextField,
// } from '@mui/material';
// import useMessage from 'antd/es/message/useMessage';
// import RouteList from '../Route/RouteList';
// import { LocationOn, Search } from '@mui/icons-material';

// const todayVN = () => {
//   const today = new Date();
//   const day = String(today.getDate()).padStart(2, '0');
//   const month = String(today.getMonth() + 1).padStart(2, '0');
//   const year = today.getFullYear();
//   return `${year}-${month}-${day}`;
// };

// const today = todayVN();

// const Home = () => {
//   const [origin, setOrigin] = useState(null);
//   const [destination, setDestination] = useState(null);
//   const [fromDate, setFromDate] = useState(today);
//   const [errors, setErrors] = useState({
//     origin: false,
//     destination: false,
//     fromDate: false,
//   });

//   const navigate = useNavigate();
//   const [messageApi, contextHolder] = useMessage();

//   const { routes, loading } = useSelector((state) => state.trips);

//   const places = useMemo(() => {
//     const map = new Map();
//     if (routes && routes.length > 0) {
//       routes.forEach((route) => {
//         if (route.origin && route.origin_code && !map.has(route.origin_code)) {
//           map.set(route.origin_code, {
//             label: route.origin,
//             code: route.origin_code,
//           });
//         }
//         if (
//           route.destination &&
//           route.destination_code &&
//           !map.has(route.destination_code)
//         ) {
//           map.set(route.destination_code, {
//             label: route.destination,
//             code: route.destination_code,
//           });
//         }
//       });
//     }
//     return Array.from(map.values());
//   }, [routes]);

//   const handleSearchRoute = () => {
//     const newErrors = {
//       origin: !origin,
//       destination: !destination,
//       fromDate: !fromDate,
//     };
//     setErrors(newErrors);
//     if (newErrors.origin || newErrors.destination || newErrors.fromDate) return;
//     if (origin.code === destination.code) {
//       messageApi.error('Origin and Destination cannot be the same!');
//       // setOrigin(null);
//       setDestination(null);
//       return;
//     }

//     const payload = {
//       origin_code: origin.code,
//       destination_code: destination.code,
//       from_date: fromDate,
//     };
//     console.log('Search payload: ', payload);

//     navigate(
//       `/trips?origin=${payload.origin_code}&destination=${payload.destination_code}&from_date=${payload.from_date}`
//     );
//   };

//   return (
//     <>
//       <Container maxWidth="lg" sx={{}}>
//         {contextHolder}
//         <h1>HOME PAGE</h1>
//         {/* Truyền profile + refreshProfile cho các màn con */}
//         {loading ? (
//           <div
//             style={{
//               height: '60vh',
//               display: 'flex',
//               flexDirection: 'column',
//               justifyContent: 'space-around',
//             }}
//           >
//             <Skeleton variant="rounded" width={'100%'} height={100} />
//             <Skeleton variant="rounded" width={'100%'} height={300} />
//           </div>
//         ) : (
//           <div>
//             <Grid container spacing={1}>
//               <Grid
//                 container
//                 size={12}
//                 spacing={2}
//                 sx={{
//                   display: 'flex',
//                   justifyContent: 'center',
//                   alignItems: 'center',
//                   border: '0px solid aqua',
//                   borderRadius: '16px',
//                   boxShadow: '0 2px 8px rgba(0,0,0,0.18)',
//                   padding: '10px',
//                   marginBottom: '10px',
//                 }}
//               >
//                 <Grid size={{ xs: 12, sm: 6, md: 4 }}>
//                   <Autocomplete
//                     startIcon={<LocationOn />}
//                     disablePortal
//                     options={places}
//                     getOptionLabel={(option) => option.label}
//                     sx={{ width: '100%' }}
//                     value={origin}
//                     onChange={(e, newValue) => setOrigin(newValue)}
//                     renderInput={(params) => (
//                       <TextField
//                         {...params}
//                         label="Select origin"
//                         error={errors.origin}
//                         helperText={errors.origin ? 'Origin is required' : ''}
//                         InputProps={{
//                           ...params.InputProps,
//                           startAdornment: (
//                             <>
//                               <LocationOn
//                                 sx={{ mr: 1, color: 'primary.main' }}
//                               />
//                               {params.InputProps.startAdornment}
//                             </>
//                           ),
//                         }}
//                       />
//                     )}
//                   />
//                 </Grid>
//                 <Grid size={{ xs: 12, sm: 6, md: 4 }}>
//                   <Autocomplete
//                     startIcon={<LocationOn />}
//                     disablePortal
//                     options={places}
//                     getOptionLabel={(option) => option.label}
//                     sx={{ width: '100%' }}
//                     value={destination}
//                     onChange={(e, newValue) => setDestination(newValue)}
//                     renderInput={(params) => (
//                       <TextField
//                         {...params}
//                         label="Select destination"
//                         error={errors.destination}
//                         helperText={
//                           errors.destination ? 'Destination is required' : ''
//                         }
//                         InputProps={{
//                           ...params.InputProps,
//                           startAdornment: (
//                             <>
//                               <LocationOn
//                                 sx={{ mr: 1, color: 'primary.main' }}
//                               />
//                               {params.InputProps.startAdornment}
//                             </>
//                           ),
//                         }}
//                       />
//                     )}
//                   />
//                 </Grid>
//                 <Grid size={{ xs: 12, sm: 12, md: 4 }}>
//                   {/* <Date */}
//                   <TextField
//                     fullWidth
//                     label="Select date"
//                     type="date"
//                     value={fromDate}
//                     onChange={(e) => setFromDate(e.target.value)}
//                     error={errors.fromDate}
//                     helperText={errors.fromDate ? 'Date is required' : ''}
//                     InputLabelProps={{ shrink: true }}
//                     slotProps={{ inputAdornment: { min: today } }}
//                   />
//                 </Grid>
//                 <Grid size={{ xs: 12, md: 4 }} sx={{}}>
//                   <Button
//                     variant="contained"
//                     startIcon={<Search />}
//                     onClick={handleSearchRoute}
//                     sx={{ width: '100%' }}
//                   >
//                     SEARCH TRIPS
//                   </Button>
//                 </Grid>
//               </Grid>
//               {/* <Grid size={12}>SHOW NEWEST TRIPS</Grid>
//               <Grid size={12}>SLIDES</Grid> */}
//             </Grid>

//             <h2>Available Routes: {routes.length}</h2>
//             <RouteList
//               routes={routes}
//               onRouteClick={(route) =>
//                 navigate(
//                   `/trips?origin=${route.origin_code}&destination=${route.destination_code}&from_date=${today}`
//                 )
//               }
//             />
//           </div>
//         )}
//       </Container>
//     </>
//   );
// };

// export default Home;
