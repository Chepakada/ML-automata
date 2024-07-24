import logo from './logo.svg';
import './App.css';
import React from "react";
import { useState } from "react";
import {Header, Footer, InputBox} from "./modules/Components.tsx"
import LinearRegressionDownload from './LinearRegressionDownload';
import CategoricPredictionDownload from './CategoricPredictionDownload';
// import { InputBox } from './modules/Home.tsx';


const App = () => {
  const [linearRegressionMetrics, setLinearRegressionMetrics] = useState({
    mae: 0.5,
    mse: 0.25,
    r2: 0.75,
  });

  const [linearRegressionImageData, setLinearRegressionImageData] = useState(
    'data:image/png;base64,...' // your base64 image data here
  );

  const [categoricPredictionMetrics, setCategoricPredictionMetrics] = useState({
    accuracy: 0.85,
    report: 'Some classification report',
  });

  const [categoricPredictionImageData, setCategoricPredictionImageData] = useState(
    'data:image/png;base64,...' // your base64 image data here
  );

  return (
    <div>
      <Header />
      <h1>Download Outputs</h1>
      <LinearRegressionDownload
        metrics={linearRegressionMetrics}
        imageData={linearRegressionImageData}
      />
      <CategoricPredictionDownload
        metrics={categoricPredictionMetrics}
        imageData={categoricPredictionImageData}
      />
      <Footer />
    </div>
  );

};

// function App() {
//   return (
//     <div>
//     <Header/>
//     {/* <InputBox/> */}
//     <Footer/>
//     </div>
//   );
// }


export default App;
