import {toRawDataItemArray} from "../interface";
import {Samples} from "../api";
import React from "react";
import {Nav, Row, Tab} from "react-bootstrap";
import {SeriesChart} from "./line-chart";

type SampleListProps = {
    data: Samples[];
}

export const SampleList: React.FC<SampleListProps> = (props) => {
    const grouped = props.data.reduce((grp: { [val: number]: Samples[] }, item) => {
        grp[item.value!] = grp[item.value!] || [];
        grp[item.value!].push(item);
        return grp;
    }, {})

    return <Tab.Container
        defaultActiveKey={"g-" + (grouped && Object.keys(grouped).length > 0 ? Object.keys(grouped)[0] : '')}
        id="tab-sample-charts"
        transition={false}
    >
        <Row>
            <Nav variant="tabs">
                {Object.keys(grouped).map((g: string) =>
                    <Nav.Item key={"g-" + g}>
                        <Nav.Link eventKey={"g-" + g}>
                            {'val=' + g}
                            <br/>
                            {'cnt=' + grouped[parseInt(g)].length}
                        </Nav.Link>
                    </Nav.Item>)}
            </Nav>
        </Row>
        <Row>
            <Tab.Content>
                {Object.keys(grouped).map((g: string) =>
                    <Tab.Pane key={"g-" + g} eventKey={"g-" + g}>
                        {grouped[parseInt(g)].slice(0, 10).map((sampleItem, i) =>
                            (<div key={"g-" + g + "-" + i}
                                  style={{
                                      display: 'inline-block',
                                      border: '1px dotted lightgray',
                                      //background: sampleItem.proved ? 'white' : 'lightyellow'
                                  }}>
                                <SeriesChart data={toRawDataItemArray(sampleItem)}/>
                            </div>))
                        }
                    </Tab.Pane>)}
            </Tab.Content>
        </Row>
    </Tab.Container>
}