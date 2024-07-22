import React, { ChangeEvent } from "react";
import { Routes, Route, BrowserRouter, Link } from 'react-router-dom';
import heroImage from '../images/hi.webp'
import { useState } from "react";
import '../App.css'
import {creater,Learning} from './Constant.tsx'



function Home() {
    return (
        <div className="home-container">
            
            <h1>Welcome to the Data Submission Portal</h1>
            <p>Please upload your data file and specify the dependent column name. Our system will process the file and provide the necessary results.Currently we are only accepting .txt, .csv, .xlss files only.</p>
            <InputBox />
        </div>
    );
}

export function InputBox() {
    const [file, setFile] = useState<FormData>();
    const [parameter, setParameter] = useState("");

    var jsonData = {
        "id": 1,
        "parameter": parameter,
        "file": file,
        "date": new Date().getUTCDate()
    }

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;

        if (files && files.length > 0) {
            const formData = new FormData();
            formData.append("file", files[0]);

            setFile(formData);
        }
    };

    const handleParameterChange = (e: ChangeEvent<HTMLInputElement>) => {
        setParameter(e.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        fetch("http://127.0.0.1:5000/files", {
            method: "POST",
            mode: "cors",
            body: file,
        });
    };

    return (
        <div className="inputbox-container">
            <form onSubmit={handleSubmit} className="inputbox-form">
                <div className="form-group">
                    <label htmlFor="databox">Data File: </label>
                    <input type="file" id="databox" accept = ".txt, .csv, .xlsx" required onChange={handleFileChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="parameter">Dependent Column Name: </label>
                    <input type="text" id="parameter" placeholder="Column Name here" required onChange={handleParameterChange} />
                </div>
                <input type="submit" id="datasubmit" value="Submit" className="submit-button" />
            </form>
        </div>
    );
}








function Hi() {
    function TextContent(props) {
        const wheretolearn = props.specs;
        return (
            <div className="text-content-container">
                <h2>{wheretolearn.learningName}</h2>
                <p>{wheretolearn.description}</p>
                <h3>Types of Learning</h3>
                
                <ul className="learning-types">
                    {wheretolearn.types.map((type, index) => (
                        <li key={index} className="learning-type-item">
                            <h4>{type.typeName}</h4>
                            <p>{type.description}</p>
                            <h5>Examples</h5>
                            <ul className="examples-list">
                                {type.examples.map((example, idx) => (
                                    <li key={idx}>{example}</li>
                                ))}
                            </ul>
                            <h5>Common Algorithms</h5>
                            <ul className="algorithms-list">
                                {type.commonAlgorithms.map((algorithm, idx) => (
                                    <li key={idx}>{algorithm}</li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
                <h3>Where to Learn</h3>
                <ul className="learning-resources">
                    {wheretolearn.learningResources.map((learningResource, index) => (
                        <li key={index} className="learning-resource-item">
                            <strong>{learningResource.platform}</strong>: {learningResource.course}
                            <p>{learningResource.description}</p>
                            <a href={learningResource.link} target="_blank" rel="noopener noreferrer">
                                Course Link
                            </a>
                        </li>
                    ))}
                </ul>
                <h3>Additional Resources</h3>
                {wheretolearn.additionalResources.map((resource, index) => (
                    <div key={index} className="additional-resources">
                        <h4>{resource.type}</h4>
                        <ul className="additional-resources-list">
                            {resource.items.map((item, idx) => (
                                <li key={idx}>
                                    {item.title ? (
                                        <>
                                            <strong>{item.title}</strong> by {item.author}
                                        </>
                                    ) : (
                                        <>
                                            <strong>{item.name}</strong>: {item.description}
                                            <a href={item.link} target="_blank" rel="noopener noreferrer">
                                                Resource Link
                                            </a>
                                        </>
                                    )}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
        );
    }

    return (
        <div className="hi-container">
        <h1 className="hi-title">Learning Resources</h1>
        <img src={heroImage} alt="Machine Learning Hero" className="hero-image" />
        {Learning.map((wheretolearn, index) => (
            <TextContent key={index} specs={wheretolearn} />
        ))}
    </div>
    );
}

export default Hi;



function CreaterCredit() {
    function TextContent(props: any) {
        const person = props.specs;
        const handleMouseEnter = () => {
            const popup = document.getElementById(`popup-${person.CreaterName}`);
            if (popup) {
                popup.style.display = 'block';
            }
        };

        const handleMouseLeave = () => {
            const popup = document.getElementById(`popup-${person.CreaterName}`);
            if (popup) {
                popup.style.display = 'none';
            }
        };

        return (
            <div className="person-card">
                <h3>{person.CreaterName}</h3>
                <p>{person.Education}</p>
                <div className="linkedin-container" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
                    <a href={person.Linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a>
                    <div className="popup" id={`popup-${person.CreaterName}`}>Go to LinkedIn</div>
                </div>
            </div>
        );
    }

    return (
        <div className="creater-credit-container">
            <h1>Creater Credit</h1>
            {creater.map((person, index) => <TextContent key={index} specs={person} />)}
        </div>
    );
}


// export default CreaterCredit;

export function Header(){
    return (
        
        <header>
        <BrowserRouter>
           <nav>
            <ul>
                <li><Link to = "/Home">Home</Link></li>
                {/* <li>Background</li> */}
                <li><Link to = "/Hi">Background</Link></li>
                <li>< Link to = "/creater-credit"> Creater Credit</Link></li>
                
            </ul>
           </nav>

           <Routes>
           <Route path="/Home" element={<Home/>} />
            <Route path="/creater-credit" element={<CreaterCredit/>} />
            <Route path="/Hi" element={<Hi/>} />
           </Routes>
        </BrowserRouter>
        </header>
        
    )
    // return (
    //     <header>
    //        <nav style = {{display: 'flex'}}>
    //         <ul style = {{display : 'flex', listStyle : 'none', padding: 0, justifyContent: 'space-between', width : '100%'}}>
    //             <li >Home</li>
    //             <li >Background</li>
    //             <li >Learning</li>
    //             <li >Creater Credit</li>
                
    //         </ul>
    //        </nav>
    //     </header>
    // )
}
export function Footer(){
    var date = new Date();

    return(
        <footer>
         {/* <footer style = {{ position: 'fixed', bottom: 0, left: 0, width: '100%', backgroundColor: '', padding:'10px' }} > */}
            <span>&copy;{date.getFullYear()}</span>
            <span>ML-automata</span>
        </footer>
    )
}


