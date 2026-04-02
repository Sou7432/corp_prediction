document.addEventListener('DOMContentLoaded', function() {
    // Sync sliders with number inputs
    const temperatureInput = document.getElementById('temperature');
    const temperatureSlider = document.getElementById('temperature-slider');
    const humidityInput = document.getElementById('humidity');
    const humiditySlider = document.getElementById('humidity-slider');
    const phInput = document.getElementById('ph');
    const phSlider = document.getElementById('ph-slider');
    const waterInput = document.getElementById('water_availability');
    const waterSlider = document.getElementById('water-slider');
    const seasonSelect = document.getElementById('season');
    const seasonInfo = document.getElementById('season-info-text');
    
    // Set initial values
    temperatureInput.value = temperatureSlider.value;
    humidityInput.value = humiditySlider.value;
    phInput.value = phSlider.value;
    waterInput.value = waterSlider.value;
    
    // Sync number inputs with sliders
    temperatureSlider.addEventListener('input', () => {
        temperatureInput.value = temperatureSlider.value;
    });
    
    humiditySlider.addEventListener('input', () => {
        humidityInput.value = humiditySlider.value;
    });
    
    phSlider.addEventListener('input', () => {
        phInput.value = phSlider.value;
    });
    
    waterSlider.addEventListener('input', () => {
        waterInput.value = waterSlider.value;
    });
    
    // Sync sliders with number inputs
    temperatureInput.addEventListener('input', () => {
        temperatureSlider.value = temperatureInput.value;
    });
    
    humidityInput.addEventListener('input', () => {
        humiditySlider.value = humidityInput.value;
    });
    
    phInput.addEventListener('input', () => {
        phSlider.value = phInput.value;
    });
    
    waterInput.addEventListener('input', () => {
        waterSlider.value = waterInput.value;
    });
    
    // Load season info when season changes
    seasonSelect.addEventListener('change', () => {
        const season = seasonSelect.value;
        fetch(`/season_info/${season}`)
            .then(response => response.json())
            .then(data => {
                seasonInfo.textContent = data.info;
            })
            .catch(error => {
                seasonInfo.textContent = 'Error loading season information.';
            });
    });
    
    // Load initial season info
    fetch(`/season_info/${seasonSelect.value}`)
        .then(response => response.json())
        .then(data => {
            seasonInfo.textContent = data.info;
        });
    
    // Handle form submission
    document.getElementById('prediction-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            temperature: temperatureInput.value,
            humidity: humidityInput.value,
            ph: phInput.value,
            water_availability: waterInput.value,
            season: seasonSelect.value
        };
        
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('crop-name').textContent = data.crop;
                document.getElementById('confidence').textContent = `Confidence: ${data.confidence}%`;
                document.getElementById('result').style.display = 'block';
                
                // Scroll to results
                document.getElementById('result').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center'
                });
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error);
        });
    });
});