import {BreakPoint, RawDataItem} from "../interface";
import React, {useEffect, useState} from "react";
import moment from 'moment';
import {RawDataApi} from '../api'
import {DropdownButton, InputGroup, Dropdown} from "react-bootstrap";

const rawDataApi = new RawDataApi({
    basePath: 'http://localhost:8080'
});

type BreakPointListProp = {
    onChange: (bp: BreakPoint) => void;
}

export const BreakPointList: React.FC<BreakPointListProp> = (props) => {

    const [state, setState] = useState({
        breakPoints: [] as BreakPoint[],
        selectedLabel: ''
    })

    useEffect(() => {
        rawDataApi.getMarketBreakPoint().then((result) => {
            let start: string = '';
            setState({
                breakPoints: result!.data!.reduce((arr: BreakPoint[], item) => {
                    const curr = item.timestamp!;
                    if (start) {
                        if (!moment(start, "YYYY-MM-DD").add(1, 'days').isSame(curr)) {
                            arr.push({
                                label: `${start} ~ ${item.timestamp}`,
                                start: new Date(start).valueOf(),
                                end: new Date(curr).valueOf()
                            })
                        }
                    }
                    start = curr;
                    return arr;
                }, []),
                selectedLabel: ''
            })
        })
    }, []);


    return <div>
        <InputGroup className="mb-3">
            <DropdownButton
                as={InputGroup.Prepend}
                variant="outline-secondary"
                title={state.selectedLabel || 'Trade Time'}
                id="input-group-dropdown-1"
            >
                {state.breakPoints.map((bp, i) =>
                    <Dropdown.Item key={'bp-' + i}
                                   onClick={() => {
                                       setState({
                                           ...state,
                                           selectedLabel: bp.label
                                       })
                                       if (props.onChange) {
                                           props.onChange(bp)
                                       }
                                   }}
                    >
                        {bp.label}
                    </Dropdown.Item>)}
            </DropdownButton>
        </InputGroup>
    </div>
}
