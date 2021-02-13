import React, {useEffect, useState} from 'react';
import {Form} from 'react-bootstrap'
import './App.css';
import {RawDataApi, SampleApi} from './api'
import {TrainDataGen} from "./components/train-data-gen";
import {BreakPointList} from "./components/break-point-list";

const configuration = {
    basePath: 'http://localhost:8080'
}

const rawDataApi = new RawDataApi(configuration);
const sampleApi = new SampleApi(configuration);

export const App: React.FC = () => {
    const [state, setState] = useState({
        hiFreq: [] as any[],
        loFreq: [] as any[]
    })

    return (
        <div className="App">
            <BreakPointList
                onChange={(bp) => {
                    setState({
                        hiFreq: [],
                        loFreq: []
                    });
                    Promise.all([
                        rawDataApi.getRawData('5', bp.start / 1000, bp.end / 1000),
                        rawDataApi.getRawData('15', bp.start / 1000, bp.end / 1000)
                    ]).then((result) => {
                        setState({
                            hiFreq: result[0].data!,
                            loFreq: result[1].data!
                        })
                    })
            }} />
            <TrainDataGen hiFreq={state.hiFreq}
                          loFreq={state.loFreq}
                          onSaveSamples={(data) => {
                              sampleApi.setSamples(data)
                          }}/>
        </div>
    );
}
