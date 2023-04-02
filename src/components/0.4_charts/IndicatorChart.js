import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { tip as d3tip } from "d3-v6-tip";
import { useResizeObserver } from "../../utils/useResizeObserver";
import { partition } from "d3";

const innerRadius = 220;
const outerRadius = innerRadius + 15;
const width = 900;
const height = 900;
const radius = 44

const chord = d3
  .chordDirected()
  .padAngle(10 / innerRadius)
  .sortSubgroups(d3.descending)
  .sortChords(d3.descending);

const ribbon = d3
  .ribbonArrow()
  .radius(innerRadius - 3)
  .padAngle(1 / innerRadius);

const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);

// Draw pie circle
const arc_ = d3
  .arc()
  .startAngle(d => d.x0)
  .endAngle(d => d.x1)
  .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
  .padRadius(radius * 1.5)
  .innerRadius(d => d.y0 * radius)
  .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 10));

// on_mouse cover range
const mousearc = d3
  .arc()
  .startAngle(d => d.x0)
  .endAngle(d => d.x1)
  .innerRadius(d => d.y0 * radius )
  .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));


const IndicatorChart = ({ chord_data }) => {
  const ref = useRef();
  const containerRef = useRef();

  const margin = {
    top: 0,
    left: 0,
    bottom: 40,
    right: 0,
  };
  const [containerWidth, containerHeight] = useResizeObserver(containerRef);


  // to add other functions...

  useEffect(() => {
    if (!containerWidth) return;

    if ((!chord_data.names) || (!chord_data.matrix) || (!chord_data.data)) return;
    
    const height = containerHeight ? containerHeight : 0;
    const width = containerWidth ? containerWidth : 500;
    // const color = d3.scaleOrdinal(chord_data.names, d3.schemeCategory10);
    const color = d3.scaleOrdinal()
                    .domain(chord_data.names)
                    .range(['#7178b5', '#0faca3', '#7ec1ca', '#a5ba37', '#f6bd0d', '#e27c40','#9b47a2']);

    // build SVG
    let svg = d3
      .select(ref.current)
      .attr("height", "100%")
      .attr("width", "100%");

    svg
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      // .append("circle") //draw a circle as background
      //   .attr("r", innerRadius+30)
      //   .attr("fill", "white")
      .style("width", "100%")
      .style("height", "auto")
      .attr("font-family", "sans-serif")
      .attr("font-size", 17);
    
    svg.selectAll('*').remove()
      
    let chords = chord(chord_data.matrix);

    for (let i = 0; i < chords.length; i++) {
      for (let j = 0; j < chord_data.data.length; j++) {
        if (
          chord_data.names[chords[i].source.index] ==
          chord_data.data[j].Stakeholders
        ) {
          if (
            chord_data.names[chords[i].target.index] ==
            chord_data.data[j].Target
          ) {
            chords[i].content = chord_data.data[j].content;
          }
        }
      }
    }
    // console.log(chords);

    // Fade arcs the mouse is not over and highlight one the mouse is over
    function onMouseOver_group(_, obj) {
      group.filter((d) => d.index !== obj.index).style("opacity", 0.2);
      // console.log(obj);
      svg
        .selectAll(".chord")
        .filter((d) => d.source.index !== obj.index)
        // .filter((d) => d.target.index !== obj.index)
        .style("opacity", 0.2);
    }

    // Fade chords the mouse is not over and highlight one the mouse is over
    function onMouseOver_chord(_, obj) {
      group
        .filter(
          (d) => d.index !== obj.source.index && d.index !== obj.target.index
        )
        .style("opacity", 0.2);

      svg
        .selectAll(".chord")
        .style("opacity", 0.2)
        .filter((d) => d.source.index == obj.source.index)
        .filter((d) => d.target.index == obj.target.index)
        .style("opacity", 1);

      // console.log(obj);
    }

    //
    function onMouseOut() {
      group.style("opacity", 1);
      svg.selectAll(".chord").style("opacity", 1);
    }


    // create Chart
    let group = svg.selectAll("g").data(chords.groups).join("g");

    // Draw arcs
    group
      .append("path")
      // .attr("id", textId.id)
      .attr("id", (d, i) => `arc${i}`) // 添加弧的id
      .attr("fill", (d) => color(d.index))
      .attr("fill-opacity", "100%")
      .attr("stroke", "black")
      .attr("d", arc)
      .on("mouseover", onMouseOver_group)
      .on("mouseout", onMouseOut)
      ;
    group.raise()
    
    // Label
    group
      .append("text")
      .attr("fill", "white")
      .each((d) => {
        d.angle = (d.startAngle + d.endAngle) / 2;
      })
      .append("textPath")
        .attr("xlink:href", (d, i) => `#arc${i}`) // 引用弧的id
        // .attr("startOffset", "10") // 文本起始位置
        .attr("text-anchor", 'left')
        .attr("dy", "10")
        .text((d) => chord_data.names[d.index])
      ;
    group.raise()
    

    // Draw chords
    svg
      .append("g")
      .attr("fill-opacity", 0.65)
      .selectAll("path")
      .data(chords)
      .join("path")
      .attr("class", "chord")
      .attr("fill", (d) => color(d.source.index))
      .attr("d", ribbon)
      // .style("mix-blend-mode", "multiply")
      .on("mouseover", onMouseOver_chord)
      // .on('mouseover', tooltip.show)
      .on("mouseout", onMouseOut)
      // .on('mouseout', tooltip.hide)
      .append("title")
      .text(
        (d) =>
          `${chord_data.names[d.source.index]} -> ${
            chord_data.names[d.target.index]
          }: \n${chord_data.content[d.source.index][d.target.index]}`
      );
    svg.raise()
  }, [chord_data, containerWidth, containerHeight]);


  return (
    <div
      ref={containerRef}
      style={{
        position: "absolute",
        left: "-50px",
        top: "150px",
        height: "100%",
        width: "40%",
        background: "none"
      }}
    >
      <svg ref={ref}>
        <g />
      </svg>
    </div>
  );
};



export default IndicatorChart;
