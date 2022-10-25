import React, {Component} from "react";
import {render} from "react-dom";

import { Button } from "@mui/material";

import Signup from './components/Login/Signup';
import { Routes, Route } from 'react-router-dom';

export default class App extends Component {

    constructor(props) {
        super(props);
    }
    render(){
        return (
        <Routes>
            <Route path="/signup" element={<Signup />} />
        </Routes>
        )
    }
}

const appDiv = document.getElementById('app');
render(<App />, appDiv);