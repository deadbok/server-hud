import React from 'react';
import PropTypes from 'prop-types';
import PanelHeader from '../header/PanelHeader';

class PanelText extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      class: 'col-' + props.size + ' ' + props.class,
      maxBB: undefined
    };
    this.scale = 1;
  }

  measure(text, scale) {
    let el = document.createElement('span');

    el.style.visibility = 'hidden';
    el.style.position = 'absolute';
    el.style.fontSize = scale + 'vh';

    document
      .body
      .appendChild(el);
    el.innerHTML = text;
    let ret = el.getBoundingClientRect();
    el
      .parentNode
      .removeChild(el);
    return (ret);
  }

  componentDidMount() {
    this.setState({
      maxBB: this
        .panelBody
        .getBoundingClientRect()
    });
  }

  /**
   * Render the text component.
   *
   * @return div with component.
   * @memberof PanelText
   */
  // return <p className="high" key={i} style={this.fixWidth(line)}>{line}</p>; },
  // this)
  render() {
    //Render each line as a seperate paragraph
    let boundingBoxes = [];

    let scale = 9999;
    if (this.scale === 1) {
      if (this.state.maxBB !== undefined) {
        this
          .props
          .lines
          .forEach(line => {
            const currentBB = this.measure(line.trim(), 1)

            scale = Math.min(this.state.maxBB.width / currentBB.width, this.state.maxBB.height / currentBB.height, scale);
            boundingBoxes.push(currentBB)
          });
      }
    }
    if (scale === 9999) {
      scale = 1;
    }
    scale = scale / this.props.lines.length;

    scale = scale + 'vh';
    /*transform: "matrix(" + scale + ", 0, 0, " + scale + ", " + originX + ", " + originY + ")"*/
    let style = {
      fontSize: scale,
      margin: 0,
      textAlign: 'center'
    };

    return <div className={this.state.class}>
      <PanelHeader title={this.props.title}/>
      <div
        className={"panel-body ph" + this.props.panel_height}
        ref={(element) => {
        this.panelBody = element;
      }}>
        {this
          .props
          .lines
          .map(function (line, i,) {
            let width = 1;
            let originX = 1;
            let originY = 1;

            if (this.state.maxBB !== undefined) {
              originX = ((this.state.maxBB.width - boundingBoxes[i].width) / 2) * scale;
              originY = (boundingBoxes[i].height * scale * i);
            }

            return <h3 key={i} style={style}>{line.trim()}</h3>;
          }, this)}
      </div>
    </div>;
  }
}

PanelText.defaultProps = {
  size: 1,
  lines: [''],
  class: '',
  panel_height: 1
}

PanelText.propTypes = {
  /** Grid size of component */
  size: PropTypes.number,
  /** Text lines */
  lines: PropTypes.arrayOf(PropTypes.string),
  class: PropTypes.string,
  panel_height: PropTypes.number
}

export default PanelText;