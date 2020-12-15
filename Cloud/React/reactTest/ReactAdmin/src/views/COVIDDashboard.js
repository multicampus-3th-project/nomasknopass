import React, { useEffect, useState } from 'react';
import axios from "axios";

// Wijmo imports
import 'wijmo/styles/wijmo.css';
import { FlexGrid, FlexGridColumn } from 'wijmo/wijmo.react.grid';
import { FlexChart, FlexPie, FlexChartSeries } from 'wijmo/wijmo.react.chart';
import { RadialGauge } from 'wijmo/wijmo.react.gauge';
import { CollectionView } from "wijmo/wijmo";
import { CollectionViewNavigator } from "wijmo/wijmo.react.input";

// Data imports
import { recentSales, salesByCountry, salesByPerson } from '../data/data';

// css
import '../assets/css/now-ui-dashboard.css';
import '../assets/css/main.css';

import {
    Card,
    CardHeader,
    CardBody,
    CardFooter,
    CardTitle,
    Row,
    Col,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem,
    Table,
    Button,
    Label,
    FormGroup,
    Input,
    UncontrolledTooltip,
} from "reactstrap";


const COVIDDashboard = () => {
    const [ispassData, setIsPassData] = useState([
        { "count": 0 },
        { "count": 0 }]);

    useEffect(() => {
    }, []);


    return (
        <>
            <div>
                <div className="content">
                    <Row>
                        <Col xs={12} md={0}>
                            <Card className="card-chart card-chart-long">
                                <CardHeader>
                                    <h5 className="card-category">Gate Total</h5>
                                    <CardTitle tag="h4">방문 기록</CardTitle>
                                    <UncontrolledDropdown>
                                        <DropdownToggle
                                            className="btn-round btn-outline-default btn-icon"
                                            color="default"
                                        >
                                            <i className="now-ui-icons loader_gear" />
                                        </DropdownToggle>
                                        <DropdownMenu right>
                                            <DropdownItem>Action</DropdownItem>
                                            <DropdownItem>Another Action</DropdownItem>
                                            <DropdownItem>Something else here</DropdownItem>
                                            <DropdownItem className="text-danger">
                                                Remove data
                      </DropdownItem>
                                        </DropdownMenu>
                                    </UncontrolledDropdown>
                                </CardHeader>
                                <CardBody>
                                    <div className="chart-area">
                                        {/* <TransactionList transactions={gateData} /> */}
                                    </div>
                                </CardBody>
                                <CardFooter>
                                    <div className="stats">  
                                        <i className="now-ui-icons arrows-1_refresh-69" /> Just
                    Updated
                  </div>
                                </CardFooter>
                            </Card>
                        </Col>
                    </Row>
                </div>
            </div>
        </>
    )


}

export default COVIDDashboard;
