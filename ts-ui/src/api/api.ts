/// <reference path="./custom.d.ts" />
// tslint:disable
/**
 * ts api
 * ts api
 *
 * OpenAPI spec version: 1.0.0
 * 
 *
 * NOTE: This file is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the file manually.
 */

import * as url from "url";
import * as portableFetch from "portable-fetch";
import { Configuration } from "./configuration";

const BASE_PATH = "/".replace(/\/+$/, "");

/**
 *
 * @export
 */
export const COLLECTION_FORMATS = {
    csv: ",",
    ssv: " ",
    tsv: "\t",
    pipes: "|",
};

/**
 *
 * @export
 * @interface FetchAPI
 */
export interface FetchAPI {
    (url: string, init?: any): Promise<Response>;
}

/**
 *
 * @export
 * @interface FetchArgs
 */
export interface FetchArgs {
    url: string;
    options: any;
}

/**
 *
 * @export
 * @class BaseAPI
 */
export class BaseAPI {

    constructor(protected configuration?: Configuration, protected basePath: string = BASE_PATH, protected fetch: FetchAPI = portableFetch) {
        if (configuration) {
            this.configuration = configuration;
            this.basePath = configuration.basePath || this.basePath;
        }
    }
};

/**
 *
 * @export
 * @class RequiredError
 * @extends {Error}
 */
export class RequiredError extends Error {
    name = "RequiredError"
    constructor(public field: string, msg?: string) {
        super(msg);
    }
}

/**
 * 
 * @export
 * @interface MarketBreakPoint
 */
export interface MarketBreakPoint {
    /**
     * 
     * @type {string}
     * @memberof MarketBreakPoint
     */
    timestamp?: string;
}
/**
 * 
 * @export
 * @interface MarketBreakPointResponse
 */
export interface MarketBreakPointResponse {
    /**
     * 
     * @type {Array<MarketBreakPoint>}
     * @memberof MarketBreakPointResponse
     */
    data?: Array<MarketBreakPoint>;
    /**
     * 
     * @type {string}
     * @memberof MarketBreakPointResponse
     */
    queryString?: string;
}
/**
 * 
 * @export
 * @interface RawData
 */
export interface RawData {
    /**
     * 
     * @type {number}
     * @memberof RawData
     */
    timestamp?: number;
    /**
     * 
     * @type {number}
     * @memberof RawData
     */
    open?: number;
    /**
     * 
     * @type {number}
     * @memberof RawData
     */
    high?: number;
    /**
     * 
     * @type {number}
     * @memberof RawData
     */
    low?: number;
    /**
     * 
     * @type {number}
     * @memberof RawData
     */
    close?: number;
    /**
     * 
     * @type {number}
     * @memberof RawData
     */
    volume?: number;
}
/**
 * 
 * @export
 * @interface RawDataResponse
 */
export interface RawDataResponse {
    /**
     * 
     * @type {Array<RawData>}
     * @memberof RawDataResponse
     */
    data?: Array<RawData>;
    /**
     * 
     * @type {string}
     * @memberof RawDataResponse
     */
    queryString?: string;
}
/**
 * RawDataApi - fetch parameter creator
 * @export
 */
