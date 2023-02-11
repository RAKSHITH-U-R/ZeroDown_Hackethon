import React, { useState } from 'react';
import './home.css';
export default function Home() {

    const [marketId, setMarketId] = useState('');
    const [score, setScore] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = await fetch(`https://market-rakshith-u-r.vercel.app/market?market_id=${marketId}`).then(res => res.json());

            console.log(data);
            setScore(data.market_id);
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
                {score && <div>Score: {score}</div>}
            </div>
        </div>
    );
}