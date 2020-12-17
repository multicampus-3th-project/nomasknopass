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

const CovidTotal = ({ data, palette }) => {
    return (
        <div className="line-total">
            <wjChart.FlexChart itemsSource={data} bindingX="statedt" chartType="Area" palette={palette}>
                <wjChart.FlexChartLegend position="None"></wjChart.FlexChartLegend>
                <wjChart.FlexChartAxis wjProperty="axisX" labelAngle={-45}></wjChart.FlexChartAxis>
                <wjChart.FlexChartAxis wjProperty="axisY"></wjChart.FlexChartAxis>
                <wjChart.FlexChartSeries binding="decidecnt" name="누적 확진자 수"></wjChart.FlexChartSeries>
                <wjChartAnimate.FlexChartAnimation animationMode="Point"></wjChartAnimate.FlexChartAnimation>
            </wjChart.FlexChart>
        </div>
    );
  }

const CovidDay = ({ data, palette }) => {
    return (
        <div className="line-total">
            <wjChart.FlexChart itemsSource={data} bindingX="statedt" chartType="Line" palette={palette}>
                <wjChart.FlexChartLegend position="Bottom"></wjChart.FlexChartLegend>
                <wjChart.FlexChartAxis wjProperty="axisY"></wjChart.FlexChartAxis>
                <wjChart.FlexChartSeries binding="decidecnt_day" name="일일 확진자 수"></wjChart.FlexChartSeries>
                <wjChart.FlexChartLineMarker isVisible={false} lines="Both" interaction="Move">
                </wjChart.FlexChartLineMarker>
                <wjChartAnimate.FlexChartAnimation animationMode="Point"></wjChartAnimate.FlexChartAnimation>
            </wjChart.FlexChart>
        </div>
    )
}
const MaskReport = ({ data, palette }) => {
    return (
        <div className="line-total">
            <wjChart.FlexChart itemsSource={data} bindingX="date" chartType="Line" palette={palette}>
                <wjChart.FlexChartLegend position="Bottom"></wjChart.FlexChartLegend>
                <wjChart.FlexChartAxis wjProperty="axisY"></wjChart.FlexChartAxis>
                <wjChart.FlexChartSeries binding="reports_num" name="마스크 신고 건수"></wjChart.FlexChartSeries>
                <wjChart.FlexChartLineMarker isVisible={false} lines="Both" interaction="Move">
                </wjChart.FlexChartLineMarker>
                <wjChartAnimate.FlexChartAnimation animationMode="Point"></wjChartAnimate.FlexChartAnimation>
            </wjChart.FlexChart>
        </div>
    )
}
const COVIDDashboard = () => {
    const [paletteTotal, setPaletteTotal] = useState(wjCharts.Palettes.standard);
    const [totalData, setTotalData] = useState([]);
    const [dayData, setDayData] = useState([]);
    const [paletteDay, setPaletteDay] = useState([ 'rgba(153,51,204,1)', 'rgba(255,136,0,1)', 'rgba(204,0,0,1)', 'rgba(0,204,163,1)', 'rgba(61,109,204,1)', 'rgba(82,82,82,1)', 'rgba(0,0,0,1)']);
    const [palettemaskReport, setMaskReport] = useState(['rgba(255,136,0,1)']);
    const [maskReportData, setMaskReportData] = useState([]);

    useEffect(() => {
        _getCovidTotal();
        _getMaskReport();
    }, []);

    const covidTotalEndpoint =
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/covidtotal";
    const maskReportEndpoint =
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/maskreport";

    const _getCovidTotal = async () => {
        await axios.get(covidTotalEndpoint).then((res) => {
          setTotalData(res.data);
          setDayData(res.data);
          console.log(res.data);
        })
      }

      const _getMaskReport = async () => {
        await axios.get(maskReportEndpoint).then((res) => {
          setMaskReportData(res.data);
          console.log(res.data);
        })
      }

    return (
        <>
            <div>
                <div className="content">
                    <Row>
                        <Col xs={12} md={6}>
                            <Card className="card-chart card-chart-long">
                                <CardHeader>
                                    <h5 className="card-category">COVID19 Total</h5>
                                    <CardTitle tag="h4">일일 확진자 수</CardTitle>
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
                                        <CovidDay data={dayData} palette={paletteDay}/>
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
                        <Col xs={12} md={6}>
                            <Card className="card-chart card-chart-long">
                                <CardHeader>
                                    <h5 className="card-category">COVID19 Total</h5>
                                    <CardTitle tag="h4">누적 확진자 수</CardTitle>
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
                                        <CovidTotal data={totalData} palette={paletteTotal}/>
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
                    <Row>
                    <Col xs={12} md={0}>
                            <Card className="card-chart card-chart-long">
                                <CardHeader>
                                    <h5 className="card-category">COVID19 Total</h5>
                                    <CardTitle tag="h4">마스크 미착용 신고건수</CardTitle>
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
                                        <MaskReport data={maskReportData} palette={palettemaskReport}/>
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
