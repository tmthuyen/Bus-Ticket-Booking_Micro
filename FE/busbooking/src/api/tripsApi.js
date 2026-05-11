import api from "./api";

const PREFIX_SERVICE = "/trips";
// GET /trips/routes
export const getRoutes = async () => {
  const res = await api.get(`${PREFIX_SERVICE}/routes`);
  // console.log("getRoutes: ", res.data);
  return {
    responseApi: res.data
  }; // tuỳ backend trả data gì
};

export const getTripById = async (trip_id) => {
  trip_id = parseInt(trip_id);
  const res = await api.get(`${PREFIX_SERVICE}/trips/${trip_id}`);
  return {
    responseApi: res.data
  };
};

// GET /trips/routes?origin_code=&destination_code=&from_date=
export const getTripsByOriginAndDestinationAndFromDate = async (origin_code, destination_code, from_date) => {
  const res = await api.get(`${PREFIX_SERVICE}/trips-by-route`, {
    params: { origin_code, destination_code, from_date }
  });
  return {
    responseApi: res.data
  };
};

// GET /trips/seats-by-trip/:trip_id
export const getSeatsByTripId = async (trip_id) => {
  trip_id = parseInt(trip_id);
  const res = await api.get(`${PREFIX_SERVICE}/seats-by-trip/${trip_id}`);
  return {
    responseApi: res.data
  };
}

// PUT /routes/:id
export const updateRoute = async (id, data) => {
  const res = await api.put(`${PREFIX_SERVICE}/routes/${id}`, data);
  return {
    responseApi: res.data
  };
};

// DELETE /routes/:id
export const deleteRoute = async (id) => {
  const res = await api.delete(`${PREFIX_SERVICE}/routes/${id}`);
  return {
    responseApi: res.data
  };
};
