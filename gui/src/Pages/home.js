
import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './home.css';
export default function Home() {

    const [marketId, setMarketId] = useState('');
    const [score, setScore] = useState(null);
    const [graphData, setGraphData] = useState([]);
    // const [isLoaded, setIsLoaded] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = await fetch(`https://market-rakshith-u-r.vercel.app/market?market_id=${marketId}`).then(res => res.json());
            const history = await fetch(`https://market-rakshith-u-r.vercel.app/history?market_id=${marketId}`).then(res => res.json());
            let chartData = [];
            Object.entries(history).forEach(([key, value]) => {
                chartData.push({
                    name: key,
                    value: value
                });
            });
            setGraphData(chartData);
            setScore(data.market_id);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div style={{ backgroundColor: "white" }}>
            <div className="main" >
                <form onSubmit={handleSubmit}>
                    <label htmlFor="marketId">Market ID:</label>
                    <input type="text" id="marketId" value={marketId} onChange={e => setMarketId(e.target.value)} />
                    <button type="submit">Calculate Score</button>
                </form>
                {score && <div>Current Score: {score}</div>}
            </div>
            <LineChart width={800} height={300} data={graphData} title={"History"}>
                <XAxis dataKey="name" label={"History"} />
                <YAxis />
                <CartesianGrid stroke="#f5f5f5" />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#ff7300" yAxisId={0} />
            </LineChart>
        </div>
    );
}


