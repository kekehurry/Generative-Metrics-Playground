import './App.css';
import React, { useState, useEffect } from "react";
import Expand from './components/Expand';

import { render } from "react-dom";
import { stateStore } from "./stores";
import styled from "styled-components";

import * as d3 from "d3";

import ResPage from "./components/0.3_resolution/ResPage";
// import PieChart from "./components/0.4_charts/pieChart";
import ChordChart from "./components/0.4_charts/ChordChart_new";
import RadarChart from "./components/0.4_charts/RadarChart";

// import Modal from "./components/Modal";
import {Slider_1, Slider_2, Slider_3, Slider_4} from "./components/Slider"

const CHORD_DATA_PATH = "/data/chord_data_2.csv";
// const PIE_DATA_PATH = "/data/pie_data_2.csv";
const RADAR_DATA_PATH = '/data/radar_data_2.json';

function App() {

  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });

  const [version,setVersion] = useState(1);
  const [isMobile, setIsMobile] = useState(false);
  const [chordData, setChordData] = useState({});
  // const [pieData, setPieData] = useState({});
  const [radarData, setRadarData] = useState({});
  // const [openModal, setOpenModal] = useState(false);

  // const handleClick = () => {
  //   const randomNumber = Math.floor(Math.random() * 201);
  //   setVersion(randomNumber);
  // };

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
        for (const { Stakeholders, Target, [ver]:value } of data)
          matrix[index.get(Stakeholders)][index.get(Target)] += Number(value);

        let content_matrix = Array.from(index, () => new Array(names.length).fill(0));
        for (const {Stakeholders, Target, content} of data) 
          content_matrix[index.get(Stakeholders)][index.get(Target)] = content;
          
        console.log(names, matrix, content_matrix,data);
        setChordData({ names: names, matrix: matrix, content: content_matrix,data: data });
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });

  }, [version]);




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
          {/* <p>Graph</p> */}
          {/* <p>version: {version}</p> */}

          <div className="chart-container">
            <ChordChart className='chord-chart' chord_data={chordData} />

          </div>
          
        </div>
        
        <div className="right">
          {/* <p>dashboard</p> */}

          <div className="slider-container">
            {/* <p>INPUT</p> */}

            <div className="slider-label">
              Residential Space:</div>
            <Slider_1  handleChange1={handleChange1} />

            <div className="slider-label" > 
              Office Space:</div>
            <Slider_2  handleChange2={handleChange2}/>

            <div className="slider-label" > 
              Amenity Space:</div>
            <Slider_3  handleChange3={handleChange3}/>

            <div className="slider-label" > 
              Civic Space:</div>
            <Slider_4  handleChange4={handleChange4}/>
          </div>
          
        </div>

        <div className="right-down">
          {/* <p>radarchart</p> */}
          <RadarChart className='radar-chart' radar_data={radarData} />
        </div>


      </div>
    </div>
  );
}

export default App;

export function renderToDOM(container) {
  render(<App />, container);
}
