import {DataSet, MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import {BreakPoint} from "../interface";
import React, {useEffect, useState} from "react";
import {Col, Dropdown, Form, ListGroup} from "react-bootstrap";

type DataSetListProps = {
    breakPoints: MarketBreakPoint[];
}

type DataSetListState = {
    dataSets: DataSet[];
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const sampleApi = new SampleApi(configuration);
const rawDataApi = new RawDataApi(configuration);

export const DataSetList: React.FC<DataSetListProps> = (props) => {
    const [state, setState] = useState({
        dataSets: []
    } as DataSetListState)

    useEffect(() => {
        const data = sampleApi.getDataSets().then(dataSets => {
            setState({
                dataSets: dataSets.data!
            })
        })
    }, [])

    return (<Form>
        <Form.Group as={Col} sm={12}>
            <ListGroup>
            {state.dataSets.map((ds, i) =>
                <ListGroup.Item>
                    {ds!.name}
                </ListGroup.Item>)
            }
            </ListGroup>
        </Form.Group>
    </Form>)
}