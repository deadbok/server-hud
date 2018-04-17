import React from 'react';
import PropTypes from 'prop-types';
import Text from '../react-svg-text/src/Text';
import PanelHeader from '../header/PanelHeader';
import PanelText from './PanelText';

/**
 * React component to draw transfer speed widgets with a linegraph in the
 * background.
 *
 * @todo Precalculate
 * @todo Make SVG component fit container automaticly.
 * @todo Make sure everthing scales gracefully at various resolutions.
 *
 * @author Martin Grønholdt.
 */
class PanelSpeed extends PanelText {
    /**
     * Creates an instance of PanelSpeed.
     *
     * @param  {any} props
     * @memberof PanelSpeed
     */
    constructor(props) {
        super(props);
        this.state = {
            class: 'col-' + props.size,
            direction: props.direction,
            text: '0.00 KiB/s',
            data: [],
            graphSamples: props.graphSamples,
            graphWait: props.graphWait,
            xPadding: props.svgWidth / 20,
            yPadding: props.svgHeight / 20,
            graphWidth: props.svgWidth - props.svgWidth / 20,
            graphHeight: props.svgHeight - props.svgHeight / 20
        };
        // Counter to keep track of sampls for the graph.
        this.i = 0;
        // Number of samples in current data.
        this.samples = 0;
        // Maximum Y value encountered in the data.
        this.maxY = 0;
        // Avarage across websocket data.
        this.avg = 0;
    }

    /**
     * Parse data recieved on the websocket.
     *
     * @param {message} message
     */
    onSocketData(message) {
        // Parse the data we want.
        let data = JSON.parse(message.data)[this.state.direction];
        // Set the text.
        this.setState({text: data});
        // Increase sample count.
        this.i++;
        // Calculate cumulative moving average average. Use this in the graph to smooth
        // it a bit.
        this.avg += parseFloat(data);
        this.avg /= 2;
        // Check if we have sampled enough that we've reached the next point in the
        // graph.
        if (this.i > this.state.graphWait) {
            /* Create a copy of the data array. If the array is fully pouplated
             * remove the first entry and add the new one at the end. If the
             * array is not fully populated add the new data to the end */
            let arrayvar = this.state.data;
            if (this.samples < this.state.graphSamples) {
                arrayvar.push({x: new Date(), y: this.avg});
                this.samples++;
            } else {
                arrayvar.shift();
                arrayvar.push({x: new Date(), y: this.avg});
            }
            // Reset sample count.
            this.i = 0;
            // Reset the average.
            this.avg = 0;
            // Replace the data with the new array.
            this.setState({data: arrayvar});
        }
    }

    /**
     * Invoked immediately after a component is mounted.
     *
     * @return {void}@memberof PanelSpeed
     */
    componentDidMount() {
        // Open the websocket connection.
        this.socket = new WebSocket('ws://malcolm:5000/ws/speed');
        this.socket.onmessage = (m) => this.onSocketData(m);
    }

    /**
     * Get the minimum x value in the dataset.
     *
     * @return {int} Minimum x value in the dataset
     * @memberof PanelSpeed
     */
    getMinX() {
        // Run through the dataset and get the minumim value.
        if (this.state.data[0] !== undefined) {
            let ret = this.state.data[0]['x'];
            this
                .state
                .data
                .forEach((elem) => {
                    ret = Math.min(ret, elem['x']);
                });
            //console.log('Min X: ' + ret);
            return ret;
        }
        return 0;
    }

    /**
     * Get the maximum x value in the dataset.
     *
     * @return {int} Maximum x value in the dataset
     * @memberof PanelSpeed
     */
    getMaxX() {
        if (this.state.data[0] !== undefined) {
            let ret = this.state.data[0]['x'];
            this
                .state
                .data
                .forEach((elem) => {
                    ret = Math.max(ret, elem['x']);
                });
            //console.log('Max X: ' + ret);
            return ret;
        }
        return 0;
    }

    /**
     * Get the minimum y.
     *
     * @return {int} Minimum y value in the dataset
     * @memberof PanelSpeed
     */
    getMinY() {
        /* Always return 0. We have no negative axis, and we do not want the
         * graph to lower bound of the graph to move. */
        return 0;
    }

