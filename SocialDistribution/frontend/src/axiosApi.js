import axios from 'axios';
import 'regenerator-runtime/runtime';
// import { useNavigate } from 'react-router-dom';

const baseURL = `http://${window.location.hostname}:8000/api/`;
const axiosInstance = axios.create({
  baseURL,
  timeout: 0, // temporary, we should fix this later when we have job scheduling setup
  headers: {
    Authorization: `JWT ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json',
    accept: 'application/json',
  },
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    // const navigate = useNavigate();
    const originalRequest = error.config;

    if (error.response.data.code === 'token_not_valid' && error.response.status === 401 && error.response.statusText === 'Unauthorized') {
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

        // exp date in token is expressed in seconds, while now() returns milliseconds:
        const now = Math.ceil(Date.now() / 1000);

        if (tokenParts.exp > now) {
          const response = await axios.post(`${baseURL}token/refresh/`, { refresh: refreshToken });

          localStorage.setItem('access_token', response.data.access);
          localStorage.setItem('refresh_token', response.data.refresh);

          axiosInstance.defaults.headers.Authorization = `JWT ${response.data.access}`;
          originalRequest.headers.Authorization = `JWT ${response.data.access}`;

          return axiosInstance(originalRequest);
        }
        // if refresh is expired
        localStorage.clear();
        window.location.href = '/login/';// Go to login but lets useHistory to route later
      } else {
        localStorage.clear();
        window.location.href = '/login/';// Go to login but lets useHistory to route later
      }
    }

    // specific error handling done elsewhere
    return Promise.reject(error);
  },
);

export default axiosInstance;