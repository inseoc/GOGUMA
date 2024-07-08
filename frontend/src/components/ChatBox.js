import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, Button, IconButton, Typography } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';

function ChatBox() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [listening, setListening] = useState(false);
    const [isPlaying, setIsPlaying] = useState(false);
    const recognitionRef = useRef(null);
    const audioContextRef = useRef(null);
    const audioSourceRef = useRef(null);
    const [interimTranscript, setInterimTranscript] = useState('');

    useEffect(() => {
        audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
        return () => {
            if (audioContextRef.current) {
                audioContextRef.current.close();
            }
        };
    }, []);

    const handleSend = async () => {
        if (input.trim()) {
            const newMessage = { sender: 'user', text: input };
            setMessages([...messages, newMessage]);
            setInput('');

            try {
                const response = await fetch('http://localhost:8000/text_to_speech', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: input }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                
                // Convert base64 to ArrayBuffer
                const binaryString = window.atob(data.audio);
                const len = binaryString.length;
                const bytes = new Uint8Array(len);
                for (let i = 0; i < len; i++) {
                    bytes[i] = binaryString.charCodeAt(i);
                }
                const arrayBuffer = bytes.buffer;

                const audioBuffer = await audioContextRef.current.decodeAudioData(arrayBuffer);

                const botMessage = { sender: 'bot', text: data.text, audio: audioBuffer };
                setMessages(prevMessages => [...prevMessages, botMessage]);

                playAudio(audioBuffer);
            } catch (error) {
                console.error('Error:', error);
            }
        }
    };

    const playAudio = (audioBuffer) => {
        if (isPlaying) {
            stopAudio();
        }

        const source = audioContextRef.current.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContextRef.current.destination);
        source.onended = () => setIsPlaying(false);
        source.start();
        audioSourceRef.current = source;
        setIsPlaying(true);
    };

    const stopAudio = () => {
        if (audioSourceRef.current) {
            audioSourceRef.current.stop();
            audioSourceRef.current = null;
        }
        setIsPlaying(false);
    };

    const startListening = () => {
        if (!('webkitSpeechRecognition' in window)) {
            alert('Your browser does not support speech recognition. Please use Chrome.');
            return;
        }

        const SpeechRecognition = window.webkitSpeechRecognition;
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = true;
        recognitionRef.current.interimResults = true;
        recognitionRef.current.lang = 'ko-KR';

        recognitionRef.current.onstart = () => {
            setListening(true);
            setInterimTranscript('');
        };

        recognitionRef.current.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            setInput(prevInput => prevInput + finalTranscript);
            setInterimTranscript(interimTranscript);
        };

        recognitionRef.current.onerror = (event) => {
            console.error('Speech recognition error', event.error);
        };

        recognitionRef.current.onend = () => {
            setListening(false);
            // 음성 인식이 끝나면 중간 결과를 최종 입력에 추가
            setInput(prevInput => prevInput + interimTranscript);
            setInterimTranscript('');
        };

        recognitionRef.current.start();
    };

    const stopListening = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', p: 2, border: '1px solid #ccc', borderRadius: '8px' }}>
            <Box sx={{ flexGrow: 1, overflow: 'auto', mb: 2 }}>
                {messages.map((msg, index) => (
                    <Box
                        key={index}
                        sx={{
                            mb: 1,
                            p: 1,
                            borderRadius: '4px',
                            alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                            backgroundColor: msg.sender === 'user' ? '#e0f7fa' : '#e0e0e0',
                            display: 'flex',
                            alignItems: 'center',
                        }}
                    >
                        <Typography variant="body1">{msg.text}</Typography>
                        {msg.audio && (
                            <IconButton onClick={() => playAudio(msg.audio)} size="small">
                                <VolumeUpIcon />
                            </IconButton>
                        )}
                    </Box>
                ))}
            </Box>
            <Box sx={{ display: 'flex', flexDirection: 'column', mb: 2 }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="메시지를 입력하세요."
                    onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                            handleSend();
                        }
                    }}
                    sx={{ mb: 1 }}
                />
                {interimTranscript && (
                    <Typography variant="body2" color="textSecondary">
                        {interimTranscript}
                    </Typography>
                )}
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Button variant="contained" color="primary" onClick={handleSend} sx={{ mr: 1 }}>
                    Send
                </Button>
                <IconButton color="primary" onClick={startListening} disabled={listening}>
                    <MicIcon />
                </IconButton>
                <IconButton color="secondary" onClick={stopListening} disabled={!listening}>
                    <StopIcon />
                </IconButton>
            </Box>
        </Box>
    );
}

export default ChatBox;