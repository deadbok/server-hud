import React from 'react';
import PanelHeader from '../header/PanelHeader';
import PanelText from './PanelText';

class PanelSpeed extends PanelText {
    constructor(props) {
        super(props);
        this.state = {
            class: 'col-' + props.size,
            direction: props.direction,
            text: '0.00 KiB/s',
            max: '0.00 KiB/s',
            data: [
                {
                    x: 0,
                    y: 0,
                    active: true
                }, {
                    x: 1,
                    y: 2,
                    active: true
                }, {
                    x: 2,
                    y: 3,
                    active: true
                }, {
                    x: 3,
                    y: 1,
                    active: true
                }
            ],
            sample: 5
        };
        this.i = 0;
    }

    onSocketOpen() {
        console.log('Connection established!')
    }

    onSocketData(message) {
        let decoded = JSON.parse(message.data);
        this.setState({
            text: decoded[this.state.direction]
        });
        this.i++;
        if (this.i > this.state.sample) {
            var arrayvar = this
                .state
                .data
                .slice();
            arrayvar.shift();
            arrayvar.push({
                x: new Date().getTime(),
                y: parseFloat(decoded[this.state.direction]),
                active: true
            });
            this.setState({data: arrayvar});
            this.i = 0;
        }
    }

    onSocketClose() {}

    componentDidMount() {
        this.socket = new WebSocket('ws://malcolm:5000/ws/speed');
        this.socket.onopen = () => this.onSocketOpen();
        this.socket.onmessage = (m) => this.onSocketData(m);
        this.socket.onclose = () => this.onSocketClose();
    }

    getMinX() {
        let ret = this.state.data[0]['x'];
        this.state.data.forEach((elem) => {
            ret = Math.min( ret, elem['x']);
        });
        //console.log('Min X: ' + ret);
        return ret;
    }

    getMaxX() {
        let ret = this.state.data[0]['x'];
        this.state.data.forEach((elem) => {
            ret = Math.max( ret, elem['x']);
        });
        //console.log('Max X: ' + ret);
        return ret;
    }

    getMinY() {
        let ret = this.state.data[0]['y'];
        this.state.data.forEach((elem) => {
            ret = Math.min( ret, elem['y']);
        });
        //console.log('Min Y: ' + ret);
        return ret;       
    }

    getMaxY() {
        let ret = this.state.data[0]['y'];
        this.state.data.forEach((elem) => {
            ret = Math.max( ret, elem['y']);
        });
        //console.log('Max Y: ' + ret);
        return ret;
    }

    getSvgX(x) {
        const {svgWidth} = this.props;
        let ret = x / (this.getMaxX() - this.getMinX()) * svgWidth;
        //console.log('SVG X: ' + ret);
        return ret;
    }

    getSvgY(y) {
        const {svgHeight} = this.props;
        let ret = y / (this.getMaxY() - this.getMinY()) * svgHeight;
        console.log('SVG Y: ' + ret);
        return ret;
    }

    makePath() {
        let pathD = "M " + this.getSvgX(this.state.data[0].x) + " " + this.getSvgY(this.state.data[0].y) + " ";
        pathD += this.state.data.map((point, i) => {
                return "L " + this.getSvgX(point.x) + " " + this.getSvgY(point.y) + " ";
            });

            const styles = {color: this.props.pathColor,
                strokeWidth: this.props.strokeWidth * 2};

        return (<path
            className="linechart_path"
            d={pathD}
            style={styles}
        />);
    }

    makeAxis() {
        const {svgWidth} = this.props;
        const {svgHeight} = this.props;

        const color = this.props.axisColor;
        const strokeWidth = this.props.strokeWidth;

        return (
            <g className="linechart_axis">
                <line x1={0} y1={svgHeight} x2={svgWidth} y2={svgHeight} stroke={color} strokeWidth={strokeWidth}/>
                <line x1={0} y1={0} x2={0} y2={svgHeight} stroke={color} strokeWidth={strokeWidth}/>
            </g>
        );
    }

    makeGrid() {
        const {svgWidth} = this.props;
        const {svgHeight} = this.props;

        const path = "M " + svgHeight + " 0 L 0 0 0 "  + svgHeight;

        const color = this.props.gridColor;
        const strokeWidth = this.props.strokeWidth;

        return (
            <g className="linechart_grid">
                <defs>
                <pattern id={"grid"} width={svgWidth/10} height={svgHeight/10} patternUnits={"userSpaceOnUse"}>
                    <path d={path} fill={"none"} stroke={color} strokeWidth={strokeWidth}/>
                </pattern>
                </defs>
                <rect width={"100%"} height={"100%"} fill={"url(#grid)"} />
            </g>
        );
    }

    renderedTextSize(string, font, fontSize) {
        var paper = Raphael(0, 0, 0, 0);
        paper.canvas.style.visibility = 'hidden';
      
        var el = paper.text(0, 0, string);
        el.attr('font-family', font);
        el.attr('font-size', fontSize);
      
        var bBox = el.getBBox();
        paper.remove();
      
        return {
          width: bBox.width,
          height: bBox.height
        };
      }

    makeCaption() {
        const svgWidth = this.props.svgWidth;
        const svgHeight = this.props.svgHeight;

        const color = this.props.textColor;

        return (
            <g className="linechart_caption">
                <text
                    x={svgWidth/2}
                    y={svgHeight/2}
                    stroke={color}
                    fill={color}
                    fontSize={svgWidth/10}
                    alignmentBaseline={"middle"}
                    textAnchor={"middle"}
                >
                {this.state.text}
            </text>
            </g>
        );
    }

    render() {
        const {svgHeight, svgWidth} = this.props;

        return (
            <div className={this.state.class}>
                <PanelHeader className={this.state.class} title={this.props.title}/>
                <svg width={svgWidth} height={svgHeight}>
                    {this.makePath()}
                    {this.makeCaption()}
                </svg>
            </div>
        );
    }
}
//                    {this.makePath()}
//                    {this.makeGrid()}


PanelSpeed.defaultProps = {
    data: [],
    svgHeight: 350,
    svgWidth: 630,
    gridColor: "#444444",
    axisColor: "#aaaaaa",
    pathColor: "lightgray",
    textColor: "white",
    strokeWidth: 2

}

export default PanelSpeed;