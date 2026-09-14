import React from 'react';

export const ConfidenceMeter = ({ value, isFake }) => {
  const percentage = Math.round(value * 100);
  const strokeColor = isFake ? '#f43f5e' : '#10b981'; // Rose-500 or Emerald-500
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative w-28 h-28 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke="#1e293b"
            strokeWidth="8"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke={strokeColor}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center">
          <span className="text-2xl font-black text-white">{percentage}%</span>
          <span className="text-[10px] tracking-wider uppercase text-slate-400">Confidence</span>
        </div>
      </div>
    </div>
  );
};
