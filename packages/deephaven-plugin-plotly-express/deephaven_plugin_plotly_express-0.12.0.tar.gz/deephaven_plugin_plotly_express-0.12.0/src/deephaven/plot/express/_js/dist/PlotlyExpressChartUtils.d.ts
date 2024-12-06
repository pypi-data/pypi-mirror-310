import type { Data, LayoutAxis, PlotlyDataLayoutConfig } from 'plotly.js';
import type { dh as DhType } from '@deephaven/jsapi-types';
export interface PlotlyChartWidget {
    getDataAsBase64: () => string;
    exportedObjects: {
        fetch: () => Promise<DhType.Table>;
    }[];
    addEventListener: (type: string, fn: (event: CustomEvent<PlotlyChartWidget>) => () => void) => void;
}
export interface PlotlyChartWidgetData {
    type: string;
    figure: {
        deephaven: {
            mappings: Array<{
                table: number;
                data_columns: Record<string, string[]>;
            }>;
            is_user_set_template: boolean;
            is_user_set_color: boolean;
        };
        plotly: PlotlyDataLayoutConfig;
    };
    revision: number;
    new_references: number[];
    removed_references: number[];
}
export declare function getWidgetData(widgetInfo: DhType.Widget): PlotlyChartWidgetData;
export declare function getDataMappings(widgetData: PlotlyChartWidgetData): Map<number, Map<string, string[]>>;
/**
 * Removes the default colors from the data
 * Data color is not removed if the user set the color specifically or the plot type sets it
 *
 * This only checks if the marker or line color is set to a color in the colorway.
 * This means it is not possible to change the order of the colorway and use the same colors.
 *
 * @param colorway The colorway from plotly
 * @param data The data to remove the colorway from. This will be mutated
 */
export declare function removeColorsFromData(colorway: string[], data: Data[]): void;
/**
 * Gets the path parts from a path replacement string from the widget data.
 * The parts start with the plotly data array as the root.
 * E.g. /plotly/data/0/x -> ['0', 'x']
 * @param path The path from the widget data
 * @returns The path parts within the plotly data array
 */
export declare function getPathParts(path: string): string[];
/**
 * Checks if a plotly series is a line series without markers
 * @param data The plotly data to check
 * @returns True if the data is a line series without marakers
 */
export declare function isLineSeries(data: Data): boolean;
/**
 * Checks if a plotly axis type is automatically determined based on the data
 * @param axis The plotly axis to check
 * @returns True if the axis type is determined based on the data
 */
export declare function isAutoAxis(axis: Partial<LayoutAxis>): boolean;
/**
 * Checks if a plotly axis type is linear
 * @param axis The plotly axis to check
 * @returns True if the axis is a linear axis
 */
export declare function isLinearAxis(axis: Partial<LayoutAxis>): boolean;
/**
 * Check if 2 axis ranges are the same
 * A null range indicates an auto range
 * @param range1 The first axis range options
 * @param range2 The second axis range options
 * @returns True if the range options describe the same range
 */
export declare function areSameAxisRange(range1: unknown[] | null, range2: unknown[] | null): boolean;
export interface DownsampleInfo {
    type: 'linear';
    /**
     * The original table before downsampling.
     */
    originalTable: DhType.Table;
    /**
     * The x column to downsample.
     */
    xCol: string;
    /**
     * The y columns to downsample.
     */
    yCols: string[];
    /**
     * The width of the x-axis in pixels.
     */
    width: number;
    /**
     * The range of the x-axis. Null if set to autorange.
     */
    range: string[] | null;
    /**
     * If the range is a datae or number
     */
    rangeType: 'date' | 'number';
}
export declare function downsample(dh: typeof DhType, info: DownsampleInfo): Promise<DhType.Table>;
/**
 * Get the indexes of the replaceable WebGL traces in the data
 * A replaceable WebGL has a type that ends with 'gl' which indicates it has a SVG equivalent
 * @param data The data to check
 * @returns The indexes of the WebGL traces
 */
export declare function getReplaceableWebGlTraceIndices(data: Data[]): Set<number>;
/**
 * Check if the data contains any traces that are at least partially powered by WebGL and have no SVG equivalent.
 * @param data The data to check for WebGL traces
 * @returns True if the data contains any unreplaceable WebGL traces
 */
export declare function hasUnreplaceableWebGlTraces(data: Data[]): boolean;
/**
 * Set traces to use WebGL if WebGL is enabled and the trace was originally WebGL
 * or swap out WebGL for SVG if WebGL is disabled and the trace was originally WebGL
 * @param data The plotly figure data to update
 * @param webgl True if WebGL is enabled
 * @param webGlTraceIndices The indexes of the traces that are originally WebGL traces
 */
export declare function setWebGlTraceType(data: Data[], webgl: boolean, webGlTraceIndices: Set<number>): void;
//# sourceMappingURL=PlotlyExpressChartUtils.d.ts.map