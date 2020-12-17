import './App.css';
import React from 'react';
import Login from './login/Login.jsx';
import AdminLayout from "./layouts/Admin.jsx";
import { Router, Route, Switch, Redirect, Link } from "react-router-dom";
import { createBrowserHistory } from "history";
import "bootstrap/dist/css/bootstrap.css";
import * as wijmo from 'wijmo/wijmo';

const key = 'dbsydde@gmail.com,E958494376337666#B0zHnisnOiwmbBJye0ICRiwiI34TQhJWQ7VVQKpmWrg5Y7ZWahx6SUN4drsyaZZ5YiVDTZhDa9kVbm56K6Y7bQZFNJlWeVR4SBhlZjVmbLNVO88maEZmM7l6YVBFVhNUNUtiTpNEWEhEd0lHVpR6QZljdXd4UuFHT9cEWJNlVHRjbxEkd8InTwlXda3WekJHWlZGc9A5ZLhzT9kVVhl6bip5KJVWT48WapFVQx4mQZ3UNLVTcPRkRrkDUrtyL6xkUJhTW7V4MvsWb8gUQh36Z6ZnVu5GcXl7SS9UVlBHdBdVTYJUbHlWSsdlQ7h7d7Q5KW9mYwkWW6YGS74kVl9EavBzUMRlQH34bJ5mS7QXZvU5RWhHTXJUOzNHT6VmWSNHTVd6b7kGU956cYRVTw24VqVVdGh7d7QDaihDMvl4LsVVVCR5RIFnZQVDNvN5NtZmRUl6R6gDdsJFO6U4cNRGWDFEbDlGc9tUcHxmI0IyUiwiIDR4Q9QkNFJjI0ICSiwSN7cTO5ITM9UTM0IicfJye&Qf35VfikEMyIlI0IyQiwiIu3Waz9WZ4hXRgACdlVGaThXZsZEIv5mapdlI0IiTisHL3JSNJ9UUiojIDJCLi86bpNnblRHeFBCIyV6dllmV4J7bwVmUg2Wbql6ViojIOJyes4nILdDOIJiOiMkIsIibvl6cuVGd8VEIgc7bSlGdsVXTg2Wbql6ViojIOJyes4nI4YkNEJiOiMkIsIibvl6cuVGd8VEIgAVQM3EIg2Wbql6ViojIOJyes4nIzMEMCJiOiMkIsISZy36Qg2Wbql6ViojIOJyes4nIVhzNBJiOiMkIsIibvl6cuVGd8VEIgQnchh6QsFWaj9WYulmRg2Wbql6ViojIOJyebpjIkJHUiwiIyEDM4QDMgcTMyEDMyAjMiojI4J7QiwiI6ETMwEjMwIjI0ICc8VkIsISbvNmLslWYtdGQlRGZ9NnYkJiOiEmTDJCLlVnc4pjIsZXRiwiI6YjN7MzM6czM4kDN8UTOiojIklkIs4nIzYHMyAjMiojIyVmdiwSZzxWYmijPy'
const hist = createBrowserHistory();  

class App extends React.Component {
  componentDidMount() {
    wijmo.setLicenseKey(key);
  }
  render() {
    return (
      <div className="App">
      <Router history={hist}>
    <Switch>
      <Route path="/admin" component={AdminLayout} />
      <Redirect to="/admin/gatedashboard" />
    </Switch>
  </Router>
    </div>

    )   
  };
};
export default App;

