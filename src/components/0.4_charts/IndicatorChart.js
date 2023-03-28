import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

import { useResizeObserver } from "../../utils/useResizeObserver";

const IndicatorChart = ({}) => {
  const ref = useRef();
  const containerRef = useRef();

  const margin = {
    top: 0,
    left: 0,
    bottom: 40,
    right: 0,
  };
  const [containerWidth, containerHeight] = useResizeObserver(containerRef);

  let data = [];

  useEffect(() => {
    const height = containerHeight ? containerHeight : 0;
    const width = containerWidth ? containerWidth : 500;

    if (!containerWidth) return;

    // build SVG
    let svg = d3
      .select(ref.current)
      .attr("height", "100%")
      .attr("width", "100%");

    // create Chart
    svg.select("g");
  }, [data, containerWidth, containerHeight]);

  return (
    <div
      ref={containerRef}
      style={{
        height: "100%",
        width: "100%",
      }}
    >
      <svg ref={ref}>
        <g />
      </svg>
    </div>
  );
};

export default IndicatorChart;
