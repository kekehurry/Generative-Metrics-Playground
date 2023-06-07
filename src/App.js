import './App.css';
import React, { useState, useEffect } from "react";
import Expand from './components/Expand';



function App() {

  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="App">
      <header className="App-header">
        <div onClick={() => setSidebarOpen(!sidebarOpen)}>
          <Expand />
        </div>
        <h3>Generative CityScope - Metrics</h3>
      </header>
      <div className="App-Content">
        {sidebarOpen &&
          <div className="sidebar">
            <p>Sidebar content goes here</p>
          </div>
        }
        <div className="left">
          <p>Graph</p>
        </div>
        <div className="right">
          <p>dashboard</p>
        </div>
      </div>
    </div>
  );
}

export default App;