import {RawDataItem, SampleDataItem} from "../interface";

type SortedStack = number[][];

const threshold = 0.02
const tickSpan = 15

function removeTick(stack: SortedStack, index: number) {
    const i = stack.findIndex((item) => item[0] === index);
    if (i >= 0) {
        stack.splice(i, 1);
    }
}

function addLow(stack: SortedStack, index: number, tick: RawDataItem) {
    const newItem = [index, tick.low];
    if (stack.length > 0) {
        const i = stack.findIndex((item) => tick.low < item[1]);
        if (i >= 0) {
            stack.splice(i, 0, newItem);
            return;
        }
    }
    stack.push(newItem);
}

function getValueByLowest(tickHi: RawDataItem, tickLo: RawDataItem, threshold: number) {
    const hiThresh = tickHi.low + threshold;
    const loThresh = tickHi.low - threshold;
    if (tickLo.high <= loThresh) {
        return 1;
    }
    if (tickLo.high <= hiThresh && tickLo.high >= loThresh && tickLo.low <= loThresh) {
        return 2;
    }
    if (tickLo.high >= hiThresh && tickLo.low <= loThresh) {
        return 4;
    }
    if (tickLo.high >= hiThresh && tickLo.low >= loThresh && tickLo.low <= hiThresh) {
        return 5;
    }
    if (tickLo.low >= hiThresh) {
        return 6;
    }
    return 3;
}

function getValueByRange(tickHi: RawDataItem, tickLo: RawDataItem, threshold: number) {
    let val = 0
    if (tickLo.high > tickHi.high + threshold) {
        val += 6;
    } else if (tickLo.high < tickHi.high - threshold) {
    } else {
        val += 3;
    }

    if (tickLo.low > tickHi.low + threshold) {
        val += 3;
    } else if (tickLo.low < tickHi.low - threshold) {
        val += 1;
    } else {
        val += 2;
    }
    return val;
}

export function generateSamples(hiFreq: RawDataItem[], loFreq: RawDataItem[]) {
    if (!hiFreq || !hiFreq.length || !loFreq || !loFreq.length) {
        return []
    }

    // equalize index
    let startHi = 0
    while (hiFreq[startHi].timestamp < loFreq[0].timestamp) {
        startHi++;
        if (startHi > hiFreq.length) {
            return []
        }
    }

    const samples: SampleDataItem[] = [];
    const lowStack: SortedStack = [];
    let indicatorLo = 0;
    for (let i = startHi; i < hiFreq.length; i++) {
        const tick = hiFreq[i];
        while (loFreq[indicatorLo].timestamp <= tick.timestamp) {
            indicatorLo++;
        }
        addLow(lowStack, i, tick)
        if (i >= tickSpan) {
            if (lowStack[0][0] == i) {
                const val = getValueByRange(tick, loFreq[indicatorLo], threshold);
                samples.push({
                    hiFreq: hiFreq.slice(i - tickSpan, i + 1),
                    nextLowFreq: loFreq[indicatorLo],
                    actual: val,
                })
            }
            removeTick(lowStack, i - tickSpan);
        }
    }
    return samples;
}