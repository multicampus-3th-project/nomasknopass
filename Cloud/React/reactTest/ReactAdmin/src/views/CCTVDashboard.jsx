import React, { useEffect, useState } from 'react';
import axios from "axios";

// Wijmo imports
import 'wijmo/styles/wijmo.css';
import * as wjChart from 'wijmo/wijmo.react.chart';
import * as wjCharts from 'wijmo/wijmo.chart';
import * as wjChartAnimate from 'wijmo/wijmo.react.chart.animation';
// Data imports
import { covidTotal, covidDay, tempData } from '../data/data';

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

const CCTVReport = ({ data, palette }) => {
    return (
        <div className="line-total">
            <wjChart.FlexChart itemsSource={data} bindingX="time" chartType="Line" palette={palette}>
                <wjChart.FlexChartLegend position="Bottom"></wjChart.FlexChartLegend>
                <wjChart.FlexChartAxis wjProperty="axisY"></wjChart.FlexChartAxis>
                <wjChart.FlexChartSeries binding="nomask" name="마스크 미착용"></wjChart.FlexChartSeries>
                <wjChart.FlexChartLineMarker isVisible={false} lines="Both" interaction="Move">
                </wjChart.FlexChartLineMarker>
                <wjChartAnimate.FlexChartAnimation animationMode="Point"></wjChartAnimate.FlexChartAnimation>
            </wjChart.FlexChart>
        </div>
    )
}
const CCTVDashboard = () => {
    const [CCTVData, setCCTVData] = useState([{'mask':0, 'nomask':0, 'incorrectmask':0}]);
    const [palette, setPalette] = useState(['rgba(255,136,0,1)']);

    useEffect(() => {
      _getCCTVData();
    }, []);

    const cctvDataEndpoint =
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/cctv";


    const _getCCTVData = async () => {
        await axios.get(cctvDataEndpoint).then((res) => {
          setCCTVData(res.data);
          console.log(res.data);
        })
      }

    return (
        <>
            <div>
                <div className="content">
                  <Row>
                    <Col xs={12} md={3}>
                      <Card className="card-chart card-chart-long">
                        <CardHeader>
                          <h5 className="card-category">CCTV Total</h5>
                          <CardTitle tag="h4">마스크 착용</CardTitle>
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
                          {CCTVData[CCTVData.length-1]['mask']}
                          </CardBody>
                          <CardFooter>
                                    <div className="stats">  
                                        <i className="now-ui-icons arrows-1_refresh-69" /> Just
                    Updated
                  </div>
                                </CardFooter>
                      </Card>
                    </Col>

                    <Col xs={12} md={3}>
                      <Card className="card-chart card-chart-long">
                        <CardHeader>
                          <h5 className="card-category">CCTV Total</h5>
                          <CardTitle tag="h4">마스크 미착용</CardTitle>
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
                          {CCTVData[CCTVData.length-1]['nomask']}
                          </CardBody>
                          <CardFooter>
                                    <div className="stats">  
                                        <i className="now-ui-icons arrows-1_refresh-69" /> Just
                    Updated
                  </div>
                                </CardFooter>
                      </Card>
                    </Col>

                    <Col xs={12} md={3}>
                      <Card className="card-chart card-chart-long">
                        <CardHeader>
                          <h5 className="card-category">CCTV Total</h5>
                          <CardTitle tag="h4">마스크 잘못 착용</CardTitle>
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
                          {CCTVData[CCTVData.length-1]['incorrectmask']}
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
                    <Row>
                    <Col xs={12} md={0}>
                            <Card className="card-chart card-chart-long">
                                <CardHeader>
                                    <h5 className="card-category">CCTV Total</h5>
                                    <CardTitle tag="h4">마스크 미착용 인원</CardTitle>
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
                                        <CCTVReport data={CCTVData} palette={palette}/>
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

export default CCTVDashboard;
