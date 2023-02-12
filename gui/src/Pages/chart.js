import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function PChart() {
    const [data, setData] = useState([]);
    const [isLoaded, setIsLoaded] = useState(false);


    const ploting = async (e) => {
        // e.preventDefault();
        try {
            const data = await fetch(`https://market-rakshith-u-r.vercel.app/top5`).then(res => res.json());
            let chartData = []
            let max = 0
            Object.entries(data).forEach(([key, value]) => {
                chartData.push({
                    name: key,
                    score: value,
                    amt: Math.max(value, max),
                });
            });
            //change all the amt in chart data to max
            chartData.forEach((item) => {
                item.amt = max;
            });
            setData(chartData);
            setIsLoaded(true);
        }
        catch (error) {
            console.log(error);
        }

    }
    useEffect(() => {
        ploting();
    }, []);

    return (
        <div style={{ backgroundColor: ' white' }}>
            {isLoaded ?
                <ResponsiveContainer width={700} height={300} aspect={3}>
                    <BarChart
                        width={500}
                        height={300}
                        data={data}
                        margin={{
                            top: 5,
                            right: 30,
                            left: 20,
                            bottom: 5,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="score" fill="#82ca9d" />
                    </BarChart>
                </ResponsiveContainer> : <div>Waiting .......</div>
            }
        </div>
    );
}