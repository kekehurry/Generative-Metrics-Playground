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
            this.p.stroke(255, 255, 255, 200);
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
            let communityAlpha = 80;
            let futureAlpha = 255;
            let futureTimer = 0;
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

                p.push();
                p.noStroke();

                // create a radial gradient and use it to fill the canvas
                const gradient = radialGradient(p.width / 2 - 30, p.height / 2 - 30, 0, //start point
                                                p.width / 2 + 50, p.height / 2 + 50, 130,  // end point
                                                // p.color(255, 255, 255, 0),  // start color
                                                // p.color(255, 255, 255, 255)); // end color 243, 234, 226
                                                p.color(232,123,116),  // start color
                                                p.color(255)); // end color 
                // p.fill(gradient);
                
                i = i + 0.5;
                if (i < 400) {
                    p.fill(166, 181, 205)
                    p.ellipse(p.width / 2, p.height / 2, i, i);
                } else {
                    p.fill(166, 181, 205)
                    p.ellipse(p.width / 2, p.height / 2, 400, 400);
                }
                p.pop();

// --------------------- text ---------------------
                // 在中间逐渐显示 "community"
                p.push();
                p.fill(161, 128, 68, communityAlpha); // 这里的 alpha 可以改变，用来控制文本的透明度
                p.textSize(40);
                p.textAlign(p.CENTER, p.CENTER);
                p.text('Community', p.width / 2, p.height / 2);
                communityAlpha += 1;
                if (communityAlpha > 255) {
                    communityAlpha = 255;
                }
                p.pop();


                // 在随机位置逐渐显示然后消失的 "future"
                if (futureTimer === 0) {
                    futurePosition = p.createVector(p.random(p.width), p.random(p.height));  // 选择一个随机位置
                    futureTimer = 30;  // 显示 "future" 1秒后开始逐渐消失
                    futureAlpha = 255;  // 重置 alpha
                    currentText = text_list[Math.floor(Math.random() * text_list.length)];
                }
                p.push();
                p.fill(161, 128, 68, futureAlpha);
                p.textSize(30);
                p.textAlign(p.CENTER, p.CENTER);
                p.text(currentText, futurePosition.x, futurePosition.y);
                if (futureTimer > 0) {
                    futureTimer--;  // 如果 timer 不为零，则减小它
                } else {
                    futureAlpha -= 10;  // 如果 timer 为零，开始减小 alpha 使文本逐渐消失
                    if (futureAlpha < 0) {
                        futureAlpha = 0;  // 保证 alpha 不会小于零
                        futureTimer = 0;  // 重置 timer，以便在下一帧开始显示新的 text
                    }
                }
                p.pop();
// --------------------- text ---------------------


            };

        }, sketchRef.current);
    }, []);

    return <div ref={sketchRef} />;


}





