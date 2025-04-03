import axios from "axios";
import { ACCESS_TOKEN } from "../constants";


const api = axios.create({
  baseURL: 'http://144.126.234.87:8002/'
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
