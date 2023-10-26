import './App.css';
import WelcomePage from './components/WelcomePage';
import React, { useState, useEffect } from "react";
import Expand from './components/Expand';

import { render } from "react-dom";
import { stateStore } from "./stores";
import styled from "styled-components";

import * as d3 from "d3";

// import ResPage from "./components/0.3_resolution/ResPage";
// import PieChart from "./components/0.4_charts/pieChart";
import ChordChart from "./components/0.4_charts/ChordChart_new";
import BubbleChart from "./components/0.4_charts/BubbleChart";
import RadarChart from "./components/0.4_charts/RadarChart";
// import WelcomePage from './components/0.1_welcome/WelcomePage';


// import Modal from "./components/Modal";
// import { Slider_1, Slider_2, Slider_3, Slider_4 } from "./components/Slider"

import CombinedSlider from './components/Slider_new';

// read data from backend
// const CHORD_DATA_PATH = "/data/chord_data_2.csv";
// const BUBBLE_DATA_PATH = "/data/bubble_data.csv";
// const PIE_DATA_PATH = "/data/pie_data_2.csv";
// const RADAR_DATA_PATH = '/data/radar_data_3.json';

import io from 'socket.io-client';
// 开发：flase 生产：true
const BUILD_MODE = false
const host_addr = BUILD_MODE ? "" : "http://127.0.0.1:5001"


const Button = styled.button`
  width: 100px;
  height: 40px;
  background-color: darkblue;
  color: #FFFFFF;
  border-radius: 5px;
  box-shadow: 5px;
  cursor: pointer;
  text-transform: uppercase;
  font-size: 15px;
  `;


