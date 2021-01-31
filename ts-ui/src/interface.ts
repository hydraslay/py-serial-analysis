import {RawData} from "./api";

export type RawDataItem = Required<RawData>

export type SampleDataItem = {
    hiFreq: RawDataItem[];
    nextLowFreq: RawDataItem;
    actual: number;
}

export type BreakPoint = {
    label: string;
    start: number;
    end: number;
}
