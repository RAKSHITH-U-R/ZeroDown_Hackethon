
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

export default function Chart() {
    const [data, setData] = useState([]);
    const ploting = async () => {

        try {
            const response = await fetch("http://127.0.0.1:8000/all");
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
            // console.log(chartData);
        } catch (error) {
            console.log("error", error);
        }

    }
    useEffect(() => {
        ploting();
    }, []);


    return (
        <div>
            <h1>sfasfkjasfkj</h1>
            <Line
                data={data}
            />
        </div>
    );
}
