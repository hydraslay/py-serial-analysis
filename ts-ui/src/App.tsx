import React, {PureComponent, useEffect, useState} from 'react';
import {ButtonGroup, Button, Form} from 'react-bootstrap'
import './App.css';
import {SeriesChart} from "./components/line-chart";
import {RawDataApi} from './api'
import {TrainDataGen} from "./components/train-data-gen";

const rawDataApi = new RawDataApi({
    basePath: 'http://localhost:8080'
});

export const App: React.FC = () => {
    const [state, setState] = useState({
        hiFreq: [] as any[],
        loFreq: [] as any[]
    })

    useEffect(() => {
        Promise.all([
            rawDataApi.getRawData('1'),
            rawDataApi.getRawData('5')
        ]).then((result) => {
            setState({
                hiFreq: result[0],
                loFreq: result[1]
            })
        })
    }, []);

    return (
        <div className="App">
            <div style={{marginBottom: '50px'}}>
                <Form.Check
                    custom
                    inline
                    label="All"
                    type='checkbox'
                    id='list-all-check'
                />
                <Form.Check
                    custom
                    inline
                    label="Proved"
                    type='checkbox'
                    id='list-proved-check'
                />
                <Form.Check
                    custom
                    inline
                    label="Unproved"
                    type='checkbox'
                    id='list-unproved-check'
                />
            </div>
            <TrainDataGen data={{hiFreq: state.hiFreq, loFreq: state.loFreq}}></TrainDataGen>
        </div>
    );
}
