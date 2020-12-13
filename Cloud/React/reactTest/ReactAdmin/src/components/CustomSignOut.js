import React from "react";
import { SignOut } from "aws-amplify-react";
import {
    Button,
    Row,
    Col,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem,
  } from "reactstrap";

export class CustomSignOut extends SignOut {
    constructor(props) {
        super(props);
        this._validAuthStates = ["signedOut"];
    }
render() {
        return (
            <div style={{textAlign:'center'}}>
              <div style={{display:'inline-block'}}>
              <span style={{color:'white'}}>Hello, Admin!</span> 
              </div>
              <div style={{display:'inline-block', marginLeft:'70px', marginRight: '0px'}}>
                <UncontrolledDropdown>
                    <DropdownToggle
                      className="btn-round btn-outline-default btn-icon"
                      color="default"
                    >
                      <i className="now-ui-icons users_circle-08"
                        style={{color:'white', fontSize: "18px"}} />
                    </DropdownToggle>
                    <DropdownMenu>
                      <DropdownItem>KF99 Admin</DropdownItem>
                      <DropdownItem 
                        className="text-danger"
                        onClick={() => super.signOut()}>
                        Sign Out
                      </DropdownItem>
                    </DropdownMenu>
                  </UncontrolledDropdown>
                  </div>
                </div>
        )
    }
}