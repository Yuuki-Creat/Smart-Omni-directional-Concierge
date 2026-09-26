// Connection Module to the backend API
const API_BASE_URL = 'https://smart-omni-directional-concierge.onrender.com/api';

export const submitIndividualCheckin = async (data) => {
    const res = await fetch(`${API_BASE_URL}/individual/checkin`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return res.json();
};

export const fetchCorporateStatus = async (corpId) => {
    const res = await fetch(`${API_BASE_URL}/corporate/status/${corpId}`);
    return res.json();
};

export const fetchFactorySchedule = async () => {
    const res = await fetch(`${API_BASE_URL}/factory/schedule`);
    return res.json();
};

export const submitStoreReception = async (ticketId) => {
    const res = await fetch(`${API_BASE_URL}/store/reception`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticket_id: ticketId }),
    });
    return res.json();
};
