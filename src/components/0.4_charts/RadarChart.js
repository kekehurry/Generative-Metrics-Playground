import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { tip as d3tip } from "d3-v6-tip";
import { useResizeObserver } from "../../utils/useResizeObserver";
// import {curveTypes} from "d3-curves-inputs"
import { curveCardinalClosed } from "d3";
import {create, select as selectDOM} from "d3-selection"
// import { partition } from "d3";

const width = 900;
const height = 900;
const margin_ = 30;
const radius = (height-(margin_*2)) / 4;
const dotRadius = 4;
const axisLabelFactor = 1.12;
const wrapWidth = 60;
const formatPercent = d3.format(',.0%')

const maxValue = 10;
const axisCircles = 2;

const device = d => ["Baseline", "Future"][d];

const rScale = d3.scaleLinear()
    .domain([0, maxValue])
    .range([0, radius]);

const RadarChart = ({ radar_data }) => {
  const ref = useRef();
  const containerRef = useRef();

  const margin = {
    top: 0,
    left: 0,
    bottom: 40,
    right: 0,
    };
  
//   const containerWidth = width;
//   const containerHeight = height;

  const [containerWidth, containerHeight] = useResizeObserver(containerRef);


  // to add other functions...

  useEffect(() => {
    if (!containerWidth) return;

    if ((!radar_data.data) ||  (!radar_data.vers)) return;
    
    const height = containerHeight ? containerHeight : 0;
    const width = containerWidth ? containerWidth : 500;

    const angleSlice = Math.PI * 2 / radar_data.axesLength;
    const curveSelect = "curveCardinalClosed"
    const radarLine = d3.lineRadial()
        .curve(d3[curveSelect])
        .radius(d => rScale(d))
        .angle((d, i) => i * angleSlice);
    const color = d3.scaleOrdinal().range(["#EDC951","#CC333F","#00A0B0"]);
    // const color = d3.scaleOrdinal(chord_data.names, d3.schemeCategory10);
    // const color = d3.scaleOrdinal()
    //                 .domain(radar_data.names)
    //                 .range(['#7178b5', '#0faca3', '#7ec1ca', '#a5ba37', '#f6bd0d', '#e27c40','#9b47a2']);

    // build SVG    
    let svg = d3
        .select(ref.current)
        .attr("height", "100%")
        .attr("width", "100%");

    svg
    .attr("viewBox", [-width / 2, -height / 2, width, height])
    .style("width", "100%")
    .style("height", "auto")
    .attr("font-family", "sans-serif")
    .attr("font-size", "15px");

    svg.selectAll('*').remove()

    const container = svg.append('g')
      .attr("width", containerWidth)
      .attr("height", containerHeight);
    // .attr('transform', `translate(${(width/2)+margin}, ${(height/2)+margin*3})`);

    let axisGrid = container.append("g")
        .attr("class", "axisWrapper");

    axisGrid.selectAll(".levels")
        .data(d3.range(1,(axisCircles+1)).reverse())
        .enter()
            .append("circle")
            .attr("class", "gridCircle")
            .attr("r", (d, i) => radius/axisCircles*d)
            .style("fill", "#CDCDCD")
            .style("stroke", "#CDCDCD")
            .style("stroke-width", "0.1px")
            .style("fill-opacity", 0.2);
    
    const axis = axisGrid.selectAll(".axis")
        .data(radar_data.axesDomain)
        .enter()
            .append("g")
            .attr("class", "axis");
    
    // Draw line
    axis.append("line")
    .attr("x1", 0)
    .attr("y1", 0)
    .attr("x2", (d, i) => rScale(maxValue*1.1) * Math.cos(angleSlice*i - Math.PI/2))
    .attr("y2", (d, i) => rScale(maxValue*1.1) * Math.sin(angleSlice*i - Math.PI/2))
    .attr("class", "line")
    .style("stroke", "white")
    .style("fill-opacity", "30%")
    .style("stroke-width", "0.1px");

    axis.append("text")
		.attr("class", "legend")
		.style("font-size", "10px")
        .attr("fill","white")
		.attr("text-anchor", "middle")
    .attr("font-family", "sans-serif")
    .attr("dy", "0.35em")
		.attr("x", (d, i) => rScale(maxValue * axisLabelFactor) * Math.cos(angleSlice*i - Math.PI/2))
		.attr("y", (d, i) => rScale(maxValue * axisLabelFactor) * Math.sin(angleSlice*i - Math.PI/2))
    .attr("transform", (d, i) => {
      const angle = angleSlice*i - Math.PI/2;
      return `rotate(${angle*180/Math.PI}, ${rScale(maxValue*axisLabelFactor)*Math.cos(angle)}, ${rScale(maxValue*axisLabelFactor)*Math.sin(angle)})`;
    })
		.text(d => d)
    ;

      // point
    const plots = container.append('g')
    .selectAll('g')
    .data(radar_data.vers)
    .join('g')
        .attr("data-name", (d, i) => device(i))
        .attr("fill", (d, i) => color(i))
        .attr("stroke", "none");

    plots.append('path')
        .attr("d", d => radarLine(d.map(v => v.value)))
        .attr("fill", (d, i) => color(i))
        .attr("fill-opacity", 0.1)
        .attr("stroke", (d, i) => color(i))
        .attr("stroke-width", 2);

    plots.selectAll("circle")
        .data(d => d)
        .join("circle")
        .attr("r", dotRadius)
        .attr("cx", (d,i) => rScale(d.value) * Math.cos(angleSlice*i - Math.PI/2))
        .attr("cy", (d,i) => rScale(d.value) * Math.sin(angleSlice*i - Math.PI/2))
        .style("fill-opacity", 0.8);

    
  }, [radar_data, containerWidth, containerHeight]);



  return (
    <div
      ref={containerRef}
      style={{
        position: "absolute",
        right: 0,
        // top: "150px",
        height: "100%",
        width: "33%",
        background: "none"
      }}
    >
        {radar_data && (
      <svg ref={ref}>
        <g />
      </svg>)}

    </div>
  );
};


export default RadarChart;