import React, { useRef, useEffect } from 'react';
import p5 from 'p5';  // 引入 p5 库

class Particle {
    constructor(p, scl, cols) {
        this.p = p;
        this.scl = scl;
        this.cols = cols;
        this.pos = p.createVector(p.random(p.width), p.random(p.height));
        this.vel = p.createVector();
        this.acc = p.createVector();
        this.maxspeed = 2;

        this.color = p.color(68, 105, 161, 5);

    }

    follow(flowfield) {
        let x = this.p.floor(this.pos.x / this.scl);
        let y = this.p.floor(this.pos.y / this.scl);
        let index = x + y * this.cols;
        let force = flowfield[index];
        this.applyForce(force);
    }

    update() {
        this.vel.add(this.acc);
        this.vel.limit(this.maxspeed);
        this.pos.add(this.vel);
        this.acc.mult(0);
    }

    applyForce(force) {
        this.acc.add(force);
    }

    edges() {
        if (this.pos.x > this.p.width) this.pos.x = 0;
        if (this.pos.x < 0) this.pos.x = this.p.width;
        if (this.pos.y > this.p.height) this.pos.y = 0;
        if (this.pos.y < 0) this.pos.y = this.p.height;
    }

    show() {
        let d = this.p.dist(this.pos.x, this.pos.y, this.p.mouseX, this.p.mouseY);
        if (d < 50) {
            // this.color = this.p.color(89, 151, 155, 5);
            this.color = this.p.color(41, 145, 186, 5);
        } else {
            // this.color = this.p.color(68, 105, 161, 5);
            this.color = this.p.color(105, 135, 190, 5);
        }
        this.p.strokeWeight(2);  // set the stroke weight

        // add shining effect
        if (this.p.random(1) < 0.01) {
            this.p.stroke(255, 255, 255, 100);
            this.p.strokeWeight(1);
        } else {
            this.p.stroke(this.color);
        }
        this.p.point(this.pos.x, this.pos.y);
    }
}

export default function Sketch() {

    const sketchRef = useRef();

    useEffect(() => {
        new p5(p => {
            let cols, rows;
            let scl = 20;
            let zoff = 0;
            let particles = [];
            let flowfield;
            let i = 0;

// --------------------- text ---------------------
            let futureAlpha = 0;
            let textPhase = 'showing';
            let textPhaseCounter = 0;
            let futureTimer = 60;
            let futurePosition;
            let text_list = ['safe','peace','activity','innovation','sustainable','accessible','diversity','convenient']
            let currentText = '';
// --------------------- text ---------------------


            const radialGradient = (sX, sY, sR, eX, eY, eR, colorS, colorE) => {
                const gradient = p.drawingContext.createRadialGradient(sX, sY, sR, eX, eY, eR);
                
                gradient.addColorStop(0, colorS.toString());
                gradient.addColorStop(1, colorE.toString());
                
                return gradient;
            };

            p.setup = () => {
                p.createCanvas(p.windowWidth, p.windowHeight);
                cols = p.floor(p.width / scl);
                rows = p.floor(p.height / scl);
                flowfield = new Array(cols * rows);
                // create particles
                for (let i = 0; i < 2000; i++) {
                    particles[i] = new Particle(p, scl, cols);
                }
                // p.background(243, 234, 226);
                p.background(19, 18, 26);

            };

            p.draw = () => {
                let yoff = 0;
                for (let y = 0; y < rows; y++) {
                    let xoff = 0;
                    for (let x = 0; x < cols; x++) {
                        let index = x + y * cols;
                        let angle = p.noise(xoff, yoff, zoff) * p.TWO_PI * 2;
                        let v = p5.Vector.fromAngle(angle);
                        v.setMag(1);
                        flowfield[index] = v;
                        xoff += 0.1;
                    }
                    yoff += 0.1;
                }
                zoff += 0.01;

                for (let i = 0; i < particles.length; i++) {
                    particles[i].follow(flowfield);
                    particles[i].update();
                    particles[i].edges();
                    particles[i].show();
                }

                // p.push();
                // p.noStroke();
                // let gradient = p.drawingContext.createLinearGradient(p.width/2, p.height/2 -200, p.width/2, p.height/2+200);
                // gradient.addColorStop(0, 'rgb(232, 28, 255)');
                // gradient.addColorStop(1, 'rgb(64, 201, 255)');
                // p.drawingContext.fillStyle = gradient;
                // // p.fill(166, 181, 205)
                // p.ellipse(p.width / 2, p.height / 2, 400, 400);
                // p.pop();


                // // create a radial gradient and use it to fill the canvas
                // const gradient = radialGradient(p.width / 2 - 30, p.height / 2 - 30, 0, //start point
                //                                 p.width / 2 + 50, p.height / 2 + 50, 130,  // end point
                //                                 // p.color(255, 255, 255, 0),  // start color
                //                                 // p.color(255, 255, 255, 255)); // end color 243, 234, 226
                //                                 p.color(232,123,116),  // start color
                //                                 p.color(255)); // end color 
                // // p.fill(gradient);
                
                // i = i + 0.5;
                // if (i < 400) {
                //     p.fill(166, 181, 205)
                //     p.ellipse(p.width / 2, p.height / 2, i, i);
                // } else {
                //     p.fill(166, 181, 205)
                //     p.ellipse(p.width / 2, p.height / 2, 400, 400);
                // }
                // p.pop();

                // --------------------- text ---------------------
                // showing text
                // p.push();
                // p.noStroke();
                // p.fill(255, 255, 255, futureAlpha); // 这里的 alpha 可以改变，用来控制文本的透明度
                // p.textSize(25);
                // p.textAlign(p.CENTER, p.CENTER);
                // futurePosition = p.createVector(p.random(p.width), p.random(p.height)); // 随机生成位置
                // currentText = text_list[Math.floor(Math.random() * text_list.length)];
                // p.text(currentText, futurePosition.x, futurePosition.y); // 在随机位置显示文本
                // futureAlpha += 0.1;
                // if (futureAlpha > 255) {
                //     futureAlpha = 255;
                // }
                // p.pop();


                // --------------------- text ---------------------


            };

        }, sketchRef.current);
    }, []);

    return <div ref={sketchRef} />;


}





