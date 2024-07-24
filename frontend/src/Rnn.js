import React from 'react';

const RNNDownload = ({ modelArchitecture, datasetConfig }) => {
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

  return (
    <div>
      <button onClick={() => downloadJSON(modelArchitecture, 'model_architecture.json')}>
        Download Model Architecture
      </button>
      <button onClick={() => downloadJSON(datasetConfig, 'dataset_config.json')}>
        Download Dataset Config
      </button>
    </div>
  );
};

export default RNNDownload;
