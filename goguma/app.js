import React, { useState } from 'react';
import { ReactMic } from 'react-mic';

function App() {
    const [record, setRecord] = useState(false);
    const [audioFile, setAudioFile] = useState(null);
    const [response, setResponse] = useState('');

    const startRecording = () => {
        setRecord(true);
    };

    const stopRecording = () => {
        setRecord(false);
    };

    const onData = (recordedBlob) => {
        console.log('chunk of real-time data is: ', recordedBlob);
    };

    const onStop = (recordedBlob) => {
        console.log('recordedBlob is: ', recordedBlob);
        setAudioFile(recordedBlob.blob);
    };

    const handleSubmit = async () => {
        if (!audioFile) return;

        const formData = new FormData();
        formData.append('file', audioFile, 'recording.wav');

        const res = await fetch('http://localhost:8000/process_audio/', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        setResponse(data.text);
    };

    return (
        <div>
            <h1>Real-time AI Voice Interaction</h1>
            <ReactMic
                record={record}
                className="sound-wave"
                onStop={onStop}
                onData={onData}
                strokeColor="#000000"
                backgroundColor="#FF4081" />
            <div>
                <button onClick={startRecording} type="button">Start</button>
                <button onClick={stopRecording} type="button">Stop</button>
                <button onClick={handleSubmit} type="button">Submit</button>
            </div>
            <p>AI Response: {response}</p>
        </div>
    );
}

export default App;