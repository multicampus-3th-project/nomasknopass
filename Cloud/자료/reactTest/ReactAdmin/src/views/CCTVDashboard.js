import React, { Component } from 'react';

// Wijmo imports
import 'wijmo/styles/wijmo.css';
import { FlexGrid, FlexGridColumn } from 'wijmo/wijmo.react.grid';
import { FlexChart, FlexPie, FlexChartSeries } from 'wijmo/wijmo.react.chart';
import { RadialGauge } from 'wijmo/wijmo.react.gauge';

// Data imports
import { recentSales, salesByCountry, salesByPerson } from '../data/data';



  class GateDashboard extends React.Component {
    constructor() {
        super();
        this.state = {
          recentSales: recentSales,
          salesByCountry: salesByCountry,
          salesByPerson: salesByPerson
        };
      }
    
      
    
      render() {
        return (
          <>
         
          </>
            );
      }
    };
export default GateDashboard;
