import React from 'react';
import PropTypes from 'prop-types';
import PanelHeader from '../header/PanelHeader';
import AutoFitText from '../base/AutoFitText';
import PanelText from './PanelText';

class PanelConnected extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      class: 'col-' + props.size + ' fleft panel-border',
      size: props.size,
      url: props.url,
      connections: 0,
      maxConnections: 10,
      xPadding: props.svgWidth / 20,
      yPadding: props.svgHeight / 20,
      graphWidth: props.svgWidth - props.svgWidth / 20,
      graphHeight: props.svgHeight - props.svgHeight / 20,
      maxBarHeight: 0,
      maxBB: undefined,
      svgHeight: props.svgHeight,
      svgWidth: props.svgWidth
    };
    this.barHeight = 0;
    if (this.props.svgHeight === -1)
    {
      this.autosize = true;
    }
    else{
      this.autosize = false;
    }
  }

  onSocketData(message) {
    let decoded = JSON.parse(message.data)['connections'];
    this.setState({connections: decoded});

    const max = 10 + Math.floor(decoded / 10) * 10
    if (max > this.state.maxConnections) {
      this.setState({maxConnections: max})
    }
  }

  onSocketClose() {}

  updateSize() {
    if (this.autosize) {
      let maxBB = this
        .panelBody
        .getBoundingClientRect();
      this.setState({maxBB: maxBB});

      let style = window.getComputedStyle(this.panelBody, null);
      let paddingX = parseFloat(style.getPropertyValue('padding-left')) + parseFloat(style.getPropertyValue('padding-right'));
      let paddingY = parseFloat(style.getPropertyValue('padding-top')) + parseFloat(style.getPropertyValue('padding-bottom'));

      let width = maxBB.width;
      let height = maxBB.height - paddingY;
      this.setState({svgHeight: height});
      this.setState({svgWidth: width});
      this.setState({
        xPadding: width / 20
      });
      this.setState({
        yPadding: height / 20
      });
      this.setState({
        graphWidth: width - width / 20
      });
      this.setState({
        graphHeight: height - height / 20
      });
      // Subtract yPadding.
      this.setState({
        maxBarHeight: height - height / 20
      });
      this.setState({
        barWidth: width - width / 20 - (width / 20 * 2) - (this.props.strokeWidth * 2)
      });
    }
  }

  componentDidMount() {
    this.socket = new WebSocket(this.state.url)
    this.socket.onmessage = (m) => this.onSocketData(m)

    this.updateSize();
    window.addEventListener("resize", this.updateSize.bind(this));
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.updateSize.bind(this));
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
     * Create the grid in the graph area.
     *
     * @return Grouped SVG rectangle.
     * @memberof PanelSpeed
     */
  makeGrid() {
    /* Make a pattern of the above path that is a tenth the size of the
       * graph area and use it to fill a rectangle spanning the whole graph
       * area */
    const id = 'grid' + Date.now();
    return (
      <g className="speedchart_grid">
        <defs>
          <pattern
            id={id}
            width={"1"}
            height={".2"}
            patternContentUnits={"objectBoundingBox"}>
            <rect
              x={"0"}
              y={"0"}
              width={"1"}
              height={".2"}
              fill={"none"}
              stroke={this.props.gridColor}
              strokeWidth={this.props.strokeWidth / 500}/>
          </pattern>
        </defs>
        <rect
          x={this.state.xPadding}
          y={this.state.yPadding}
          width={this.state.graphWidth - (this.state.xPadding * 2)}
          height={this.state.maxBarHeight}
          fill={`url(#${id})`}/>
      </g>
    );
  }
  /**
     * Create the grid in the graph area.
     *
     * @return Grouped SVG rectangle.
     * @memberof PanelSpeed
     */
  makeBar() {
    this.barHeight = (this.state.maxBarHeight / this.state.maxConnections) * this.state.connections;
    this.barStart = this.state.maxBarHeight - this.barHeight;

    /* Make a pattern of the above path that is a tenth the size of the
      * graph area and use it to fill a rectangle spanning the whole graph
      * area */
    return (
      <g className="connections_bar">
        <rect
          x={this.state.xPadding + (this.props.strokeWidth / 2) + (this.state.barWidth * 0.1)}
          y={this.state.yPadding + this.barStart}
          width={this.state.barWidth * 0.80}
          height={this.barHeight}
          fill={this.props.barColor}
          fillOpacity={0.9}
          stroke={this.props.barLine}
          strokeWidth={this.props.strokeWidth * 2}/>
      </g>
    );
  }

  /**
     * Create the graph caption.
     *
     * @return Grouped SVG with the caption text.
     * @memberof PanelSpeed
     */
  makeCaption() {
    /* Place the caption with the center in the middle of the graph. The
     * caption takes up 80% of the graphs with */
    return (
      <g className="connection_caption">
        <AutoFitText
          x={this.state.graphWidth / 2}
          y={this.state.graphHeight / 2}
          height={this.state.graphHeight}
          width={this.state.barWidth}
          text={this.state.connections}
          color={this.props.textColor}
          strokeWidth={this.props.strokeWidth}
          maxScale={this.props.maxScale}/>
      </g>
    );
  }

  render() {
    if (this.state.maxBB === undefined) {
      return (
        <div className={this.state.class}>
          <PanelHeader className={this.state.class} title={this.props.title}/>
          <div
            className={"panel-body ph" + this.props.panel_height}
            ref={(element) => {
            this.panelBody = element;
          }}></div>
        </div>
      );
    } else {
      return (
        <div className={this.state.class}>
          <PanelHeader className={this.state.class} title={this.props.title}/>
          <div
            className={"panel-body ph" + this.props.panel_height}
            ref={(element) => {
            this.panelBody = element;
          }}>
            <svg
              width={this.state.svgWidth}
              height={this.state.svgHeight}
              display={"block"}>
              {this.makeGrid()}
              {this.makeBar()}
              {this.makeCaption()}
            </svg>
          </div>
        </div>
      );
    }
  }
}

PanelConnected.defaultProps = {
  svgHeight: -1,
  svgWidth: -1,
  gridColor: "#333333",
  barLine: "#444444",
  barColor: "#222222",
  textColor: "white",
  strokeWidth: 2,
  maxScale: 8,
  panel_height: 1,
  autosize: true
}

PanelConnected.propTypes = {
  /** Height of the graph */
  svgHeight: PropTypes.number,
  /** Width of the graph */
  svgWidth: PropTypes.number,
  /** Color of the grid */
  gridColor: PropTypes.string,
  /** Color of the bar */
  barColor: PropTypes.string,
  /** Text color */
  textColor: PropTypes.string,
  /** Base line witdh of axes, and grid. The graph line is twice this width */
  strokeWidth: PropTypes.number,
  panel_height: PropTypes.number
}

export default PanelConnected;