import * as React from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Avatar,
  Button,
  Tooltip,
  MenuItem,
  Grid,
  Container,
  Divider,
} from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';
import { Link } from 'react-router-dom'; 
import './CustomerHeader.css';

const pages = [
  { name: 'Home', path: '/' },
  { name: 'Routes', path: '/routes' },
  { name: 'Lookup ticket', path: '/lookup-ticket' }, 
  { name: 'Contact', path: '/contact' },
];
const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];

function CustomerHeader({ user = null }) {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
    <AppBar
      position="static"
      sx={{ backgroundColor: 'inherit', color: 'black !important' }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Grid container spacing={0} sx={{ width: '100%', paddingX: '0px' }}>
            <Grid size={12}>
              <Box
                sx={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginX: 'auto',
                }}
              >
                <Box
                  sx={{
                    display: { xs: 'flex', md: 'none' },
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <IconButton
                    size="large"
                    aria-label="account of current user"
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    onClick={handleOpenNavMenu}
                    color="inherit"
                  >
                    <MenuIcon />
                  </IconButton>
                  <Menu
                    id="menu-appbar"
                    anchorEl={anchorElNav}
                    anchorOrigin={{
                      vertical: 'bottom',
                      horizontal: 'left',
                    }}
                    keepMounted
                    transformOrigin={{
                      vertical: 'top',
                      horizontal: 'left',
                    }}
                    open={Boolean(anchorElNav)}
                    onClose={handleCloseNavMenu}
                    sx={{ display: { xs: 'block', md: 'none' } }}
                  >
                    {pages.map((page) => (
                      <MenuItem key={page.name} onClick={handleCloseNavMenu}>
                        <Link
                          to={page.path}
                          style={{ fontWeight: 'bold', textDecoration: 'none', color: 'black' }}
                        >
                          <Typography textAlign="center">
                            {page.name}
                          </Typography>
                        </Link>
                      </MenuItem>
                    ))}
                  </Menu>
                </Box>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <IconButton
                    size="large"
                    onClick={() => console.log('Go to Home')}
                    color="inherit"
                  >
                    <Link to="/" style={{ color: 'inherit' }}>
                      <img
                        src="/bus_logo.png"
                        alt="Bus Ticket Booking System"
                        style={{ width: '50px', height: '50px' }}
                      />
                    </Link>
                  </IconButton>
                  <Typography
                    variant="h5"
                    noWrap
                    component="a"
                    href="#app-bar-with-responsive-menu"
                    sx={{
                      mr: 2,
                      display: { xs: 'none', md: 'flex' },
                      fontFamily: 'monospace',
                      fontWeight: 700,
                      letterSpacing: '.1rem',
                      color: 'inherit',
                      textDecoration: 'none',
                    }}
                  >
                    BUS TICKET BOOKING SYSTEM
                  </Typography>
                </div>

                {!user ? (
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <Button variant='contained' component={Link} to="/login" className="link">
                      Login
                    </Button>
                    <Divider
                      orientation="vertical"
                      variant="inset"
                      style={{ height: '30px', width: '0px', margin: '0 2px' }}
                    />
                    <Button variant='contained' component={Link} to="/register" className="link">
                      Register
                    </Button>
                  </div>
                ) : (
                  <div>
                    <Box sx={{ flexGrow: 0, display: 'flex', alignItems: 'center' }}>
                      <Typography
                        variant="body1"
                        sx={{ display: 'inline', marginRight: '10px' }}
                      >
                        {user?.full_name}
                      </Typography>
                      <Tooltip title="Open settings">
                        <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                          <Avatar
                            alt="Remy Sharp"
                            src="/static/images/avatar/2.jpg"
                          />
                        </IconButton>
                      </Tooltip>
                      <Menu
                        sx={{ mt: '45px' }}
                        id="menu-appbar"
                        anchorEl={anchorElUser}
                        anchorOrigin={{
                          vertical: 'top',
                          horizontal: 'right',
                        }}
                        keepMounted
                        transformOrigin={{
                          vertical: 'top',
                          horizontal: 'right',
                        }}
                        open={Boolean(anchorElUser)}
                        onClose={handleCloseUserMenu}
                      >
                        {settings.map((setting) => (
                          <MenuItem key={setting} onClick={handleCloseUserMenu}>
                            <Typography sx={{ textAlign: 'center' }}>
                              {setting}
                            </Typography>
                          </MenuItem>
                        ))}
                      </Menu>
                    </Box>
                  </div>
                )}
              </Box>
            </Grid>
            <Grid size={12} sx={{ display: { sx: 'none', md: 'flex' } }}>
              <Box
                sx={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                }}
              >
                <Box
                  sx={{
                    width: '100%',
                    marginX: 'auto',
                    display: { xs: 'none', md: 'flex' },
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}  
                >
                  {pages.map((page) => (
                    <Button
                      key={page.name}
                      component={Link}
                      to={page.path}
                      sx={{ my: 2, mx: 3, color: 'black', display: 'block' }}
                      className="link"
                    >
                      <Typography style={{width: '100%'}}  fontWeight={600}>{page.name}</Typography>
                    </Button>
                  ))}
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default CustomerHeader;
