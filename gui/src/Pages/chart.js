
import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';

export default function PChart() {
    const [graph, setData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const ploting = async () => {

        try {
            const response = await fetch("https://market-rakshith-u-r.vercel.app/all");
            const data = await response.json();
            // console.log(Object.values(data));
            const chartData = {
                labels: Object.keys(data),
                datasets: [
                    {
                        label: 'Line Chart',
                        data: Object.values(data),
                        backgroundColor: 'rgba(75,192,192,0.4)',
                        borderColor: 'rgba(75,192,192,1)',
                        borderWidth: 1,
                        pointRadius: 0
                    }
                ]
            };
            setData(chartData);
            setIsLoading(true);
            // console.log(chartData);
        } catch (error) {
            console.log("error", error);
        }

    }
    useEffect(() => {
        ploting();
    }, []);



    return (
        <div className='area'>{isLoading ? <div className="area"><Line data={graph} /> <Bar data={graph} /> </div> : <div> <h1>Wait.....</h1></div>}</div>
    );
}