export const RawDataApiFetchParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * get Market Break Points
         * @summary get Market Break Points
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getMarketBreakPoint(options: any = {}): FetchArgs {
            const localVarPath = `/market_break_points`;
            const localVarUrlObj = url.parse(localVarPath, true);
            const localVarRequestOptions = Object.assign({ method: 'GET' }, options);
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            localVarUrlObj.query = Object.assign({}, localVarUrlObj.query, localVarQueryParameter, options.query);
            // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
            delete localVarUrlObj.search;
            localVarRequestOptions.headers = Object.assign({}, localVarHeaderParameter, options.headers);

            return {
                url: url.format(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * get RawData
         * @summary get RawData
         * @param {string} interval 
         * @param {number} start 
         * @param {number} end 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getRawData(interval: string, start: number, end: number, options: any = {}): FetchArgs {
            // verify required parameter 'interval' is not null or undefined
            if (interval === null || interval === undefined) {
                throw new RequiredError('interval','Required parameter interval was null or undefined when calling getRawData.');
            }
            // verify required parameter 'start' is not null or undefined
            if (start === null || start === undefined) {
                throw new RequiredError('start','Required parameter start was null or undefined when calling getRawData.');
            }
            // verify required parameter 'end' is not null or undefined
            if (end === null || end === undefined) {
                throw new RequiredError('end','Required parameter end was null or undefined when calling getRawData.');
            }
            const localVarPath = `/raw`;
            const localVarUrlObj = url.parse(localVarPath, true);
            const localVarRequestOptions = Object.assign({ method: 'GET' }, options);
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (interval !== undefined) {
                localVarQueryParameter['interval'] = interval;
            }

            if (start !== undefined) {
                localVarQueryParameter['start'] = start;
            }

            if (end !== undefined) {
                localVarQueryParameter['end'] = end;
            }

            localVarUrlObj.query = Object.assign({}, localVarUrlObj.query, localVarQueryParameter, options.query);
            // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
            delete localVarUrlObj.search;
            localVarRequestOptions.headers = Object.assign({}, localVarHeaderParameter, options.headers);

            return {
                url: url.format(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * RawDataApi - functional programming interface
 * @export
 */
export const RawDataApiFp = function(configuration?: Configuration) {
    return {
        /**
         * get Market Break Points
         * @summary get Market Break Points
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getMarketBreakPoint(options?: any): (fetch?: FetchAPI, basePath?: string) => Promise<MarketBreakPointResponse> {
            const localVarFetchArgs = RawDataApiFetchParamCreator(configuration).getMarketBreakPoint(options);
            return (fetch: FetchAPI = portableFetch, basePath: string = BASE_PATH) => {
                return fetch(basePath + localVarFetchArgs.url, localVarFetchArgs.options).then((response) => {
                    if (response.status >= 200 && response.status < 300) {
                        return response.json();
                    } else {
                        throw response;
                    }
                });
            };
        },
        /**
         * get RawData
         * @summary get RawData
         * @param {string} interval 
         * @param {number} start 
         * @param {number} end 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getRawData(interval: string, start: number, end: number, options?: any): (fetch?: FetchAPI, basePath?: string) => Promise<RawDataResponse> {
            const localVarFetchArgs = RawDataApiFetchParamCreator(configuration).getRawData(interval, start, end, options);
            return (fetch: FetchAPI = portableFetch, basePath: string = BASE_PATH) => {
                return fetch(basePath + localVarFetchArgs.url, localVarFetchArgs.options).then((response) => {
                    if (response.status >= 200 && response.status < 300) {
                        return response.json();
                    } else {
                        throw response;
                    }
                });
            };
        },
    }
};

/**
 * RawDataApi - factory interface
 * @export
 */
export const RawDataApiFactory = function (configuration?: Configuration, fetch?: FetchAPI, basePath?: string) {
    return {
        /**
         * get Market Break Points
         * @summary get Market Break Points
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getMarketBreakPoint(options?: any) {
            return RawDataApiFp(configuration).getMarketBreakPoint(options)(fetch, basePath);
        },
        /**
         * get RawData
         * @summary get RawData
         * @param {string} interval 
         * @param {number} start 
         * @param {number} end 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getRawData(interval: string, start: number, end: number, options?: any) {
            return RawDataApiFp(configuration).getRawData(interval, start, end, options)(fetch, basePath);
        },
    };
};

/**
 * RawDataApi - object-oriented interface
 * @export
 * @class RawDataApi
 * @extends {BaseAPI}
 */
export class RawDataApi extends BaseAPI {
    /**
     * get Market Break Points
     * @summary get Market Break Points
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RawDataApi
     */
    public getMarketBreakPoint(options?: any) {
        return RawDataApiFp(this.configuration).getMarketBreakPoint(options)(this.fetch, this.basePath);
    }

    /**
     * get RawData
     * @summary get RawData
     * @param {string} interval 
     * @param {number} start 
     * @param {number} end 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof RawDataApi
     */
    public getRawData(interval: string, start: number, end: number, options?: any) {
        return RawDataApiFp(this.configuration).getRawData(interval, start, end, options)(this.fetch, this.basePath);
    }

}
