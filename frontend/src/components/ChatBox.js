import React, { useState } from 'react';
import { Box, TextField, Button, IconButton, Typography } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';

function ChatBox() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSend = async () => {
        if (input.trim()) {
            const newMessage = { sender: 'user', text: input };
            setMessages([...messages, newMessage]);
            setInput('');

            try {
                const response = await fetch('http://localhost:8000/gpt_generation', {  // FastAPI 서버 주소
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: input }),  // 필드명을 'text'로 수정
                });

                const data = await response.json();
                setMessages([...messages, newMessage, { sender: 'bot', text: data.result }]);
            } catch (error) {
                console.error('Error:', error);
            }
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
                        }}
                    >
                        <Typography variant="body1">{msg.text}</Typography>
                    </Box>
                ))}
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="메시지를 입력하세요."
                    sx={{ mr: 1 }}
                />
                <Button variant="contained" color="primary" onClick={handleSend} sx={{ mr: 1 }}>
                    Send
                </Button>
                <IconButton color="primary" className="mic-button">
                    <MicIcon />
                </IconButton>
                <IconButton color="secondary" className="stop-button">
                    <StopIcon />
                </IconButton>
            </Box>
        </Box>
    );
}

export default ChatBox;
