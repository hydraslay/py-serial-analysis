import React, {useEffect, useState} from 'react';
import './App.css';
import {MarketBreakPoint, RawDataApi} from './api'
import {TrainDataGen} from "./components/train-data-gen";
import {DataSetList} from "./components/dataset-list";

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
            <TrainDataGen breakPoints={state.breakPoints}/>
            <DataSetList breakPoints={state.breakPoints}></DataSetList>
        </div>
    );
}
