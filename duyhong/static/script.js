document.addEventListener('DOMContentLoaded', function() {
    // Update file name when selected
    const fileInput = document.getElementById('file');
    const fileNameSpan = document.getElementById('file-name');
    
    fileInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            fileNameSpan.textContent = this.files[0].name;
        } else {
            fileNameSpan.textContent = 'Chọn file...';
        }
    });
    
    // Add floating particles for magical effect
    createParticles();
});

function createParticles() {
    const colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00', '#ff0000', '#0000ff'];
    const container = document.body;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random properties
        const size = Math.random() * 5 + 2;
        const color = colors[Math.floor(Math.random() * colors.length)];
        const duration = Math.random() * 10 + 10;
        const delay = Math.random() * 5;
        
        // Position randomly in viewport
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Apply styles
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.backgroundColor = color;
        particle.style.position = 'absolute';
        particle.style.borderRadius = '50%';
        particle.style.opacity = '0.7';
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '0';
        
        // Animation
        particle.style.animation = `float ${duration}s ease-in-out ${delay}s infinite`;
        
        // Add to DOM
        container.appendChild(particle);
    }
    
    // Add CSS for animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% {
                transform: translate(0, 0) rotate(0deg);
                opacity: 0.7;
            }
            50% {
                transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(180deg);
                opacity: 0.3;
            }
            100% {
                transform: translate(0, 0) rotate(360deg);
                opacity: 0.7;
            }
        }
    `;
    document.head.appendChild(style);
}