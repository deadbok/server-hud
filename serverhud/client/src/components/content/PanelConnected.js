import React from 'react';
import PanelText from './PanelText';

class PanelConnected extends PanelText {
  constructor(props) {
    super(props);
    this.state = {
      size: props.size,
      url: props.url,
      text: '0'
    };
  }

  onSocketData(message) {
    let decoded = JSON.parse(message.data);
    this.setState({text: decoded['connections']});
  }

  onSocketClose() {}

  componentDidMount() {
    this.socket = new WebSocket('ws://malcolm:5000/ws/connections')
    this.socket.onmessage = (m) => this.onSocketData(m)
  }

  render() {
    return <PanelText
      title={this.props.title}
      text={this.state.text}
      size={this.props.size}/>;
  }
}

export default PanelConnected;