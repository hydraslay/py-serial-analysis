import React, {PureComponent} from 'react';
import {CartesianGrid, Legend, Line, LineChart, ReferenceLine, Tooltip, XAxis, YAxis,} from 'recharts';
import {RawDataItem} from "../interface";

type SeriesChartProp = {
    data: RawDataItem[]
}

export class SeriesChart extends PureComponent<SeriesChartProp> {
    render() {
        let minY = 999, maxY = 0, minX = '0', maxX = '0'
        return (
            <LineChart
                width={400}
                height={200}
                data={this.props.data.map((item, i) => {
                    minY = item.low < minY ? item.low : minY
                    maxY = item.high > maxY ? item.high : maxY
                    const dt = new Date(item.timestamp * 1000);
                    const time = dt.getHours() + ':' + (dt.getMinutes() >= 10 ? dt.getMinutes() : '0' + dt.getMinutes())
                    if (i === 0) {
                        minX = time
                    }
                    maxX = time
                    return {
                        ...item,
                        time
                    }
                })}
                margin={{
                    top: 20, right: 10, left: 10, bottom: 5,
                }}
                style={{display: 'inline-block'}}
            >
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis xAxisId="hi" dataKey="time" scale={'auto'} domain={[minX, maxX]}/>
                <YAxis yAxisId="left" scale="auto" domain={[minY, maxY]} />
                {/*<YAxis yAxisId="right" orientation="right" scale="auto"/>*/}
                <Tooltip/>
                {/*<Legend/>*/}
                {/*{*/}
                {/*    this.props.data && this.props.data.length*/}
                {/*        ? <ReferenceLine xAxisId="hi" x={this.props.data[this.props.data.length - 2].timestamp} stroke="gray"/>*/}
                {/*        : null*/}
                {/*}*/}
                {/*<ReferenceLine y={1890} stroke="red"/>*/}
                <Line type="monotone" xAxisId="hi" yAxisId="left" dataKey="high" stroke="#b83418"/>
                <Line type="monotone" xAxisId="hi" yAxisId="left" dataKey="low" stroke="#36aa09"/>
                {/*<Line type="monotone" yAxisId="right" dataKey="volume" stroke="#82ca9d"/>*/}
            </LineChart>
        );
    }
}
