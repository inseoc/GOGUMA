import React, { useState } from 'react';
import { Container, Typography, Button, TextField, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel } from '@mui/material';
import ChatBox from './ChatBox';

function App() {
    const [gender, setGender] = useState('');
    const [persona, setPersona] = useState('');
    const [chatActive, setChatActive] = useState(false);

    const handleApply = async () => {
        if (gender && persona) {
            try {
                const response = await fetch('http://localhost:8000/setting_for_persona', {  // FastAPI 서버 주소
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ gender, persona }),
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.status === 200) {
                        setChatActive(true);
                    } else {
                        console.error('Error setting persona:', data.response);
                    }
                } else {
                    console.error('Error setting persona:', response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    };

    return (
        <Container component="main" maxWidth="xs" style={{ marginTop: '2rem' }}>
            <Typography component="h1" variant="h5" align="center" gutterBottom>
                Persona Chat App
            </Typography>
            <FormControl component="fieldset" fullWidth margin="normal">
                <FormLabel component="legend">성별</FormLabel>
                <RadioGroup row value={gender} onChange={(e) => setGender(e.target.value)}>
                    <FormControlLabel value="남성" control={<Radio />} label="남성" />
                    <FormControlLabel value="여성" control={<Radio />} label="여성" />
                </RadioGroup>
            </FormControl>
            <TextField
                label="페르소나"
                variant="outlined"
                fullWidth
                margin="normal"
                value={persona}
                onChange={(e) => setPersona(e.target.value)}
            />
            <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={handleApply}
                disabled={!gender || !persona}
                style={{ marginTop: '1rem' }}
            >
                적용
            </Button>
            {chatActive && <ChatBox />}
        </Container>
    );
}

export default App;
