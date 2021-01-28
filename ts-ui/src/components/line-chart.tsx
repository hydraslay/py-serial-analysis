import React, {PureComponent} from 'react';
import {CartesianGrid, Legend, Line, LineChart, ReferenceLine, Tooltip, XAxis, YAxis,} from 'recharts';

type SeriesChartProp = {
    data: {
        timestamp: number;
        open: number;
        high: number;
        low: number;
        close: number;
        volume: number;
    }[]
}

export class SeriesChart extends PureComponent<SeriesChartProp> {
    render() {
        let min = 999
        let max = 0
        return (
            <LineChart
                width={400}
                height={200}
                data={this.props.data.map((item) => {
                    min = item.close < min ? item.close : min
                    max = item.close > max ? item.close : max
                    return {
                        timestamp: item.timestamp,
                        close: item.close
                    }
                })}
                margin={{
                    top: 20, right: 10, left: 10, bottom: 5,
                }}
                style={{display: 'inline-block'}}
            >
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="timestamp"/>
                <YAxis yAxisId="left" scale="auto" domain={[min, max]} />
                {/*<YAxis yAxisId="right" orientation="right" scale="auto"/>*/}
                <Tooltip/>
                <Legend/>
                {/*<ReferenceLine x="4" stroke="gray"/>*/}
                {/*<ReferenceLine y={1890} stroke="red"/>*/}
                <Line type="monotone" yAxisId="left" dataKey="close" stroke="#8884d8"/>
                {/*<Line type="monotone" yAxisId="right" dataKey="volume" stroke="#82ca9d"/>*/}
            </LineChart>
        );
    }
}
