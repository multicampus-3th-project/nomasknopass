import './App.css';
import React from 'react';
// import { Route, Link } from 'react-router-dom';
import Home from './components/Home';
import axios from "axios";


class App extends React.Component {
  

  componentDidMount() {
    this._apiTest();
  }

  apiEndPoint = "https://qzs1jeah5l.execute-api.ap-northeast-2.amazonaws.com/test/dev";

  _apiTest = async () => {
    await axios.get(this.apiEndPoint).then((res) => {
      const response = res.data['aaa'];
      console.log("테스트" + response);
    })
  }

  render() {

    return (
      <div>
      </div>
    )
  };
};


export default App;
