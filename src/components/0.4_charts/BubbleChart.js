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

// const ribbon = d3
//   .ribbon()
//   .radius(innerRadius - 5)
//   .padAngle(1 / innerRadius);

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


const BubbleChart = ({ bubble_data, onStakeholderClick, onScoreClick }) => {
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

    if ((!bubble_data.names) || (!bubble_data.matrix) || (!bubble_data.data)) return;

    const height = containerHeight ? containerHeight : 0;
    const width = containerWidth ? containerWidth : 500;
    // const color = d3.scaleOrdinal(chord_data.names, d3.schemeCategory10);
    const color = d3.scaleOrdinal()
      .domain(bubble_data.names)
      .range(['#7178b5', '#0faca3', '#7ec1ca', '#a5ba37', '#f6bd0d', '#e27c40', '#9b47a2']);

    const color_2 = d3.scaleOrdinal()
      .domain(bubble_data.names)
      .range(['#4F5698', '#0C8A82', '#7ec1ca', '#a5ba37', '#f6bd0d', '#e27c40', '#9b47a2']);


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
      .attr("font-size", 16);

    svg.selectAll('*').remove()

    let chords = chord(bubble_data.matrix);

    for (let i = 0; i < chords.length; i++) {
      for (let j = 0; j < bubble_data.data.length; j++) {
        if (
          bubble_data.names[chords[i].source.index] ===
          bubble_data.data[j].Stakeholders
        ) {
          if (
            bubble_data.names[chords[i].target.index] ===
            bubble_data.data[j].Target
          ) {
            chords[i].content = bubble_data.data[j].content;
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

    // 计算新的圆心位置
    function computeNewPosition(centerX, centerY, oldX, oldY, distance) {
      var dx = oldX - centerX;
      var dy = oldY - centerY;
      var angle = Math.atan2(dy, dx);
      return [centerX + distance * Math.cos(angle), centerY + distance * Math.sin(angle)];
    }

    // 分割text
    function splitText(str, maxLength) {
      var words = str.split(' ');
      var lines = [];
      var currentLine = words[0];
  
      for (var i = 1; i < words.length; i++) {
          if (currentLine.length + words[i].length + 1 <= maxLength) {
              currentLine += ' ' + words[i];
          } else {
              lines.push(currentLine);
              currentLine = words[i];
          }
      }
      lines.push(currentLine);
      return lines;
  }

    // 创建半径数组
    // 未来更改为input的circle size
    const radius = [40, 60, 80, 90, 100, 50, 80];

    // 创建位移数组
    // 未来更改为input的move distance
    const distance = [20, 30, 30, 40, 100, 10, 80];

    // 创建总分
    // 未来更改为input的score
    const score = [10, 30, 30, 40, 100, 10, 80];

    // 设置画面中心
    const centerX = 0;
    const centerY = 0;

    // Tax max width
    // const maxWidth = 100;

    // create Chart
    let group = svg.selectAll("g")
      .data(chords.groups.map((d, i) => ({ ...d, radius: radius[i], distance: distance[i], score: score[i] })))
      .join("g");


    // Draw outside standard arcs
    group
      .append("path")
      // .attr("id", textId.id)
      .attr("id", (d, i) => `arc${i}`) // 添加弧的id
      .attr("fill", (d) => 'white')
      .attr("fill-opacity", "10%")
      // .attr("stroke", "black")
      .attr("d", arc_out_out)
      .on("mouseover", onMouseOver_group)
      .on("mouseout", onMouseOut)
      ;
    // group.raise()

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


    // Draw background circles
    group
      .append("circle")
      .attr("cx", function (d) {
        var centroid = arc_out_out.centroid(d);
        var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
        console.log("*****************************************")
        console.log(d)
        console.log(centroid)
        console.log(newPosition)
        console.log("*****************************************")
        return newPosition[0];
      })
      .attr("cy", function (d) {
        var centroid = arc_out_out.centroid(d);
        var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
        return newPosition[1];
      })
      .attr("r", d => d.radius)  // 设置半径
      .style("fill", (d) => color_2(d.index)) // 设置填充颜色
      .style("fill-opacity", "50%")  // 设置透明度
      .on('click', (event, d) => {
        handleStakeholderClick(bubble_data.names[d.index]);
        handleScoreClick(d.score);
      })
      .on("mouseover", onMouseOver_group)
      .on("mouseout", onMouseOut);
    group.raise()
    
    // Label name text
    // group
    //   .append("text")
    //   .attr("fill", "white")
    //   .attr("x", function (d) {
    //     var centroid = arc_out_out.centroid(d);
    //     var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
    //     return newPosition[0];
    //   })
    //   .attr("y", function (d) {
    //     var centroid = arc_out_out.centroid(d);
    //     var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
    //     return newPosition[1] + 5;
    //   })
    //   .attr("text-anchor", "middle")  // 让文本在指定的坐标中居中
    //   .attr("font-size", "15px")  // 设置字体大小
    //   .style("fill-opacity", "80%")  // 设置透明度
    //   .text((d) => bubble_data.names[d.index]);
    // group.raise()

    // Label name text
    group.each(function(d, i) {
      var lines = splitText(bubble_data.names[d.index], 15);  // 假设最大长度为20字符
  
      var text = d3.select(this)
          .append("text")
          .attr("fill", "white")
          .attr("x", function (d) {
              var centroid = arc_out_out.centroid(d);
              var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
              return newPosition[0];
          })
          .attr("y", function (d) {
              var centroid = arc_out_out.centroid(d);
              var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
              return newPosition[1];
          })
          .attr("text-anchor", "middle")  // 让文本在指定的坐标中居中
          .attr("font-size", "20px")
          .attr("font-family", "inter")
          .attr("font-weight", "bold")
          .attr("font-style", "italic")
          .style("fill-opacity", "70%");
  
      // 添加多行文本
      lines.forEach(function(line, index) {
          text.append("tspan")
              .attr("x", function () {
                  return text.attr("x");
              })
              .attr("y", function () {
                  return (text.attr("y") - 20) + (index * 18); // 18为每行的高度，可根据需要进行调整
              })
              .text(line);
      });
  });

    // Label Score Value
    group
      .append("text")
      .attr("fill", "white")
      .attr("x", function (d) {
        var centroid = arc_out_out.centroid(d);
        var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
        return newPosition[0];
      })
      .attr("y", function (d) {
        var centroid = arc_out_out.centroid(d);
        var newPosition = computeNewPosition(centerX, centerY, centroid[0], centroid[1], outerRadius * 1.8 - d.distance);
        return newPosition[1] + 30;
      })
      .attr("text-anchor", "start")  // 让文本在指定的坐标中居中
      .attr("font-family", "inter")
      .attr("font-weight", "bold")
      .attr("font-size", "25px")  // 设置字体大小
      .attr("font-style", "italic")
      .style("fill-opacity", "70%")  // 设置透明度
      .text((d) => d.score);
    group.raise()


    // Draw arcs
    // group
    //   .append("path")
    //   // .attr("id", textId.id)
    //   .attr("id", (d, i) => `arc${i}`) // 添加弧的id
    //   .attr("fill", (d) => color(d.index))
    //   .attr("fill-opacity", "100%")
    //   .attr("stroke", "black")
    //   .attr("d", arc)
    //   .on("mouseover", onMouseOver_group)
    //   .on("mouseout", onMouseOut)
    //   ;
    // group.raise()




    // // Label
    // group
    //   .append("text")
    //   .attr("fill", "white")
    //   .each((d) => {
    //     d.angle = (d.startAngle + d.endAngle) / 2;
    //   })
    //   .append("textPath")
    //   .attr("xlink:href", (d, i) => `#arc${i}`) // 引用弧的id
    //   .attr("startOffset", "10") // 文本起始位置
    //   .attr("text-anchor", 'left')
    //   .attr("dy", "10")
    //   .text((d) => bubble_data.names[d.index])
    //   .on('click', (event, d) => {
    //     handleStakeholderClick(bubble_data.names[d.index]);
    //   });
    // group.raise()

    // ---------------------渐变--------------------- //
    // // 在 SVG 容器中添加一个 defs 元素，用于定义渐变
    // let defs = svg.append("defs");

    // // 添加径向渐变
    // let gradient = defs.append("radialGradient")
    //   .attr("id", "gradient") // 设置渐变的 id，之后将用这个 id 来引用这个渐变
    //   .attr("cx", "50%")      // 渐变的中心在 chord 的中间
    //   .attr("cy", "50%")
    //   .attr("r", "50%")       // 渐变的半径
    //   .attr("fx", "50%")      // 渐变的焦点在 chord 的中间
    //   .attr("fy", "50%"); 

    // // 在径向渐变中添加两个停止颜色
    // gradient.append("stop")
    //   .attr("offset", "40%")  // 在 40% 的位置，设置第一个停止颜色
    //   .attr("stop-color", "rgba(255, 255, 255, 0.1)");  // 半透明的白色
    // gradient.append("stop")
    //   .attr("offset", "60%")  // 在 60% 的位置，设置第二个停止颜色
    //   .attr("stop-color", "rgba(255, 255, 255, 1)");  // 不透明的白色

    // Draw chords
    // svg
    //   .append("g")
    //   .attr("fill-opacity", 0.7)
    //   .selectAll("path")
    //   .data(chords)
    //   .join("path")
    //   .attr("class", "chord")
    //   .attr("fill", (d) => color(d.source.index))

      //---------------------渐变--------------------- //
      // .attr("fill", "url(#gradient)") // 引用上面定义的渐变
      // .attr("fill", (d) => color(d.source.index))
      // // 为每个 chord 创建一个独立的渐变
      // .each(function(d) {
      //   let sourceColor = d3.rgb(color(d.source.index)); // 使用 D3 的颜色函数获取 RGB 颜色

      //   let gradient = defs.append("linearGradient") // 创建线性渐变
      //       .attr("id", "gradient-" + d.source.index); // 为每个渐变设置唯一的 ID

      //   gradient.append("stop") // 设置渐变的起始颜色（不透明）
      //       .attr("offset", "0%")
      //       .attr("stop-color", sourceColor ); // 转换为 RGBA 颜色，alpha 通道为 80（半透明）

      //   gradient.append("stop") // 中间处为透明
      //       .attr("offset", "50%")
      //       .attr("stop-color", sourceColor + "80"); 


      //   gradient.append("stop") // 设置渐变的终止颜色（不透明）
      //       .attr("offset", "100%")
      //       .attr("stop-color", sourceColor); // 原始颜色（不透明）

      //   // 应用渐变到当前的 chord
      //   d3.select(this)
      //       .style("fill", "url(#gradient-" + d.source.index + ")");
      // })
      //---------------------渐变--------------------- //

      // .attr("d", ribbon)
      // // .style("mix-blend-mode", "multiply")
      // .on("mouseover", onMouseOver_chord)
      // // .on('mouseover', tooltip.show)
      // .on("mouseout", onMouseOut)
      // // .on('mouseout', tooltip.hide)
      // .append("title")
      // .text(
      //   (d) =>
      //     `${bubble_data.names[d.source.index]} -> ${bubble_data.names[d.target.index]
      //     }: \n${bubble_data.content[d.source.index][d.target.index]} ${d.source.index === d.target.index ? "" : `\n${bubble_data.names[d.target.index]} -> ${bubble_data.names[d.source.index]}: \n${bubble_data.content[d.target.index][d.source.index]}`}
      //     `
      // );
    svg.raise()
  }, [bubble_data, containerWidth, containerHeight]);


  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        left: "10%",
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



export default BubbleChart;
