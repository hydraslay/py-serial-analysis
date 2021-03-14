import {DataSet, FitApi, MarketBreakPoint, SampleApi} from "../api";
import React, {useEffect, useState} from "react";
import {Button, Col, Form, FormCheck, ListGroup, Toast} from "react-bootstrap";
import {DataSetEditor} from "./dataset-editor";
import {DelayConfirm} from "../util/delay-confirm";
import {secondsToDays, tsToDateStr} from "../interface";

type DataSetListProps = {
    breakPoints: MarketBreakPoint[];
}

type DataSetListState = {
    dataSets: DataSet[];
    selectedId: number[];
    editing: DataSet | null;
    showToast: boolean;
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const sampleApi = new SampleApi(configuration);
const fitApi = new FitApi(configuration);

export const DataSetList: React.FC<DataSetListProps> = (props) => {
    const [state, setState] = useState({
        dataSets: [],
        selectedId: [],
        editing: false,
        showToast: false
    } as DataSetListState)

    const refreshDataSets = () => {
        sampleApi.getDataSets().then(dataSets => {
            setState({
                dataSets: dataSets.data!,
                selectedId: [],
                editing: null,
                showToast: false
            })
        })
    }

    useEffect(() => {
        refreshDataSets()
    }, [])

    return (<Form>
        <Form.Group as={Col} sm={12}>
            <ListGroup>
                {state.dataSets.map((ds, i) => {
                    const arr = ds!.uidFrom!.split('-');
                    const signature = arr.slice(0, 4).join('-');
                    const from = tsToDateStr(arr[4]);
                    const duration = secondsToDays(parseInt(ds!.uidTo!.split('-')[4]) - parseInt(arr[4]));
                    return (<ListGroup.Item
                            key={'dataSet' + i}
                            style={{
                                textAlign: 'left'
                            }}
                        >
                            <FormCheck
                                style={{display: 'inline', marginRight: '10px'}}
                                checked={state.selectedId.indexOf(ds.id!) >= 0}
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
                               }}
                            />
                            <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>{ds!.name}</Form.Text>
                            <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>{signature}</Form.Text>
                            <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>{from}</Form.Text>
                            <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>~ {duration} days</Form.Text>
                            <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>has {ds!.count} samples</Form.Text>
                            <Button
                                onClick={() => {
                                    setState({
                                        ...state,
                                        editing: ds
                                    })
                                }}
                                variant='outline-primary'
                            ><i className='fa fa-edit'/></Button>
                        </ListGroup.Item>);
                    })
                }
            </ListGroup>

        </Form.Group>
        <Form.Group as={Col} sm={12} style={{textAlign: 'left'}}>
            <Button
                style={{marginRight: '10px'}}
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
            <Button
                style={{
                marginLeft: '30px'
            }}
                disabled={state.selectedId.length !== 1}
                onClick={() => {
                    fitApi.setFit({
                        model: '',
                        dataSet: state.selectedId[0]
                    }).then(() => {
                        setState({
                            ...state,
                            selectedId: [],
                            editing: null,
                            showToast: true
                        })
                    })
                }}
            >
                {'>> FIT <<'}
            </Button>
        </Form.Group>
        <Toast
            onClose={() => setState({
                ...state,
                showToast: false
            })}
            show={state.showToast} delay={3000} autohide>
            <Toast.Header>
                <strong className="mr-auto">Fit process started</strong>
            </Toast.Header>
            {/*<Toast.Body>Fit process started</Toast.Body>*/}
        </Toast>
        {state.editing
            ? <Form.Group as={Col} sm={12}>
                <DataSetEditor
                    breakPoints={props.breakPoints}
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