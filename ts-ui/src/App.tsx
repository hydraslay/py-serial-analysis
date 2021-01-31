import React, {useEffect, useState} from 'react';
import {Form} from 'react-bootstrap'
import './App.css';
import {RawDataApi} from './api'
import {TrainDataGen} from "./components/train-data-gen";
import {BreakPointList} from "./components/break-point-list";

const rawDataApi = new RawDataApi({
    basePath: 'http://localhost:8080'
});

export const App: React.FC = () => {
    const [state, setState] = useState({
        hiFreq: [] as any[],
        loFreq: [] as any[]
    })

    return (
        <div className="App">
            <BreakPointList
                onChange={(bp) => {
                    Promise.all([
                        rawDataApi.getRawData('1', bp.start, bp.end),
                        rawDataApi.getRawData('5', bp.start, bp.end)
                    ]).then((result) => {
                        setState({
                            hiFreq: result[0],
                            loFreq: result[1]
                        })
                    })
            }} />
            <TrainDataGen data={{hiFreq: state.hiFreq, loFreq: state.loFreq}}/>
        </div>
    );
}
