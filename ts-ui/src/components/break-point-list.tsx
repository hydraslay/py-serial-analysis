import {BreakPoint} from "../interface";
import React from "react";
import moment from 'moment';
import {Dropdown, DropdownButton, InputGroup} from "react-bootstrap";

type BreakPointListProp = {
    data: Array<string | undefined>;
    selectedLabel: string
    onChange: (bp: BreakPoint) => void;
}

export const BreakPointList: React.FC<BreakPointListProp> = (props) => {

    let start: string = '';
    const breakPoints = props.data.reduce((arr: BreakPoint[], item) => {
        const curr = item!;
        if (start) {
            if (!moment(start, "YYYY-MM-DD").add(1, 'days').isSame(curr)) {
                arr.push({
                    label: `${start} ~ ${item}`,
                    start: new Date(start).valueOf(),
                    end: new Date(curr).valueOf()
                })
            }
        }
        start = curr;
        return arr;
    }, [])

    return <div>
        <InputGroup className="mb-3">
            <DropdownButton
                as={InputGroup.Prepend}
                variant="outline-secondary"
                title={props.selectedLabel || 'Trade Time'}
                id="input-group-dropdown-1"
            >
                {breakPoints.map((bp, i) =>
                    <Dropdown.Item key={bp.label}
                                   onClick={() => {
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
