import ReactSlider from "react-slider";
import React from "react";
import { useState } from "react";

const CombinedSlider = (props) => {
  // 初始值可以根据需要进行调整
  const [selectedValues, setSelectedValues] = useState([0.2, 0.5, 0.8]);

  const handleChange = (values) => {
    setSelectedValues(values);
    // 可以根据滑块的值来计算和传递你需要的四个值
    // 计算四个输出值
    const value1 = values[0];
    const value2 = values[1] - values[0];
    const value3 = values[2] - values[1];
    const value4 = 1 - values[2];

    // 通过 props 传递四个输出值给父组件
    // props.handleChange(values.slice(0, 3));
    props.handleChange([value1, value2, value3, value4]);

  };

  return (
    <div className="slider-container">
      <div className="slider-content">
        <div className="slider-label">Land Use</div>
        <ReactSlider
          className="horizontal-slider"
          thumbClassName="example-thumb"
          trackClassName="example-track"
          min={0}
          max={1}
          step={0.1}
          value={selectedValues}
          onChange={handleChange}
        />
      </div>
      {/* <div className="slider-values">
        {selectedValues.map((value, index) => (
          <div key={index} className="slider-value">
            {value.toFixed(2)}
          </div>
        ))}
      </div> */}
    </div>
  );
};

export default CombinedSlider;
