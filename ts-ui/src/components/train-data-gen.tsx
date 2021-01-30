import React from 'react';

import {Nav, Row, Tab} from "react-bootstrap";
import {SeriesChart} from "./line-chart";
import {RawDataItem, SampleDataItem} from "../interface";
import {generateSamples} from "../algorithm/sample-gen";

type TrainDataGenProps = {
    data: {
        hiFreq: RawDataItem[];
        loFreq: RawDataItem[];
    }
}

export const TrainDataGen: React.FC<TrainDataGenProps> = (props) => {
    const all = generateSamples(props.data.hiFreq, props.data.loFreq);
    const grouped = all.reduce((grp: { [val: number]: SampleDataItem[] }, item) => {
        grp[item.actual] = grp[item.actual] || [];
        grp[item.actual].push(item);
        return grp;
    }, {})
    return (<div>
        <Tab.Container
            defaultActiveKey={"g-" + (grouped && Object.keys(grouped).length > 0 ? Object.keys(grouped)[0] : '')}
            id="tab-sample-charts"
            transition={false}
        >
            <Row>
                <Nav variant="tabs">
                    {Object.keys(grouped).map((g: string) =>
                        <Nav.Item key={"g-" + g}>
                            <Nav.Link eventKey={"g-" + g}>
                                <img src={`./${g}.png`} style={{marginRight: '5px'}} alt={g}/>
                                {'value=' + g}
                                <br/>
                                {'count=' + grouped[parseInt(g)].length}
                            </Nav.Link>
                        </Nav.Item>)}
                </Nav>
            </Row>
            <Row>
                <Tab.Content>
                    {Object.keys(grouped).map((g: string) =>
                        <Tab.Pane key={"g-" + g} eventKey={"g-" + g}>
                            {grouped[parseInt(g)].slice(0, 20).map((sampleItem, i) =>
                                (<div key={"g-" + g + "-" + i}
                                      style={{
                                          display: 'inline-block',
                                          border: '1px dotted lightgray',
                                          //background: sampleItem.proved ? 'white' : 'lightyellow'
                                      }}>
                                    <SeriesChart data={sampleItem.hiFreq.concat(sampleItem.nextLowFreq)}/>
                                </div>))
                            }
                        </Tab.Pane>)}
                </Tab.Content>
            </Row>
        </Tab.Container>
        {/*<ButtonGroup vertical style={{verticalAlign: 'middle', marginLeft: '10px'}}>*/}
        {/*    <Button variant={sampleItem.actual === 1 ? 'success' : 'outline-success'}>Rise</Button>*/}
        {/*    <Button variant={sampleItem.actual === 2 ? 'danger' : 'outline-danger'}>Drop</Button>*/}
        {/*    <Button variant={sampleItem.actual === 3 ? 'warning' : 'outline-warning'}>Flat</Button>*/}
        {/*</ButtonGroup>*/}
    </div>)
}