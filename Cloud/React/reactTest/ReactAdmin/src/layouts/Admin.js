import NavBar from '../components/NavBar';
import Sidebar from "../components/Sidebar";
import routes from "../routes.js";
import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";

import '../assets/css/now-ui-dashboard.css';


import Login from '../login/Login';
import { CustomSignOut } from '../components/CustomSignOut';

import Amplify from "aws-amplify";
import { AmplifyAuthenticator, AmplifySignIn, AmplifySignOut } from "@aws-amplify/ui-react";
import awsconfig from "../login/Userpool";

Amplify.configure(awsconfig);



class Admin extends React.Component {
  state = {
    backgroundColor: "blue",
  };
  mainPanel = React.createRef();

  render() {
    return (
      <AmplifyAuthenticator>
        <AmplifySignIn
          slot="sign-in"
          headerText="KF99 Dashboard Sign In"
          style={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          <div slot="secondary-footer-content"></div>
        </AmplifySignIn>
        <div className="wrapper">
          <Sidebar
            {...this.props}
            routes={routes}
            backgroundColor={this.state.backgroundColor}
          />
          <div className="main-panel" ref={this.mainPanel}>
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
      </AmplifyAuthenticator>
    );
  }
}

export default Admin;