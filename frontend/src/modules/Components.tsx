import React, { ChangeEvent } from "react";
import { Routes, Route, BrowserRouter, Link } from 'react-router-dom';

// import { GoogleLogin, GoogleLogout, GoogleLoginResponse, GoogleLoginResponseOffline } from 'react-google-login';

import { GoogleLogin, GoogleLogout, GoogleLoginResponse, GoogleLoginResponseOffline } from 'react-google-login';

import heroImage from '../images/hi.webp'
import { useState } from "react";
import '../App.css'
import {creater,Learning} from './Constant.tsx'

const clientId = '335169073502-ptdlb09an2kk7u4cj545022s4suig5f2.apps.googleusercontent.com';






const Login = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [user, setUser] = useState<any>(null);
  
    const onSuccess = (response: GoogleLoginResponse | GoogleLoginResponseOffline) => {
      if ('profileObj' in response) {
        console.log('Login Success: currentUser:', response.profileObj);
        setIsLoggedIn(true);
        setUser(response.profileObj);
      } else {
        console.log('Login Success: response:', response);
      }
    };
  
    const onFailure = (response: any) => {
      console.error('Login failed: res:', response);
      alert('Failed to login. Please try again later.');
    };
  
    const onLogoutSuccess = () => {
      console.log('Logged out');
      setIsLoggedIn(false);
      setUser(null);
    };
  
    return (
      <div className="login-container">
        <div className="login-box">
          <h2 className="login-title">Welcome to ML-Automata</h2>
          <p className="login-description">Login with your Google account to access the ML-Automata platform. Our system provides cutting-edge machine learning tools to help you analyze your data with ease.</p>
          {isLoggedIn ? (
            <div className="logout-section">
              <h3 className="welcome-message">Welcome, {user?.name}</h3>
              <GoogleLogout
                clientId={clientId}
                buttonText="Logout"
                onLogoutSuccess={onLogoutSuccess}
                className="logout-button"
              />
            </div>
          ) : (
            <div className="login-section">
              <GoogleLogin
                clientId={clientId}
                buttonText="Login with Google"
                onSuccess={onSuccess}
                onFailure={onFailure}
                cookiePolicy={'single_host_origin'}
                isSignedIn={true}
                className="login-button"
              />
            </div>
          )}
        </div>
      </div>
    );
  };
  
// export default Login;

interface Result{
    type?:string;
    output?:string;
    metrics?:any;
    image?:string;
    images?:{
        metric_image:string;
        scatter_image:string;
    }
}

interface TaskID{
    task_id?:string;
}

interface TaskStatus{
    state?:string,
    status?:string,
    result?:Result
}


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
    const [result, setResult] = useState<Result| null>(null);
    const [taskId, setTaskId] = useState<TaskID| null>(null);
    const [taskStatus, setTaskStatus] = useState<TaskStatus| null>(null);


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

    const handleSubmit =async (event:any) => {
        event.preventDefault();

        fetch("http://127.0.0.1:5000/files", {
            method: "POST",
            mode: "cors",
            body: file,
        });

        const jsonData  = {data: parameter}

        const paramResponse = fetch("http://127.0.0.1:5000/column_name", {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type":"application/json"
            },
            body:JSON.stringify(jsonData)
        })

        const paramData = (await paramResponse).json();
        console.log("Parameter repsonse:", paramData);

        const taskIDreq = await fetch("http://127.0.0.1:5000/start-task", {
            method:"POST",
            mode:"cors"
        });
        const taskID: TaskID = await taskIDreq.json();
        console.log("Result response:", taskID);

        setTaskId(taskID)
        

        const checkStatus = async(taskID: TaskID) => {
            const intervalID = setInterval(async() => {
            try{
                const response = await fetch(`http://localhost:5000/task-status/${taskID.task_id}`)
                console.log(taskID.task_id)
                const data: TaskStatus = await response.json();
                setTaskStatus(data);
                console.log(taskStatus);
                if (data.state === "SUCCESS" || data.state === "FAILURE"){
                    clearInterval(intervalID);
                    if (data.result){
                        setResult(data.result);
                    }
                }
            }
            catch(error){
                console.error("Error checking status:", error)
            }
        }, 5000);
    }
        checkStatus(taskID)
        
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
            {taskStatus && (
                <div className = "task-status">
                    <h2>Task Status</h2>
                    <p>State: {taskStatus.state}</p>
                    {taskStatus.status && <p> Status: {taskStatus.status}</p>}
                </div>
            )}
            {result && (
            <div className="result_container">
                <h2>Results</h2>
                <pre>{JSON.stringify(result, null, 2)}</pre>
                {result.type && <p><strong>Type:</strong>{result.type}</p>}
                {result.output && <p><strong>Output:</strong>{result.output}</p>}
                {result.metrics && (
                    <div>
                        <h3>Metrics</h3>
                        <pre>{JSON.stringify(result.metrics, null, 2)}</pre>
                        </div>
                )}
                {result.image && <img src = {`data:image/png;base64, ${result.image}`} alt="Result Visualization"/>}
                {result.images && (
                        <> 
                            <img src= {`data:image/png;base64,${result.images.metric_image}`} id= "metric_image" alt="Metric Visualization" />
                            <img src={`data:image/png;base64,${result.images.scatter_image}`} id= "scatter_image" alt="Scatter Plot Visualization" />
                        </>
                    )}
                </div>)}
        </div>
        
    );
}








function Hi() {
    function TextContent(props:any) {
        const wheretolearn = props.specs;
        return (
            <div className="text-content-container">
                <h2>{wheretolearn.learningName}</h2>
                <p>{wheretolearn.description}</p>
                <h3>Types of Learning</h3>
                
                <ul className="learning-types">
                    {wheretolearn.types.map((type:any, index:any) => (
                        <li key={index} className="learning-type-item">
                            <h4>{type.typeName}</h4>
                            <p>{type.description}</p>
                            <h5>Examples</h5>
                            <ul className="examples-list">
                                {type.examples.map((example:any, idx:any) => (
                                    <li key={idx}>{example}</li>
                                ))}
                            </ul>
                            <h5>Common Algorithms</h5>
                            <ul className="algorithms-list">
                                {type.commonAlgorithms.map((algorithm:any, idx:any) => (
                                    <li key={idx}>{algorithm}</li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
                <h3>Where to Learn</h3>
                <ul className="learning-resources">
                    {wheretolearn.learningResources.map((learningResource:any, index:any) => (
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
                {wheretolearn.additionalResources.map((resource:any, index:any) => (
                    <div key={index} className="additional-resources">
                        <h4>{resource.type}</h4>
                        <ul className="additional-resources-list">
                            {resource.items.map((item:any, idx:any) => (
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
                <li><Link to="/login">Login</Link></li> {/* Add Login link */}
                
            </ul>
           </nav>

           <Routes>
           <Route path="/Home" element={<Home/>} />
            <Route path="/creater-credit" element={<CreaterCredit/>} />
            <Route path="/Hi" element={<Hi/>} />
            <Route path="/login" element={<Login />} /> Add Login route
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
