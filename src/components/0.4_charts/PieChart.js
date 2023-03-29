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
        // const width = 1000
        // const height = 1000
        const colorRange = ['#4f5698', '#0c8a82', '#50abb7', '#84952c', '#d6a408', '#d86521','#743579'];
        const color = d3.scaleOrdinal(colorRange.slice(0, pieData.pie_data.children.length + 1));
        const format = d3.format(",d");
        const radius = width / 10;


        const svg = d3.select(ref.current);


        // // build SVG
        // let svg = d3
        //   .select(ref.current)
        //   // .attr("height", "100%")
        //   .attr("width", "100%");

        svg
          .attr("viewBox", [-width / 2, -height / 2, width, height])
          // .style("width", "40%")
          // .style("height", "auto")
          .style("max-width", `${width}px`)
          .attr("font-family", "sans-serif")
          .attr("font-size", '15px');
      

        //draw the arc
        const arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
            .padRadius(radius * 1.5)
            .innerRadius(d => d.y0 * radius)
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

        const mousearc = d3
            .arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .innerRadius(d => d.y0 * radius )
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));


        // const g = svg.append("g")
        //     .attr("transform", `translate(${width / 2},${width / 2})`);
        
        // Make this into a view, so that the currently hovered sequence is available to the breadcrumb
        const element = svg.node();
        element.value = { sequence: [], percentage: 0.0 };
    
        const tooltip = d3tip()
          .style('border', 'solid 4px black')
          .style('background-color', '#ffffff')
          .style('border-radius', '10px')
          .style("padding", "3px")
          .style('float', 'left')
          .style('font-family', 'monospace')
          // .style('font-size', '30px')
          .html((event, d) => `
              <div style='float: left'>
              Name: ${d.data.name} <br/>
              Value: ${d.value} 
              </div>`);
        
        svg.call(tooltip);

        const label = svg
            .raise()
            .attr("text-anchor", "left")
            .style("user-select", "none")
          .selectAll("text")
          .data(pieData.root.descendants().slice(1))
          .join("text")
            .each(d => { d.angle = (d.x0 + d.x1) / 2  })
            .attr("fill-opacity", "100%")
            // .attr("fill-size",'0.35em')
            .attr("transform", d => `
              rotate(${(d.angle * 180 / Math.PI - 90)})
              translate(${d.y0*radius })
              ${d.angle > Math.PI ? "rotate(180)" : ""}
              `)
            .attr("dy", "0.35em")
            .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
            .text(d => d.data.name);
        
          label.raise();
    
        // const label = svg
        //   .append("text")
        //   .attr("text-anchor", "middle")
        //   .attr("fill", "#888")
        //   .style("visibility", "hidden");
    
        // label
        //   .append("tspan")
        //   .attr("class", "percentage")
        //   .attr("x", 0)
        //   .attr("y", 0)
        //   .attr("dy", "-0.1em")
        //   .attr("font-size", "5em")
        //   .text("");
      
        // label
        //   .append("tspan")
        //   .attr("x", 0)
        //   .attr("y", 0)
        //   .attr("dy", "1.5em")
        //   .text("of indicators begin \n with this category");
    
        // svg
        //   .attr("viewBox", `${-width} ${-width} ${width} ${width}`)
        //   .style("max-width", `${width}px`)
        //   .style("font", "12px sans-serif");

        // Draw arc
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
              // label.style("visibility", "hidden");
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
              sequence.indexOf(node) >= 0 ? 0.7 : 0.3
              );
              const percentage = ((100 * d.value) / pieData.root.value ).toPrecision(3);
              // // Center label
              // label
              // .style("visibility", null)
              // .select(".percentage")
              // .text(percentage + "%");
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