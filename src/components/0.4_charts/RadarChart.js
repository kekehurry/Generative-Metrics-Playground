import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { tip as d3tip } from "d3-v6-tip";
import { useResizeObserver } from "../../utils/useResizeObserver";
// import {curveTypes} from "d3-curves-inputs"
import { curveCardinalClosed } from "d3";
import {create, select as selectDOM} from "d3-selection"
// import { partition } from "d3";

// const width = 900;
const height = 600;
const margin_ = 30;
const radius = (height-(margin_*2)) / 4.5;
const dotRadius = 3.5;
const axisLabelFactor = 1.12;
// const wrapWidth = 60;
// const formatPercent = d3.format(',.0%')

const maxValue = 2;
const axisCircles = 2;

const device = d => ["Baseline", "Future"][d];

const rScale = d3.scaleLinear()
    .domain([0, maxValue])
    .range([0, radius]);

const RadarChart = ({ radar_data }) => {
  const ref = useRef();
  const containerRef = useRef();

  // const margin = {
  //   top: 0,
  //   left: 0,
  //   bottom: 0,
  //   right: 0,
  //   };
  
//   const containerWidth = width;
//   const containerHeight = height;

  const [containerWidth, containerHeight] = useResizeObserver(containerRef);


  // to add other functions...

  useEffect(() => {
    if (!containerWidth) return;

    if ((!radar_data.data) ||  (!radar_data.vers)) return;
    
    const height = containerHeight ? containerHeight : 0;
    const width = containerWidth ? containerWidth : 500;

    // console.log(radar_data.axesDomain); // add this line to log axesCategory

    const angleSlice = Math.PI * 2 / radar_data.axesLength;
    const curveSelect = "curveCardinalClosed"
    const radarLine = d3.lineRadial()
        .curve(d3[curveSelect])
        .radius(d => rScale(d))
        .angle((d, i) => i * angleSlice);
    const color = d3.scaleOrdinal().range(["#5FD5EC","#2276FC","#EE6F7C"]);
    const color_2 = d3.scaleOrdinal().range(["#F7C034","#5FD5EC","#F7C034"]);
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
    
    // container.append("circle")
    //     .attr("cx", 0)
    //     .attr("cy", 0)
    //     .attr("r", radius*1.5)
    //     .style("fill", "none")  // 不填充颜色
    //     .style("stroke", "#EE6F7C")  // 边线颜色为黑色
    //     .style("stroke-width", "3px");  // 边线宽度为1像素

    axisGrid.selectAll(".levels")
        .data(d3.range(1,(axisCircles+1)).reverse())
        .enter()
            .append("circle")
            .attr("class", "gridCircle")
            .attr("r", (d, i) => radius/axisCircles*d)
            .style("fill", "#CDCDCD")
            .style("stroke", "#CDCDCD")
            .style("stroke-width", "0.1px")
            .style("fill-opacity", 0);
    
    const axis = axisGrid.selectAll(".axis")
        .data(radar_data.axesDomain)
        .enter()
            .append("g")
            .attr("class", "axis");
    
    // Draw line
    axis.append("line")
    .attr("x1", 0)
    .attr("y1", 0)
    .attr("x2", (d, i) => rScale(maxValue*1) * Math.cos(angleSlice*i - Math.PI/2))
    .attr("y2", (d, i) => rScale(maxValue*1) * Math.sin(angleSlice*i - Math.PI/2))
    .attr("class", "line")
    .style("stroke", "white")
    .style("fill-opacity", "100%")
    .style("stroke-width", "0.1px");

    // draw axis label
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
        .attr("fill", (d, i) => color_2(i+1))
        .attr("stroke", 'white')
        .style("stroke-width", "1px");

    plots.append('path')
        .attr("d", d => radarLine(d.map(v => v.value)))
        .attr("fill", (d, i) => color_2(i+1))
        .attr("fill-opacity", 0.24)
        .attr("stroke", (d, i) => color_2(i+1))
        .attr("stroke-width", 1.5);

    plots.selectAll("circle")
        .data(d => d)
        .join("circle")
        .attr("r", dotRadius/2)
        .attr("cx", (d,i) => rScale(d.value) * Math.cos(angleSlice*i - Math.PI/2))
        .attr("cy", (d,i) => rScale(d.value) * Math.sin(angleSlice*i - Math.PI/2))
        .style("fill-opacity", 1);
    
    function axesByCategory() {
      const categories = {};
      radar_data.axesDomain.forEach((axis, i) => {
        const category = radar_data.axesCategory[i]; // Get category from axesCategory
        if (!categories[category]) categories[category] = [];
        categories[category].push({ axis, index: i });
      });
      return categories;
    }

    function drawCategoryArcs() {
      const categories = axesByCategory();
      // console.log(categories)
    
      const arc_ = d3.arc()
        .innerRadius(radius * 1.5)
        .outerRadius(radius * 1.53)
        .padAngle(30/ radius)
        .cornerRadius(5);
      const arcs_ = container.append('g')
        .attr('class', 'category-arcs');
    
      arcs_.selectAll('.category-arc')
        .data(Object.entries(categories)) // Use Object.entries to include the category names in the data
        .enter()
        .append('path')
        .attr('class', 'category-arc')
        .attr('id', (d, i) => `category-arc-${i}`) // Add an id to each path
        .attr('d', d => arc_({
          startAngle: angleSlice * (d[1][0].index-1),
          endAngle: angleSlice * (d[1][d[1].length - 1].index + 1)
        }))
        // .style('fill', 'white')
        .style('fill', (d, i) => color(d[0]))
        .style('stroke', 'none')
        .style('stroke-width', '2px');
    
    }

    function drawCategoryText() {
      const categories = axesByCategory();
    
      const arc = d3.arc()
        .innerRadius(radius * 1.6)
        .outerRadius(radius * 1.61)
        .padAngle(30/ radius)
        .cornerRadius(5);
      const arcs = container.append('g')
        .attr('class', 'category-arcs');
    
      const categoryArcs = arcs.selectAll('.category-arcs')
        .data(Object.entries(categories)) // Use Object.entries to include the category names in the data
        .enter()
        .append('path')
        .attr('class', 'category-arcs')
        .attr('id', (d, i) => `category-arcs-${i}`) // Add an id to each path
        .attr('d', d => arc({
          startAngle: angleSlice * (d[1][0].index-1),
          endAngle: angleSlice * (d[1][d[1].length - 1].index + 1)
        }))
        // .style('fill', 'white')
        .style('fill', 'none')
        .style('stroke', 'none')
        .style('stroke-width', '2px');
    
      // Add the category labels along the arcs
      categoryArcs.each(function(d, i) {
        const pathId = `#category-arcs-${i}`; // id of the path
        arcs.append('text')
          .append('textPath') // Use textPath to let the text follow the path
          .attr('xlink:href', pathId) // The id of the path along which the text should be drawn
          .text(d[0]) // Use the category name as the text
          .attr('startOffset', '0%') // This can be adjusted to position the text along the path
          // .style('fill', (d, i) => color(d))
          .style('fill', 'white')
          .style('font-family', 'inter')
          .style('font-size', '15px'); 
      });
    }

    // Add the category arcs after drawing the grid and axes.
    drawCategoryArcs();
    drawCategoryText();

    
    
  }, [radar_data, containerWidth, containerHeight]);



  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        right: 0,
        // top: "150px",
        height: "100%",
        width: "100%",
        background: "none"
      }}
    >
        {radar_data && (
      <svg ref={ref} >
        <g />
      </svg>)}

    </div>
  );
};


export default RadarChart;