import React, { useEffect, useState } from 'react';
import axios from "axios";
import useInterval from 'use-interval'
import ToggleSwitch from '../components/ToggleSwitch';
import PanelHeader from '../components/PanelHeader';
import ReactstrapImageGallery from "../components/gallery/ReactstrapImageGallery";

// Wijmo imports
import 'wijmo/styles/wijmo.css';
import * as wjChart from 'wijmo/wijmo.react.chart';
import * as wjCharts from 'wijmo/wijmo.chart';
import * as wjChartAnimate from 'wijmo/wijmo.react.chart.animation';
import * as wjGauge from 'wijmo/wijmo.react.gauge';

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

const images_url = [{"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
                {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
                {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
                {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
                {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
                {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'}]

const CCTVReport = ({ data, palette }) => {
  return (
    <div className="line-total">
      <wjChart.FlexChart itemsSource={data} bindingX="time" chartType="Line" palette={palette}>
        <wjChart.FlexChartLegend position="Bottom"></wjChart.FlexChartLegend>
        <wjChart.FlexChartAxis wjProperty="axisY"></wjChart.FlexChartAxis>
        <wjChart.FlexChartSeries binding="nomask" name="마스크 미착용" chartType={wjCharts.ChartType.LineSymbols}></wjChart.FlexChartSeries>
        <wjChart.FlexChartLineMarker isVisible={false} lines="Both" interaction="Move">
        </wjChart.FlexChartLineMarker>
        {/* <wjChartAnimate.FlexChartAnimation animationMode="Point"></wjChartAnimate.FlexChartAnimation> */}
      </wjChart.FlexChart>
    </div>
  )
}

const CCTVReportOne = ({ data, palette }) => {
  return (
    <div className="report-one" id={palette}>
      <wjGauge.LinearGauge min={0} max={30} value={data} showText="None" step={3} isReadOnly={true} isAnimated={true}>
      </wjGauge.LinearGauge>
    </div>
  )
}
const CCTVDashboard = () => {
  const [CCTVData, setCCTVData] = useState([{ 'mask': 0, 'nomask': 0, 'incorrectmask': 0 }]);
  const [palette, setPalette] = useState(['rgba(255,136,0,1)']);
  const [updateStart, setUpdateStart] = useState(false);
  const [images, setImages] = useState([{"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
  {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
  {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
  {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
  {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'},
  {"url": 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg'}]
)

  useEffect(() => {
    _getCCTVData();
    let interval = null;
    if (updateStart) {
      interval = setInterval(() => {
        _getCCTVData();
        setImages(images_url);
        console.log("하는거맞자너..");
      }, 6000);
    }
    return () => {
      if (interval !== null) {
        clearInterval(interval);
      }
    }
  }, [updateStart]);

  const cctvDataEndpoint =
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/cctv";


  const _getCCTVData = async () => {
    await axios.get(cctvDataEndpoint).then((res) => {
      setCCTVData(res.data);
      console.log("지금나온거야? " + res.data);
    })
  }

  function x(e) {
    e.preventDefault();
    const start = updateStart;
    setUpdateStart(!start);
  }

  const onNewsletterChange = (checked) => {
    setUpdateStart(checked);
  }

  return (
    <>
    <PanelHeader size="sm" />
        <div className="cctv">
          <Row>
            <Col sm="12" md={{ size: 6}} style={{padding: '20px'}}> 
                <ToggleSwitch id="newsletter" checked={ updateStart } onChange={ onNewsletterChange } small={true}/>
                <label htmlFor="newsletter" className="toggle-label">실시간 업데이트</label>
            </Col>
          </Row>
          <Row>
            <Col xs={12} md={{ size: 3 }}>
              <Card className="card-chart card-chart-long text-center">
                <CardHeader>
                  <CardTitle tag="h4">마스크 착용</CardTitle>
                </CardHeader>
                <CardBody>
                  <h1 className="report_num">{CCTVData[CCTVData.length - 1]['mask']}</h1>
                  <CCTVReportOne data={CCTVData[CCTVData.length - 1]['mask']} palette="yellow"></CCTVReportOne>
                </CardBody>
                <CardFooter>
                  <div className="stats">
                    <i className="now-ui-icons arrows-1_refresh-69" /> Just
                    Updated
                  </div>
                </CardFooter>
              </Card>
            </Col>

            <Col xs={12} md={{ size: 3 }}>
              <Card className="card-chart card-chart-long text-center">
                <CardHeader>
                  <CardTitle tag="h4">마스크 미착용</CardTitle>
                </CardHeader>
                <CardBody>
                  <h1 className="report_num">{CCTVData[CCTVData.length - 1]['nomask']}</h1>
                  <CCTVReportOne data={CCTVData[CCTVData.length - 1]['nomask']} palette="green"></CCTVReportOne>
                </CardBody>
                <CardFooter>
                  <div className="stats">
                    <i className="now-ui-icons arrows-1_refresh-69" /> Just
                    Updated
                  </div>
                </CardFooter>
              </Card>
            </Col>

            <Col xs={12} md={{ size: 3 }}>
              <Card className="card-chart card-chart-long text-center">
                <CardHeader>
                  <CardTitle tag="h4">마스크 오착용</CardTitle>
                </CardHeader>
                <CardBody>
                  <h1 className="report_num">{CCTVData[CCTVData.length - 1]['incorrectmask']}</h1>
                  <CCTVReportOne data={CCTVData[CCTVData.length - 1]['incorrectmask']} palette="blue"></CCTVReportOne>
                </CardBody>
                <CardFooter>
                  <div className="stats">
                    <i className="now-ui-icons arrows-1_refresh-69" /> Just
                    Updated
                  </div>
                </CardFooter>
              </Card>
            </Col>

            <Col xs={12} md={{ size: 3 }}>
              <Card className="card-chart card-chart-long text-center">
                <CardHeader>
                  <CardTitle tag="h4">총 인원</CardTitle>
                </CardHeader>
                <CardBody>
                  <h1 className="report_num">
                    {CCTVData[CCTVData.length - 1]['mask'] + CCTVData[CCTVData.length - 1]['nomask'] + CCTVData[CCTVData.length - 1]['incorrectmask']}
                  </h1>
                  <CCTVReportOne data={CCTVData[CCTVData.length - 1]['mask'] + CCTVData[CCTVData.length - 1]['nomask'] + CCTVData[CCTVData.length - 1]['incorrectmask']}
                   palette="red"></CCTVReportOne>
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
                    <CCTVReport data={CCTVData.slice(CCTVData.length-11,CCTVData.length)} palette={palette} />
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
                  <h5 className="card-category">CCTV Total</h5>
                  <CardTitle tag="h4">CCTV 모니터링</CardTitle>
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
                  <div className="gallery-area">
                  <ReactstrapImageGallery images={images}/>
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
    </>
  )


}

export default CCTVDashboard;
