// @ts-check

/**
 * @type {WeatherConfig}
 */
// @ts-ignore
const config = window.WEATHER_CONFIG || {
    apiKey: '',
    units: 'metric',
    updateInterval: 1800000
};

/** 
 * @typedef {Object} WeatherData
 * @property {Array<Object>} list - List of weather forecasts
 * @property {Object} city - City information
 * @property {string} city.name - City name
 * @property {string} city.country - Country code
 */

/** @type {Object.<string, string>} */
const weatherIcons = {
    '01d': 'wi-day-sunny',
    '02d': 'wi-day-cloudy',
    '03d': 'wi-cloud',
    '04d': 'wi-cloudy',
    '09d': 'wi-showers',
    '10d': 'wi-rain',
    '11d': 'wi-thunderstorm',
    '13d': 'wi-snow',
    '50d': 'wi-fog',
    '01n': 'wi-night-clear',
    '02n': 'wi-night-alt-cloudy',
    '03n': 'wi-cloud',
    '04n': 'wi-night-cloudy',
    '09n': 'wi-night-showers',
    '10n': 'wi-night-rain',
    '11n': 'wi-night-thunderstorm',
    '13n': 'wi-night-snow',
    '50n': 'wi-night-fog'
};

/**
 * Get the weather icon class for a given icon code
 * @param {string} iconCode - The OpenWeatherMap icon code
 * @returns {string} The weather icon class
 */
function getWeatherIconClass(iconCode) {
    return weatherIcons[iconCode] || 'wi-na';
}

/**
 * Format temperature to rounded integer
 * @param {number} temp - The temperature to format
 * @returns {number} The rounded temperature
 */
function formatTemp(temp) {
    return Math.round(temp);
}

/**
 * Create a simple weather widget
 * @param {WeatherData} data - The weather data from OpenWeatherMap
 * @returns {string} The HTML for the widget
 */
function createSimpleWidget(data) {
    const current = data.list[0];
    let html = '<i class="wi ' + getWeatherIconClass(current.weather[0].icon) + '"></i>';
    html += '<h2>' + formatTemp(current.main.temp) + '&deg;C</h2>';
    html += '<div class="city">' + data.city.name + ', ' + data.city.country + '</div>';
    html += '<div class="currently">' + current.weather[0].main + '</div>';
    html += '<div class="celcious">' + formatTemp(current.main.temp) + '&deg;C</div>';
    return html;
}

/**
 * Create a detailed weather widget
 * @param {WeatherData} data - The weather data from OpenWeatherMap
 * @returns {string} The HTML for the widget
 */
function createDetailedWidget(data) {
    const current = data.list[0];
    const forecasts = data.list.filter((item, index) => index % 8 === 0).slice(0, 5);

    let html = '<div class="top">';
    html += '<i class="wi ' + getWeatherIconClass(current.weather[0].icon) + '"></i>';
    html += '<div class="currently">' + current.weather[0].main + '</div>';
    html += '<div class="updates">' + new Date(current.dt * 1000).toLocaleDateString() + '</div>';
                html += '</div>';

                html += '<div class="middle">';
    html += '<div class="city">' + data.city.name + ' <span>' + data.city.country + '</span></div>';
    html += '<div class="temp">' + formatTemp(current.main.temp) + '<span>&deg;C</span></div>';
                html += '</div>';
                
                html += '<div class="nextdays">';
    forecasts.forEach((forecast, index) => {
        const date = new Date(forecast.dt * 1000);
        const day = date.toLocaleDateString('en-US', { weekday: 'short' });
        html += '<div class="days day' + (index + 1) + '">';
        html += '<span class="d">' + day + '</span>';
        html += '<span class="h">' + formatTemp(forecast.main.temp_max) + '&deg;</span>';
        html += '<span class="h">' + formatTemp(forecast.main.temp_min) + '&deg;</span>';
        html += '</div>';
    });
                html += '</div>';

    return html;
}

/**
 * Handle weather loading errors
 * @param {string} targetId - The ID of the target element
 * @param {Error} error - The error that occurred
 */
function handleError(targetId, error) {
    console.error('Weather Error:', error);
    const element = document.getElementById(targetId);
    if (element) {
        element.innerHTML = '<p class="weather-error">Weather data currently unavailable</p>';
    }
}

/**
 * Load weather data for a location
 * @param {string} location - The location to get weather for
 * @param {string} targetId - The ID of the target element
 * @param {boolean} [detailed=false] - Whether to show detailed view
 */
async function loadWeather(location, targetId, detailed = false) {
    try {
        const element = document.getElementById(targetId);
        if (!element) return;

        element.innerHTML = '<p class="weather-loading">Loading weather data...</p>';

        const url = 'https://api.openweathermap.org/data/2.5/forecast?' +
            'q=' + encodeURIComponent(location) +
            '&units=' + config.units +
            '&appid=' + config.apiKey;

        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Weather API returned status ' + response.status);
        }

        const data = await response.json();
        element.innerHTML = detailed ? createDetailedWidget(data) : createSimpleWidget(data);

    } catch (error) {
        handleError(targetId, error instanceof Error ? error : new Error(String(error)));
    }
}

/**
 * Initialize all weather widgets
 */
function initWeather() {
    loadWeather('New York City', 'weather-one', true);
    loadWeather('New York City', 'weather-two', false);
    loadWeather('Sydney', 'weather-three', false);
    loadWeather('New York', 'weather-four', false);
}

/**
 * Safe initialization with error handling
 */
function safeInit() {
    try {
        initWeather();
        setInterval(initWeather, config.updateInterval);
    } catch (error) {
        console.error('Weather widget initialization error:', error);
    }
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', safeInit);

// Add styles for loading and error states
(function() {
    const style = document.createElement('style');
    style.textContent = `
        .weather-loading,
        .weather-error {
            padding: 15px;
            text-align: center;
            color: #666;
            font-style: italic;
        }
        
        .weather-error {
            color: #d9534f;
        }
    `;
    document.head.appendChild(style);
})();

