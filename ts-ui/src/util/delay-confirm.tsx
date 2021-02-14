import React, {useState} from "react";
import {Button, OverlayTrigger, Popover, ProgressBar} from "react-bootstrap";

export type DelayConfirmProp = {
    disabled: boolean;
    text: string;
    description: string;
    onConfirm: () => void;
}

let timeout = null as NodeJS.Timeout | null

export const DelayConfirm: React.FC<DelayConfirmProp> = (props) => {
    const [state, setState] = useState({
        progress: 100,
        show: false
    })
    const open = () => {
        let p = {
            progress: 100
        }
        timeout = setInterval((param) => {
            param[0].progress = param[0].progress > 0 ? param[0].progress - 10 : 0;
            if (param[0].progress <= 0) {
                close()
            }
            setState({
                show: true,
                progress: param[0].progress
            })
        }, 200, [p])
        setState({
            show: true,
            progress: 100
        })
    }
    const close = () => {
        clearTimeout(timeout!);
        setState({
            ...state,
            show: false,
        })
    }
    const popover = (
        <Popover id="popover-basic">
            <Popover.Title as="h3">Are You Sure</Popover.Title>
            <Popover.Content>
                Are you sure to {props.description} ?
                <br/>
                This change may <strong>not</strong> be recovered by any action.
                <br/>
                <ProgressBar variant='danger' style={{height: '5px'}} now={state.progress}/>
                <br/>
                <Button disabled={state.progress > 0}
                    style={{marginRight: '10px'}}
                        onClick={() => {
                            close()
                            props.onConfirm()
                        }}
                >Yes</Button>
                <Button variant='secondary'
                        onClick={() => {
                            close()
                        }}
                >No</Button>
            </Popover.Content>
        </Popover>
    );

    return <OverlayTrigger rootClose
                           show={state.show}
                           onToggle={(now) => {
                               if (now) {
                                   open()
                               } else {
                                   close()
                               }
                           }}
                           trigger="click" placement="right" overlay={popover}
    >
        <Button disabled={props.disabled} variant="primary">{props.text}</Button>
    </OverlayTrigger>
}