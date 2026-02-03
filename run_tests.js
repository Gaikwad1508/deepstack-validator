const fs = require('fs');
const { execSync } = require('child_process');

const ENV_FILE = '.env';
const CONFIG_FILE = 'promptfooconfig.yaml';
const TEMP_CONFIG_FILE = 'temp_promptfooconfig.yaml';

console.log("🚀 Starting Test Runner (Bypass Mode)...");

try {
    // 1. EXTRACT API KEY FROM .env
    // We look for the first line that looks like GROQ_API_KEY=... and is NOT a comment
    const envContent = fs.readFileSync(ENV_FILE, 'utf8');
    const lines = envContent.split('\n');
    let apiKey = '';

    for (const line of lines) {
        const trimmed = line.trim();
        // Skip comments (#)
        if (trimmed && !trimmed.startsWith('#') && trimmed.includes('GROQ_API_KEY=')) {
            const parts = trimmed.split('=');
            if (parts.length >= 2) {
                // Remove quotes and whitespace
                apiKey = parts[1].trim().replace(/['"]/g, '');
                break;
            }
        }
    }

    if (!apiKey) {
        throw new Error("Could not find a valid GROQ_API_KEY in .env");
    }
    console.log("✅ Loaded API Key from .env");

    // 2. CREATE TEMP CONFIG FILE
    // We read the original yaml, and replace 'process.env.GROQ_API_KEY' with the ACTUAL key
    let configContent = fs.readFileSync(CONFIG_FILE, 'utf8');
    
    // Replace the variable with the actual string key
    const injectedContent = configContent.replace(
        'process.env.GROQ_API_KEY', 
        `"${apiKey}"`
    );

    fs.writeFileSync(TEMP_CONFIG_FILE, injectedContent);
    console.log("📝 Generated temporary config with injected key...");

    // 3. RUN THE TEST using the TEMP config
    console.log("🏃 Running Promptfoo...");
    try {
        execSync(`npx promptfoo@0.60.0 eval --no-cache --config ${TEMP_CONFIG_FILE}`, { 
            stdio: 'inherit' 
        });
    } catch (err) {
        // We catch here so we ensure cleanup happens even if tests fail
        console.error("⚠️ Tests finished with some failures.");
    }

} catch (error) {
    console.error("❌ Critical Error:", error.message);
} finally {
    // 4. CLEANUP (Critical Step)
    // Delete the temp file so the key is never left on disk
    if (fs.existsSync(TEMP_CONFIG_FILE)) {
        fs.unlinkSync(TEMP_CONFIG_FILE);
        console.log("🧹 Cleanup: Temporary config file deleted.");
    }
}