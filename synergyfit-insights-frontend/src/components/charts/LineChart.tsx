// Line Chart component

'use client';

import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Title, 
  Tooltip, 
  Legend,
  ChartOptions
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { ChartDataPoint } from '@/types/api';

// Register Chart.js components
ChartJS.register(
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Title, 
  Tooltip, 
  Legend
);

interface LineChartProps {
  data: ChartDataPoint[];
  title: string;
  yAxisLabel?: string;
  color?: string;
}

export default function LineChart({ 
  data,
  title,
  yAxisLabel = '',
  color = 'rgb(53, 162, 235)'
}: LineChartProps) {
  // Prepare data for Chart.js
  const labels = data.map(point => new Date(point.date).toLocaleDateString());
  const values = data.map(point => point.value);
  
  const chartData = {
    labels,
    datasets: [
      {
        label: title,
        data: values,
        borderColor: color,
        backgroundColor: `${color}33`, // Add 20% opacity
        tension: 0.2,
        fill: true,
      },
    ],
  };
  
  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: title,
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.dataset.label}: ${context.parsed.y}`,
        },
      },
    },
    scales: {
      y: {
        title: {
          display: !!yAxisLabel,
          text: yAxisLabel || '',
        },
        beginAtZero: false,
      }
    }
  };
  
  return (
    <div className="h-64 w-full">
      <Line data={chartData} options={options} />
    </div>
  );
}
