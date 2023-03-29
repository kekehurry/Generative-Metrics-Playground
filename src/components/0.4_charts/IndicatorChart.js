import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { tip as d3tip } from "d3-v6-tip";
import { useResizeObserver } from "../../utils/useResizeObserver";

const innerRadius = 170;
const outerRadius = innerRadius + 6;
const width = 440;
const height = 440;

const chord = d3
  .chordDirected()
  .padAngle(10 / innerRadius)
  .sortSubgroups(d3.descending)
  .sortChords(d3.descending);

const ribbon = d3
  .ribbonArrow()
  .radius(innerRadius - 0.5)
  .padAngle(1 / innerRadius);

const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);

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

  useEffect(() => {
    if (!containerWidth) return;

    if ((!chord_data.matrix) || (!chord_data.matrix) || (!chord_data.data)) return;
    
    const height = containerHeight ? containerHeight : 0;
    const width = containerWidth ? containerWidth : 500;
    const color = d3.scaleOrdinal(chord_data.names, d3.schemeCategory10);

    // build SVG
    let svg = d3
      .select(ref.current)
      .attr("height", "100%")
      .attr("width", "100%");

    svg
      .attr("viewBox", [-width / 6, -height / 6, width, height])
      .style("width", "100%")
      .style("height", "auto")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10);

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

    const tooltip = d3tip()
      .style("border", "solid 2px black")
      .style("background-color", "white")
      .style("border-radius", "10px")
      .style("float", "right")
      .style("font-family", "monospace")
      .html(
        (event, d) => `
      <div style='float: right'>
        Name: ${d.name} <br/>
        Value: ${d.value} 
      </div>`
      );

    svg.call(tooltip);

    // create Chart
    let group = svg.selectAll("g").data(chords.groups).join("g");

    // Draw arcs
    group
      .append("path")
      // .attr("id", textId.id)
      .attr("fill", (d) => color(d.index))
      .attr("stroke", "#fff")
      .attr("d", arc)
      .on("mouseover", onMouseOver_group)
      .on("mouseout", onMouseOut);

    // Label
    group
      .append("text")
      .each((d) => {
        d.angle = (d.startAngle + d.endAngle) / 2;
      })
      .attr("dy", ".35em")
      //   .attr("stroke", "white")
      .attr(
        "transform",
        (d) => `
            rotate(${(d.angle * 180) / Math.PI - 90})
            translate(${innerRadius + 10})
            ${d.angle > Math.PI ? "rotate(180)" : ""}
        `
      )
      //   .attr("xlink:href", textId.href)
      .attr("text-anchor", (d) => (d.angle > Math.PI ? "end" : null))
      .text((d) => chord_data.names[d.index]);

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
      .style("mix-blend-mode", "multiply")
      .on("mouseover", onMouseOver_chord)
      // .on('mouseover', tooltip.show)
      .on("mouseout", onMouseOut)
      // .on('mouseout', tooltip.hide)
      .append("title")
      .text(
        (d) =>
          `${chord_data.names[d.source.index]} to ${
            chord_data.names[d.target.index]
          }: \n${d.content[d.source.index][d.target.index]}`
      );
  }, [chord_data, containerWidth, containerHeight]);

  return (
    <div
      ref={containerRef}
      style={{
        position: "absolute",
        height: "100%",
        width: "100%",
        background: "white",
      }}
    >
      <svg ref={ref}>
        <g />
      </svg>

    </div>
  );
};

export default IndicatorChart;
