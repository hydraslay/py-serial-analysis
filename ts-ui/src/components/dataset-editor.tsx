import {DataSet, MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import React, {useState} from "react";
import {Button, Dropdown, DropdownButton, FormControl, InputGroup} from "react-bootstrap";

type DataSetEditorProps = {
    breakPoints: MarketBreakPoint[];
    onSave: (data: DataSet) => void;
    onCancel: () => void;
}

type DataSetEditorState = {
    id: string;
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
        id: '',
        name: '',
        from: '',
        to: ''
    } as DataSetEditorState)

    return (<div>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Data Set Name</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl aria-describedby="basic-addon1"/>
        </InputGroup>
        <InputGroup size="sm" className="mb-3">
            <InputGroup.Prepend>
                <InputGroup.Text id="inputGroup-sizing-sm">Time Span From</InputGroup.Text>
            </InputGroup.Prepend>
            <DropdownButton
                as={InputGroup.Prepend}
                variant="outline-secondary"
                title={'from timestamp'}
            >
                {props.breakPoints.map((bp, i) =>
                    <Dropdown.Item key={bp.timestamp}
                                   onClick={() => {
                                   }}
                    >
                        {bp.timestamp}
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
                title={'from timestamp'}
            >
                {props.breakPoints.map((bp, i) =>
                    <Dropdown.Item key={bp.timestamp}
                                   onClick={() => {
                                   }}
                    >
                        {bp.timestamp}
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