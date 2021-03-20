import {DataSet, FitApi, MarketBreakPoint, Model, ModelApi, SampleApi} from "../api";
import React, {useEffect, useState} from "react";
import {Button, Col, Form, FormCheck, ListGroup, Toast} from "react-bootstrap";
import {DelayConfirm} from "../util/delay-confirm";
import {DataSetEditor} from "./dataset-editor";
import {ModelEditor} from "./model-editor";
import {secondsToDays, tsToDateStr} from "../interface";

type ModelListProps = {
}

type ModelListState = {
    data: Model[];
    editing: Model | null;
    selectedModel: string[];
    showToast: boolean;
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const modelApi = new ModelApi(configuration);
const fitApi = new FitApi(configuration);

export const ModelList: React.FC<ModelListProps> = (props) => {

    const [state, setState] = useState({
        data: [],
        editing: null,
        selectedModel: [],
        showToast: false
    } as ModelListState)

    const refreshModels = () => {
        modelApi.getModels().then((result) => {
            setState({
                ...state,
                data: result.data!
            })
        })
    }
    useEffect(() => {
        refreshModels()
    }, []);

    return (<Form>
        <Form.Group as={Col} sm={12}>
            <ListGroup>
                {state.data.map((m, i) => {
                    return (<ListGroup.Item
                        key={'dataSet' + i}
                        style={{
                            textAlign: 'left'
                        }}
                    >
                        <FormCheck
                            style={{display: 'inline', marginRight: '10px'}}
                            checked={state.selectedModel.indexOf(m.model!) >= 0}
                            onChange={(a) => {
                                const newSelectedId = [...state.selectedModel]
                                if (a.target.checked) {
                                    newSelectedId.splice(0, 0, m.model!)
                                } else {
                                    newSelectedId.splice(newSelectedId.indexOf(m.model!), 1)
                                }
                                setState({
                                    ...state,
                                    selectedModel: newSelectedId
                                })
                            }}
                        />
                        <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>{m.model!}</Form.Text>
                        <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>{m.description!}</Form.Text>
                        <Form.Text style={{display: 'inline', marginRight: '10px', fontSize: '16px'}}>{m.stat!}</Form.Text>
                        <Button
                            onClick={() => {
                                setState({
                                    ...state,
                                    editing: m
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
                disabled={state.selectedModel.length === 0}
                text='－'
                description='delete selected data set'
                onConfirm={() => {
                    alert('deleted')
                }}
            />
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
                <ModelEditor
                    onSave={d => {
                        modelApi.setModel(d).then(() => {
                            refreshModels()
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