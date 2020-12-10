import React from 'react';
import axios from "axios";

class Home extends React.Component {
    state = {
        response: null
    };

    componentDidMount() {
        this._apiTest();
    }

    apiEndPoint = "https://qzs1jeah5l.execute-api.ap-northeast-2.amazonaws.com/test/dev";
    
    _apiTest = async () => {
        console.log("뭐했나요?")
        await axios.get(this.apiEndPoint).then((res) => {
            const response = res.data;
            this.setState({response});
            console.log("나왔나요?"+response);
        })
    }
  
    render() {
  
        return (
            <div>

            </div>
        )
    }
}
export default Home;