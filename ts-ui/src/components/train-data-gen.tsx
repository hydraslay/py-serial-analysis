import React, {useState} from 'react';

import {Button, Col, Form, ListGroup, ProgressBar} from "react-bootstrap";
import {BreakPoint, RawDataItem, SampleDataItem, toSampleArray} from "../interface";
import {generateSamples} from "../algorithm/sample-gen";
import {MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import {SampleList} from "./sample-list";
import moment from "moment";

type TrainDataGenProps = {
    breakPoints: MarketBreakPoint[];
}

type TrainDataGenState = {
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
        samples: [],
        progress: -1
    } as TrainDataGenState)

    const generateUpload = async (bp: BreakPoint) => {
        setState({
            samples: [],
            progress: 0
        })
        const result = await Promise.all([
            rawDataApi.getRawData('5', bp.start / 1000, bp.end / 1000),
            rawDataApi.getRawData('15', bp.start / 1000, bp.end / 1000)
        ])
        setState({
            samples: [],
            progress: 30
        })
        const all = generateSamples(result[0].data as RawDataItem[], result[1].data as RawDataItem[]);
        setState({
            ...state,
            samples: all,
            progress: 70
        })
        await sampleApi.setSamples(toSampleArray(state.samples))
        setState({
            samples: all,
            progress: 100
        })
    }

    const renderList = () => {
        let start: string = '';
        const breakPoints = props.breakPoints.reduce((arr: BreakPoint[], item) => {
            const curr = item.timestamp!;
            if (start) {
                if (!moment(start, "YYYY-MM-DD").add(1, 'days').isSame(curr)) {
                    arr.push({
                        label: `${start} ~ ${item.timestamp}`,
                        start: new Date(start).valueOf(),
                        end: new Date(curr).valueOf()
                    })
                }
            }
            start = curr;
            return arr;
        }, [])

        return <div
            style={{
                overflowY: "scroll",
                height: '500px',
                border: '1px solid lightgray',
                borderRadius: '5px',
            }}
        >
            <ListGroup>
                {breakPoints.map((bp, i) => {
                    return <ListGroup.Item style={{textAlign: 'left'}}>
                        <Form.Text style={{display: 'inline'}}>
                            {bp.label}
                        </Form.Text>
                        <Button variant='primary'
                                style={{
                                    marginLeft: '10px',
                                    marginRight: '10px'
                                }}
                                onClick={() => {
                                    generateUpload(bp).then(r => {})
                                }}
                        ><i className="fas fa-microchip"></i></Button>
                    </ListGroup.Item>
                })}
            </ListGroup>
        </div>
    }

    return (<div style={{border: '1px solid lightgray', borderRadius: '5px', margin: '5px', padding: '5px'}}>
            <Form>
                <Form.Group as={Col} sm={12}>
                    {renderList()}
                </Form.Group>
                <Form.Group as={Col} sm={12}>
                    {state.progress >= 0
                        ? <ProgressBar max={100} now={state.progress} style={{height: '5px'}}/>
                        : null}
                </Form.Group>
                <Form.Group as={Col} sm={12}>
                    <SampleList data={toSampleArray(state.samples)}/>
                </Form.Group>
            </Form>
        </div>
    )
}