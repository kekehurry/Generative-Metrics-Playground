import React, { useState, useEffect, useRef } from 'react';
import './WelcomePage.css';
import { Link, Element } from 'react-scroll';
import Sketch from './Sketch.js';
import Page1Image from './image/1.jpg';
import Page2Image from './image/2.jpg';
import Page3Image from './image/3.jpg';
import Page4Image from './image/4.jpg';
import Page5Image from './image/5.jpg';
import Page6Image from './image/6.jpg';
import Page7Image from './image/7.jpg';

function WelcomePage({ enterSite }) {
    const sketchRef = useRef();
    const [showText, setShowText] = useState(false);
    const page2Ref = useRef(null);

    useEffect(() => {
        const handleScroll = () => {
            if (page2Ref.current) {
                const rect = page2Ref.current.getBoundingClientRect();
                if (rect.top <= window.innerHeight * 0.5) {
                    setShowText(true);
                } else {
                    setShowText(false);
                }
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div className="welcomepage">
            <Element name="page1" className="page">
                {/* <h1>Welcome to Our Community</h1> */}
                <img src={Page1Image} alt="page1" className='pageImage'/>
                {/* <p>Some text content... Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur nec pharetra magna. Vivamus sit amet libero in dolor laoreet dignissim eu eu urna. Proin feugiat, enim sit amet volutpat tempus, elit quam condimentum metus, sit amet hendrerit turpis quam nec risus.</p> */}
                <Link to="page2" spy={true} smooth={true}></Link>
            </Element>

            <Element name="page2" className="page" ref={page2Ref}>
                {/* <h1>Page 2</h1> */}
                <img src={Page2Image} alt="page2" className='pageImage'/>
                {/* {showText && <p>Some more text content... Sed sit amet dui non sapien venenatis finibus in eget lectus. Sed tristique massa eu lectus facilisis, eu consectetur elit cursus. Aenean in malesuada elit, sed facilisis ligula. Integer nec magna sed libero sagittis aliquet.</p>} */}
                <Link to="page3" spy={true} smooth={true}></Link>
            </Element>

            <Element name="page3" className="page">
                {/* <h1>Page 3</h1> */}
                {/* <p>Even more text content... Phasellus id dapibus velit. Cras interdum egestas tortor, nec interdum ante facilisis non. Fusce lacinia, arcu eget dictum posuere, felis lorem tempor tellus, a tristique elit enim sit amet nisi.</p> */}
                <img src={Page3Image} alt="page3" className='pageImage'/>
                <Link to="welcomePage" spy={true} smooth={true}></Link>
            </Element>

            <Element name="page4" className="page">
                {/* <h1>Page 4</h1> */}
                {/* <p>Even more text content... Phasellus id dapibus velit. Cras interdum egestas tortor, nec interdum ante facilisis non. Fusce lacinia, arcu eget dictum posuere, felis lorem tempor tellus, a tristique elit enim sit amet nisi.</p> */}
                <img src={Page4Image} alt="page4" className='pageImage'/>
                <Link to="welcomePage" spy={true} smooth={true}></Link>
            </Element>

            <Element name="page5" className="page">
                {/* <h1>Page 5</h1> */}
                {/* <p>Even more text content... Phasellus id dapibus velit. Cras interdum egestas tortor, nec interdum ante facilisis non. Fusce lacinia, arcu eget dictum posuere, felis lorem tempor tellus, a tristique elit enim sit amet nisi.</p> */}
                <img src={Page5Image} alt="page5" className='pageImage'/>
                <Link to="welcomePage" spy={true} smooth={true}></Link>
            </Element>

            <Element name="page6" className="page">
                {/* <h1>Page 6</h1> */}
                {/* <p>Even more text content... Phasellus id dapibus velit. Cras interdum egestas tortor, nec interdum ante facilisis non. Fusce lacinia, arcu eget dictum posuere, felis lorem tempor tellus, a tristique elit enim sit amet nisi.</p> */}
                <img src={Page6Image} alt="page6" className='pageImage'/>
                <Link to="welcomePage" spy={true} smooth={true}></Link>
            </Element>

            <Element name="page7" className="page">
                {/* <h1>Page 7</h1> */}
                {/* <p>Even more text content... Phasellus id dapibus velit. Cras interdum egestas tortor, nec interdum ante facilisis non. Fusce lacinia, arcu eget dictum posuere, felis lorem tempor tellus, a tristique elit enim sit amet nisi.</p> */}
                <img src={Page7Image} alt="page7" className='pageImage'/>
                <button className="enterButton" onClick={enterSite}>Enter</button>
                <Link to="welcomePage" spy={true} smooth={true}></Link>
            </Element>

            {/* <Element name="welcomePage" className="page">
                <button className="enterButton" onClick={enterSite}>Enter</button>
            </Element> */}

            {/* <div className="welcomepage">
                <div className="Circle">Community</div>
                <div className="Circle_" />
                <div className="sketchContainer">
                    <Sketch />
                </div>
                <button className="enterButton" onClick={enterSite}>Enter</button>
            </div> */}
        </div>
    );
}

export default WelcomePage;