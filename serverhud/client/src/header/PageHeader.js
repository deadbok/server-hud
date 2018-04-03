import React from 'react';

class PageHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      date: new Date(),
      title: props.title
    };
  }

  componentDidMount() {
    this.timerID = setInterval(() => this.tick(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({date: new Date()});
  }
  render() {
    return <div className="header">
      <div className="text-center" id="clock">{this.state.title} - {window.location.hostname} - {this.state.date.toLocaleTimeString()}
      </div>
    </div>;
  }
}

export default PageHeader;