import React from 'react';
import PropTypes from 'prop-types';
import PanelText from './PanelText';

class PanelHost extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      size: props.size,
      url: props.url,
      lines: ['none']
    };
  }

  onSocketData(message) {
    let decoded = JSON.parse(message.data);
    let text = decoded['remote_host'].split('\n');
    this.setState({lines: text});
  }

  onSocketClose() {}

  componentDidMount() {
    this.socket = new WebSocket(this.state.url)
    this.socket.onmessage = (m) => this.onSocketData(m)
  }

  render() {
    return (<PanelText
      title={this.props.title}
      lines={this.state.lines}
      size={this.props.size}
      class={"fleft panel-border"}/>);
  }
}

PanelHost.defaultProps = {
  size: 1,
  url: 'ws://127.0.0.1/remote_host',
  title: ''
}

PanelHost.propTypes = {
  /** Grid size of compoment */
  size: PropTypes.number,
  /** Websocket url */
  url: PropTypes.string,
  /** Title */
  title: PropTypes.string
}

export default PanelHost;