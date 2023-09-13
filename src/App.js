import './App.css';
import WelcomePage from './components/WelcomePage';
import React, { useState, useEffect } from "react";
import Expand from './components/Expand';

import { render } from "react-dom";
import { stateStore } from "./stores";
import styled from "styled-components";

import * as d3 from "d3";

import ResPage from "./components/0.3_resolution/ResPage";
// import PieChart from "./components/0.4_charts/pieChart";
import ChordChart from "./components/0.4_charts/ChordChart_new";
import BubbleChart from "./components/0.4_charts/BubbleChart";
import RadarChart from "./components/0.4_charts/RadarChart";
// import WelcomePage from './components/0.1_welcome/WelcomePage';


// import Modal from "./components/Modal";
import { Slider_1, Slider_2, Slider_3, Slider_4 } from "./components/Slider"

const CHORD_DATA_PATH = "/data/chord_data_2.csv";
const BUBBLE_DATA_PATH = "/data/chord_data_2.csv";
// const PIE_DATA_PATH = "/data/pie_data_2.csv";
const RADAR_DATA_PATH = '/data/radar_data_3.json';



function App() {

  const [showGraph, setShowGraph] = useState(false);
  const [selectedStakeholder, setSelectedStakeholder] = useState(null);
  const [selectedScore, setSelectedScore] = useState(0);

  function enterSite() {
    setShowGraph(true);
  }

  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });

  const [version, setVersion] = useState(1);
  const [isMobile, setIsMobile] = useState(false);
  const [chordData, setChordData] = useState({});
  const [bubbleData, setBubbleData] = useState({});
  // const [pieData, setPieData] = useState({});
  const [radarData, setRadarData] = useState({});
  // const [openModal, setOpenModal] = useState(false);

  // const handleClick = () => {
  //   const randomNumber = Math.floor(Math.random() * 201);
  //   setVersion(randomNumber);
  // };
  const [selectedButton, setSelectedButton] = useState('label1');

  const handleChange1 = (value) => {
    setVersion(value);
  };

  const handleChange2 = (value) => {
    setVersion(value);
  };

  const handleChange3 = (value) => {
    setVersion(value);
  };

  const handleChange4 = (value) => {
    setVersion(value);
  };

  // const ProgressBar = (props) => {
  //   const { bgcolor, completed } = props;
  //   return (
  //     <div>
  //       <div>
  //         <span>{`${completed}%`}</span>
  //       </div>
  //     </div>
  //   );
  // };

  const testData = [
    { name: "Taxes", bgcolor: "#7178B5", completed: 60 },
    { name: "Social cohesion", bgcolor: "#7178B5", completed: 55 },
    { name: "Management cost", bgcolor: "#7178B5", completed: 77 },
    { name: "Pollution", bgcolor: "#7178B5", completed: 23 },
    { name: "Equity", bgcolor: "#7178B5", completed: 36 },
    { name: "Safety & Security", bgcolor: "#7178B5", completed: 35 },
    { name: "Voting rate", bgcolor: "#7178B5", completed: 33 },
  ];

  const ProgressBar = (props) => {
    const { bgcolor, completed, name } = props;

    const containerStyles = {
      height: 10,
      width: '60px',
      backgroundColor: "#e0e0de",
      borderRadius: 50,
      margin: '5px 0'
    }

    const fillerStyles = {
      height: '100%',
      width: `${completed}%`,
      backgroundColor: bgcolor,
      borderRadius: 'inherit',
    }

    const labelStyles = {
      padding: 5,
      color: 'white',
      fontWeight: 'bold',
      fontSize: '14px',
      textAlign: 'left'
    }

    return (
      <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={labelStyles}>{name}</span>
        <div style={containerStyles}>
          <div style={fillerStyles} />
        </div>
      </div>
    );
  };

  // handle windows resize
  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }
    window.addEventListener("resize", handleResize);
    handleResize();
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    if (windowSize.width < 1100 || windowSize.height < 400) setIsMobile(true);
    else setIsMobile("ontouchstart" in document.documentElement);
  }, [windowSize.width, windowSize.height]);

  // load chord data
  useEffect(() => {
    fetch(CHORD_DATA_PATH)
      .then((response) => response.text())
      .then((csvData) => {
        let data = d3.csvParse(csvData);
        delete data.columns;
        let names = Array.from(
          new Set(data.flatMap((d) => [d.Stakeholders, d.Target]))
        );
        let ver = `value_${version}`;
        let index = new Map(names.map((name, i) => [name, i]));
        let matrix = Array.from(index, () => new Array(names.length).fill(0));
        for (const { Stakeholders, Target, [ver]: value } of data)
          matrix[index.get(Stakeholders)][index.get(Target)] += Number(value);

        let content_matrix = Array.from(index, () => new Array(names.length).fill(0));
        for (const { Stakeholders, Target, content } of data)
          content_matrix[index.get(Stakeholders)][index.get(Target)] = content;

        console.log(names, matrix, content_matrix, data);
        setChordData({ names: names, matrix: matrix, content: content_matrix, data: data });
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });

  }, [version]);

  // load bubble data
  useEffect(() => {
    fetch(BUBBLE_DATA_PATH)
      .then((response) => response.text())
      .then((csvData) => {
        let data = d3.csvParse(csvData);
        delete data.columns;
        let names = Array.from(
          new Set(data.flatMap((d) => [d.Stakeholders, d.Target]))
        );
        let ver = `value_${version}`;
        let index = new Map(names.map((name, i) => [name, i]));
        let matrix = Array.from(index, () => new Array(names.length).fill(0));
        for (const { Stakeholders, Target, [ver]: value } of data)
          matrix[index.get(Stakeholders)][index.get(Target)] += Number(value);

        let content_matrix = Array.from(index, () => new Array(names.length).fill(0));
        for (const { Stakeholders, Target, content } of data)
          content_matrix[index.get(Stakeholders)][index.get(Target)] = content;

        console.log(names, matrix, content_matrix, data);
        setBubbleData({ names: names, matrix: matrix, content: content_matrix, data: data });
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });

  }, [version]);

  // load radar data
  useEffect(() => {
    fetch(RADAR_DATA_PATH)
      .then((response) => response.json())
      .then(data => {
        let vers = data[version];
        const axesLength = vers[0].length;
        const axesDomain = vers[0].map(d => d.axis)
        const axesCategory = vers[0].map(d => d.category) // Add this line


        console.log(data, vers, axesLength, axesDomain);
        setRadarData({ data: data, vers: vers, axesLength: axesLength, axesDomain: axesDomain, axesCategory: axesCategory });
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });
  }, [version]);

  // --------------------------------------------welcomepage--------------------------------------------
  if (!showGraph) {
    return <WelcomePage enterSite={enterSite} />;
  } else {
    // --------------------------------------------welcomepage--------------------------------------------

    const splitTestData = [];
    const chunkSize = 2;
    for (let i = 0; i < testData.length; i += chunkSize) {
      splitTestData.push(testData.slice(i, i + chunkSize));
    }

    return (
      <div className="App">
        {/* <WelcomePage/> */}
        <header className="App-header">
          <div onClick={() => setSidebarOpen(!sidebarOpen)}>
            <Expand />
          </div>
          <h3>Generative CityScope - Metrics</h3>
        </header>
        <div className="App-Content">
          {sidebarOpen &&
            <div className="sidebar">
              <p>Sidebar content goes here</p >
            </div>
          }

          <div className="left">
            {/* <p>Graph</p > */}
            {/* <p>version: {version}</p > */}

            {/* <div className="chart-container">
            <ChordChart className='chord-chart' chord_data={chordData} />
          </div> */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
                <button
                  onClick={() => setSelectedButton('label1')}
                  style={{
                    backgroundColor: selectedButton === 'label1' ? '#5A5A89' : '#191932',
                    color: 'white',
                    border: 'none',
                    width: '100px',
                    height: '30px',
                    marginRight: '5px'
                  }}
                >
                  Label1
                </button>
                <button
                  onClick={() => setSelectedButton('label2')}
                  style={{
                    backgroundColor: selectedButton === 'label2' ? '#5A5A89' : '#191932',
                    color: 'white',
                    border: 'none',
                    width: '100px',
                    height: '30px',
                    marginLeft: '5px'
                  }}
                >
                  Label2
                </button>
              </div>

              {/* <div className="chart-container">
              {selectedButton === 'label1' ?
                <ChordChart className='chord-chart' chord_data={chordData} onStakeholderClick={setSelectedStakeholder} />
                :
                <div>Another component or empty div goes here</div>
              }
            </div> */}
            </div>




            {/* <div className="chart-container">
            <ChordChart className='chord-chart' chord_data={chordData} onStakeholderClick={setSelectedStakeholder} />  // Modify this line
          </div> */}
            <div className="chart-container">
              {selectedButton === 'label1' ?
                <ChordChart className='chord-chart' chord_data={chordData} onStakeholderClick={setSelectedStakeholder} onScoreClick={setSelectedScore}/>
                :
                <BubbleChart className='chord-chart' bubble_data={bubbleData} onStakeholderClick={setSelectedStakeholder} onScoreClick={setSelectedScore} />
                // <div><p>Another component</p></div>
              }
            </div>

          </div>

          <div className="right" style={{ fontSize: '14px', width: '600px', height: '30%', boxSizing: 'border-box', color: 'white', padding: '0 20px 0 0' }}>
            <p style={{ fontFamily: 'inter', fontWeight: 'bold',fontSize: '22px', textAlign: 'left' }}>{selectedStakeholder ? `${selectedStakeholder}` : "Stakeholder"}</p>
            <p style={{ fontFamily: 'sans-serif', fontSize: '28px', textAlign: 'left', fontWeight: 'bold', fontStyle:'italic' }}>{selectedScore ? `${selectedScore}` : "Score"} </p>
            {splitTestData.map((chunk, chunkIndex) => (
              <div style={{ display: 'flex', justifyContent: 'space-between' }} key={chunkIndex}>
                {chunk.map((item, idx) => (
                  <div style={{ width: '45%' }} key={idx}>
                    <ProgressBar name={item.name} bgcolor={item.bgcolor} completed={item.completed} />
                  </div>
                ))}
              </div>
            ))}
          </div>

          <div className="right-down">
            {/* <p>radarchart</p > */}
            <RadarChart className='radar-chart' radar_data={radarData} />
          </div>

          <div className="down">
            {/* <p>slider</p > */}

            <div className="slider-container">
              {/* <p>INPUT</p > */}

              <div className="slider-label">
                Residential Space:
                <Slider_1 handleChange1={handleChange1} />
              </div>

              <div className="slider-label" >
                Office Space:
                <Slider_2 handleChange2={handleChange2} />
              </div>


              <div className="slider-label" >
                Amenity Space:
                <Slider_3 handleChange3={handleChange3} />
              </div>


              <div className="slider-label" >
                Civic Space:
                <Slider_4 handleChange4={handleChange4} />
              </div>

            </div>

          </div>


        </div>
      </div>
    );
  }
}

export default App;

export function renderToDOM(container) {
  render(<App />, container);
}