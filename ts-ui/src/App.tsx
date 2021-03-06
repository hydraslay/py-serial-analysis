import React, {useEffect, useState} from 'react';
import './App.css';
import {MarketBreakPoint, RawDataApi} from './api'
import {TrainDataGen} from "./components/train-data-gen";
import {DataSetList} from "./components/dataset-list";
import {Tab, Tabs} from "react-bootstrap";

const configuration = {
    basePath: 'http://localhost:8080'
}

const rawDataApi = new RawDataApi(configuration);

export const App: React.FC = () => {
    const [state, setState] = useState({
        breakPoints: [] as MarketBreakPoint[]
    })

    useEffect(() => {
        rawDataApi.getMarketBreakPoint().then((result) => {
            setState({
                ...state,
                breakPoints: result!.data!
            })
        })
    }, []);

    return (
        <div className="App">
            <Tabs
                id="controlled-tab-example"
                defaultActiveKey='list'
                transition={false}
            >
                <Tab eventKey="list" title="Data Set">
                    <DataSetList breakPoints={state.breakPoints}></DataSetList>
                </Tab>
                <Tab eventKey="gen" title="Generator">
                    <TrainDataGen breakPoints={state.breakPoints}/>
                </Tab>
            </Tabs>
        </div>

    );
}