    /**
     * Get the maximum Y value ever encountered in the dataset.
     *
     * @return {int} Maximum x value encountered
     * @memberof PanelSpeed
     */
    getMaxY() {
        // If the dataset is empty, return 0.
        if (this.state.data[0] !== undefined) {
            /* Get the maximum y value in the current dataset diveded by ten to
             * loose precision. */
            let ret = this.state.data[0]['y'];
            this
                .state
                .data
                .forEach((elem) => {
                    ret = Math.max(ret, elem['y']) / 10;
                });
            /* Since we only want the y axis to be precise to the nearest larger
             * tens, round up the number before multiplying by 10 */
            ret = Math.ceil(ret) * 10;
            // Save value if it is the lergest yet.
            if (ret > this.maxY) {
                this.maxY = ret
            }
            //console.log('Max X: ' + this.maxY);
            return this.maxY;
        }
        return 0;

    }

    /**
     * Perform a scaling  of a an x value in the dataset to fit in the graph
     * area.
     *
     * @param  {int} x
     * @return {int} Scaled x value
     * @memberof PanelSpeed
     */
    getSvgX(x) {
        let ret = (this.state.graphWidth / (this.getMaxX() - this.getMinX())) * (x - this.getMinX()) + this.state.xPadding;
        //console.log('SVG X: ' + ret);
        return ret;
    }

    /**
     * Perform a scaling  of a an y value in the dataset to fit in the graph
     * area.
     *
     * @param  {int} y
     * @return {int} Scaled y value
     * @memberof PanelSpeed
     */
    getSvgY(y) {
        let ret = this.state.graphHeight - ((this.state.graphHeight / (this.getMaxY() - this.getMinY())) * (y - this.getMinY()));
        //console.log('SVG Y: ' + ret);
        return ret;
    }

    /**
     * Calculate the size of the bounding box containing a string when rendered
     * to svg.
     *
     * @param  {string} str
     * @param  {Object} style
     * @return Width in pixel of the rendered text
     * @memberof PanelSpeed
     */
    getStringBounds(str, style) {
        // Create the SVG, and a text elemnts.
        let svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        let textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        textElement.setAttribute('id', '__react_svg_speed_text_measurement_id');
        // Add them to the body.
        svg.appendChild(textElement);
        document
            .body
            .appendChild(svg);
        // Set style and content of the text element.
        Object.assign(textElement.style, style);
        textElement.textContent = str;
        // Get the length of the text in the element.
        let ret = textElement.getBBox();
        // Remove the element.
        document
            .body
            .removeChild(svg);
        return {width: ret.width, height: ret.height};
    }

    /**
     * Create the graph line from the current dataset.
     *
     * @return Grouped SVG path.
     * @memberof PanelSpeed
     */
    makePath() {
        // Add the lowest point ((0,0) relative) as the start point of the path.
        let pathD = "M " + this.state.xPadding + " " + this.state.graphHeight;
        // Add all points in the dataset to the path.
        this
            .state
            .data
            .map((point, i) => {
                pathD += " L " + this
                    .getSvgX(point.x)
                    .toFixed(9) + " " + this
                    .getSvgY(point.y)
                    .toFixed(9);

                return 0;
            });
        /* Add the point farthest along the x-axis and lowest on the y-axis, and
         * close the path to fill the area. */
        pathD += " L " + this.props.svgWidth + " " + this.state.graphHeight + " Z";

        return (<path
            className="speedchart_path"
            d={pathD}
            stroke={this.props.pathLine}
            fill={this.props.pathColor}
            strokeWidth={this.props.strokeWidth * 2}/>);
    }

    /**
     * Create the bare axis lines, with no subdivisions.
     *
     * @return Grouped SVG lines.
     * @memberof PanelSpeed
     */
    makeAxis() {
        return (
            <g className="speedchart_axis">
                <line
                    x1={this.state.xPadding}
                    y1={this.state.graphHeight}
                    x2={this.props.svgWidth}
                    y2={this.state.graphHeight}
                    stroke={this.props.axisColor}
                    strokeWidth={this.props.strokeWidth}/>
                <line
                    x1={this.state.xPadding}
                    y1={0}
                    x2={this.state.xPadding}
                    y2={this.state.graphHeight}
                    stroke={this.props.axisColor}
                    strokeWidth={this.props.strokeWidth}/>
            </g>
        );
    }

