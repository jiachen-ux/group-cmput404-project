import React, {Component} from "react";
import {render} from "react-dom";

import { Button } from "@mui/material";

export default class App extends Component {
    constructor(props) {
        super(props);
    }
    render(){
        return (
        <><h1>If you see this, the React is working</h1>
        <Button variant="contained">Contained</Button></>
        )
    }
}

const appDiv = document.getElementById('app');
render(<App />, appDiv);