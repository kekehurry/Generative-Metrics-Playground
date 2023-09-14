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
const BUBBLE_DATA_PATH = "/data/bubble_data.csv";
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

  const bgColor = [
    {stakeholder: "Developer", bgcolor: "#7178B5"},
    {stakeholder: "Government", bgcolor: "#0FACA3"},
    {stakeholder: "Industry group", bgcolor: "#7ec1ca"},
    {stakeholder: "Local Business Owners", bgcolor: "#a5ba37"},
    {stakeholder: "Nonprofit Institution", bgcolor: "#f6bd0d"},
    {stakeholder: "Residents", bgcolor: "#e27c40"},
    {stakeholder: "Workforce", bgcolor: "#9b47a2"}
  ];

  const allTestData = [
    { stakeholder: "Developer", indicator: "Taxes", baseline: 25, score: 60 },
    { stakeholder: "Developer", indicator: "Social cohesion",baseline: 50, score: 55 },
    { stakeholder: "Developer", indicator: "Management cost", baseline: 22, score: 77 },
    { stakeholder: "Developer", indicator: "Pollution",baseline: 84, score: 23 },
    { stakeholder: "Developer", indicator: "Equity", baseline: 20, score: 36 },
    { stakeholder: "Developer", indicator: "Safety & Security", baseline: 40, score: 35 },
    { stakeholder: "Developer", indicator: "Voting rate", baseline: 50, score: 33 },
    { stakeholder: "Government",indicator: "Taxes",baseline: 25, score: 60 },
    { stakeholder: "Government",indicator: "Social cohesion",baseline: 40, score: 55 },
    { stakeholder: "Government",indicator: "Management cost", baseline: 25, score: 77 },
    { stakeholder: "Industry group",indicator: "Taxes",baseline: 25,score: 60 },
    { stakeholder: "Industry group",indicator: "Social cohesion", baseline: 20,score: 55 },
    { stakeholder: "Industry group",indicator: "Management cost", baseline: 25, score: 77 },
    { stakeholder: "Local Business Owners",indicator: "Taxes", baseline: 25,score: 60 },
    { stakeholder: "Local Business Owners",indicator: "Social cohesion", baseline: 25,score: 55 },
    { stakeholder: "Local Business Owners",indicator: "Management cost", baseline: 25, score: 77 },
    { stakeholder: "Nonprofit Institution",indicator: "Taxes", baseline: 25,score: 60 },
    { stakeholder: "Nonprofit Institution",indicator: "Social cohesion", baseline: 25,score: 55 },
    { stakeholder: "Nonprofit Institution",indicator: "Management cost", baseline: 25, score: 77 },
    { stakeholder: "Residents",indicator: "Taxes", baseline: 25,score: 60 },
    { stakeholder: "Residents",indicator: "Social cohesion", baseline: 25,score: 55 },
    { stakeholder: "Residents",indicator: "Management cost", baseline: 25, score: 77 },
    { stakeholder: "Workforce",indicator: "Taxes", baseline: 25,score: 60 },
    { stakeholder: "Workforce",indicator: "Social cohesion", baseline: 25,score: 55 },
    { stakeholder: "Workforce",indicator: "Management cost", baseline: 25, score: 77 }
  ];

  const selectedData = allTestData.filter(data => data.stakeholder === selectedStakeholder);

  const getBgColor = (stakeholderName) => {
    const stakeholderObj = bgColor.find(s => s.stakeholder === stakeholderName);
    return stakeholderObj ? stakeholderObj.bgcolor : '#e0e0de';  // Default color in case stakeholder not found
  }

  const ProgressBar = (props) => {
    const { score, indicator, stakeholder, baseline } = props;

    const bgcolor = getBgColor(stakeholder);

    const containerStyles = {
      height: 10,
      width: '60px',
      backgroundColor: "#e0e0de",
      borderRadius: 50,
      margin: '5px 0'
    }

    const fillerStyles = {
      height: '100%',
      width: `${score}%`,
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
        <span style={labelStyles}>{indicator}</span>
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
    for (let i = 0; i < selectedData.length; i += chunkSize) {
      splitTestData.push(selectedData.slice(i, i + chunkSize));
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
                <BubbleChart className='chord-chart' chord_data={chordData} bubble_data={bubbleData} onStakeholderClick={setSelectedStakeholder} onScoreClick={setSelectedScore} />
                // <div><p>Another component</p></div>
              }
            </div>

          </div>

          <div className="right" style={{ fontSize: '14px', width: '600px', height: '30%', boxSizing: 'border-box', color: 'white', padding: '0 20px 0 0' }}>
            <p style={{ fontFamily: 'inter', fontWeight: 'bold',fontSize: '22px', textAlign: 'left' }}>{selectedStakeholder ? `${selectedStakeholder}` : "Stakeholder"}</p>
            <p style={{ fontFamily: 'sans-serif', fontSize: '28px', textAlign: 'left', fontWeight: 'bold', fontStyle:'italic' }}>{selectedScore ? `${selectedScore}` : "Score"} </p>
            {splitTestData.map((chunk, chunkIndex) => (
              <div style={{ display: 'flex', justifyContent: 'space-between' }} key={chunkIndex}>
                {chunk.map((data, idx) => (
                  <div style={{ width: '45%' }} key={idx}>
                    <ProgressBar
                      indicator={data.indicator}
                      score={data.score}
                      stakeholder={data.stakeholder}
                    />
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