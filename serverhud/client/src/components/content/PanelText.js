import React from 'react';
import PanelHeader from '../header/PanelHeader';

class PanelText extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      class: 'col-' + props.size
    };
  }

  render() {
    return <div className={this.state.class}>
      <PanelHeader className={this.state.class} title={this.props.title}/>
      <div className="panel-body">
        <h1 className="text-center high" id="connections">{this.props.text}</h1>
      </div>
    </div>;
  }
}

export default PanelText;