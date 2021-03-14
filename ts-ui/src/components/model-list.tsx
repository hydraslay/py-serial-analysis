import {DataSet, FitApi, MarketBreakPoint, Model, ModelApi, SampleApi} from "../api";
import React, {useEffect, useState} from "react";
import {Col, Form, ListGroup} from "react-bootstrap";

type ModelListProps = {
}

type ModelListState = {
    data: Model[];
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const modelApi = new ModelApi(configuration);
const fitApi = new FitApi(configuration);

export const ModelList: React.FC<ModelListProps> = (props) => {

    const [state, setState] = useState({
        data: []
    } as ModelListState)

    useEffect(() => {
        modelApi.getModels().then((result) => {
            setState({
                ...state,
                data: result
            })
        })
    }, []);

    return (<Form>
        <Form.Group as={Col} sm={12}>
            <ListGroup>



            </ListGroup>
        </Form.Group>
    </Form>)

}