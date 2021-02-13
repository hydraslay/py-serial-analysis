import React from 'react';

import {Button} from "react-bootstrap";
import {RawDataItem, toSampleArray} from "../interface";
import {generateSamples} from "../algorithm/sample-gen";
import {Samples} from "../api";
import {SampleList} from "./sample-list";

type TrainDataGenProps = {
    hiFreq: RawDataItem[];
    loFreq: RawDataItem[];
    onSaveSamples: (data: Array<Samples>) => void;
}

export const TrainDataGen: React.FC<TrainDataGenProps> = (props) => {
    const all = generateSamples(props.hiFreq, props.loFreq);

    return (<div>
        <div>
            <Button variant='primary'
                    onClick={() => {
                        props.onSaveSamples(toSampleArray(all))
                    }}>Generate Samples</Button>
            <Button variant='primary'
                    onClick={() => {
                        props.onSaveSamples(toSampleArray(all))
                    }}>Save Samples</Button>
        </div>
        <SampleList data={toSampleArray(all)}/>
    </div>)
}