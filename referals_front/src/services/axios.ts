import axios from "axios";

export const API_URL = 'http://localhost:8000/api/';

const $api = axios.create({
	baseURL: API_URL,
	timeout: 5000,
	withCredentials: true,
	xsrfCookieName: 'csrftoken',
	xsrfHeaderName: 'X-CSRFToken',
	headers: {
		'Content-Type': 'application/json',
		accept: 'application/json',
	},
});

export default $api;
