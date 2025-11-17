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
} from '@mui/material';
import { Home, Menu as MenuIcon } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { Divider } from 'antd';
import './CustomerHeader.css';


const pages = [
  { name: 'Home', path: '/' },
  { name: 'Routes', path: '/routes' },
  { name: 'Bookings', path: '/bookings' },
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
    <AppBar position="static" sx={{backgroundColor: 'inherit', color: 'black !important'}}>
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
                    <MenuItem key={page.name} onClick={handleCloseNavMenu} >
                      <Link
                        to={page.path}
                        style={{ textDecoration: 'none', color: 'black' }}
                      >
                        <Typography textAlign="center">{page.name}</Typography>
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
                    <Home />
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
                    letterSpacing: '.3rem',
                    color: 'inherit',
                    textDecoration: 'none',
                  }}
                >
                  BUS TICKET BOOKING SYSTEM
                </Typography>
              </div>

              {!user ? (
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <Button
                    component={Link}
                    to="/login"
                    className='link'
                  >
                    Login
                  </Button>
                  <Divider type="vertical"
                    style={{ height: '30px', width: '2px', margin: '0 5px' }}
                   />
                  <Button
                    component={Link}
                    to="/register"
                    className='link'
                  >
                    Register
                  </Button>
                </div>
              ) : (
                <div>
                  <Box sx={{ flexGrow: 0 }}>
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
                    sx={{ my: 2, color: 'black', display: 'block' }}
                    className="link"
                  >
                    {page.name}
                  </Button>
                ))}
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
}
export default CustomerHeader;
