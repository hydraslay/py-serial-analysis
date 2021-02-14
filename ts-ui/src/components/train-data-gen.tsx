import React, {useState} from 'react';

import {Button, Col, Form, ProgressBar} from "react-bootstrap";
import {BreakPoint, RawDataItem, SampleDataItem, toSampleArray} from "../interface";
import {generateSamples} from "../algorithm/sample-gen";
import {MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import {SampleList} from "./sample-list";
import {BreakPointList} from "./break-point-list";

type TrainDataGenProps = {
    breakPoints: MarketBreakPoint[];
}

type TrainDataGenState = {
    selectedBP: BreakPoint | undefined;
    samples: SampleDataItem[];
    progress: number;
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const sampleApi = new SampleApi(configuration);
const rawDataApi = new RawDataApi(configuration);

export const TrainDataGen: React.FC<TrainDataGenProps> = (props) => {
    const [state, setState] = useState({
        selectedBP: undefined,
        samples: [],
        progress: -1
    } as TrainDataGenState)

    return (<Form>
        <Form.Group as={Col} sm={12}>
            <BreakPointList placeHolder='select time span'
                            data={props.breakPoints.map((bp) => bp.timestamp!)}
                            selectedLabel={state.selectedBP ? state.selectedBP.label : ''}
                            onChange={(bp) => {
                                setState({
                                    ...state,
                                    selectedBP: bp,
                                    samples: [],
                                    progress: -1
                                })
                            }}/>
        </Form.Group>
        <Form.Group as={Col} sm={12} style={{textAlign: 'left'}}>
            <Button variant='primary'
                    style={{marginRight: '10px'}}
                    disabled={!state.selectedBP}
                    onClick={() => {
                        if (!state.selectedBP) {
                            return;
                        }
                        setState({
                            ...state,
                            progress: 0
                        })
                        Promise.all([
                            rawDataApi.getRawData('5', state.selectedBP.start / 1000, state.selectedBP.end / 1000),
                            rawDataApi.getRawData('15', state.selectedBP.start / 1000, state.selectedBP.end / 1000)
                        ]).then((result) => {
                            setState({
                                ...state,
                                progress: 50
                            })
                            setTimeout(() => {
                                const all = generateSamples(result[0].data as RawDataItem[], result[1].data as RawDataItem[]);
                                setState({
                                    ...state,
                                    samples: all,
                                    progress: 100
                                })
                            }, 100)
                        })
                    }}>Generate Samples</Button>
            <Button variant='primary'
                    disabled={!state.samples.length}
                    onClick={() => {
                        setState({
                            ...state,
                            progress: 10
                        })
                        sampleApi.setSamples(toSampleArray(state.samples)).then(() => {
                            setState({
                                ...state,
                                progress: 100
                            })
                        })
                    }}>Save Samples</Button>
        </Form.Group>
        <Form.Group as={Col} sm={12}>
            {state.progress >= 0
                ? <ProgressBar max={100} now={state.progress} style={{height: '5px'}}/>
                : null}
        </Form.Group>
        <Form.Group as={Col} sm={12}>
            <SampleList data={toSampleArray(state.samples)}/>
        </Form.Group>
    </Form>)
}