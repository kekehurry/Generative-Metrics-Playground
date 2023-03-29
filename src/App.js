import React, { useEffect, useState } from "react";
import { render } from "react-dom";
import { stateStore } from "./stores";

import * as d3 from "d3";

import ResPage from "./components/0.3_resolution/ResPage";
import IndicatorChart from "./components/0.4_charts/IndicatorChart";
import PieChart from "./components/0.4_charts/PieChart";

const CHOARD_DATA_PATH = "/data/chord_new.csv";
const PIE_DATA_PATH = "/data/pie_new.csv";

const App = () => {
  //   const { page } = stateStore;

  // responsive design
  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });
  const [isMobile, setIsMobile] = useState(false);
  const [chordData, setChordData] = useState({});
  const [pieData, setPieData] = useState({});

  // const version = pieData.range([1, 10], {value: 10, step: 1, label: "Version"});
  const version =6;

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
    fetch(CHOARD_DATA_PATH)
      .then((response) => response.text())
      .then((csvData) => {
        let data = d3.csvParse(csvData);
        delete data.columns;
        let names = Array.from(
          new Set(data.flatMap((d) => [d.Stakeholders, d.Target]))
        );
        let version = `value_${Math.floor(Math.random()*10)}`;
        let index = new Map(names.map((name, i) => [name, i]));
        let matrix = Array.from(index, () => new Array(names.length).fill(0));
        for (const { Stakeholders, Target, [version]:value } of data)
          matrix[index.get(Stakeholders)][index.get(Target)] += Number(value);

        console.log(names, matrix, data);
        setChordData({ names: names, matrix: matrix, data: data });
      });

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

  }, []);

  // load pie data
  useEffect(() => {
    fetch(PIE_DATA_PATH)
      .then((response) => response.text())
      .then((csvData) => {
        let sample = d3.csvParseRows(csvData);
        delete sample.columns;
        let data = buildHierarchy(sample)
        let root = d3.hierarchy(data).sum(d => d.value).sort((a, b) => b.value - a.value);
        let partition = d3.partition().size([2 * Math.PI, root.height + 1])
        let version = 1

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
       // process data
        setPieData({ sample: sample, data: data, partition: partition });
      });
  }, []);

  return isMobile ? (
    <ResPage />
  ) : (
    <div>
      <IndicatorChart chord_data={chordData} />
      <PieChart pieData={pieData}/>
    </div>
  );
};

export default App;

export function renderToDOM(container) {
  render(<App />, container);
}
