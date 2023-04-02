import React, { useEffect, useState } from "react";
import { render } from "react-dom";
import { stateStore } from "./stores";
import styled from "styled-components";

import "./App.css";

import * as d3 from "d3";

import ResPage from "./components/0.3_resolution/ResPage";
import PieChart from "./components/0.4_charts/pieChart";
import IndicatorChart from "./components/0.4_charts/IndicatorChart";
import RadarChart from "./components/0.4_charts/RadarChart";
import Modal from "./components/Modal";
// import Slider from "./components/slider"


const CHORD_DATA_PATH = "/data/chord_data.csv";
const PIE_DATA_PATH = "/data/pie_new.csv";
const RADAR_DATA_PATH = '/data/radar_all.json';

const Button = styled.button`
    background-color: darkgray;
    color: #FFFFFF;
    &:hover{
      color: white;
    }
    border-radius: 5px;
    box-shadow: 0px 2px 2px lightgray;
    cursor: pointer;
    text-transform: uppercase;
    `;



const App = () => {
  //   const { page } = stateStore;

  // responsive design
  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });
  const [version,setVersion] = useState(1);
  const [isMobile, setIsMobile] = useState(false);
  const [chordData, setChordData] = useState({});
  const [pieData, setPieData] = useState({});
  const [radarData, setRadarData] = useState({});
  const [openModal, setOpenModal] = useState(false);
  // const [value,setValue] = useState(1);

  const handleClick = () => {
    const randomNumber =Math.floor(Math.random()*10);
    setVersion(randomNumber);
  };

  // const changeValue = (event, value) => {
  //   setVersion(value);
  // };


  
  //   const [version, setVersionData] = useState({}); 用这里

  // const version = pieData.range([1, 10], {value: 10, step: 1, label: "Version"});
  // 改这里
  // const version =Math.floor(Math.random()*10);

  // const version = randomNumber;

  function buildHierarchy(csv) {
    // Helper function that transforms the given CSV into a hierarchical format.
    const root = { name: "root", children: [] };
    for (let i = 0; i < csv.length; i++) {
      const sequence = csv[i][0];
      const size = +csv[i][version];
      if (isNaN(size)) {
        // e.g. if this is a header row
        continue;
      }
      const parts = sequence.split("-");
      let currentNode = root;
      for (let j = 0; j < parts.length; j++) {
        const children = currentNode["children"];
        const nodeName = parts[j];
        let childNode = null;
        if (j + 1 < parts.length) {
          // Not yet at the end of the sequence; move down the tree.
          let foundChild = false;
          for (let k = 0; k < children.length; k++) {
            if (children[k]["name"] == nodeName) {
              childNode = children[k];
              foundChild = true;
              break;
            }
          }
          // If we don't already have a child node for this branch, create it.
          if (!foundChild) {
            childNode = { name: nodeName, children: [] };
            children.push(childNode);
          }
          currentNode = childNode;
        } else {
          // Reached the end of the sequence; create a leaf node.
          childNode = { name: nodeName, value : size };
          children.push(childNode);
        }
      }
    }
    return root;
  }

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

  // load pie data
  useEffect(() => {
    fetch(PIE_DATA_PATH)
      .then((response) => response.text())
      .then((csvData) => {
      
        let data = d3.csvParseRows(csvData);
        let pie_data = buildHierarchy(data);
        
        let partition = data => {
          const root = d3.hierarchy(data)
              .sum(d => d.value)
              .sort((a, b) => b.value - a.value);
          return d3.partition()
              .size([2 * Math.PI, root.height + 1])
            (root);
        };

        let root = partition(pie_data);
        console.log("root:", root);

        setPieData({ root: root, pie_data: pie_data, data: data });
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
        const axesLength =  vers[0].length;
        const axesDomain = vers[0].map(d => d.axis)

        console.log( data,vers, axesLength, axesDomain);
        setRadarData({ data: data ,vers: vers, axesLength: axesLength, axesDomain:axesDomain});
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });
  }, [version]);

  

  return isMobile ? (
    <ResPage />
  ) : (
    <div className="App">
      <h1 style={{ color: "white", fontSize: "60px",position: "relative", top: "60px", textAlign: "center" }}>
        Generative CityScope - Metrics
      </h1>
      <h2 style={{ color: "white", fontSize: "40px",position: "relative", top: "30px", textAlign: "center"}}>
        Define the future community
      </h2>

      <PieChart pieData={pieData}/>
      <IndicatorChart chord_data={chordData} />
      <RadarChart radar_data={radarData} />

      <Button  
        className="openModalBtn" 
        onClick={() => {
          setOpenModal(true);
        }}
        style ={{ position: "fixed", top: "30%", left: "40%", transform: "translate(-50%, -50%)"}} 
      >
        Generate
      </Button>
      {openModal && <Modal closeModal={setOpenModal} />}

      <Button onClick={handleClick} className="openModalBtn" style={{position: "fixed", top: "30%", left: "60%", transform: "translate(-50%, -50%)"}}>
      {/* style={{ color: "black", fontSize: "20px",position: "relative", top: "60px", left:"750px"}} */}
        See Performance
      </Button>

      {/* <Slider  >
      </Slider> */}


    </div>
  );
};

export default App;

export function renderToDOM(container) {
  render(<App />, container);
}
