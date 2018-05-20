import React from 'react';
import PanelText from './PanelText';

class PanelAccesses extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      size: props.size,
      url: props.url,
      lines: ['0'],
    };
  }

  onSocketData(message) {
    let decoded = [JSON.parse(message.data)['accesses'].toString()];
    this.setState({lines: decoded});
  }

  onSocketClose() {}

  componentDidMount() {
    this.socket = new WebSocket(this.state.url)
    this.socket.onmessage = (m) => this.onSocketData(m)
  }

  render() {
    return <PanelText
      title={this.props.title}
      lines={this.state.lines}
      size={this.props.size}
      class={"fleft panel-border"}/>;
  }
}

export default PanelAccesses;