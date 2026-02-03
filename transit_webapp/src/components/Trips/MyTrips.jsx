import React from 'react';
import { Lightbulb } from 'lucide-react';

const MyTrips = () => {
    const weeklyData = [
        { day: 'Mon', value: 1.2 },
        { day: 'Tue', value: 2.1 },
        { day: 'Wed', value: 1.8 },
        { day: 'Thu', value: 2.6 },
        { day: 'Fri', value: 1.6 },
        { day: 'Sat', value: 3.2 },
        { day: 'Sun', value: 2.9 }
    ];

    const maxWeeklyValue = 3.2;

    return (
        <div className="trips-screen screen">
            <div className="trips-header">
                <h1 className="eco-title">Eco Journey</h1>
                <p className="eco-subtitle">Track your environmental impact</p>
            </div>

            <div className="eco-tip-banner">
                <div className="tip-icon-container">
                    <Lightbulb size={24} color="#FFFFFF" fill="#FFEB3B" />
                </div>
                <div className="tip-content">
                    <h3>Eco Tip of the Day</h3>
                    <p>Taking the bus instead of driving can save up to 2.6 kg of CO₂ per trip!</p>
                </div>
            </div>

            <div className="eco-card monthly-progress">
                <h3>Monthly CO₂ Progress</h3>
                <div className="gauge-container">
                    <svg className="gauge-svg" viewBox="0 0 100 50">
                        {/* Background arc */}
                        <path
                            d="M 10 45 A 35 35 0 0 1 90 45"
                            fill="none"
                            stroke="#E9ECEF"
                            strokeWidth="8"
                            strokeLinecap="round"
                        />
                        {/* Progress arc (79%) */}
                        <path
                            d="M 10 45 A 35 35 0 0 1 65 15"
                            fill="none"
                            stroke="#002B49"
                            strokeWidth="8"
                            strokeLinecap="round"
                            strokeDasharray="110"
                            strokeDashoffset="23"
                        />
                    </svg>
                    <div className="gauge-info">
                        <span className="gauge-value">47.3</span>
                        <span className="gauge-label">kg CO₂ saved</span>
                    </div>
                </div>
                <p className="goal-text">79% of monthly goal (60 kg)</p>
            </div>

            <div className="eco-card weekly-impact">
                <h3>This Week's Impact</h3>
                <div className="bar-chart-container">
                    <div className="y-axis">
                        <span>3.2</span>
                        <span>2.4</span>
                        <span>1.6</span>
                        <span>0.8</span>
                        <span>0</span>
                    </div>
                    <div className="bars-and-labels">
                        <div className="bars-container">
                            {weeklyData.map((d, i) => (
                                <div key={i} className="bar-wrapper">
                                    <div
                                        className="chart-bar"
                                        style={{ height: `${(d.value / maxWeeklyValue) * 100}%` }}
                                    ></div>
                                </div>
                            ))}
                        </div>
                        <div className="x-axis">
                            {weeklyData.map((d, i) => (
                                <span key={i}>{d.day}</span>
                            ))}
                        </div>
                    </div>
                    <div className="y-axis-label">kg CO₂</div>
                </div>
            </div>
        </div>
    );
};

export default MyTrips;
