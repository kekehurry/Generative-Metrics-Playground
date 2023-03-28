import React, { useEffect, useState } from "react";
import { render } from "react-dom";
import { stateStore } from "./stores";

import * as d3 from "d3";

import ResPage from "./components/0.3_resolution/ResPage";
import IndicatorChart from "./components/0.4_charts/IndicatorChart";

const CHOARD_DATA_PATH = "/data/chord_data_3.csv";

const App = () => {
  //   const { page } = stateStore;

  // responsive design
  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });
  const [isMobile, setIsMobile] = useState(false);
  const [chordData, setChordData] = useState({});

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

  // load date
  useEffect(() => {
    fetch(CHOARD_DATA_PATH)
      .then((response) => response.text())
      .then((csvData) => {
        let data = d3.csvParse(csvData);
        let names = Array.from(
          new Set(data.flatMap((d) => [d.Stakeholders, d.Target]))
        );
        let index = new Map(names.map((name, i) => [name, i]));
        let matrix = Array.from(index, () => new Array(names.length).fill(0));
        for (const { Stakeholders, Target, count } of data)
          matrix[index.get(Stakeholders)][index.get(Target)] += Number(count);

        // console.log(names, matrix);
        setChordData({ names: names, matrix: matrix });
      });
  }, []);

  return isMobile ? (
    <ResPage />
  ) : (
    <div>
      <IndicatorChart chord_data={chordData} />
    </div>
  );
};

export default App;

export function renderToDOM(container) {
  render(<App />, container);
}
