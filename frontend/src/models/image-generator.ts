/* tslint:disable */
/* eslint-disable */
/**
 * Stability demo
 * Stability demo
 *
 * OpenAPI spec version: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
/**
 * 
 * @export
 * @interface ImageGenerator
 */
export interface ImageGenerator {
    /**
     * 
     * @type {string}
     * @memberof ImageGenerator
     */
    promptEnhanced?: string;
    /**
     * 
     * @type {number}
     * @memberof ImageGenerator
     */
    numberOfImages?: number;
    /**
     * 
     * @type {number}
     * @memberof ImageGenerator
     */
    numberOfInferenceSteps?: number;
    /**
     * 
     * @type {number}
     * @memberof ImageGenerator
     */
    height?: number;
    /**
     * 
     * @type {number}
     * @memberof ImageGenerator
     */
    width?: number;
    /**
     * 
     * @type {string}
     * @memberof ImageGenerator
     */
    sessionId?: string;
    /**
     * 
     * @type {string}
     * @memberof ImageGenerator
     */
    actionId?: string;
}
