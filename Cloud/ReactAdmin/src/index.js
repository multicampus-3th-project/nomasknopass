import React, { Component } from 'react';
import { render } from 'react-dom';
import NavBar from './components/NavBar';

// Wijmo imports
import 'wijmo/styles/wijmo.css';
import { FlexGrid, FlexGridColumn } from 'wijmo/wijmo.react.grid';
import { FlexChart, FlexPie, FlexChartSeries } from 'wijmo/wijmo.react.chart';
import { RadialGauge } from 'wijmo/wijmo.react.gauge';

import './App.css';

// Data imports
import { recentSales, salesByCountry, salesByPerson } from './data/data';
  
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
    <ChartPanel title="Today's Sales ($)">
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
    <ChartPanel title="Sales By Country">
      <FlexChart itemsSource={salesData}
        bindingX="country"
        style={{ height: "290px" }}
        palette={['rgba(171,125,246, 1)']}>
        <FlexChartSeries name="Sales" binding="sales" />
      </FlexChart>
    </ChartPanel>
  );
}

const SalesPie = ({ salesData }) => {
  return (
    <ChartPanel title="Sales by Salesperson">
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
    <DataPanel title="Recent Transactions">
      <FlexGrid style={{ width: "100%" }}
        itemsSource={transactions}>
        <FlexGridColumn header="Client Name" binding="client" width="2*" />
        <FlexGridColumn header="Description" binding="description" width="3*" />
        <FlexGridColumn header="Total ($)" binding="value" width="1*" />
        <FlexGridColumn header="Quantity" binding="itemCount" width="1*" />
      </FlexGrid>
    </DataPanel>
  );
}

class App extends Component {
  constructor() {
    super();
    this.state = {
      recentSales: recentSales,
      salesByCountry: salesByCountry,
      salesByPerson: salesByPerson
    };
  }

  calculateSales() {
    let totalSales = 0;
    this.state.recentSales.forEach(sale => totalSales += sale.value);
    return totalSales;
  }

  render() {
    return (
      <>
        <NavBar title="Sales Dashboard" />
        <div className="container">
          <div className="row">
            <Gauge data={this.calculateSales()} />
            <SalesChart salesData={this.state.salesByCountry} />
            <SalesPie salesData={this.state.salesByPerson} />
          </div>
          <div className="row">
            <TransactionList transactions={this.state.recentSales} />
          </div>
        </div>
      </>
    );
  }
}

render(<App />, document.getElementById('root'));
