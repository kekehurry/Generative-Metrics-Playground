import React, { useEffect, useRef } from 'react';
// import p5 from 'p5';
import './WelcomePage.css';
import Sketch from './Sketch.js';

function WelcomePage({ enterSite }) {
    // const sketchRef = useRef();

    // useEffect(() => {
    //     new p5(Sketch, sketchRef.current);
    //     return function cleanup() {
    //         sketchRef.current.remove();
    //     };
    // }, []);


    return (
        <div className="welcomepage">
            <Sketch />
        <button className="enterButton" onClick={enterSite}>Enter</button>
        </div>
    );
    }

export default WelcomePage;