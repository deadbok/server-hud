import React, {Component} from 'react';
//Headers
import PageHeader from './components/header/PageHeader';
import PanelHeader from './components/header/PanelHeader';
//Content
import PanelConnected from './components/content/PanelConnected';
import PanelSpeed from './components/content/PanelSpeed';
import PanelHost from './components/content/PanelHost';
import PanelUptime from './components/content/PanelUptime'
import PanelAccesses from './components/content/PanelAccesses'
import './App.css';

class App extends Component {
  render() {
    return (
      <div>
        <div className="top-row">
          <PageHeader className="panel-heading" title="serverhud"/>
          <PanelHeader title="Web server stats"/> {/* <div className="panel-row"> */}
          <PanelConnected
            title="Connected"
            url="ws://192.168.3.3:5000/ws/connections"
            size={4}
            maxScale={9}
            panel_height={2}/>
          <PanelHost
            url="ws://192.168.3.3:5000/ws/remote_host"
            title="Latest remote address"
            size={8}/>
          <PanelUptime url="ws://192.168.3.3:5000/ws/uptime" title="Uptime" size={4}/>
          <PanelAccesses
            url="ws://192.168.3.3:5000/ws/accesses"
            title="Accesses"
            size={4}/> {/* </div> */}
        </div>
        <div className="bottom-row">
          <PanelHeader title="Firewall stats"/>
          <div className="panel-row">
            <PanelConnected
              title="Connected"
              url="ws://malcolm:5000/ws/connections"
              size={4}
              maxScale={9}
              panel_height={2}/>
            <PanelSpeed
              title="Receive speed"
              direction="receive"
              size={8}
              maxScale={9}
              xAxisDivisions={10}
              yAxisDivisions={5}/>
            <PanelSpeed
              title="Send speed"
              direction="send"
              size={8}
              maxScale={9}
              xAxisDivisions={10}
              yAxisDivisions={5}/>
          </div>
        </div>
        <div className="footer">
          <div className="text-center">
            server-hud Copyright &copy; 2015-2018 Martin Bo Kristensen Gr&oslash;nholdt.
          </div>
        </div>
      </div>
    );
  }
}

export default App;
