import React from 'react';
import PropTypes from 'prop-types';
import PanelText from './PanelText';

class PanelUptime extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      size: props.size,
      url: props.url,
      lines: ['0']
    };
  }

  onSocketData(message) {
    let decoded = JSON.parse(message.data);
    let text = decoded['uptime'].split(',');
    this.setState({lines: text});
  }

  onSocketClose() {}

  componentDidMount() {
    this.socket = new WebSocket(this.state.url)
    this.socket.onmessage = (m) => this.onSocketData(m)
  }

  render() {
    const style = {fontSize: '4.5vh'};
    return <PanelText
      title={this.props.title}
      lines={this.state.lines}
      size={this.props.size}
      class={"fleft panel-border"}/>;
  }
}

PanelUptime.defaultProps = {
    size: 1,
    url: 'ws://127.0.0.1/uptime',
    title: ''
  }
  
  PanelUptime.propTypes = {
    /** Grid size of compoment */
    size: PropTypes.number,
    /** Websocket url */
    url: PropTypes.string,
    /** Title */
    title: PropTypes.string
  }

export default PanelUptime;