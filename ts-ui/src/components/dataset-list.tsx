import {DataSet, MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import React, {useEffect, useState} from "react";
import {Button, Col, Form, FormCheck, ListGroup} from "react-bootstrap";
import {DataSetEditor} from "./dataset-editor";
import {DelayConfirm} from "../util/delay-confirm";

type DataSetListProps = {
    breakPoints: MarketBreakPoint[];
}

type DataSetListState = {
    dataSets: DataSet[];
    selectedId: number[];
    editing: DataSet | null;
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

    const refreshDataSets = () => {
        const data = sampleApi.getDataSets().then(dataSets => {
            setState({
                dataSets: dataSets.data!,
                selectedId: [],
                editing: null
            })
        })
    }

    useEffect(() => {
        refreshDataSets()
    }, [])

    return (<Form>
        <Form.Group as={Col} sm={12}>
            <ListGroup>
                {state.dataSets.map((ds, i) =>
                    <ListGroup.Item style={{textAlign: 'left'}}>
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
                        <Form.Text style={{display: 'inline', marginRight: '10px'}}>{ds!.name}</Form.Text>
                        <Form.Text style={{display: 'inline', marginRight: '10px'}}>{ds!.uidFrom}</Form.Text>
                        <Form.Text style={{display: 'inline', marginRight: '10px'}}>---</Form.Text>
                        <Form.Text style={{display: 'inline', marginRight: '10px'}}>{ds!.uidTo}</Form.Text>
                        <Button
                            onClick={() => {
                                setState({
                                    ...state,
                                    editing: ds
                                })
                            }}
                            variant='outline-primary'
                        ><i className='fa fa-edit'/></Button>
                    </ListGroup.Item>)
                }
            </ListGroup>

        </Form.Group>
        <Form.Group as={Col} sm={12}>
            <Button style={{marginRight: '10px'}}
                    onClick={() => {
                        setState({
                            ...state,
                            editing: {}
                        })
                    }}
            >
                ＋
            </Button>
            <DelayConfirm
                disabled={state.selectedId.length === 0}
                text='－'
                description='delete selected data set'
                onConfirm={() => {
                    alert('deleted')
                }}
            />
        </Form.Group>
        {state.editing
            ? <Form.Group as={Col} sm={12}>
                <DataSetEditor breakPoints={props.breakPoints}
                               onSave={d => {
                                   sampleApi.setDataSet(d).then(() => {
                                       refreshDataSets()
                                   })
                               }}
                               editing={state.editing}
                               onCancel={() => {
                                   setState({
                                       ...state,
                                       editing: null
                                   })
                               }}
                />
            </Form.Group>
            : null
        }
    </Form>)
}