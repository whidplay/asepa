import streamlit as st # type: ignore

st.title("Percent Breaker")

st.markdown("""
## <Game Tips>

1. 이 게임은 패들로 공을 튕겨 벽돌을 깨는 게임입니다.
2. 10초마다 화면에 벽돌 한 줄이 새로 생기게 됩니다.
3. 공이 패들에 닿지 못하거나, 벽돌이 빨간 점선을 넘을 경우 게임 오버입니다.
4. 간혹 벽돌을 깼을 때, 패들에 닿으면 특정한 능력을 얻는 삼각형이 아래로 떨어집니다.
5. 특정한 능력으로는 패들의 크기 조절, 공의 속도 조절이 있습니다.
6. 100점을 달성한 상태로 벽돌을 깨면 게임에서 승리합니다.
7. PC 환경에서 게임을 플레이하는 것을 추천합니다.
8. 타임어택으로 게임을 플레이하면 더욱 재밌습니다.
""")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        canvas {
            background-color: #000000;
            display: block;
            margin: 0 auto;
        }
        #startButton {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            font-size: 20px;
        }
        #startButton.hidden {
            display: none;
        }
        #timer {
            font-size: 24px;
            color: #0095DD;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <button id="startButton">Start</button>
    <div id="timer">Time: 00:00.00</div>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const startButton = document.getElementById('startButton');
        const timerElement = document.getElementById('timer');

        let ballRadius = 10;
        let x, y, dx, dy, paddleHeight, paddleWidth, paddleX, rightPressed, leftPressed, brickRowCount, brickColumnCount, brickWidth, brickHeight, brickPadding, brickOffsetTop, brickOffsetLeft, score, interval, addRowInterval, dangerLineY;
        const colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#8B00FF"];
        let bricks = [];
        let bubbles = [];
        let gameStarted = false;
        let gameOver = false;
        let startTime, elapsedTime, timerInterval;

        function initializeGame() {
            canvas.width = window.innerWidth * 0.8;
            canvas.height = window.innerHeight * 0.7;
            ballRadius = 10;
            x = canvas.width / 2;
            y = canvas.height - 30;
            dx = 2;
            dy = -2;
            paddleHeight = 5;
            paddleWidth = canvas.width * 0.2;
            paddleX = (canvas.width - paddleWidth) / 2;
            rightPressed = false;
            leftPressed = false;
            brickRowCount = 4;
            brickColumnCount = 8;
            brickWidth = canvas.width / brickColumnCount - 10;
            brickHeight = 20;
            brickPadding = 10;
            brickOffsetTop = 30;
            brickOffsetLeft = (canvas.width - (brickColumnCount * (brickWidth + brickPadding) - brickPadding)) / 2;
            score = 0;
            dangerLineY = canvas.height - paddleHeight - 50;
            bricks = [];
            for(let c = 0; c < brickColumnCount; c++) {
                bricks[c] = [];
                for(let r = 0; r < brickRowCount; r++) {
                    bricks[c][r] = { x: 0, y: 0, status: 1, color: colors[(c + r) % colors.length] };
                }
            }

            if (interval) {
                clearInterval(interval);
            }
            if (addRowInterval) {
                clearInterval(addRowInterval);
            }
            if (timerInterval) {
                clearInterval(timerInterval);
            }

            gameStarted = false;
            gameOver = false;
            startTime = null;
            elapsedTime = 0;

            startButton.classList.remove('hidden');
            updateTimerDisplay();
        }

        function updateTimerDisplay() {
            if (startTime) {
                const now = new Date().getTime();
                elapsedTime = (now - startTime) / 1000;
                const minutes = Math.floor(elapsedTime / 60);
                const seconds = Math.floor(elapsedTime % 60);
                const milliseconds = Math.floor((elapsedTime % 1) * 100);
                timerElement.textContent = `Time: ${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(milliseconds).padStart(2, '0')}`;
            } else {
                timerElement.textContent = `Time: 00:00.00`;
            }
        }

        function keyDownHandler(e) {
            if(e.key === "Right" || e.key === "ArrowRight") {
                rightPressed = true;
            }
            else if(e.key === "Left" || e.key === "ArrowLeft") {
                leftPressed = true;
            }
        }

        function keyUpHandler(e) {
            if(e.key === "Right" || e.key === "ArrowRight") {
                rightPressed = false;
            }
            else if(e.key === "Left" || e.key === "ArrowLeft") {
                leftPressed = false;
            }
        }

        function createBubble(x, y) {
            bubbles.push({
                x: x,
                y: y,
                radius: 10,
                color: "rgba(0, 255, 255, 0.8)"
            });
        }

        function applyAbility() {
    const random = Math.random();

    if (random < 0.15) {
        dx *= 0.8;
        dy *= 0.8;
    } else if (random < 0.30) {
        dx *= 1.5;
        dy *= 1.5;
    } else if (random < 0.65) {
        paddleWidth *= 0.8;
    } else {
        paddleWidth *= 1.2;
    }
}

        function collisionDetection() {
            for(let c = 0; c < brickColumnCount; c++) {
                for(let r = 0; r < brickRowCount; r++) {
                    const b = bricks[c][r];
                    if(b.status === 1) {
                        if(x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                            dy = -dy;
                            b.status = 0;
                            score++;
                            if (Math.random() < 0.10) {
                                createBubble(b.x + brickWidth / 2, b.y + brickHeight / 2);
                            }
                            if(score > 100) {
                                alert("YOU WIN!");
                                document.location.reload();
                            }
                        }
                    }
                }
            }
        }

        function drawBall() {
            ctx.beginPath();
            ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
            ctx.fillStyle = "#FF0000";
            ctx.fill();
            ctx.closePath();
        }

        function drawPaddle() {
            ctx.beginPath();
            ctx.rect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight);
            ctx.fillStyle = "#0095DD";
            ctx.fill();
            ctx.closePath();
        }

        function drawBricks() {
            for(let c = 0; c < brickColumnCount; c++) {
                for(let r = 0; r < brickRowCount; r++) {
                    if(bricks[c][r].status === 1) {
                        const brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                        const brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                        bricks[c][r].x = brickX;
                        bricks[c][r].y = brickY;
                        ctx.beginPath();
                        ctx.rect(brickX, brickY, brickWidth, brickHeight);
                        ctx.fillStyle = bricks[c][r].color;
                        ctx.fill();
                        ctx.closePath();
                    }
                }
            }
        }

        function drawScore() {
            ctx.font = "16px Arial";
            ctx.fillStyle = "#0095DD";
            ctx.fillText("Score: " + score, 8, 20);
        }

        function drawBubbles() {
            bubbles.forEach((bubble, index) => {
                ctx.beginPath();
                
                const height = bubble.radius * Math.sqrt(3);
                ctx.moveTo(bubble.x, bubble.y - height / 2);
                ctx.lineTo(bubble.x - bubble.radius, bubble.y + height / 2);
                ctx.lineTo(bubble.x + bubble.radius, bubble.y + height / 2);
                ctx.closePath();
                
                ctx.fillStyle = bubble.color;
                ctx.fill();
                
                bubble.y += 2;

                if (bubble.y > canvas.height) {
                    bubbles.splice(index, 1);
                }
            });
        }

        function drawDangerLine() {
            ctx.beginPath();
            ctx.setLineDash([5, 15]);
            ctx.moveTo(0, dangerLineY);
            ctx.lineTo(canvas.width, dangerLineY);
            ctx.strokeStyle = "#FF0000";
            ctx.stroke();
            ctx.closePath();
        }

        function checkGameOver() {
            if (!gameOver) {
                for (let c = 0; c < brickColumnCount; c++) {
                    for (let r = 0; r < brickRowCount; r++) {
                        const b = bricks[c][r];
                        if (b.status === 1 && b.y + brickHeight > dangerLineY) {
                            gameOver = true;
                            clearInterval(interval);
                            clearInterval(addRowInterval);
                            clearInterval(timerInterval);
                            setTimeout(() => {
                                drawBreakEffect();
                                setTimeout(() => {
                                    alert("GAME OVER");
                                    document.location.reload();
                                }, 1000);
                            }, 1000);
                            return;
                        }
                    }
                }
            }
        }

        function checkBubblePaddleCollision() {
            bubbles.forEach((bubble, index) => {
                if (bubble.y + bubble.radius > canvas.height - paddleHeight - 10 && 
                    bubble.x > paddleX && bubble.x < paddleX + paddleWidth) {
                    bubbles.splice(index, 1);
                    applyAbility();
                }
            });
        }

        function drawBreakEffect() {
            const particles = [];
            const numParticles = 30;
            for (let i = 0; i < numParticles; i++) {
                particles.push({
                    x: x,
                    y: y,
                    dx: (Math.random() - 0.5) * 10,
                    dy: (Math.random() - 0.5) * 10,
                    radius: Math.random() * 5 + 2,
                    color: "rgba(255, 0, 0, 0.8)",
                    lifetime: Math.random() * 20 + 10
                });
            }

            function animateParticles() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                drawBricks();
                drawPaddle();
                drawScore();
                drawBubbles();
                drawDangerLine();

                particles.forEach((particle, index) => {
                    ctx.beginPath();
                    ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
                    ctx.fillStyle = particle.color;
                    ctx.fill();
                    ctx.closePath();

                    particle.x += particle.dx;
                    particle.y += particle.dy;
                    particle.lifetime--;

                    if (particle.lifetime <= 0) {
                        particles.splice(index, 1);
                    }
                });

                if (particles.length > 0) {
                    requestAnimationFrame(animateParticles);
                }
            }

            animateParticles();
        }

        function checkBallPaddleCollision() {
    const ballLeft = x - ballRadius;
    const ballRight = x + ballRadius;
    const ballTop = y - ballRadius;
    const ballBottom = y + ballRadius;

    const paddleLeft = paddleX;
    const paddleRight = paddleX + paddleWidth;
    const paddleTop = canvas.height - paddleHeight - 10;
    const paddleBottom = canvas.height - paddleHeight - 10 + paddleHeight;

    if (ballRight > paddleLeft && ballLeft < paddleRight && ballBottom > paddleTop && ballTop < paddleBottom) {
        dy = -dy;

        // Optional: Adjust ball direction based on where it hits the paddle
        const ballCenterX = x;
        const paddleCenterX = paddleX + paddleWidth / 2;
        const distanceFromCenter = ballCenterX - paddleCenterX;
        const normalizedDistance = distanceFromCenter / (paddleWidth / 2);
        dx = 2 * normalizedDistance;
    }
}

