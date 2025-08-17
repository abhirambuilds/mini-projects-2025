class MemoryGame {
    constructor() {
        this.cards = [];
        this.flippedCards = [];
        this.matchedPairs = 0;
        this.moves = 0;
        this.score = 0;
        this.hintsLeft = 3;
        this.gameStarted = false;
        this.timer = null;
        this.seconds = 0;
        this.currentDifficulty = 'easy';
        this.soundEnabled = true;
        this.isDarkTheme = true;
        this.bestTimes = this.loadBestTimes();
        
        this.difficultySettings = {
            easy: { pairs: 6, gridCols: 4, timeBonus: 1000, moveBonus: 50 },
            medium: { pairs: 8, gridCols: 4, timeBonus: 1500, moveBonus: 75 },
            hard: { pairs: 10, gridCols: 5, timeBonus: 2000, moveBonus: 100 },
            extreme: { pairs: 12, gridCols: 6, timeBonus: 2500, moveBonus: 125 }
        };
        
        this.cardIcons = [
            '🚀', '🎮', '🎨', '🎭', '🎪', '🎯', '🎲', '🎸',
            '🎹', '🎺', '🎻', '🎤', '🎧', '🎬', '🎭', '🎪',
            '🎨', '🎯', '🎲', '🎸', '🎹', '🎺', '🎻', '🎤',
            '🌟', '💎', '🔥', '⚡', '🌈', '🎊', '🎉', '🏆'
        ];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.createGame();
        this.createFloatingParticles();
        this.updateDisplay();
        this.loadSettings();
    }
    
    setupEventListeners() {
        // Difficulty button listeners
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.changeDifficulty(e.target.closest('.difficulty-btn').dataset.difficulty);
            });
        });
        
        // Control buttons
        document.getElementById('sound-toggle').addEventListener('click', () => this.toggleSound());
        document.getElementById('theme-toggle').addEventListener('click', () => this.toggleTheme());
        document.getElementById('new-game-btn').addEventListener('click', () => this.createGame());
        document.getElementById('hint-btn').addEventListener('click', () => this.useHint());
        document.getElementById('play-again-btn').addEventListener('click', () => this.playAgain());
        document.getElementById('share-btn').addEventListener('click', () => this.shareScore());
    }
    
    createFloatingParticles() {
        const container = document.querySelector('.container');
        for (let i = 0; i < 10; i++) {
            const particle = document.createElement('div');
            particle.className = 'floating-particle';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 6 + 's';
            container.appendChild(particle);
        }
    }
    
    loadSettings() {
        this.soundEnabled = localStorage.getItem('soundEnabled') !== 'false';
        this.isDarkTheme = localStorage.getItem('isDarkTheme') !== 'false';
        this.updateTheme();
        this.updateSoundIcon();
    }
    
    saveSettings() {
        localStorage.setItem('soundEnabled', this.soundEnabled);
        localStorage.setItem('isDarkTheme', this.isDarkTheme);
    }
    
    toggleSound() {
        this.soundEnabled = !this.soundEnabled;
        this.updateSoundIcon();
        this.saveSettings();
        this.playSound('toggle');
    }
    
    toggleTheme() {
        this.isDarkTheme = !this.isDarkTheme;
        this.updateTheme();
        this.saveSettings();
        this.playSound('toggle');
    }
    
    updateTheme() {
        if (this.isDarkTheme) {
            document.body.classList.remove('light-theme');
            document.getElementById('theme-toggle').innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            document.body.classList.add('light-theme');
            document.getElementById('theme-toggle').innerHTML = '<i class="fas fa-sun"></i>';
        }
    }
    
    updateSoundIcon() {
        const icon = this.soundEnabled ? 'fa-volume-up' : 'fa-volume-mute';
        document.getElementById('sound-toggle').innerHTML = `<i class="fas ${icon}"></i>`;
    }
    
    playSound(type) {
        if (!this.soundEnabled) return;
        
        // Create audio context for sound effects
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        switch(type) {
            case 'flip':
                oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
                break;
            case 'match':
                oscillator.frequency.setValueAtTime(523, audioContext.currentTime);
                oscillator.frequency.setValueAtTime(659, audioContext.currentTime + 0.1);
                oscillator.frequency.setValueAtTime(784, audioContext.currentTime + 0.2);
                break;
            case 'win':
                oscillator.frequency.setValueAtTime(523, audioContext.currentTime);
                oscillator.frequency.setValueAtTime(659, audioContext.currentTime + 0.1);
                oscillator.frequency.setValueAtTime(784, audioContext.currentTime + 0.2);
                oscillator.frequency.setValueAtTime(1047, audioContext.currentTime + 0.3);
                break;
            case 'hint':
                oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
                oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);
                break;
            case 'toggle':
                oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
                oscillator.frequency.setValueAtTime(400, audioContext.currentTime + 0.1);
                break;
        }
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    }
    
    changeDifficulty(difficulty) {
        // Update active button
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-difficulty="${difficulty}"]`).classList.add('active');
        
        this.currentDifficulty = difficulty;
        this.createGame();
    }
    
    createGame() {
        this.resetGame();
        this.createCards();
        this.shuffleCards();
        this.renderGame();
        this.updateProgress();
    }
    
    resetGame() {
        this.cards = [];
        this.flippedCards = [];
        this.matchedPairs = 0;
        this.moves = 0;
        this.score = 0;
        this.hintsLeft = 3;
        this.gameStarted = false;
        this.seconds = 0;
        
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        
        this.updateDisplay();
        this.updateProgress();
        this.hideWinScreen();
        this.updateHintButton();
    }
    
    createCards() {
        const { pairs } = this.difficultySettings[this.currentDifficulty];
        const selectedIcons = this.cardIcons.slice(0, pairs);
        
        // Create pairs of cards
        for (let i = 0; i < pairs; i++) {
            this.cards.push({
                id: i * 2,
                icon: selectedIcons[i],
                isFlipped: false,
                isMatched: false
            });
            
            this.cards.push({
                id: i * 2 + 1,
                icon: selectedIcons[i],
                isFlipped: false,
                isMatched: false
            });
        }
    }
    
    shuffleCards() {
        // Fisher-Yates shuffle algorithm
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }
    
    renderGame() {
        const gameBoard = document.getElementById('game-board');
        const { pairs, gridCols } = this.difficultySettings[this.currentDifficulty];
        
        // Set grid columns
        gameBoard.style.gridTemplateColumns = `repeat(${gridCols}, 1fr)`;
        
        // Clear board
        gameBoard.innerHTML = '';
        
        // Create card elements
        this.cards.forEach(card => {
            const cardElement = this.createCardElement(card);
            gameBoard.appendChild(cardElement);
        });
    }
    
    createCardElement(card) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        cardDiv.dataset.id = card.id;
        
        // Create card front and back
        const cardFront = document.createElement('div');
        cardFront.className = 'card-front';
        cardFront.innerHTML = '❓';
        
        const cardBack = document.createElement('div');
        cardBack.className = 'card-back';
        cardBack.innerHTML = card.icon;
        
        cardDiv.appendChild(cardFront);
        cardDiv.appendChild(cardBack);
        
        // Add click event
        cardDiv.addEventListener('click', () => this.flipCard(card));
        
        return cardDiv;
    }
    
    flipCard(card) {
        // Prevent flipping if card is already flipped, matched, or if two cards are already flipped
        if (card.isFlipped || card.isMatched || this.flippedCards.length >= 2) {
            return;
        }
        
        // Start timer on first card flip
        if (!this.gameStarted) {
            this.startTimer();
            this.gameStarted = true;
        }
        
        // Flip the card
        card.isFlipped = true;
        this.flippedCards.push(card);
        
        // Play sound
        this.playSound('flip');
        
        // Update display
        this.updateCardDisplay(card);
        
        // Check if two cards are flipped
        if (this.flippedCards.length === 2) {
            this.moves++;
            this.updateDisplay();
            this.updateProgress();
            this.checkMatch();
        }
    }
    
    updateCardDisplay(card) {
        const cardElement = document.querySelector(`[data-id="${card.id}"]`);
        if (cardElement) {
            if (card.isFlipped) {
                cardElement.classList.add('flipped');
            } else {
                cardElement.classList.remove('flipped');
            }
            
            if (card.isMatched) {
                cardElement.classList.add('matched');
            }
        }
    }
    
    checkMatch() {
        const [card1, card2] = this.flippedCards;
        
        if (card1.icon === card2.icon) {
            // Match found
            card1.isMatched = true;
            card2.isMatched = true;
            this.matchedPairs++;
            
            // Calculate score
            const { timeBonus, moveBonus } = this.difficultySettings[this.currentDifficulty];
            const timeScore = Math.max(0, timeBonus - this.seconds * 10);
            const moveScore = Math.max(0, moveBonus - this.moves * 5);
            this.score += timeScore + moveScore;
            
            // Play sound
            this.playSound('match');
            
            // Update display
            this.updateCardDisplay(card1);
            this.updateCardDisplay(card2);
            this.updateDisplay();
            
            // Clear flipped cards
            this.flippedCards = [];
            
            // Check if game is won
            if (this.matchedPairs === this.difficultySettings[this.currentDifficulty].pairs) {
                this.gameWon();
            }
        } else {
            // No match, flip cards back after delay
            setTimeout(() => {
                card1.isFlipped = false;
                card2.isFlipped = false;
                
                this.updateCardDisplay(card1);
                this.updateCardDisplay(card2);
                
                this.flippedCards = [];
            }, 1000);
        }
    }
    
    useHint() {
        if (this.hintsLeft <= 0 || this.flippedCards.length > 0) return;
        
        // Find unmatched cards
        const unmatchedCards = this.cards.filter(card => !card.isMatched && !card.isFlipped);
        if (unmatchedCards.length === 0) return;
        
        // Find a pair
        const card1 = unmatchedCards[0];
        const card2 = unmatchedCards.find(card => card.icon === card1.icon && card.id !== card1.id);
        
        if (card2) {
            // Highlight the pair briefly
            this.highlightCards([card1, card2]);
            this.hintsLeft--;
            this.updateHintButton();
            this.playSound('hint');
        }
    }
    
    highlightCards(cards) {
        cards.forEach(card => {
            const element = document.querySelector(`[data-id="${card.id}"]`);
            if (element) {
                element.style.boxShadow = '0 0 30px rgba(255, 255, 0, 0.8)';
                element.style.borderColor = '#ffff00';
            }
        });
        
        // Remove highlight after 2 seconds
        setTimeout(() => {
            cards.forEach(card => {
                const element = document.querySelector(`[data-id="${card.id}"]`);
                if (element) {
                    element.style.boxShadow = '';
                    element.style.borderColor = '';
                }
            });
        }, 2000);
    }
    
    updateHintButton() {
        const hintBtn = document.getElementById('hint-btn');
        const hintsLeftSpan = document.getElementById('hints-left');
        
        hintsLeftSpan.textContent = this.hintsLeft;
        hintBtn.disabled = this.hintsLeft <= 0 || this.flippedCards.length > 0;
    }
    
    startTimer() {
        this.timer = setInterval(() => {
            this.seconds++;
            this.updateDisplay();
        }, 1000);
    }
    
    updateProgress() {
        const { pairs } = this.difficultySettings[this.currentDifficulty];
        const progress = (this.matchedPairs / pairs) * 100;
        
        document.getElementById('progress-fill').style.width = `${progress}%`;
        document.getElementById('progress-text').textContent = `${Math.round(progress)}% Complete`;
    }
    
    updateDisplay() {
        // Update timer
        const minutes = Math.floor(this.seconds / 60);
        const remainingSeconds = this.seconds % 60;
        document.getElementById('timer').textContent = 
            `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        
        // Update moves
        document.getElementById('moves').textContent = this.moves;
        
        // Update score
        document.getElementById('score').textContent = this.score.toLocaleString();
        
        // Update best time
        const bestTime = this.bestTimes[this.currentDifficulty];
        if (bestTime) {
            const bestMinutes = Math.floor(bestTime / 60);
            const bestSeconds = bestTime % 60;
            document.getElementById('best-time').textContent = 
                `${bestMinutes.toString().padStart(2, '0')}:${bestSeconds.toString().padStart(2, '0')}`;
        } else {
            document.getElementById('best-time').textContent = '--:--';
        }
    }
    
    gameWon() {
        // Stop timer
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        
        // Check for best time
        const currentTime = this.seconds;
        const bestTime = this.bestTimes[this.currentDifficulty];
        
        if (!bestTime || currentTime < bestTime) {
            this.bestTimes[this.currentDifficulty] = currentTime;
            this.saveBestTimes();
        }
        
        // Calculate final score and stars
        const finalScore = this.calculateFinalScore();
        const stars = this.calculateStars();
        
        // Update final stats
        document.getElementById('final-time').textContent = document.getElementById('timer').textContent;
        document.getElementById('final-moves').textContent = this.moves;
        document.getElementById('final-score').textContent = finalScore.toLocaleString();
        
        // Update stars display
        this.updateStarsDisplay(stars);
        
        // Play win sound
        this.playSound('win');
        
        // Show win screen
        this.showWinScreen();
    }
    
    calculateFinalScore() {
        const { pairs } = this.difficultySettings[this.currentDifficulty];
        const baseScore = pairs * 100;
        const timeBonus = Math.max(0, 1000 - this.seconds * 5);
        const moveBonus = Math.max(0, 500 - this.moves * 10);
        
        return baseScore + timeBonus + moveBonus;
    }
    
    calculateStars() {
        const { pairs } = this.difficultySettings[this.currentDifficulty];
        const maxTime = pairs * 15; // 15 seconds per pair
        const maxMoves = pairs * 2; // 2 moves per pair
        
        let stars = 3;
        if (this.seconds > maxTime * 1.5 || this.moves > maxMoves * 1.5) stars--;
        if (this.seconds > maxTime * 2 || this.moves > maxMoves * 2) stars--;
        
        return Math.max(1, stars);
    }
    
    updateStarsDisplay(stars) {
        const starsDisplay = document.getElementById('final-stars');
        starsDisplay.innerHTML = '';
        
        for (let i = 0; i < 3; i++) {
            const star = document.createElement('i');
            star.className = i < stars ? 'fas fa-star' : 'far fa-star';
            star.style.color = i < stars ? '#ffd700' : '#ccc';
            starsDisplay.appendChild(star);
        }
    }
    
    loadBestTimes() {
        const saved = localStorage.getItem('bestTimes');
        return saved ? JSON.parse(saved) : {};
    }
    
    saveBestTimes() {
        localStorage.setItem('bestTimes', JSON.stringify(this.bestTimes));
    }
    
    showWinScreen() {
        const winScreen = document.getElementById('win-screen');
        winScreen.classList.add('show');
    }
    
    hideWinScreen() {
        const winScreen = document.getElementById('win-screen');
        winScreen.classList.remove('show');
    }
    
    playAgain() {
        this.hideWinScreen();
        this.createGame();
    }
    
    shareScore() {
        const { pairs } = this.difficultySettings[this.currentDifficulty];
        const text = `🎮 I just completed the ${this.currentDifficulty} level Memory Game in ${document.getElementById('final-time').textContent} with ${this.moves} moves! 🧠✨`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Memory Game Score',
                text: text,
                url: window.location.href
            });
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(text).then(() => {
                alert('Score copied to clipboard!');
            });
        }
    }
}

// Initialize the game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MemoryGame();
});
