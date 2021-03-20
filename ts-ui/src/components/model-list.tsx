import {DataSet, FitApi, MarketBreakPoint, Model, ModelApi, SampleApi} from "../api";
import React, {useEffect, useState} from "react";
import {Button, Col, Form, ListGroup, Toast} from "react-bootstrap";
import {DelayConfirm} from "../util/delay-confirm";
import {DataSetEditor} from "./dataset-editor";
import {ModelEditor} from "./model-editor";

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