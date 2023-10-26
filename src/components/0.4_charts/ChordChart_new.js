import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { tip as d3tip } from "d3-v6-tip";
import { useResizeObserver } from "../../utils/useResizeObserver";
import { partition } from "d3";
import { useCallback } from 'react';

const innerRadius = 160;
const outerRadius = innerRadius + 8;
// const width = 900;
// const height = 900;
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
  .innerRadius(outerRadius * 1.7)
  .outerRadius(outerRadius * 1.7 + 2)
  .cornerRadius(10);

const arc_out_out = d3
  .arc()
  .innerRadius(outerRadius * 1.8)
  .outerRadius(outerRadius * 1.8 + 2)
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
  .innerRadius(d => d.y0 * radius)
  .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));


const ChordChart = ({ chord_data, bubble_data, indicator_data, onStakeholderClick, onScoreClick }) => {
  const ref = useRef();
  const containerRef = useRef();

  // const margin = {
  //   top: 0,
  //   left: 0,
  //   bottom: 0,
  //   right: 0,
  // };
  const [containerWidth, containerHeight] = useResizeObserver(containerRef);
  const handleStakeholderClick = useCallback(onStakeholderClick, []);
  const handleScoreClick = useCallback(onScoreClick, []);


  // to add other functions...

  useEffect(() => {
    if (!containerWidth) return;

    if ((!chord_data.names) || (!chord_data.matrix) || (!chord_data.data)) return;

    const height = containerHeight ? containerHeight : 0;
    const width = containerWidth ? containerWidth : 500;
    // const color = d3.scaleOrdinal(chord_data.names, d3.schemeCategory10);
    const color = d3.scaleOrdinal()
      .domain(chord_data.names)
      .range(['#7178b5', '#0faca3', '#7ec1ca', '#a5ba37', '#f6bd0d',  '#9b47a2']); // '#e27c40',

    const color_2 = d3.scaleOrdinal()
      .domain(chord_data.names)
      .range(['#7178B5', '#0FACA3',  '#7ec1ca', '#a5ba37', '#f6bd0d', '#9b47a2']); //,'#e27c40'


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
          chord_data.names[chords[i].source.index] ===
          chord_data.data[j].stakeholder
        ) {
          if (
            chord_data.names[chords[i].target.index] ===
            chord_data.data[j].target
          ) {
            chords[i].indicator = chord_data.data[j].indicator;
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
        .filter((d) => d.source.index === obj.source.index)
        .filter((d) => d.target.index === obj.target.index)
        .style("opacity", 1);

      // console.log(obj);
    }

    //
    function onMouseOut() {
      group.style("opacity", 1);
      svg.selectAll(".chord").style("opacity", 1);
    }

    // 创建总分
    // 未来更改为input的score
    // const score = [10, 30, 30, 40, 100, 10, 80];
    const score = bubble_data.map(item => item.score);

    // 设置画面中心
    const centerX = 0;
    const centerY = 0;


    const bgColor = [
      // {stakeholder: "Developer", bgcolor: "#9b47a2"},
      // {stakeholder: "Government", bgcolor: "#0FACA3"},
      // // {stakeholder: "Industry group", bgcolor: "#7ec1ca"},
      // {stakeholder: "Local Business Owners", bgcolor: "#a5ba37"},
      // {stakeholder: "Nonprofit Institution", bgcolor: "#f6bd0d"},
      // {stakeholder: "Residents", bgcolor: "#e27c40"},
      // {stakeholder: "Workforce", bgcolor: "#7178B5"}
      {stakeholder: "Residents", bgcolor: "#7178B5"},
      {stakeholder: "Local Business Owners", bgcolor: "#0FACA3"},
      {stakeholder: "Nonprofit Institution", bgcolor: "#7ec1ca"},
      {stakeholder: "Government", bgcolor: "#a5ba37"},
      {stakeholder: "Workforce", bgcolor: "#f6bd0d"},
      {stakeholder: "Industry Group", bgcolor: "#e27c40"},
      {stakeholder: "Developer", bgcolor: "#9b47a2"}
    ];


    // create Chart
    let group = svg.selectAll("g")
      .data(chords.groups.map((d, i) => ({ ...d,score: score[i] })))
      .join("g");


    // Draw outside standard arcs
    group
      .append("path")
      // .attr("id", textId.id)
      .attr("id", (d, i) => `arc${i}`) // 添加弧的id
      .attr("fill", (d) => 'white')
      // .attr("fill", "black")
      .attr("fill-opacity", "10%")
      // .attr("stroke", "black")
      .attr("d", arc_out_out)
      .on("mouseover", onMouseOver_group)
      .on("mouseout", onMouseOut)
      ;
    // group.raise()

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
      .on('click', (event, d) => {
        handleStakeholderClick(chord_data.names[d.index]);
        handleScoreClick(d.score);
      });
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
      // .attr("fill", "black")
      .each((d) => {
        d.angle = (d.startAngle + d.endAngle) / 2;
      })
      .append("textPath")
      .attr("xlink:href", (d, i) => `#arc${i}`) // 引用弧的id
      .attr("startOffset", "10") // 文本起始位置
      .attr("text-anchor", 'left')
      .attr("dy", "10")
      .text((d) => chord_data.names[d.index])
      .on('click', (event, d) => {
        handleStakeholderClick(chord_data.names[d.index]);
        handleScoreClick(d.score);
      });
    group.raise()

    // --------------------- 以下为中圈indicator value的绘制 ---------------------

    // 为每个圆弧计算辅助线的数据
    const computeLinesForArc = function(d) {
      const stakeholderItems = indicator_data.filter(item => item.stakeholder === chord_data.names[d.index]); // 根据数据结构，可能需要调整
      const numItems = stakeholderItems.length;
      const angleStep = (d.endAngle - d.startAngle) / (numItems + 1);
      const linesData = [];

      for (let i = 1; i <= numItems; i++) {
          const angle = d.startAngle + angleStep * i - Math.PI / 2;
          linesData.push({
              x1: centerX + Math.cos(angle) * 180,
              y1: centerY + Math.sin(angle) * 180,
              x2: centerX + Math.cos(angle) * 280,
              y2: centerY + Math.sin(angle) * 280,
              index: d.index
          });
      }

      return linesData;
    }

    // 为每个圆弧绘制辅助线
    group.each(function(d, i) {
      const arcGroup = d3.select(this);
      const linesData = computeLinesForArc(d);

      arcGroup.selectAll()
          .data(linesData)
          .enter()
          .append("line")
          .attr("class", "helper-line")
          .attr("x1", d => d.x1)
          .attr("y1", d => d.y1)
          .attr("x2", d => d.x2)
          .attr("y2", d => d.y2)
          // 设置线的样式
          .style("stroke", "grey") // 设置线条颜色
          .style("stroke-width", 0.5)
          .style("stroke-opacity", "100%")  // 设置透明度
          .style("stroke-dasharray", "4,2"); // 设置虚线

      // 如果你希望线被放到底层，你可以这样做：
      // arcGroup.lower();
    });

    function computeCirclePosition(lineData, score) {
      const dx = lineData.x2 - lineData.x1;
      const dy = lineData.y2 - lineData.y1;
  
      // 计算单位方向向量
      const len = Math.sqrt(dx * dx + dy * dy);
      const ux = dx / len;
      const uy = dy / len;
  
      // 使用单位方向向量和score值计算新的位置
      const newX = lineData.x1 + ux * score;
      const newY = lineData.y1 + uy * score;
  
      return [newX, newY];
  }

    group.selectAll('line.helper-line')
      .each(function(d, i) {
        // console.log('d:', d); // 打印 d
        // console.log('i:', i); // 打印 i
        // console.log('d.index:', d.index);  // 打印 d.index

        const currentStakeholder = chord_data.names[d.index];  // 这里获取当前的stakeholder
        // const correspondingData = indicator_data[i];
        // console.log('currentStakeholder:',currentStakeholder);
        const correspondingDataItems = indicator_data.filter(item => item.stakeholder === currentStakeholder);

        const correspondingData = correspondingDataItems[i]; // 使用索引 i 来获取对应的数据条目
        // console.log('correspondingData:', correspondingData);

        // 获取大圆和小圆的位置
        const bigCirclePos = computeCirclePosition(d3.select(this).data()[0], correspondingData.score);
        const smallCirclePos = computeCirclePosition(d3.select(this).data()[0], correspondingData.baseline);
        // console.log('Data score:', correspondingData.score);
        // console.log('Data baseline:', correspondingData.baseline);

        // 绘制大圆
        d3.select(this.parentNode)
            .append("circle")
            .attr("cx", bigCirclePos[0])
            .attr("cy", bigCirclePos[1])
            .attr("r", 6.5)
            .style("fill", "white")
            // .style("fill", "black")
            .style("fill-opacity", "100%");

        // 绘制大圆的颜色
        d3.select(this.parentNode)
            .append("circle")
            .attr("cx", bigCirclePos[0])
            .attr("cy", bigCirclePos[1])
            .attr("r", 5)
            .style("fill", (d) => color_2(d.index))
            .style("fill-opacity", "100%")
            .on('click', (event, d) => {
              handleStakeholderClick(chord_data.names[d.index])
              handleScoreClick(d.score)
            });

        // 绘制小圆
        d3.select(this.parentNode)
            .append("circle")
            .attr("cx", smallCirclePos[0])
            .attr("cy", smallCirclePos[1])
            .attr("r", 4.5)
            .style("fill", 'grey')
            .style("fill-opacity", "100%");

        // 绘制小圆的颜色
        d3.select(this.parentNode)
            .append("circle")
            .attr("cx", smallCirclePos[0])
            .attr("cy", smallCirclePos[1])
            .attr("r", 3)
            .style("fill", "white")
            // .style("fill", "black")
            .style("fill-opacity", "100%")
            .on('click', (event, d) => {
              handleStakeholderClick(chord_data.names[d.index])
              handleScoreClick(d.score)
            });

        // 绘制连接大圆和小圆的线段
        d3.select(this.parentNode)
            .append('line')
            .attr("x1", bigCirclePos[0])
            .attr("y1", bigCirclePos[1])
            .attr("x2", smallCirclePos[0])
            .attr("y2", smallCirclePos[1])
            .style("stroke", (d) => color_2(d.index))
            .style("stroke-width", 2)
            .lower();
      });


    // Draw chords
    svg
      .append("g")
      .attr("fill-opacity", 0.7)
      .selectAll("path")
      .data(chords)
      .join("path")
      .attr("class", "chord")
      .attr("fill", (d) => color(d.source.index))
      .attr("d", ribbon)
      .on("mouseover", onMouseOver_chord)
      .on("mouseout", onMouseOut)
      .append("title")
      .text(
        (d) =>
          `${chord_data.names[d.source.index]} -> ${chord_data.names[d.target.index]
          }: \n${chord_data.indicator[d.source.index][d.target.index]} ${d.source.index === d.target.index ? "" : `\n${chord_data.names[d.target.index]} -> ${chord_data.names[d.source.index]}: \n${chord_data.indicator[d.target.index][d.source.index]}`}
          `
      );
    svg.raise()
  }, [chord_data, bubble_data, indicator_data, containerWidth, containerHeight]);


  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        left: "8%",
        // top: "150px",
        height: "90%",
        width: "100%",
        background: "none"
      }}
    >
      <svg ref={ref}>
        <g />
      </svg>
      {/* <div style={{ 
        position: "absolute", 
        top: "50%", 
        left: "50%",
        width: "50%",
        height: "50%",
        background:"radial-gradient(circle at center, transparent, black 100%)",
        // background: "white",
        borderRadius: "50%",
        transform: "translate(-50%, -50%)",
        zIndex:200
      }} /> */}
    </div>
  );
};



export default ChordChart;
