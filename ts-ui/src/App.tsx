import React, {PureComponent, useState} from 'react';
import {ButtonGroup, Button, Form} from 'react-bootstrap'
import './App.css';
import {SeriesChart} from "./components/line-chart";
import {RawDataApi} from './api'

const rawDataApi = new RawDataApi({
    basePath: 'http://localhost:8080'
});

export const App: React.FC = () => {
    const [state, setState] = useState({
        data: [] as any[]
    })
    if (!state.data.length) {
        rawDataApi.getRawData().then((result) => {
            setState({
                data: result
            })
        })
    }
    const samples = Array(30).fill({lbl: 1, proved: true})
    return (
        <div className="App">
            <div style={{marginBottom: '50px'}}>
                <Form.Check
                    custom
                    inline
                    label="All"
                    type='checkbox'
                    id='list-all-check'
                />
                <Form.Check
                    custom
                    inline
                    label="Proved"
                    type='checkbox'
                    id='list-proved-check'
                />
                <Form.Check
                    custom
                    inline
                    label="Unproved"
                    type='checkbox'
                    id='list-unproved-check'
                />
            </div>
            {samples.map((sampleItem) => {
                return <div style={{
                    display: 'inline-block',
                    border: '1px dotted lightgray',
                    background: sampleItem.proved ? 'white' : 'lightyellow'
                }}>
                    <ButtonGroup vertical style={{verticalAlign: 'middle', marginLeft: '10px'}}>
                        <Button variant={sampleItem.lbl === 1 ? 'success' : 'outline-success'}>Rise</Button>
                        <Button variant={sampleItem.lbl === 2 ? 'danger' : 'outline-danger'}>Drop</Button>
                        <Button variant={sampleItem.lbl === 3 ? 'warning' : 'outline-warning'}>Flat</Button>
                    </ButtonGroup>
                    <SeriesChart data={state.data}/>
                </div>
            })}
        </div>
    );
}
