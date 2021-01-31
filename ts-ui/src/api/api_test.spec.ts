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

import * as api from "./api"
import { Configuration } from "./configuration"

const config: Configuration = {}

describe("RawDataApi", () => {
  let instance: api.RawDataApi
  beforeEach(function() {
    instance = new api.RawDataApi(config)
  });

  test("getMarketBreakPoint", () => {
    return expect(instance.getMarketBreakPoint({})).resolves.toBe(null)
  })
  test("getRawData", () => {
    const interval: string = "interval_example"
    const start: number = 1.2
    const end: number = 1.2
    return expect(instance.getRawData(interval, start, end, {})).resolves.toBe(null)
  })
})

