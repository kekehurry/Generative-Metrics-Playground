import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { tip as d3tip } from "d3-v6-tip";
import { useResizeObserver } from "../../utils/useResizeObserver";
import { partition } from "d3";

const innerRadius = 150;
const outerRadius = innerRadius + 8;
const width = 900;
const height = 900;
const radius = 44

const chord = d3
  .chord()
  .padAngle(10 / innerRadius)
  .sortSubgroups(d3.descending)
  .sortChords(d3.descending);

const ribbon = d3
  .ribbon()
  .radius(innerRadius - 5)
  .padAngle(1 / innerRadius);

// Draw pie circle
const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius).cornerRadius(10);
// Draw outside circle
const arc_out = d3
  .arc()
  .innerRadius(outerRadius *1.7)
  .outerRadius(outerRadius *1.7 + 2)
  .cornerRadius(10);

// Draw pie circle, not using
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


const ChordChart = ({ chord_data }) => {
  const ref = useRef();
  const containerRef = useRef();

  const margin = {
    top: 0,
    left: 0,
    bottom: 0,
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

    const color_2 = d3.scaleOrdinal()
                    .domain(chord_data.names)
                    .range(['#4F5698', '#0C8A82', '#7ec1ca', '#a5ba37', '#f6bd0d', '#e27c40','#9b47a2']);


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
      .attr("font-size", 13);
    
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

    // Draw outside arcs
    group
      .append("path")
      // .attr("id", textId.id)
      .attr("id", (d, i) => `arc${i}`) // 添加弧的id
      .attr("fill", (d) => color_2(d.index))
      .attr("fill-opacity", "100%")
      // .attr("stroke", "black")
      .attr("d", arc_out)
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
        .attr("startOffset", "10") // 文本起始位置
        .attr("text-anchor", 'left')
        .attr("dy", "10")
        .text((d) => chord_data.names[d.index])
      ;
    group.raise()
    

    // 在 SVG 容器中添加一个 defs 元素，用于定义渐变
    let defs = svg.append("defs");

    // 添加径向渐变
    let gradient = defs.append("radialGradient")
      .attr("id", "gradient") // 设置渐变的 id，之后将用这个 id 来引用这个渐变
      .attr("cx", "50%")      // 渐变的中心在 chord 的中间
      .attr("cy", "50%")
      .attr("r", "50%")       // 渐变的半径
      .attr("fx", "50%")      // 渐变的焦点在 chord 的中间
      .attr("fy", "50%"); 
    
    // 在径向渐变中添加两个停止颜色
    gradient.append("stop")
      .attr("offset", "40%")  // 在 40% 的位置，设置第一个停止颜色
      .attr("stop-color", "rgba(255, 255, 255, 0.1)");  // 半透明的白色
    gradient.append("stop")
      .attr("offset", "60%")  // 在 60% 的位置，设置第二个停止颜色
      .attr("stop-color", "rgba(255, 255, 255, 1)");  // 不透明的白色

    // Draw chords
    svg
      .append("g")
      // .attr("fill-opacity", 0.7)
      .selectAll("path")
      .data(chords)
      .join("path")
      .attr("class", "chord")
      // .attr("fill", "url(#gradient)") // 引用上面定义的渐变
      // .attr("fill", (d) => color(d.source.index))
      // 为每个 chord 创建一个独立的渐变
      .each(function(d) {
        let sourceColor = d3.rgb(color(d.source.index)); // 使用 D3 的颜色函数获取 RGB 颜色

        let gradient = defs.append("linearGradient") // 创建线性渐变
            .attr("id", "gradient-" + d.source.index); // 为每个渐变设置唯一的 ID

        gradient.append("stop") // 设置渐变的起始颜色（不透明）
            .attr("offset", "0%")
            .attr("stop-color", sourceColor ); // 转换为 RGBA 颜色，alpha 通道为 80（半透明）
        
        gradient.append("stop") // 中间处为透明
            .attr("offset", "50%")
            .attr("stop-color", sourceColor + "80"); 
    

        gradient.append("stop") // 设置渐变的终止颜色（不透明）
            .attr("offset", "100%")
            .attr("stop-color", sourceColor); // 原始颜色（不透明）

        // 应用渐变到当前的 chord
        d3.select(this)
            .style("fill", "url(#gradient-" + d.source.index + ")");
      })
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
          }: \n${chord_data.content[d.source.index][d.target.index]} ${d.source.index === d.target.index ? "" : `\n${chord_data.names[d.target.index]} -> ${chord_data.names[d.source.index]}: \n${chord_data.content[d.target.index][d.source.index]}`}
          `
      );
    svg.raise()
  }, [chord_data, containerWidth, containerHeight]);


  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        // right: "0",
        // top: "150px",
        height: "100%",
        width: "100%",
        background: "none"
      }}
    >
      <svg ref={ref}>
        <g />
      </svg>
    </div>
  );
};



export default ChordChart;
