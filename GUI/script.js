function setTheme(themeName) { document.body.className = themeName; }

document.addEventListener('DOMContentLoaded', function() {
    const board = document.getElementById('board');
    const message = document.getElementById('message');
    const resetBtn = document.getElementById('reset');
    // تم حذف undoBtn من هنا
    const btnHuman = document.getElementById('modeHuman');
    const btnAI = document.getElementById('modeAI');
    const scoreHumanEl = document.getElementById('scoreHuman');
    const scoreAIEl = document.getElementById('scoreAI');
    const modal = document.getElementById('winnerModal');
    const winnerText = document.getElementById('winnerText');
    const modalResetBtn = document.getElementById('modalResetBtn');
    
    let scoreHuman = 0;
    let scoreAI = 0;
    const dropSound = new Audio('/static/sounds/drop.mp3'); 
    const winSound = new Audio('/static/sounds/win.mp3');
    dropSound.volume = 0.5;

    let grid = Array(6).fill().map(() => Array(7).fill(''));
    let gameActive = true;
    let currentMode = 'HvC'; 
    let aiLoopTimeout = null;

    function initBoard() {
        board.innerHTML = ''; 
        const frame = document.createElement('div');
        frame.classList.add('board-frame');
        for (let r = 0; r < 6; r++) {
            const rowDiv = document.createElement('div');
            rowDiv.classList.add('row');
            for (let c = 0; c < 7; c++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = r; cell.dataset.col = c;
                cell.addEventListener('click', () => {
                    if (currentMode === 'HvC' && gameActive && grid[0][c] === '') humanMove(c);
                });
                rowDiv.appendChild(cell);
            }
            frame.appendChild(rowDiv);
        }
        board.appendChild(frame);
    }

    function updateBoardUI(newGrid) {
        let pieceDropped = false;
        document.querySelectorAll('.winning-cell').forEach(el => el.classList.remove('winning-cell'));
        for (let r = 0; r < 6; r++) {
            for (let c = 0; c < 7; c++) {
                const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${c}']`);
                const oldVal = grid[r][c];
                const newVal = newGrid[r][c];
                if (oldVal === '' && newVal !== '') {
                    const piece = document.createElement('div');
                    piece.classList.add('piece');
                    piece.classList.add(newVal === 'X' ? 'red' : 'yellow');
                    cell.appendChild(piece);
                    cell.classList.add('taken');
                    pieceDropped = true;
                } else if (newVal === '') { 
                    cell.innerHTML = '';
                    cell.classList.remove('taken');
                }
            }
        }
        grid = newGrid;
        if (pieceDropped) { dropSound.currentTime = 0; dropSound.play().catch(e => {}); }
    }

    function highlightWin(coords) {
        if (!coords || coords.length === 0) return;
        coords.forEach(pos => {
            const cell = document.querySelector(`.cell[data-row='${pos[0]}'][data-col='${pos[1]}']`);
            if (cell) cell.classList.add('winning-cell');
        });
    }

    function fireConfetti() {
        var duration = 3000;
        var end = Date.now() + duration;
        (function frame() {
            confetti({ particleCount: 5, angle: 60, spread: 55, origin: { x: 0 } });
            confetti({ particleCount: 5, angle: 120, spread: 55, origin: { x: 1 } });
            if (Date.now() < end) requestAnimationFrame(frame);
        }());
    }

    function humanMove(col) {
        if (!gameActive) return;
        fetch('/human_move', {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ col: col })
        }).then(res => res.json()).then(data => {
            updateBoardUI(data.grid);
            if (data.winner) handleWinner(data.winner, data.win_coords);
            else { gameActive = false; message.textContent = 'Thinking...'; setTimeout(requestAiMove, 500); }
        });
    }

    function requestAiMove() {
        fetch('/ai_auto_move', { method: 'POST' }).then(res => res.json()).then(data => {
            updateBoardUI(data.grid);
            if (data.winner) handleWinner(data.winner, data.win_coords);
            else {
                if(currentMode === 'HvC') { message.textContent = 'Your turn (Red)'; gameActive = true; }
                else if(currentMode === 'CvC') aiLoopTimeout = setTimeout(requestAiMove, 800);
            }
        });
    }

    // تم حذف الجزء الخاص بـ undoBtn.addEventListener

    function handleWinner(winner, coords) {
        gameActive = false; clearTimeout(aiLoopTimeout); highlightWin(coords);
        if (winner !== 'Draw') {
            fireConfetti(); winSound.currentTime = 0; winSound.play().catch(e => {});
            if (winner === 'X') { scoreHuman++; scoreHumanEl.textContent = scoreHuman; }
            else if (winner === 'O' && currentMode === 'HvC') { scoreAI++; scoreAIEl.textContent = scoreAI; }
        }
        let text = winner === 'Draw' ? "DRAW!" : (winner === 'X' ? "RED WINS!" : "YELLOW WINS!");
        winnerText.textContent = text; winnerText.style.color = winner === 'X' ? "#ff6b6b" : "#f1c40f";
        setTimeout(() => { modal.style.display = "flex"; }, 1000);
    }

    function resetGame(mode) {
        clearTimeout(aiLoopTimeout); currentMode = mode; modal.style.display = "none";
        if (mode === 'HvC') { btnHuman.classList.add('active-mode'); btnAI.classList.remove('active-mode'); message.textContent = "Your turn (Red)"; }
        else { btnHuman.classList.remove('active-mode'); btnAI.classList.add('active-mode'); message.textContent = "Starting AI Loop..."; }
        fetch('/reset', { method: 'POST' }).then(res => res.json()).then(data => {
            updateBoardUI(data.grid); gameActive = true;
            if (mode === 'CvC') setTimeout(requestAiMove, 500);
        });
    }

    resetBtn.addEventListener('click', () => resetGame(currentMode));
    modalResetBtn.addEventListener('click', () => resetGame(currentMode));
    btnHuman.addEventListener('click', () => { btnHuman.classList.add('active-mode'); btnAI.classList.remove('active-mode'); resetGame('HvC'); });
    btnAI.addEventListener('click', () => { btnAI.classList.add('active-mode'); btnHuman.classList.remove('active-mode'); resetGame('CvC'); });

    initBoard();
    resetGame('HvC');
});