    /**
     * Create the grid in the graph area.
     *
     * @return Grouped SVG rectangle.
     * @memberof PanelSpeed
     */
    makeGrid() {
        const tenthHeight = this.state.graphHeight / 10;
        const tenthWidth = this.state.graphWidth / 10;
        // Make a path that paints an upside down "L"
        const path = "M0 0 L0 " + tenthHeight + " " + tenthWidth + " " + tenthHeight;

        /* Make a pattern of the above path that is a tenth the size of the
         * graph area and use it to fill a rectangle spanning the whole graph
         * area */
        return (
            <g className="speedchart_grid">
                <defs>
                    <pattern
                        id={"grid"}
                        width={".10"}
                        height={".10"}
                        patternContentUnits={"objectBoundingBox"}>
                        <rect
                            x={"0"}
                            y={"0"}
                            width={"0.1"}
                            height={"0.1"}
                            fill={"none"}
                            stroke={this.props.gridColor}
                            strokeWidth={this.props.strokeWidth / 500}/>
                    </pattern>
                </defs>
                <rect
                    x={this.state.xPadding}
                    y={0}
                    width={this.props.svgWidth - this.state.xPadding}
                    height={this.state.graphHeight}
                    fill={"url(#grid)"}/>
            </g>
        );
    }

    /**
     * Create the graph caption.
     *
     * @return Grouped SVG with the capton text.
     * @memberof PanelSpeed
     */
    makeCaption() {
        /* Place the caption with the center in the middle of the graph. The
         * caption takes up 80% of the graphs with */
        return (
            <g className="speedchart_caption">
                <Text
                    y={this.state.graphHeight / 2}
                    x={this.state.graphWidth / 2 + this.state.xPadding}
                    verticalAnchor="middle"
                    textAnchor="middle"
                    width={this.state.graphWidth * 0.8}
                    scaleToFit
                    stroke={this.props.textColor}
                    fill={this.props.textColor}>
                    {this.state.text}
                </Text>
            </g>
        );
    }

    /**
     * Create unit labels at the end point of each axis.
     *
     * @return Grouped SVG with axis label text.
     * @memberof PanelSpeed
     */
    makeUnitLabels() {
        // Get the bounds of the labels text.
        const timeBounds = this.getStringBounds(this.props.xUnitLabel, {})
        const speedBounds = this.getStringBounds(this.props.yUnitLabel, {})

        // Create the label in the right places.
        return (
            <g className="speedchart_axis_labels">
                <Text
                    y={this.props.svgHeight / 100}
                    x={this.state.graphWidth / 100 + this.state.xPadding}
                    verticalAnchor="start"
                    textAnchor="start"
                    scaleToFit
                    stroke={this.props.textColor}
                    fill={this.props.textColor}
                    width={speedBounds.width}>
                    KiB/s
                </Text>
                <Text
                    y={this.state.graphHeight - timeBounds.height}
                    x={this.props.svgWidth - timeBounds.width}
                    verticalAnchor="start"
                    textAnchor="start"
                    width={timeBounds.width}
                    scaleToFit
                    stroke={this.props.textColor}
                    fill={this.props.textColor}>
                    Time
                </Text>
            </g>
        );
    }

    /**
     * Create ticks along the axes.
     *
     * @return Grouped SVG rectangles with axes ticks as line patterns.
     * @memberof PanelSpeed
     */
    makeAxisTicks() {
        // Calculate the witdh of the axis ticks
        let strokeWidth = this.props.strokeWidth / 500;

        // Do to rectangles with patterns making up the tick lines.
        return (
            <g className="speedchart_axis_ticks">
                <defs>
                    <pattern
                        id={"axis_ticks_y"}
                        x={0}
                        y={0}
                        width={1}
                        height={0.1}
                        patternContentUnits={"objectBoundingBox"}>
                        <line
                            x1={0}
                            y1={0}
                            x2={1}
                            y2={0}
                            stroke={this.props.textColor}
                            strokeWidth={strokeWidth}/>
                    </pattern>
                </defs>
                <rect
                    x={0}
                    width={this.state.xPadding}
                    height={this.state.graphHeight}
                    fill={"url(#axis_ticks_y)"}/>
                <defs>
                    <pattern
                        id={"axis_ticks_x"}
                        x={0}
                        y={0}
                        width={0.1}
                        height={1}
                        patternContentUnits={"objectBoundingBox"}>
                        <line
                            x1={0}
                            y1={0}
                            x2={0}
                            y2={1}
                            stroke={this.props.textColor}
                            strokeWidth={strokeWidth}/>
                    </pattern>
                </defs>
                <rect
                    x={this.state.xPadding + this.state.graphWidth / 10}
                    y={this.state.graphHeight}
                    width={this.state.graphWidth}
                    height={this.state.yPadding}
                    fill={"url(#axis_ticks_x)"}/>
            </g>
        );
    }

