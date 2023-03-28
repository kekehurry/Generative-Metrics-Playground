import React, { useEffect, useState } from "react";
import { render } from "react-dom";
import { stateStore } from "./stores";

import ResPage from "./components/0.3_resolution/ResPage";
import IndicatorChart from "./components/0.4_charts/IndicatorChart";

const App = () => {
  //   const { page } = stateStore;

  // responsive design
  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }
    window.addEventListener("resize", handleResize);
    handleResize();
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    if (windowSize.width < 1100 || windowSize.height < 400) setIsMobile(true);
    else setIsMobile("ontouchstart" in document.documentElement);
  }, [windowSize.width, windowSize.height]);

  return isMobile ? (
    <ResPage />
  ) : (
    <div>
      <IndicatorChart />
    </div>
  );
};

export default App;

export function renderToDOM(container) {
  render(<App />, container);
}
