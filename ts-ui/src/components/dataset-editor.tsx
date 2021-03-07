import {DataSet, MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import React, {useEffect, useState} from "react";
import {Button, Dropdown, DropdownButton, FormControl, InputGroup} from "react-bootstrap";
import {dateStrToTs, tsToDateStr} from "../interface";

type DataSetEditorProps = {
    breakPoints: MarketBreakPoint[];
    onSave: (data: DataSet) => void;
    onCancel: () => void;
    editing: DataSet;
}

type DataSetEditorState = {
    id: number | undefined;
    name: string;
    from: string;
    to: string;
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const sampleApi = new SampleApi(configuration);
const rawDataApi = new RawDataApi(configuration);

export const DataSetEditor: React.FC<DataSetEditorProps> = (props) => {
    const [state, setState] = useState({
        id: undefined,
        name: '',
        from: '',
        to: ''
    } as DataSetEditorState)

    useEffect(() => {
        const editing = props.editing
        setState({
            id: editing.id!,
            name: editing.name!,
            from: editing.uidFrom!,
            to: editing.uidTo!
        })
    }, [props.editing])

    const tsFrom = state.from.split('-').slice(-1)[0];
    const tsTo = state.to.split('-').slice(-1)[0];
    const model = state.from.split('-').slice(0, -1).join('-');
    return (<div>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Data Set Name</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl
                value={state.name}
                onChange={(e) => {
                    setState({
                        ...state,
                        name: e.target.value
                    })
                }}
                aria-describedby="basic-addon1"/>
        </InputGroup>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Model Signature</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl
                value={model}
                onChange={(e) => {
                    setState({
                        ...state,
                        from: e.target.value + '-' + tsFrom,
                        to: e.target.value + '-' + tsTo,
                    })
                }}
                aria-describedby="basic-addon1"/>
        </InputGroup>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Time Span From</InputGroup.Text>
            </InputGroup.Prepend>
            <DropdownButton
                as={InputGroup.Prepend}
                variant="outline-secondary"
                title={state.from ? tsToDateStr(tsFrom) : 'from timestamp'}
            >
                {props.breakPoints.map((bpFrom, i) =>
                    <Dropdown.Item
                        key={bpFrom.timestamp}
                        onClick={() => {
                            setState({
                                ...state,
                                from: model + '-' + dateStrToTs(bpFrom.timestamp!)
                            })
                        }}
                    >
                        {bpFrom.timestamp}
                    </Dropdown.Item>)}
            </DropdownButton>
        </InputGroup>

        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Time Span To</InputGroup.Text>
            </InputGroup.Prepend>
            <DropdownButton
                as={InputGroup.Prepend}
                variant="outline-secondary"
                title={state.to ? tsToDateStr(tsTo) : 'from timestamp'}
            >
                {props.breakPoints.map((bpTo, i) =>
                    <Dropdown.Item
                        key={bpTo.timestamp}
                        onClick={() => {
                            setState({
                                ...state,
                                to: model + '-' + dateStrToTs(bpTo.timestamp!)
                            })
                        }}
                    >
                        {bpTo.timestamp}
                    </Dropdown.Item>)}
            </DropdownButton>
        </InputGroup>

        <InputGroup>
            <Button style={{marginRight: '10px'}}
                    onClick={() => {
                        props.onSave({
                            id: state.id,
                            name: state.name,
                            uidFrom: state.from,
                            uidTo: state.to
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