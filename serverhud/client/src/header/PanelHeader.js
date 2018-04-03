import React from 'react';

class PanelHeader extends React.Component {
  render() {
    return <div className="panel-heading">
      <div className="text-center">{this.props.title}</div>
    </div>;
  }
}

export default PanelHeader;