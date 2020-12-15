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
// import '../index.css';

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




const ChartPanel = ({ title, children }) => { 
  return (
    <div className="col-lg-4 col-md-6 col-sm-12 mt-1">
      <div className="card-header">
        <h5 class="card-category">Global Sales</h5>
        <h4 class="card-title">통계</h4>
      </div>
      <div className="card dashboardPanel">
        <div className="card-body">
          <h5 className="card-title">{title}</h5>
          {children}
        </div>
      </div>
    </div>
  );
}
  
const DataPanel = ({ title, children }) => {
  return (
    <div className="col-sm-12">
      <div className="card dashboardRow">
        <div className="card-body">
          <h5 className="card-title">{title}</h5>
          {children}
        </div>
      </div>
    </div>
  )
}
  
const Gauge = ({ data }) => {
  return (
    // <ChartPanel title="총 방문자 수">
      <div className="gauge">
        <RadialGauge
          min={0} max={3000}
          step={50} isReadOnly={true}
          thickness={0.15}
          value={data}
        />
      </div>
    // </ChartPanel>
  );
}
  
const SalesChart = ({ salesData }) => {
  return (
    // <ChartPanel title="게이트 통과 여부">
    <div className="chart">
      <FlexChart itemsSource={salesData}
        bindingX="ispass"
        style={{ height: "250px" }}
        palette={['rgba(169,49,222, 1)']}>
        <FlexChartSeries name="count" binding="count" />
      </FlexChart>
      </div>
    // </ChartPanel>
  );
}
  
const SalesPie = ({ salesData }) => {
  return (
    // <ChartPanel title="시간대별 방문자 수">
    <div class="pie">
      <FlexPie itemsSource={salesData}
        binding="count"
        bindingName="time"
        innerRadius={0.70}
        style={{ height: "250px" }} 
                palette={['rgba(255,91,82, 1)', 'rgba(82,146,255, 1)', 'rgba(255,203,83, 1)', 'rgba(47,219,159, 1)']} />
    </div>
    // </ChartPanel>
  );
}
  
const TransactionList = ({ transactions }) => {
  return (
    // <DataPanel title="방문 기록">
    <div class="transaction">
      <FlexGrid style={{ width: "100%" }}
        itemsSource={transactions}>
        <FlexGridColumn header="통과 여부" binding="ispass" width="1*" />
        <FlexGridColumn header="체온" binding="temperature" width="1*" />
        <FlexGridColumn header="방문 시각" binding="visited" width="2*" />
      </FlexGrid>
      <div class="page">
      <CollectionViewNavigator headerFormat="Page {currentPage:n0} of {pageCount:n0}" byPage={true} cv={transactions}/>
      </div>
      </div>
    // </DataPanel>
  );
}

  const GateDashboard = () => {
    const [ gateData, setGateData ] = useState([]);
    const [ ispassData, setIsPassData ] = useState([
      {"count": 0},
      {"count": 0}]);
    const [ visitedCount, setVisitedCount ] = useState([]);

    useEffect(() => {
      _getDB();
      _getIsPass();
      _getvisitedCount();
    }, []);

    const dataEndpoint =
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/data";
    const ispassEndpoint = 
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/ispass";
    const visitedEndpoint = 
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/visitedcount";


    const _getDB = async () => {
      let data = [];
      await axios.get(dataEndpoint).then((res) => {
          // setGateData(res.data);
          console.log(res.data);
          data = res.data;
      });
      setGateData(new CollectionView(data, {
        pageSize: 10,
      }));
    //   return new CollectionView(data, {
    //     pageSize: 6,
    // });
    };

    const _getIsPass = async () => {
      await axios.get(ispassEndpoint).then((res) => {
        setIsPassData(res.data)
        console.log(res.data);
      })
    }

    const _getvisitedCount = async () => {
      await axios.get(visitedEndpoint).then((res) => {
        setVisitedCount(res.data)
        console.log("visited : " + res.data);
      })
    }

    const calculateSales = () => {
      let totalSales = 0;
      // console.log("맞잖아!!!!!!!!!!" + ispassData[0]['count']);
      totalSales = ispassData[0]['count'] + ispassData[1]['count']
      return totalSales;
    }

    return (
      <>
          <div>
            <div className="content">

            <Row>
            <Col xs={12} md={4}>
              <Card className="card-chart">
                <CardHeader>  
                  <h5 className="card-category">Gate Total</h5>
                  <CardTitle tag="h4">총 방문자 수</CardTitle>
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
                  <Gauge data={calculateSales()} />
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
            <Col xs={12} md={4}>
              <Card className="card-chart">
                <CardHeader>
                  <h5 className="card-category">Gate Total</h5>
                  <CardTitle tag="h4">게이트 통과 여부</CardTitle>
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
                  <SalesChart salesData={ispassData } />
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
            <Col xs={12} md={4}>
              <Card className="card-chart">
                <CardHeader>
                  <h5 className="card-category">Gate Total</h5>
                  <CardTitle tag="h4">시간대별 방문자 수</CardTitle>
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
                  <SalesPie salesData={visitedCount} />
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
                  <TransactionList transactions={gateData} />
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

export default GateDashboard;
