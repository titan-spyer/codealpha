document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;

    // Define a few color palettes for the 3-layer horizontal gradient
    const palettes = [
        ['#88c0f8ff', '#78549aff', '#FBC2EB'], // Light Blue -> Lavender -> Pink
        ['#5b7cb0ff', '#4ea8d1ff', '#6ab0eeff'], // Sky Blue -> Light Blue -> Lime Green
        ['#f6d365', '#fda085', '#ffdde1'], // Gold -> Coral -> Light Pink
        ['#84fab0', '#8fd3f4', '#a1c4fd'], // Mint Green -> Light Blue -> Sky Blue
        ['#ff9a9e', '#fecfef', '#fad0c4'], // Soft Pink Gradients
        ['#8EC5FC', '#b570f5', '#7d2fc2']  // Red -> Pink -> Peach
    ];

    let currentPaletteIndex = 0;

    function changeBackground() {
        // Get the current palette
        const palette = palettes[currentPaletteIndex];
        
        // Apply the new 3-layer horizontal gradient
        body.style.background = `linear-gradient(to right, ${palette[0]}, ${palette[1]}, ${palette[2]})`;
        
        // Move to the next palette, looping back to the start
        currentPaletteIndex = (currentPaletteIndex + 1) % palettes.length;
    }

    // Set the initial background and then change it every 7 seconds
    changeBackground();
    setInterval(changeBackground, 7000);
});