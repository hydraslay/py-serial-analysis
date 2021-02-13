import {RawData, Samples} from "./api";

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
            sampleData: d.hiFreq
        }
    })
    return arr;
}

export type BreakPoint = {
    label: string;
    start: number;
    end: number;
}
