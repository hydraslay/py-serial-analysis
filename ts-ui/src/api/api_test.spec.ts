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

describe("ModelApi", () => {
  let instance: api.ModelApi
  beforeEach(function() {
    instance = new api.ModelApi(config)
  });

  test("getModels", () => {
    return expect(instance.getModels({})).resolves.toBe(null)
  })
  test("getSampleTypes", () => {
    return expect(instance.getSampleTypes({})).resolves.toBe(null)
  })
  test("setModel", () => {
    const body: api.Model = undefined
    return expect(instance.setModel(body, {})).resolves.toBe(null)
  })
})

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

describe("SampleApi", () => {
  let instance: api.SampleApi
  beforeEach(function() {
    instance = new api.SampleApi(config)
  });

  test("getSamples", () => {
    return expect(instance.getSamples({})).resolves.toBe(null)
  })
  test("setSamples", () => {
    const body: Array<api.Samples> = undefined
    return expect(instance.setSamples(body, {})).resolves.toBe(null)
  })
})

