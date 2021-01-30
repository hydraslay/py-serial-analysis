import React, {PureComponent, useState} from 'react';

import {Button, ButtonGroup} from "react-bootstrap";
import {SeriesChart} from "./line-chart";
import {RawDataItem, SampleDataItem} from "../interface";

type TrainDataGenProps = {
    data: {
        hiFreq: RawDataItem[];
        loFreq: RawDataItem[];
    }
}

type SortedStack = number[][];

const threshold = 0.02
const tickSpan = 15

function removeTick(stack: SortedStack, index: number) {
    const i = stack.findIndex((item) => item[0] === index);
    if (i >= 0) {
        stack.splice(i, 1);
    }
}

function addLow(stack: SortedStack, index: number, tick: RawDataItem) {
    const newItem = [index, tick.low];
    if (stack.length > 0) {
        const i = stack.findIndex((item) => tick.low < item[1]);
        if (i >= 0) {
            stack.splice(i, 0, newItem);
            return;
        }
    }
    stack.push(newItem);
}

function getValue(tickHi: RawDataItem, tickLo: RawDataItem, threshold: number) {
    const hiThresh = tickHi.low + threshold;
    const loThresh = tickHi.low - threshold;
    if (tickLo.high <= loThresh) {
        return 1;
    }
    if (tickLo.high <= hiThresh && tickLo.high >= loThresh && tickLo.low <= loThresh) {
        return 2;
    }
    if (tickLo.high >= hiThresh && tickLo.low <= loThresh) {
        return 4;
    }
    if (tickLo.high >= hiThresh && tickLo.low >= loThresh && tickLo.low <= hiThresh) {
        return 5;
    }
    if (tickLo.low >= hiThresh) {
        return 6;
    }
    return 3;
}

function generateSamples(hiFreq: RawDataItem[], loFreq: RawDataItem[]) {
    if (!hiFreq || !hiFreq.length || !loFreq || !loFreq.length) {
        return []
    }

    // equalize index
    let startHi = 0
    while (hiFreq[startHi].timestamp < loFreq[0].timestamp) {
        startHi++;
        if (startHi > hiFreq.length) {
            return []
        }
    }

    const samples: SampleDataItem[] = [];
    const lowStack: SortedStack = [];
    let indicatorLo = 0;
    for (let i = startHi; i < hiFreq.length; i++) {
        const tick = hiFreq[i];
        while (loFreq[indicatorLo].timestamp <= tick.timestamp) {
            indicatorLo++;
        }
        addLow(lowStack, i, tick)
        if (i >= tickSpan) {
            if (lowStack[0][0] == i) {
                const val = getValue(tick, loFreq[indicatorLo], threshold);
                samples.push({
                    hiFreq: hiFreq.slice(i - tickSpan, i + 1),
                    nextLowFreq: loFreq[indicatorLo],
                    actual: val,
                })
            }
            removeTick(lowStack, i - tickSpan);
        }
    }
    return samples.slice(0, 30);
}

export const TrainDataGen: React.FC<TrainDataGenProps> = (props) => {
    return (<div>
        {generateSamples(props.data.hiFreq, props.data.loFreq).map((sampleItem, i) => {
            return <div key={i}
                style={{
                display: 'inline-block',
                border: '1px dotted lightgray',
                //background: sampleItem.proved ? 'white' : 'lightyellow'
            }}>
                <ButtonGroup vertical style={{verticalAlign: 'middle', marginLeft: '10px'}}>
                    <Button variant={sampleItem.actual === 1 ? 'success' : 'outline-success'}>Rise</Button>
                    <Button variant={sampleItem.actual === 2 ? 'danger' : 'outline-danger'}>Drop</Button>
                    <Button variant={sampleItem.actual === 3 ? 'warning' : 'outline-warning'}>Flat</Button>
                </ButtonGroup>
                <SeriesChart data={sampleItem.hiFreq.concat(sampleItem.nextLowFreq)}/>
            </div>
        })}
    </div>)
}