import {RawData, Samples} from "./api";
import moment from "moment";

export type RawDataItem = Required<RawData>

export type SampleDataItem = {
    hiFreq: RawDataItem[];
    nextLowFreq: RawDataItem;
    actual: number;
}

export const toSampleArray = (data: SampleDataItem[]) => {
    const arr: Samples[] = data.map((d) => {
        return {
            uid: `v3-5m-15m-${d.hiFreq.length}-${d.hiFreq[0].timestamp}`,
            value: d.actual,
            sampleData: d.hiFreq,
            extraData: [d.nextLowFreq]
        }
    })
    return arr;
}

export const toRawDataItemArray = (data: Samples) => {
    const arr: RawDataItem[] = data.sampleData!.concat(data.extraData!) as Array<Required<RawData>>
    return arr;
}

export type BreakPoint = {
    label: string;
    start: number;
    end: number;
}

export type BreakPointSummary = {
    count: number
} & BreakPoint


export function tsToDateStr(ts: number | string) {
    return moment(new Date((typeof ts === 'string' ? parseInt(ts) : ts) * 1000)).format('YYYY/MM/DD');
}

export function dateStrToTs(dt: string) {
    return moment(dt, 'YYYY/MM/DD').toDate().valueOf() / 1000;
}

export function secondsToDays(sec: number) {
    return Math.round(sec / 3600 / 24)
}
