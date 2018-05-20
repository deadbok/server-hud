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
  render() {
    //Render each line as a separate paragraph
    let scalingValues = [];

    if (this.state.maxBB !== undefined) {
      this
        .props
        .lines
        .forEach(line => {
          let scale = 0.1;
          let currentBB = this.measure(line.trim(), scale);

          while (((this.state.maxBB.width * 0.75) > currentBB.width) && ((this.state.maxBB.height / this.props.lines.length) > currentBB.height)) {
            scale += 2;
            currentBB = this.measure(line.trim(), scale);
          }
          scale -= 2;

          scalingValues.push(scale)
        });
    }

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

            let style = {
              fontSize: scalingValues[i] + 'vh',
              margin: 0,
              textAlign: 'center'
            };

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