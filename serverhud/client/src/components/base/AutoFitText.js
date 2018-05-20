import React from 'react';
import PropTypes from 'prop-types';

class AutoFitText extends React.Component {
    constructor(props) {
        super(props);
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

    render() {
        let bounds = this.getStringBounds(this.props.text);
        if (this.props.chars > 0)
        {
            bounds = this.getStringBounds(Array(this.props.chars + 1).join('0'));
        }

        let y = this.props.y;
        let x = this.props.x;
        let scale = Math.min(this.props.width / bounds.width, this.props.height / bounds.height);

        if (this.props.maxScale > 0) {
            if (scale > this.props.maxScale) {
                scale = this.props.maxScale;
            }
        }

        scale = scale - (scale / 5);

        let originX = x - scale * x;
        let originY = (bounds.height * scale / 2) + y - scale * y;
        return (

            <text
                y={y}
                x={x}
                textAnchor={this.props.textAnchor}
                stroke={this.props.color}
                fill={this.props.color}
                transform={`matrix(${scale}, 0, 0, ${scale}, ${originX}, ${originY})`}>
                {this.props.text}
            </text>

        );
    }
}

AutoFitText.defaultProps = {
    x: 0,
    y: 0,
    height: 0,
    width: 0,
    text: 0,
    color: "white",
    strokeWidth: 1,
    maxScale: 0,
    textAnchor: "middle",
    chars: 0
}

AutoFitText.propTypes = {
    /** Height of the text */
    height: PropTypes.number,
    /** Width of the text */
    width: PropTypes.number,
    /** Text color */
    color: PropTypes.string,
    /** Base witdh text contour */
    strokeWidth: PropTypes.number
}

export default AutoFitText;