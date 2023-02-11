import React, { useState } from 'react';
import './home.css';
import LineChart from './chart';
export default function Home() {

    const [marketId, setMarketId] = useState('');
    const [score, setScore] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Call an API endpoint to retrieve the data for the specified market ID
            const data = await fetch(`http://127.0.0.1:8000/market?market_id=${marketId}`).then(res => res.json());

            // Calculate the score using the given attributes
            // const calculatedScore = calculateScore(data);
            console.log(data);
            // Set the score state to the calculated score
            setScore(data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div >
            <div className="main" >
                <form onSubmit={handleSubmit}>
                    <label htmlFor="marketId">Market ID:</label>
                    <input type="text" id="marketId" value={marketId} onChange={e => setMarketId(e.target.value)} />
                    <button type="submit">Calculate Score</button>
                </form>
                <button type="submit" onClick={LineChart}>plot</button>
                {score && <div>Score: {score}</div>}
            </div>
        </div>
    );
}