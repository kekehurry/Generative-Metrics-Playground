import ReactSlider from "react-slider";
import React from "react"
import { useState } from "react";

// const onChange = (value) => {
//     console.log('onChange: ', value);
//   };
// const onAfterChange = (value) => {
//     console.log('onAfterChange: ', value);
//   };

const Slider_1 = (props) => {
  const [selectedValue, setSelectedValue] = useState(0); // Initialize with the default value or minimum value


  return (
    <div className="slider-container">
      <div className="slider-content">
        <div className="slider-label">Residential Space</div>
        <ReactSlider
          className="horizontal-slider"
          thumbClassName="example-thumb"
          trackClassName="example-track"
          min={0}
          max={1}
          step={0.1}
          onChange={(value) => {
            setSelectedValue(value);
            props.handleChange1(value);
          }}
        />
      </div>
      <div className="slider-value">{selectedValue.toFixed(2)} </div>
    </div>
  );
};

const Slider_2 = (props) => {
  const [selectedValue, setSelectedValue] = useState(0); // Initialize with the default value or minimum value


  return (
    <div className="slider-container">
      <div className="slider-content">
        <div className="slider-label">Office Space</div>
        <ReactSlider
          className="horizontal-slider"
          thumbClassName="example-thumb"
          trackClassName="example-track"
          min={0}
          max={props.max}
          step={0.1}
          onChange={(value) => {
            setSelectedValue(value);
            props.handleChange2(value);
          }}
        />
      </div>
      <div className="slider-value">{selectedValue.toFixed(2)} </div>
    </div>
  );
};

const Slider_3 = (props) => {
  const [selectedValue, setSelectedValue] = useState(0); // Initialize with the default value or minimum value


  return (
    <div className="slider-container">
      <div className="slider-content">
        <div className="slider-label">Amenity Space</div>
        <ReactSlider
          className="horizontal-slider"
          thumbClassName="example-thumb"
          trackClassName="example-track"
          min={0}
          max={props.max}
          step={0.1}
          onChange={(value) => {
            setSelectedValue(value);
            props.handleChange3(value);
          }}
        />
      </div>
      <div className="slider-value">{selectedValue.toFixed(2)} </div>
    </div>
  );
};

const Slider_4 = (props) => {
  const [selectedValue, setSelectedValue] = useState(0); // Initialize with the default value or minimum value


  return (
    <div className="slider-container">
      <div className="slider-content">
        <div className="slider-label">Civic Space</div>
        <ReactSlider
          className="horizontal-slider"
          thumbClassName="example-thumb"
          trackClassName="example-track"
          min={0}
          max={props.max}
          step={0.1}
          onChange={(value) => {
            setSelectedValue(value);
            props.handleChange4(value);
          }}
        />
      </div>
      <div className="slider-value">{selectedValue.toFixed(2)}</div>
    </div>
  );
};

export {Slider_1, Slider_2, Slider_3, Slider_4};