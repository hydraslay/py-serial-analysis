import React, {useEffect, useState} from "react";
import {Button, Dropdown, DropdownButton, FormControl, InputGroup} from "react-bootstrap";
import {dateStrToTs, tsToDateStr} from "../interface";
import {Model} from "../api";

type ModelEditorProps = {
    onSave: (data: Model) => void;
    onCancel: () => void;
    editing: Model;
}

type ModelEditorState = {
    modelName: string;
    description: string;
    params: string;
    stat: string;
}

const configuration = {
    basePath: 'http://localhost:8080'
}

export const ModelEditor: React.FC<ModelEditorProps> = (props) => {
    const [state, setState] = useState({
        modelName: '',
        description: '',
        params: '',
    } as ModelEditorState)

    useEffect(() => {
        const editing = props.editing
        setState({
            modelName: editing.model!,
            description: editing.description!,
            params: editing.params!,
            stat: editing.stat!
        })
    }, [props.editing])

    return (<div>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Name</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl
                value={state.modelName}
                onChange={(e) => {
                    setState({
                        ...state,
                        modelName: e.target.value
                    })
                }}
                aria-describedby="basic-addon1"/>
        </InputGroup>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Description</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl
                value={state.description}
                onChange={(e) => {
                    setState({
                        ...state,
                        description: e.target.value
                    })
                }}
                aria-describedby="basic-addon1"/>
        </InputGroup>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Params</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl
                value={state.params}
                onChange={(e) => {
                    setState({
                        ...state,
                        params: e.target.value
                    })
                }}
                aria-describedby="basic-addon1"/>
        </InputGroup>

        <InputGroup>
            <Button style={{marginRight: '10px'}}
                    onClick={() => {
                        props.onSave({
                            model: state.modelName,
                            description: state.description,
                            params: state.params,
                            stat: '1'
                        })
                    }}
            >Save</Button>
            <Button variant='secondary'
                    onClick={() => {
                        props.onCancel()
                    }}
            >Cancel</Button>
        </InputGroup>
    </div>)
}