function App() {

  const [showGraph, setShowGraph] = useState(false);
  const [selectedStakeholder, setSelectedStakeholder] = useState('Developer');
  const [selectedScore, setSelectedScore] = useState(0);

  function enterSite() {
    setShowGraph(true);
  }

  // 这是一个异步函数，用于触发后端的计算
  async function triggerComputation() {
    try {
        const response = await fetch(`${host_addr}/api/compute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data.message);
    } catch (error) {
        console.error('Error during the computation:', error);
        throw error; // 重新抛出错误，以便外部代码可以捕获它
    }
  }

  const fetchDataFromServer = async () => {
    try {
        const responses = await Promise.all([
          fetch(`${host_addr}/api/get_data/indicator.json`),
          fetch(`${host_addr}/api/get_data/bubble_data.json`),
          fetch(`${host_addr}/api/get_data/index_score.json`),
          fetch(`${host_addr}/api/get_data/radar_data.json`)
        ]);

        // 解析 JSON 数据
        const data = await Promise.all(responses.map(response => response.json()));
        console.log('Received ALL JSON data:', data); // 打印 JSON 数据
        // 更新状态
        setChordData(data[0]);
        setBubbleData(data[1]);
        setIndicatorData(data[2]);
        setRadarData(data[3]);

        loadRadarData();
        loadChordData();
        loadBubbleData();
        loadIndicatorData();

    } catch (error) {
        console.error("Error fetching data:", error);
    } 
  };

  const sendDataToServer = async () => {
    const payload = {
      bcr: bcr,
      tier: tier,
      residential: residential, 
      office: office,
      amenity: amenity,
      civic: civic
    };
    console.log("Sending data:", payload); // 打印将要发送的数据

    try {
        const response = await fetch(`${host_addr}/api/receive_values`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload),
        });

        if(!response.ok) {
          throw new Error(`Server responded with an error`);
        }
        console.log('INPUT Data sent to receive_values');

        // 然后发送数据到 save_data 路由
        const saveResponse = await fetch(`${host_addr}/api/save_data/input`, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!saveResponse.ok) {
            throw new Error('Server responded with an error for save_data');
        }

        console.log('INPUT Data sent to save_data');

        const data = await response.json();
        console.log(data.message);  // 打印从Flask返回的消息

        // 在 sendDataToServer 函数内触发计算并获取数据
        await triggerComputation();  // 等待计算完成
        console.log('Calculation done!');

        // 计算完成后，再次获取数据
        await fetchDataFromServer();

    } catch (error) {
        console.error("Error sending data:", error);
    }
  };


  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });

  // for test
  // const [version, setVersion] = useState(1);
  // for real
  const [bcr, setBCR] = useState(0.6);
  const [tier, setTier] = useState(3);
  const [residential, setResidential] = useState(0.2);
  const [office, setOffice] = useState(0.3);
  const [amenity, setAmenity] = useState(0.2);
  const [civic, setCivic] = useState(0.3);

  const [isMobile, setIsMobile] = useState(false);
  const [chordData, setChordData] = useState({});
  const [indicatorData, setIndicatorData] = useState([]); 
  const [bubbleData, setBubbleData] = useState({});
  // const [pieData, setPieData] = useState({});
  const [radarData, setRadarData] = useState({});
  // const [openModal, setOpenModal] = useState(false);

  // const handleClick = () => {
  //   const randomNumber = Math.floor(Math.random() * 201);
  //   setVersion(randomNumber);
  // };
  const [selectedButton, setSelectedButton] = useState('label1');


  // ------------------key from user input-------------------------------
  // --------------------------------------------------------------------
  // for test  
  // const handleChange1 = (value) => {
  //   setVersion(value);
  // };
  // const handleChange2 = (value) => {
  //   setVersion(value);
  // };
  // const handleChange3 = (value) => {
  //   setVersion(value);
  // };
  // const handleChange4 = (value) => {
  //   setVersion(value);
  // };

  // for real
  const handleChange1 = (values) => {

    // 从 values 数组中提取值
    const [receivedValue1, receivedValue2, receivedValue3, receivedValue4] = values;

    console.log("Received values: ", values);
    // console.log("Calculated values: ", residential, office, amenity, civic);

    // 更新状态
    setResidential(receivedValue1);
    // sendDataToServer(receivedValue1);
    setOffice(receivedValue2);
    // sendDataToServer(receivedValue2);
    setAmenity(receivedValue3);
    // sendDataToServer(receivedValue3);
    setCivic(receivedValue4);
    // sendDataToServer(receivedValue4);
    
  };

  // const handleChange1 = (value) => {
  //   setResidential(value);
  //   sendDataToServer();
  // };

  // const handleChange2 = (value) => {
  //   setOffice(value);
  //   sendDataToServer();
  // };

  // const handleChange3 = (value) => {
  //   setAmenity(value);
  //   sendDataToServer();
  // };

  // const handleChange4 = (value) => {
  //   setCivic(value);
  //   sendDataToServer();
  // };

  // // BCR
  // const handleChange5 = (value) => {
  //   setBCR(value);
  // };

  // // Tier
  // const handleChange6 = (value) => {
  //   setTier(value);
  // };

  // BCR
  const handleChange5 = (e) => {
    setBCR(parseFloat(e.target.value));
    // sendDataToServer();
  };

  // Tier
  const handleChange6 = (e) => {
    setTier(parseInt(e.target.value, 10));
    // sendDataToServer();
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

  // color setting for progress bar
  const bgColor = [
    {stakeholder: "Residents", bgcolor: "#7178B5"},
    {stakeholder: "Local Business Owners", bgcolor: "#0FACA3"},
    {stakeholder: "Nonprofit Institution", bgcolor: "#7ec1ca"},
    {stakeholder: "Government", bgcolor: "#a5ba37"},
    {stakeholder: "Workforce", bgcolor: "#f6bd0d"},
    {stakeholder: "Industry Group", bgcolor: "#e27c40"},
    {stakeholder: "Developer", bgcolor: "#9b47a2"}
  ];
  // data for progress bar & indicator bar
  // data from backend：
  // stakeholders.py: index_score.csv (data for chord chart: interaction value)
  // const allTestData = [
  //   { stakeholder: "Developer", indicator: "Taxes", baseline: 25, score: 60 },
  //   { stakeholder: "Developer", indicator: "Social cohesion",baseline: 50, score: 55 },
  //   { stakeholder: "Developer", indicator: "Management cost", baseline: 22, score: 77 },
  //   { stakeholder: "Developer", indicator: "Pollution",baseline: 84, score: 23 },
  //   { stakeholder: "Developer", indicator: "Equity", baseline: 20, score: 36 },
  //   { stakeholder: "Developer", indicator: "Safety & Security", baseline: 40, score: 35 },
  //   { stakeholder: "Developer", indicator: "Voting rate", baseline: 50, score: 33 },
  //   { stakeholder: "Government",indicator: "Taxes",baseline: 25, score: 60 },
  //   { stakeholder: "Government",indicator: "Social cohesion",baseline: 40, score: 55 },
  //   { stakeholder: "Government",indicator: "Management cost", baseline: 25, score: 77 },
  //   { stakeholder: "Industry group",indicator: "Taxes",baseline: 25,score: 60 },
  //   { stakeholder: "Industry group",indicator: "Social cohesion", baseline: 20,score: 55 },
  //   { stakeholder: "Industry group",indicator: "Management cost", baseline: 25, score: 77 },
  //   { stakeholder: "Local Business Owners",indicator: "Taxes", baseline: 25,score: 60 },
  //   { stakeholder: "Local Business Owners",indicator: "Social cohesion", baseline: 25,score: 55 },
  //   { stakeholder: "Local Business Owners",indicator: "Management cost", baseline: 25, score: 77 },
  //   { stakeholder: "Nonprofit Institution",indicator: "Taxes", baseline: 25,score: 60 },
  //   { stakeholder: "Nonprofit Institution",indicator: "Social cohesion", baseline: 25,score: 55 },
  //   { stakeholder: "Nonprofit Institution",indicator: "Management cost", baseline: 25, score: 77 },
  //   { stakeholder: "Residents",indicator: "Taxes", baseline: 25,score: 60 },
  //   { stakeholder: "Residents",indicator: "Social cohesion", baseline: 25,score: 55 },
  //   { stakeholder: "Residents",indicator: "Management cost", baseline: 25, score: 77 },
  //   { stakeholder: "Workforce",indicator: "Taxes", baseline: 25,score: 60 },
  //   { stakeholder: "Workforce",indicator: "Social cohesion", baseline: 25,score: 55 },
  //   { stakeholder: "Workforce",indicator: "Management cost", baseline: 25, score: 77 }
  // ];

  // const selectedData = allTestData.filter(data => data.stakeholder === selectedStakeholder);
  
  const getBgColor = (stakeholderName) => {
    const stakeholderObj = bgColor.find(s => s.stakeholder === stakeholderName);
    return stakeholderObj ? stakeholderObj.bgcolor : '#e0e0de';  // Default color in case stakeholder not found
  }

  // progress bar component （right up）
  const ProgressBar = (props) => {
    const { score, indicator, stakeholder} = props;

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

  // const bubbleTestData = [
  //   { stakeholder: "Developer", score: 70, radius: 40, distance: 25 },
  //   { stakeholder: "Government", score: 30, radius: 62, distance: 200 },
  //   { stakeholder: "Industry group", score: 30, radius: 85, distance: 30 },
  //   { stakeholder: "Local Business Owners", score: 40, radius: 95, distance: 200 },
  //   { stakeholder: "Nonprofit Institution", score: 100, radius: 105, distance: 100 },
  //   { stakeholder: "Residents", score: 10, radius: 25, distance: 10 },
  //   { stakeholder: "Workforce", score: 80, radius: 25, distance: 80 }
  // ];
    
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
  // useEffect(() => {
  //   fetch(CHORD_DATA_PATH)
  //     .then((response) => response.text())
  //     .then((csvData) => {
  //       let data = d3.csvParse(csvData);
  //       delete data.columns;
  //       let names = Array.from(
  //         new Set(data.flatMap((d) => [d.Stakeholders, d.Target]))
  //       );
  //       // let ver = `value_${version}`;
  //       let ver = `value_1`;  // this should be simulated result
  //       let index = new Map(names.map((name, i) => [name, i]));
  //       let matrix = Array.from(index, () => new Array(names.length).fill(0));
  //       for (const { Stakeholders, Target, [ver]: value } of data)
  //         matrix[index.get(Stakeholders)][index.get(Target)] += Number(value);

  //       let content_matrix = Array.from(index, () => new Array(names.length).fill(0));
  //       for (const { Stakeholders, Target, content } of data)
  //         content_matrix[index.get(Stakeholders)][index.get(Target)] = content;

  //       console.log(names, matrix, content_matrix, data);
  //       setChordData({ names: names, matrix: matrix, content: content_matrix, data: data });
  //     })

  //     .catch((error) => {
  //       console.error("Error fetching the data:", error);
  //     });

  // // }, [version]);
  //   }, []);

  // load chord data
  const loadChordData = () => {
    fetch(`${host_addr}/api/get_data/indicator.json`)
        .then((response) => response.json())  // 解析返回的 JSON 数据
        .then((data) => {
            console.log('Received chord JSON data:', data); // 打印 JSON 数据
            // 然后，处理和转换从Flask后端返回的jsonData?
            // let data = d3.csvParse(jsonData);
            // delete data.columns;
            let names = Array.from(
              new Set(data.flatMap((d) => [d.stakeholder]))
            );

            let ver = `value`;  // this should be simulated result
            
            let index = new Map(names.map((name, i) => [name, i]));
            let matrix = Array.from(index, () => new Array(names.length).fill(0));
            for (const { stakeholder, target,  value } of data)
              matrix[index.get(stakeholder)][index.get(target)] += Number(value);

            let indicator_matrix = Array.from(index, () => new Array(names.length).fill(0));
            for (const { stakeholder, target, indicator } of data)
              indicator_matrix[index.get(stakeholder)][index.get(target)] = indicator;

            console.log(names, matrix, indicator_matrix, data);
            setChordData({ names: names, matrix: matrix, indicator: indicator_matrix, data: data });
        })
        .catch((error) => {
            console.error("Error fetching the data:", error);
        });
      };

  useEffect(() => {
    loadChordData();
    }, []);

  // load bubble data
  const loadBubbleData = () => {
    fetch(`${host_addr}/api/get_data/bubble_data.json`)
      .then((response) => response.json())  // 解析返回的 JSON 数据
      .then((data) => {
        console.log('Received bubble JSON data:', data); // 打印 JSON 数据
        
        setBubbleData(data);
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });
    };

  useEffect(() => {
    loadBubbleData();
    } , []);

  // load indicator data
  const loadIndicatorData = () => {
    fetch(`${host_addr}/api/get_data/index_score.json`)
      .then((response) => response.json())  // 解析返回的 JSON 数据
      .then((data) => {
        console.log('Received indicator JSON data:', data); // 打印 JSON 数据
        
        setIndicatorData(data);
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });
    };

  useEffect(() => {
    loadIndicatorData();
    } , []);


  const selectedData = indicatorData.filter(data => data.stakeholder === selectedStakeholder);

  // // load radar data
  // useEffect(() => {
  //   fetch(RADAR_DATA_PATH)
  //     .then((response) => response.json())
  //     .then(data => {
  //       let vers = data[1];
  //       const axesLength = vers[0].length;
  //       const axesDomain = vers[0].map(d => d.axis)
  //       const axesCategory = vers[0].map(d => d.category) // Add this line


  //       console.log(data, vers, axesLength, axesDomain);
  //       setRadarData({ data: data, vers: vers, axesLength: axesLength, axesDomain: axesDomain, axesCategory: axesCategory });
  //     })

  //     .catch((error) => {
  //       console.error("Error fetching the data:", error);
  //     });
  // }, []);

  // load radar data
  const loadRadarData = () => {
    fetch(`${host_addr}/api/get_data/radar_data.json`)
      .then((response) => response.json()) // 解析返回的 JSON 数据
      .then(data => {
        console.log('Received radar JSON data:', data); // 打印 JSON 数据
        
        const axesLength = data[0].length;
        const axesDomain = data[0].map(d => d.indicator);
        const axesCategory = data[0].map(d => d.category);
    
        // console.log(data,  axesLength, axesDomain, axesCategory);
        setRadarData({ data: data, axesLength: axesLength, axesDomain: axesDomain, axesCategory: axesCategory });
      })

      .catch((error) => {
        console.error("Error fetching the data:", error);
      });
    };

  useEffect(() => {
    loadRadarData();
    } , []);

useEffect(() => {
      const socket = io(`${host_addr}`);
  
      socket.on('connect', () => {
          console.log('Connected to the server!');
      });
  
      socket.on('refresh', (data) => {
          console.log('Received message:', data);
          fetchDataFromServer();
      });
  
      return () => {
          socket.disconnect();
      };
  }, []);

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
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
                <button
                  onClick={() => setSelectedButton('label1')}
                  style={{
                    backgroundColor: selectedButton === 'label1' ? '#5A5A89' : '#191932',
                    color: 'white',
                    border: 'none',
                    width: '120px',
                    height: '30px',
                    // marginRight: '5px',
                    borderRadius: '5px',
                    marginLeft: '140px'
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
                    width: '120px',
                    height: '30px',
                    // marginLeft: '5px',
                    borderRadius: '5px',
                    // marginLeft: '200px'
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
                <ChordChart className='chord-chart' chord_data={chordData} bubble_data={bubbleData} indicator_data={indicatorData} onStakeholderClick={setSelectedStakeholder} onScoreClick={setSelectedScore}/>
                :
                <BubbleChart className='chord-chart' chord_data={chordData} bubble_data={bubbleData} onStakeholderClick={setSelectedStakeholder} onScoreClick={setSelectedScore} />
                // <div><p>Another component</p></div>
              }
            </div>

          </div>

          <div className="right" style={{ fontSize: '14px', width: '600px', height: '28%', boxSizing: 'border-box', color: 'white', padding: '0 20px 0 0' }}>
            <p style={{ fontFamily: 'inter', fontWeight: 'bold',fontSize: '22px', textAlign: 'left',marginBottom:'10px' }}>{selectedStakeholder ? `${selectedStakeholder}` : "Stakeholder"}</p>
            <p style={{ fontFamily: 'sans-serif', fontSize: '28px', textAlign: 'left', fontWeight: 'bold', fontStyle:'italic',marginTop:'0px', marginBottom:'20px' }}>{selectedScore ? `${selectedScore}` : "Score"} </p>
            {splitTestData.map((chunk, chunkIndex) => (
              <div style={{ width: '80%', display: 'flex', justifyContent: 'space-between', marginTop:'0px',marginBottom:'0px' }} key={chunkIndex}>
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

            <div className="slider-container" >
              {/* <p>INPUT</p > */}
              <div className='slider-label' style={{ display: 'flex', flexDirection: 'column', padding: '2px 0 0 0'}}>
                Building Coverage Ratio
                {/* <input type="number" placeholder="0.6" step="0.1" min="0" max="1" handleChange5={handleChange5} /> */}
                <input 
                  type="number" 
                  placeholder="0.6" 
                  step="0.1" 
                  min="0" 
                  max="1" 
                  value={bcr} 
                  onChange={handleChange5} 
                />
              </div>

              <div className='slider-label' style={{ display: 'flex', flexDirection: 'column', padding: '2px 0 0 0'}}>
                Tier Number    
                {/* <input type="number" placeholder="3" step="1" min="0" max="30" handleChange6={handleChange6} /> */}
                <input 
                  type="number" 
                  placeholder="3" 
                  step="1" 
                  min="0" 
                  max="30" 
                  value={tier} 
                  onChange={handleChange6} 
                />
              </div>

              <div className="slider-label">
                <CombinedSlider value = {[residential, office, amenity, civic]} handleChange={handleChange1}
                />
              </div>

              <div className="values">
                <div style={{margin: '0 10px'}}>Residential Space: {residential.toFixed(2)}</div>
                <div style={{margin: '0 10px'}}>Office Space: {office.toFixed(2)}</div>
                <div style={{margin: '0 10px'}}>Amenity Space: {amenity.toFixed(2)}</div>
                <div style={{margin: '0 10px'}}>Civic Space: {civic.toFixed(2)}</div>
              </div>

              {/* <div className="slider-label">
                <Slider_1 handleChange1={handleChange1} />
              </div> */}

              {/* <div className="slider-label" >
                <Slider_2 handleChange2={handleChange2} max={1 - residential} />
              </div>


              <div className="slider-label" >
                <Slider_3 handleChange3={handleChange3} max={1 - residential - office}/>
              </div>


              <div className="slider-label" >
                <Slider_4 handleChange4={handleChange4} max={1- residential-office-amenity}/>
              </div> */}

              <div className="button" style={{margin: '0 50px'}}>
                <Button onClick={sendDataToServer}>Send Data</Button>
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