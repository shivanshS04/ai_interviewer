import streamlit as st
import streamlit.components.v1 as components

def speech_to_text_component(key="speech_input"):
    """
    Creates a speech-to-text component using the browser's Web Speech API.
    Stores transcribed text in localStorage for retrieval.
    """
    speech_html = f"""
    <div style="text-align: center; margin: 10px 0;">
        <button id="micButton" style="
            background-color: #FF4B4B;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s;
        " onclick="toggleRecording()">
            🎤
        </button>
        <div id="status" style="margin-top: 10px; font-size: 14px; color: #666; font-weight: bold;"></div>
        <div id="transcript" style="margin-top: 10px; font-size: 14px; color: #333; padding: 15px; background: #f0f0f0; border-radius: 8px; min-height: 60px; border: 2px solid #ddd;"></div>
    </div>
    
    <script>
        let recognition = null;
        let isRecording = false;
        let finalTranscript = '';
        const storageKey = 'voice_transcript_{key}';
        
        // Load existing transcript from localStorage
        const savedTranscript = localStorage.getItem(storageKey);
        if (savedTranscript) {{
            finalTranscript = savedTranscript;
            document.getElementById('transcript').innerText = finalTranscript || 'Click microphone to start...';
        }}
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            recognition.onresult = function(event) {{
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {{
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {{
                        finalTranscript += transcript + ' ';
                        // Save to localStorage
                        localStorage.setItem(storageKey, finalTranscript.trim());
                    }} else {{
                        interimTranscript += transcript;
                    }}
                }}
                
                const displayText = finalTranscript + interimTranscript;
                document.getElementById('status').innerText = isRecording ? 'Listening...' : 'Paused - Click "Load Text" below';
                document.getElementById('transcript').innerText = displayText || 'Speak now...';
            }};
            
            recognition.onerror = function(event) {{
                document.getElementById('status').innerText = 'Error: ' + event.error;
                isRecording = false;
                updateButton();
            }};
            
            recognition.onend = function() {{
                if (isRecording) {{
                    recognition.start();
                }}
            }};
        }} else {{
            document.getElementById('status').innerText = 'Speech recognition not supported';
        }}
        
        function toggleRecording() {{
            if (!recognition) return;
            
            isRecording = !isRecording;
            
            if (isRecording) {{
                finalTranscript = '';
                localStorage.setItem(storageKey, '');
                recognition.start();
                document.getElementById('status').innerText = 'Listening...';
                document.getElementById('transcript').innerText = 'Speak now...';
            }} else {{
                recognition.stop();
                document.getElementById('status').innerText = 'Paused - Click "Load Text" below';
            }}
            
            updateButton();
        }}
        
        function updateButton() {{
            const button = document.getElementById('micButton');
            if (isRecording) {{
                button.style.backgroundColor = '#00CC00';
                button.innerText = '⏸️';
            }} else {{
                button.style.backgroundColor = '#FF4B4B';
                button.innerText = '🎤';
            }}
        }}
    </script>
    """
    
    return components.html(speech_html, height=180)


def text_to_speech_component(text, speed=1.3):
    """
    Creates a text-to-speech component using the browser's Web Speech API.
    Automatically speaks the provided text.
    
    Args:
        text: The text to speak
        speed: Speech rate (0.5 to 2.0, default 1.3)
    """
    # Escape quotes in text for JavaScript
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    
    tts_html = f"""
    <script>
        function speak() {{
            if ('speechSynthesis' in window) {{
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance("{safe_text}");
                utterance.lang = 'en-US';
                utterance.rate = {speed};
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                window.speechSynthesis.speak(utterance);
            }}
        }}
        
        // Auto-play when component loads
        speak();
    </script>
    """
    
    components.html(tts_html, height=0)
