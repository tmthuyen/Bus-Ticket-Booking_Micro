export const parseTicketInfo = (ticketInfo) => {
  if (!ticketInfo) return null;

  const info = {
    id: ticketInfo.id,
    bookingCode: ticketInfo.booking_code,
    fullName: ticketInfo.full_name,
    phone: ticketInfo.phone,
    email: ticketInfo.email,
    status: ticketInfo.status,
    seatQuantity: ticketInfo.seat_quantity,
    totalPrice: ticketInfo.total_price,
    createdAt: ticketInfo.created_at,
    seatAssignments: ticketInfo.seat_assignments
      .map((seat) => seat.seat_number)
      .join(', '),
    origin: ticketInfo.trip?.route?.origin,
    destination: ticketInfo.trip?.route?.destination,
    departureTime: ticketInfo.trip?.departure_time,
    arrivalTime: ticketInfo.trip?.arrival_time,
    busPlateNumber: ticketInfo.trip?.bus?.plate_number,
  };

  return info;
};
