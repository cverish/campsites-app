import axios, { AxiosInstance } from "axios";

const API_URI = process.env.REACT_APP_API_URI;

const http: AxiosInstance = axios.create({
  baseURL: API_URI,
  headers: {
    "Content-type": "application/json",
  },
});

export default http;
