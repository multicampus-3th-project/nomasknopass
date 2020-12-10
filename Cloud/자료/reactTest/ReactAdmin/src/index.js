import React, { Component } from 'react';
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";

import AdminLayout from "./layouts/Admin.js";

// css
import "bootstrap/dist/css/bootstrap.css";


import './App.css';

const hist = createBrowserHistory();

ReactDOM.render(
  <Router history={hist}>
    <Switch>
      <Route path="/admin" render={(props) => <AdminLayout {...props} />} />
      <Redirect to="/admin/gatedashboard" />
    </Switch>
  </Router>,
  document.getElementById("root")
);
 