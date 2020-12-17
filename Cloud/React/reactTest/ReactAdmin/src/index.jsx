import React, { Component } from 'react';
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { BrowserRouter, Router, Route, Switch, Redirect } from "react-router-dom";
import App from './App';
import AdminLayout from "./layouts/Admin.jsx";
// css
import "bootstrap/dist/css/bootstrap.css";
import './App.css';

ReactDOM.render(
  <BrowserRouter>
      <App />
  </BrowserRouter>,
  document.getElementById('root')
);