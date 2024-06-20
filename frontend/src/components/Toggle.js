import React from 'react';

function Toggle({ label, options = [], inputType = 'radio', value, onChange }) {
    return (
        <div className="toggle">
            <label>{label}</label>
            {inputType === 'text' ? (
                <input type="text" value={value} onChange={(e) => onChange(e.target.value)} />
            ) : (
                options.map((option) => (
                    <label key={option}>
                        <input
                            type="radio"
                            value={option}
                            checked={value === option}
                            onChange={() => onChange(option)}
                        />
                        {option}
                    </label>
                ))
            )}
        </div>
    );
}

export default Toggle;
