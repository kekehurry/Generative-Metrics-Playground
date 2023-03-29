import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { tip as d3tip } from "d3-v6-tip";
import { useResizeObserver } from "../../utils/useResizeObserver";


const PieChart = ({ pieData }) => {
    const ref = useRef();
    const containerRef = useRef();
    const [containerWidth, containerHeight] = useResizeObserver(containerRef);

    useEffect(() => {
      if (!containerWidth) return;
      if ((!pieData.root) || (!pieData.pie_data) ) return;
      
        const width = containerWidth ? containerWidth*0.7 : 10;
        const height = containerWidth ? containerWidth*0.7 : 10;
        const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, pieData.pie_data.children.length + 1))
        const format = d3.format(",d")
        const radius = width / 10


        const svg = d3.select(ref.current);

        // // build SVG
        // let svg = d3
        //   .select(ref.current)
        //   // .attr("height", "100%")
        //   .attr("width", "100%");

        svg
          .attr("viewBox", [-width / 2, -height / 2, width, height])
          .style("width", "40%")
          .style("height", "auto")
          .attr("font-family", "sans-serif")
          .attr("font-size", 10);
      
        const g = svg.append("g")
          .attr("transform", `translate(${width / 2},${width / 2})`);  

        //draw the arc
        const arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
            .padRadius(radius * 1.5)
            .innerRadius(d => d.y0 * radius)
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1))

        const mousearc = d3
            .arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .innerRadius(d => d.y0 * radius )
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1))

        // const g = svg.append("g")
        //     .attr("transform", `translate(${width / 2},${width / 2})`);
        
        // Make this into a view, so that the currently hovered sequence is available to the breadcrumb
        const element = svg.node();
        element.value = { sequence: [], percentage: 0.0 };
    
        const tooltip = d3tip()
          .style('border', 'solid 2px black')
          .style('background-color', 'white')
          .style('border-radius', '10px')
          .style("padding", "5px")
          .style('float', 'left')
          .style('font-family', 'monospace')
          .html((event, d) => `
              <div style='float: left'>
              Name: ${d.data.name} <br/>
              Value: ${d.value} 
              </div>`);
        
        svg.call(tooltip);
    
        const label = svg
          .append("text")
          .attr("text-anchor", "middle")
          .attr("fill", "#888")
          .style("visibility", "hidden");
    
        label
          .append("tspan")
          .attr("class", "percentage")
          .attr("x", 0)
          .attr("y", 0)
          .attr("dy", "-0.1em")
          .attr("font-size", "3em")
          .text("");
      
        label
          .append("tspan")
          .attr("x", 0)
          .attr("y", 0)
          .attr("dy", "1.5em")
          .text("of indicators begin with this category");
    
        // svg
        //   .attr("viewBox", `${-width} ${-width} ${width} ${width}`)
        //   .style("max-width", `${width}px`)
        //   .style("font", "12px sans-serif");
    
        const path = svg
          .selectAll("path")
          .data(
              pieData.root.descendants().filter(d => {
                  return d.depth && d.x1 - d.x0 > 0.001;
              })
          )
          .join("path")
          .attr("fill", d => { while (d.depth > 1) d = d.parent; return color(d.data.name); })
          .attr("d", arc);

    
        path.append("title")
            .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);
    
    
        svg
          .append("g")
          .attr("fill", "none")
          .attr("pointer-events", "all")
          .on('mouseout', tooltip.hide)
          .on("mouseleave", () => {
              path.attr("fill-opacity", 0.65);
              label.style("visibility", "hidden");
              // Update the value of this view
              element.value = { sequence: [], percentage: 0.0 };
              element.dispatchEvent(new CustomEvent("input"));
          })
          .selectAll("path")
          .data(
              pieData.root.descendants().filter(d => {
              // Don't draw the root node, and for efficiency, filter out nodes that would be too small to see
              return d.depth && d.x1 - d.x0 > 0.001;
              })
          )
          .join("path")
          .attr("d", mousearc)
          .on('mouseover', tooltip.show)
          .on("mouseenter", (event, d) => {
              // Get the ancestors of the current segment, minus the root
              const sequence = d
              .ancestors()
              .reverse()
              .slice(1);
              // Highlight the ancestors
              path.attr("fill-opacity", node =>
              sequence.indexOf(node) >= 0 ? 1.0 : 0.3
              );
              const percentage = ((100 * d.value) / pieData.root.value ).toPrecision(3);
              // Center label
              label
              .style("visibility", null)
              .select(".percentage")
              .text(percentage + "%");
              // Update the value of this view with the currently hovered sequence and percentage
              element.value = { sequence, percentage };
              element.dispatchEvent(new CustomEvent("input"));
           });

    }, [pieData, containerWidth, containerHeight]);
  
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
          {pieData && (
          <svg ref={ref}>
            <g/>
          </svg>)}

        </div>
      );
};

export default PieChart;