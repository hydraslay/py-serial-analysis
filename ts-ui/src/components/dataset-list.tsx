import {DataSet, MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import {BreakPoint} from "../interface";
import React, {useEffect, useState} from "react";
import {Button, Col, Dropdown, Form, FormCheck, ListGroup} from "react-bootstrap";
import {DataSetEditor} from "./dataset-editor";
import {DelayConfirm} from "../util/delay-confirm";

type DataSetListProps = {
    breakPoints: MarketBreakPoint[];
}

type DataSetListState = {
    dataSets: DataSet[];
    selectedId: string[];
    editing: boolean;
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const sampleApi = new SampleApi(configuration);
const rawDataApi = new RawDataApi(configuration);

export const DataSetList: React.FC<DataSetListProps> = (props) => {
    const [state, setState] = useState({
        dataSets: [],
        selectedId: [],
        editing: false
    } as DataSetListState)

    useEffect(() => {
        const data = sampleApi.getDataSets().then(dataSets => {
            setState({
                dataSets: dataSets.data!,
                selectedId: [],
                editing: false
            })
        })
    }, [])

    return (<Form>
        <Form.Group as={Col} sm={12}>
            <ListGroup>
            {state.dataSets.map((ds, i) =>
                <ListGroup.Item>
                    <FormCheck style={{display: 'inline', marginRight: '10px'}}
                    onChange={(a) => {
                        const newSelectedId = [...state.selectedId]
                        if (a.target.checked) {
                            newSelectedId.splice(0, 0, ds.id!)
                        } else {
                            newSelectedId.splice(newSelectedId.indexOf(ds.id!), 1)
                        }
                        setState({
                            ...state,
                            selectedId: newSelectedId
                        })
                    }}/>
                    {ds!.name}
                </ListGroup.Item>)
            }
            </ListGroup>

        </Form.Group>
        <Form.Group as={Col} sm={12}>
            <Button style={{marginRight: '10px'}}
                    onClick={() => {
                        setState({
                            ...state,
                            editing: true
                        })
                    }}
            >
                ＋
            </Button>
            <DelayConfirm
                disabled={state.selectedId.length === 0}
                text='－' description='delete data set' onConfirm={() => {
                alert('deleted')
            }} />
        </Form.Group>
        { state.editing
            ? <Form.Group as={Col} sm={12}>
                <DataSetEditor breakPoints={props.breakPoints} />
            </Form.Group>
            : null}
    </Form>)
}