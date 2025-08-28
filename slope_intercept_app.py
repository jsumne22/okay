from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Slope-Intercept Learner</title>
    <style>
        body { font-family: sans-serif; }
        #graph { border: 1px solid #333; background: #fafafa; }
        .input-row { margin: 10px 0; }
        .correct { color: green; }
        .incorrect { color: red; }
    </style>
</head>
<body>
    <h2>Slope-Intercept Practice</h2>
    <p>Drag the blue point to a new location. The line will always go through the origin (0,0) and the blue point.</p>
    <canvas id="graph" width="400" height="400"></canvas>
    <div class="input-row">
        <label>Enter the equation of the line (y = mx + b): </label>
        <input id="eqn" type="text" placeholder="y = mx + b">
    </div>
    <div class="input-row">
        <label>What is the value of b? </label>
        <input id="bval" type="text" placeholder="b">
    </div>
    <button onclick="checkAnswer()">Check Answer</button>
    <button onclick="newProblem()">New Problem</button>
    <div id="feedback"></div>
    <script>
    const canvas = document.getElementById('graph');
    const ctx = canvas.getContext('2d');
    const size = 400;
    const scale = 20; // 1 unit = 20px, so 20*10 = 200px from center
    let dragging = false;
    let point = {x: 4, y: 3}; // initial point
    let offset = {x: 0, y: 0};

    function toCanvas(x, y) {
        // Convert math coords to canvas coords
        return [size/2 + x*scale, size/2 - y*scale];
    }
    function toMath(x, y) {
        // Convert canvas coords to math coords
        return [(x - size/2)/scale, (size/2 - y)/scale];
    }
    function draw() {
        ctx.clearRect(0,0,size,size);
        // Draw grid
        ctx.strokeStyle = '#ddd';
        for(let i=-10;i<=10;i++){
            let [cx,cy] = toCanvas(i,0);
            ctx.beginPath(); ctx.moveTo(cx,0); ctx.lineTo(cx,size); ctx.stroke();
            [cx,cy] = toCanvas(0,i);
            ctx.beginPath(); ctx.moveTo(0,cy); ctx.lineTo(size,cy); ctx.stroke();
        }
        // Draw axes
        ctx.strokeStyle = '#333';
        ctx.beginPath(); ctx.moveTo(0,size/2); ctx.lineTo(size,size/2); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(size/2,0); ctx.lineTo(size/2,size); ctx.stroke();
        // Draw origin
        let [ox,oy] = toCanvas(0,0);
        ctx.fillStyle = 'black';
        ctx.beginPath(); ctx.arc(ox,oy,5,0,2*Math.PI); ctx.fill();
        // Draw draggable point
        let [px,py] = toCanvas(point.x, point.y);
        ctx.fillStyle = 'blue';
        ctx.beginPath(); ctx.arc(px,py,8,0,2*Math.PI); ctx.fill();
        // Draw line
        ctx.strokeStyle = 'red';
        ctx.beginPath(); ctx.moveTo(ox,oy); ctx.lineTo(px,py); ctx.stroke();
    }
    function isOnPoint(mx, my) {
        let [px,py] = toCanvas(point.x, point.y);
        return Math.hypot(mx-px, my-py) < 12;
    }
    canvas.onmousedown = function(e) {
        let rect = canvas.getBoundingClientRect();
        let mx = e.clientX - rect.left, my = e.clientY - rect.top;
        if(isOnPoint(mx,my)) {
            dragging = true;
            offset.x = mx - toCanvas(point.x, point.y)[0];
            offset.y = my - toCanvas(point.x, point.y)[1];
        }
    };
    canvas.onmousemove = function(e) {
        if(dragging) {
            let rect = canvas.getBoundingClientRect();
            let mx = e.clientX - rect.left - offset.x, my = e.clientY - rect.top - offset.y;
            let [x,y] = toMath(mx, my);
            // Clamp to -10..10
            x = Math.max(-10, Math.min(10, Math.round(x)));
            y = Math.max(-10, Math.min(10, Math.round(y)));
            if(x === 0 && y === 0) return; // don't allow origin
            point.x = x; point.y = y;
            draw();
        }
    };
    canvas.onmouseup = function(){ dragging = false; };
    canvas.onmouseleave = function(){ dragging = false; };
    function checkAnswer() {
        let eqn = document.getElementById('eqn').value.replace(/\s+/g,'');
        let bval = document.getElementById('bval').value.trim();
        let m = (point.x === 0) ? 0 : (point.y/point.x);
        let b = 0;
        let correctEqn = `y=${m}x+${b}`;
        let altEqn = `y=${m}x`;
        let correct = (eqn === correctEqn || eqn === altEqn) && (bval == '0' || bval == 0);
        let feedback = document.getElementById('feedback');
        if(correct) {
            feedback.innerHTML = `<div class='correct'>Correct!<br>
            The slope m = (y2-y1)/(x2-x1) = (${point.y}-0)/(${point.x}-0) = ${m}.<br>
            Since the line passes through the origin, b = 0.<br>
            The equation is y = ${m}x + 0.<br>
            <b>Try a new problem!</b></div>`;
        } else {
            feedback.innerHTML = `<div class='incorrect'>Try again!<br>
            The line goes through (0,0) and (${point.x},${point.y}).<br>
            Slope m = (${point.y}-0)/(${point.x}-0) = ${m}.<br>
            b = 0 since it crosses the y-axis at the origin.</div>`;
        }
    }
    function newProblem() {
        // Pick a random point not at origin
        let x=0,y=0;
        while(x===0 && y===0) {
            x = Math.floor(Math.random()*21)-10;
            y = Math.floor(Math.random()*21)-10;
        }
        point.x = x; point.y = y;
        document.getElementById('eqn').value = '';
        document.getElementById('bval').value = '';
        document.getElementById('feedback').innerHTML = '';
        draw();
    }
    draw();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
