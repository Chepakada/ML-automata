
import React from 'react';

const CategoricPredictionDownload = ({ metrics, imageData }) => {
  const downloadJSON = (data, filename) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const downloadImage = (data, filename) => {
    const link = document.createElement('a');
    link.href = data;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <button onClick={() => downloadJSON(metrics, 'categoric_prediction_metrics.json')}>
        Download Metrics JSON
      </button>
      <button onClick={() => downloadImage(imageData, 'confusion_matrix.png')}>
        Download Confusion Matrix Image
      </button>
    </div>
  );
};

export default CategoricPredictionDownload;
