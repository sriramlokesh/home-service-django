// @ts-check

/**
 * @typedef {{
 *   apiKey: string,
 *   units: string,
 *   updateInterval: number
 * }} WeatherConfig
 */

/**
 * @type {WeatherConfig}
 */
// @ts-ignore
window.WEATHER_CONFIG = {
    apiKey: 'YOUR_OPENWEATHERMAP_API_KEY', // Replace with your actual API key
    units: 'metric',
    updateInterval: 1800000 // 30 minutes in milliseconds
}; 