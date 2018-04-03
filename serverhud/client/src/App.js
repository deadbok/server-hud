import React, {Component} from 'react';
import ContainerDimensions from 'react-container-dimensions'
//Headers
import PageHeader from './header/PageHeader';
import PanelHeader from './header/PanelHeader';
//Content
import PanelConnected from './content/PanelConnected';
import PanelSpeed from './content/PanelSpeed';
import PanelText from './content/PanelText';
//import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div>
        <PageHeader className="panel-heading" title="serverhud"/>
        <PanelHeader title="Web server stats"/>
        <div className="panel-row">
          <PanelText title="Connected" text="0" size="2"></PanelText>
          <PanelText title="Latest remote address" text="0.0.0.0" size="6"></PanelText>
          <PanelText title="Uptime" text="00:00" size="2"></PanelText>
          <PanelText title="Accesses" text="0" size="2"></PanelText>
        </div>
        <PanelHeader title="Firewall stats"/>
        <div className="panel-row">
          <PanelConnected title="Connected" size="2"/>
          <PanelSpeed title="Receive speed" direction="receive" size="5"/>
          <PanelSpeed title="Send speed" direction="send" size="5"/>
        </div>
      </div>
    );
  }
}

export default App;
