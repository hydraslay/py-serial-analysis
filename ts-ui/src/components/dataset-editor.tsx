import {MarketBreakPoint, RawDataApi, SampleApi} from "../api";
import {BreakPoint, SampleDataItem} from "../interface";
import React from "react";
import {Col, Dropdown, DropdownButton, Form, InputGroup} from "react-bootstrap";

type DataSetEditorProps = {
    breakPoints: MarketBreakPoint[];
}

type DataSetEditorState = {
    selectedBP: BreakPoint | undefined;
    samples: SampleDataItem[];
    progress: number;
}

const configuration = {
    basePath: 'http://localhost:8080'
}

const sampleApi = new SampleApi(configuration);
const rawDataApi = new RawDataApi(configuration);

export const DataSetEditor: React.FC<DataSetEditorProps> = (props) => {
    return (<Form>
        <Form.Group as={Col} sm={12}>
            <DropdownButton
                as={InputGroup.Prepend}
                variant="outline-secondary"
                title={'from'}
            >
                {props.breakPoints.map((bp, i) =>
                    <Dropdown.Item key={bp.timestamp}
                                   onClick={() => {
                                   }}
                    >
                        {bp.timestamp}
                    </Dropdown.Item>)}
            </DropdownButton>
        </Form.Group>
    </Form>)
}