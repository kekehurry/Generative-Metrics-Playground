import ReactSlider from "react-slider";
import React from "react"

// const onChange = (value) => {
//     console.log('onChange: ', value);
//   };
// const onAfterChange = (value) => {
//     console.log('onAfterChange: ', value);
//   };

const Slider_1 = (props) => {

  return (
    <ReactSlider
      className="horizontal-slider"
      thumbClassName="example-thumb"
      trackClassName="example-track"
      min={0}
      max={49}
      onChange={(value) => props.handleChange1(value)}
    //   onAfterChange = {onAfterChange}
      // renderThumb={(props, state) => <div {...props}>{state.valueNow}</div>}

    />
  );
};

const Slider_2 = (props) => {

  return (
    <ReactSlider
      className="horizontal-slider"
      thumbClassName="example-thumb"
      trackClassName="example-track"
      min={50}
      max={99}
      // invert={true}
      onChange={(value) => props.handleChange2(value)}
    //   onAfterChange = {onAfterChange}
      // renderThumb={(props, state) => <div {...props}>{state.valueNow}</div>}

    />
  );
};

const Slider_3 = (props) => {

  return (
    <ReactSlider
      className="horizontal-slider"
      thumbClassName="example-thumb"
      trackClassName="example-track"
      min={100}
      max={149}
      // invert={true}
      onChange={(value) => props.handleChange3(value)}
    //   onAfterChange = {onAfterChange}
      // renderThumb={(props, state) => <div {...props}>{state.valueNow}</div>}

    />
  );
};

const Slider_4 = (props) => {

  return (
    <ReactSlider
      className="horizontal-slider"
      thumbClassName="example-thumb"
      trackClassName="example-track"
      min={150}
      max={199}
      // invert={true}
      onChange={(value) => props.handleChange4(value)}
    //   onAfterChange = {onAfterChange}
      // renderThumb={(props, state) => <div {...props}>{state.valueNow}</div>}

    />
  );
};

export {Slider_1, Slider_2, Slider_3, Slider_4};