function draw() {
    if (gameStarted && !gameOver) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBricks();
        drawBall();
        drawPaddle();
        drawScore();
        drawBubbles();
        drawDangerLine();
        collisionDetection();
        checkBubblePaddleCollision();
        checkGameOver();
        
        checkBallPaddleCollision();

        if (x + dx > canvas.width - ballRadius || x - ballRadius < 0) {
            dx = -dx;
        }
        if (y + dy < ballRadius) {
            dy = -dy;
        } else if (y + dy > canvas.height - ballRadius - paddleHeight - 10) {
            if (x > paddleX && x < paddleX + paddleWidth) {
                dy = -dy;
            } else if (y + dy > canvas.height - ballRadius) {
                if (!gameOver) {
                    gameOver = true;
                    clearInterval(interval);
                    clearInterval(addRowInterval);
                    clearInterval(timerInterval);
                    setTimeout(() => {
                        drawBreakEffect();
                        setTimeout(() => {
                            alert("GAME OVER");
                            document.location.reload();
                        }, 1000);
                    }, 1000);
                }
            }
        }

        if (rightPressed && paddleX < canvas.width - paddleWidth) {
            paddleX += 7;
        } else if (leftPressed && paddleX > 0) {
            paddleX -= 7;
        }

        x += dx;
        y += dy;

        updateTimerDisplay();
    }
}

        function addBrickRow() {
            if (!gameOver) {
                for(let c = 0; c < brickColumnCount; c++) {
                    bricks[c].unshift({ x: 0, y: 0, status: 1, color: colors[Math.floor(Math.random() * colors.length)] });
                }
                brickRowCount++;

                for(let c = 0; c < brickColumnCount; c++) {
                    for(let r = 0; r < brickRowCount; r++) {
                        bricks[c][r].y += brickHeight + brickPadding;
                    }
                }
            }
        }

        function startGame() {
            if (!gameStarted) {
                gameStarted = true;
                startButton.classList.add('hidden');
                startTime = new Date().getTime();
                timerInterval = setInterval(updateTimerDisplay, 10);
                interval = setInterval(draw, 10);
                addRowInterval = setInterval(addBrickRow, 10000);
            }
        }

        document.addEventListener("keydown", keyDownHandler, false);
        document.addEventListener("keyup", keyUpHandler, false);
        startButton.addEventListener('click', startGame);

        initializeGame();
    </script>
</body>
</html>
"""

st.components.v1.html(game_code, height=520)