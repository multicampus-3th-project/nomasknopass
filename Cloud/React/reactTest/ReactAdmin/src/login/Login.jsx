import React, { useState } from 'react';
import { CognitoUser, AuthenticationDetails } from 'amazon-cognito-identity-js';
import Userpool from './Userpool';
import '../assets/css/now-ui-dashboard.css';

import {
  Button,
  Card,
  CardHeader,
  CardBody,
  FormGroup,
  Form,
  Input,
  Row,
  Col,
} from "reactstrap";


const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const onSubmit = (event) => {
    event.preventDefault();

    const user = new CognitoUser({
      Username: email,
      Pool: Userpool,
    });

    const authDetails = new AuthenticationDetails({
      Username: email,
      Password: password,
    });

    user.authenticateUser(authDetails, {
      onSuccess: (data) => {
        console.log('onSuccess: ', data);
      },
      onFailure: (err) => {
        console.error('onFailure: ', err);
      },
      newPasswordRequired: (data) => {
        console.log('newPasswordRequired: ', data);
      },
    });
  };

  return (
    <div>
      <Row>
        <Col md="6">
          <Card>
            <CardHeader>
              <div className="div-title">
              <h4 className="title">KF99 Dashboard</h4>
              </div>
            </CardHeader>
            <CardBody>
              <Form
                onSubmit={onSubmit}>
                <Row>
                  <Col sm="12" md={{ size: 6, offset: 3 }}>
                    <FormGroup>
                      <label htmlFor="email">Email</label>
                      <Input
                        placeholder="Email"
                        type="text"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                      />
                    </FormGroup>
                  </Col>
                </Row>
                <Row>
                  <Col sm="12" md={{ size: 6, offset: 3 }}>
                    <FormGroup>
                      <label htmlFor="password">Password</label>
                      <Input
                        placeholder="Password"
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                      />
                    </FormGroup>
                  </Col>
                </Row>
                <Row>
                <Col sm="12" md={{ size: 6, offset: 3 }}>
                <Button
                  color="info"
                  block
                  type="submit"
                >
                  Login
                </Button>
                </Col>
                </Row>
              </Form>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Login;
