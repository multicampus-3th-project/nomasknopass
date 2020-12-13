import NavBar from '../components/NavBar';
import Sidebar from "../components/Sidebar";
import routes from "../routes.js";
import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";

import '../assets/css/now-ui-dashboard.css';

import Login from '../login/Login';


class Admin extends React.Component {
    state = {
      backgroundColor: "blue",   
    };
    mainPanel = React.createRef();
    
    render() {
      return (
        <div className="wrapper">
          <Sidebar
            {...this.props}
            routes={routes}
            backgroundColor={this.state.backgroundColor}
          />
            <div className="main-panel" ref={this.mainPanel}>
          <Login></Login>

            <Switch>
            {routes.map((prop, key) => {
              return (
                <Route
                  path={prop.layout + prop.path}
                  component={prop.component}
                  key={key}
                />
              );
            })}
            <Redirect from="/admin" to="/admin/gatedashboard" />
          </Switch>
            </div>
        </div>
      );
    }
  }
  
  export default Admin;