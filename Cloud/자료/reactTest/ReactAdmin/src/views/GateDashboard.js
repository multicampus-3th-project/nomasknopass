import React, { Component } from 'react';
import axios from "axios";

// Wijmo imports
import 'wijmo/styles/wijmo.css';
import { FlexGrid, FlexGridColumn } from 'wijmo/wijmo.react.grid';
import { FlexChart, FlexPie, FlexChartSeries } from 'wijmo/wijmo.react.chart';
import { RadialGauge } from 'wijmo/wijmo.react.gauge';

// Data imports
import { recentSales, salesByCountry, salesByPerson } from '../data/data';

// css
import '../assets/css/now-ui-dashboard.css';



const ChartPanel = ({ title, children }) => { 
    return (
      <div className="col-lg-4 col-md-6 col-sm-12 mt-1">
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
      <ChartPanel title="총 방문자 수">
        <div className="gauge">
          <RadialGauge
            min={0} max={500000}
            step={50} isReadOnly={true}
            thickness={0.15}
            value={data}
          />
        </div>
      </ChartPanel>
    );
  }
  
  const SalesChart = ({ salesData }) => {
    return (
      <ChartPanel title="게이트 통과 여부">
        <FlexChart itemsSource={salesData}
          bindingX="ispass"
          style={{ height: "290px" }}
          palette={['rgba(171,125,246, 1)']}>
          <FlexChartSeries name="count" binding="count" />
        </FlexChart>
      </ChartPanel>
    );
  }
  
  const SalesPie = ({ salesData }) => {
    return (
      <ChartPanel title="시간대별 방문자 수">
        <FlexPie itemsSource={salesData}
          binding="sales"
          bindingName="name"
          innerRadius={0.70}
          style={{ height: "290px" }} 
                  palette={['rgba( 171,125,246, 1)', 'rgba( 38, 193, 201, 1)', 'rgba( 129,201, 38, 1)', 'rgba( 250, 202, 0, 1)']} />
      </ChartPanel>
    );
  }
  
  const TransactionList = ({ transactions }) => {
    return (
      <DataPanel title="방문 기록">
        <FlexGrid style={{ width: "100%" }}
          itemsSource={transactions}>
          <FlexGridColumn header="통과 여부" binding="ispass" width="2*" />
          <FlexGridColumn header="방문 시각" binding="visited" width="3*" />
          <FlexGridColumn header="체온" binding="temperature" width="1*" />
        </FlexGrid>
      </DataPanel>
    );
  }

  class GateDashboard extends React.Component {
          
    dataEndpoint =
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/data";
    ispassEndpoint = 
    "https://o43ghtnv70.execute-api.ap-northeast-2.amazonaws.com/dev/ispass";
    
    constructor() {
        super();
        this.state = {
          recentSales: recentSales,
          salesByCountry: salesByCountry,
          salesByPerson: salesByPerson,
          gateData: [],
          ispassData: []
        };
      }

      componentWillMount() {
        this._getDB();
        this._getIsPass();
      }

      _getDB = async () => {
        await axios.get(this.dataEndpoint).then((res) => {
            const gateData = res.data;
            this.setState({ gateData });
            console.log(res.data);
        });
      };

      _getIsPass = async () => {
        await axios.get(this.ispassEndpoint).then((res) => {
          const ispassData = res.data;
          this.setState({ ispassData });
          console.log(res.data);
        })
      }
    
      calculateSales() {
        let totalSales = 0;
        console.log("맞잖아!!!!!!!!!!" + this.state.ispassData[0]);
        // totalSales = this.state.ispassData[0]['count'] + this.state.ispassData[1]['count]']
        return totalSales;
      }
    
      render() {
        return (
          <>
          <div>
            <div className="content">
              <div className="row">
                <Gauge data={this.calculateSales()} />
                <SalesChart salesData={this.state.ispassData } />
                <SalesPie salesData={this.state.salesByPerson} />
              </div>
              <div className="row">
                <TransactionList transactions={this.state.gateData} />
              </div>
            </div>
            </div>
          </>
            );
      }
    };
export default GateDashboard;