    /**
     * Draw axes values.
     * 
     * @return 
     * @memberof PanelSpeed
     */
    makeAxisValue() {
        const color = this.props.textColor;

        let labelBounds = this.getStringBounds('0', {});
        let x = this.state.xPadding - (this.state.xPadding / 10);
        let y = 0;

        let ret = [];
        for (let i = 1; i < 11; i++) {
            y = (this.state.graphHeight) - ((this.state.graphHeight / 10) * i) + (this.state.graphHeight / 40);
            if (this.maxY === 0) {
                ret.push(
                    <Text
                        y={y}
                        x={x}
                        key={i}
                        verticalAnchor={"start"}
                        textAnchor={"end"}
                        width={labelBounds.width}
                        scaleToFit
                        stroke={this.props.textColor}
                        fill={this.props.textColor}>0</Text>
                );
            } else {
                labelBounds = this.getStringBounds(((this.maxY / 10) * i).toString().slice(0, 3), {});
                ret.push(
                    <Text
                        y={y}
                        x={x}
                        key={i}
                        verticalAnchor={"start"}
                        textAnchor={"end"}
                        width={labelBounds.width}
                        scaleToFit
                        stroke={this.props.textColor}
                        fill={this.props.textColor}>{(this.maxY / 10) * i}</Text>
                );
            }
        }

        let label = "00:00";
        labelBounds = this.getStringBounds('00:00', {});
        y = this.props.svgHeight - (this.state.yPadding - 4);
        x = 0;
        let j = 0;

        for (let i = 0; i < 10; i++) {
            x = this.state.xPadding + ((this.state.graphWidth / 10) * (i + 1)) - 4;
            if (this.state.data.length < 10) {
                labelBounds = this.getStringBounds('00:00', {});
                ret.push(
                    <Text
                        y={y}
                        x={x}
                        key={i + 20}
                        verticalAnchor={"start"}
                        textAnchor={"end"}
                        width={labelBounds.width}
                        scaleToFit
                        stroke={this.props.textColor}
                        fill={this.props.textColor}>00:00</Text>
                );
            } else {
                j = Math.floor((this.state.data.length - 1) / 10 * i);
                label = this
                    .state
                    .data[j]
                    .x
                    .toLocaleTimeString()
                    .slice(0, 5);
                labelBounds = this.getStringBounds(label, {});
                ret.push(
                    <Text
                        y={y}
                        x={x}
                        key={i + 20}
                        verticalAnchor={"start"}
                        textAnchor={"end"}
                        width={labelBounds.width}
                        scaleToFit
                        stroke={this.props.textColor}
                        fill={this.props.textColor}>{label}</Text>
                );
            }
        }

        return (
            <g className="speedchart_axis_values_x">{ret}</g>
        );
    }

    render() {
        const {svgHeight, svgWidth} = this.props;

        return (
            <div className={this.state.class}>
                <PanelHeader className={this.state.class} title={this.props.title}/>
                <svg width={svgWidth} height={svgHeight}>
                    {this.makePath()}
                    {this.makeGrid()}
                    {this.makeAxis()}
                    {this.makeAxisTicks()}
                    {this.makeAxisValue()}
                    {this.makeUnitLabels()}
                    {this.makeCaption()}
                </svg>
            </div>
        );
    }
}

PanelSpeed.defaultProps = {
    svgHeight: 350,
    svgWidth: 630,
    gridColor: "#333333",
    axisColor: "white",
    pathColor: "#222222",
    pathLine: "#444444",
    textColor: "white",
    strokeWidth: 2,
    graphSamples: 150,
    graphWait: 6,
    direction: 'receive',
    xUnitLabel: 'Time',
    yUnitLabel: 'KiB/s'
}

PanelSpeed.propTypes = {
    /** Height of the graph */
    svgHeight: PropTypes.number,
    /** Width of the graph */
    svgWidth: PropTypes.number,
    /** Color of the grid */
    gridColor: PropTypes.string,
    /** Color of the axes */
    axisColor: PropTypes.string,
    /** Color of the fill area under the graph line */
    pathColor: PropTypes.string,
    /** Color of the graph line */
    pathLine: PropTypes.string,
    /** Text color */
    textColor: PropTypes.string,
    /** Base line witdh of axes, and grid. The graph line is twice this width */
    strokeWidth: PropTypes.number,
    /** Number of sample points used to draw the graph */
    graphSamples: PropTypes.number,
    /** Number of valus to skip between sampling for the graph */
    graphWait: PropTypes.number,
    /** Trafic direction to show */
    direction: PropTypes.oneOf(['receive', 'send']),
    /** Unit label drawn by the X axis */
    xUnitLabel: PropTypes.string,
    /** Unit label drawn by the Y axis */
    yUnitLabel: PropTypes.string
}

export default PanelSpeed;