import React, { ChangeEvent, useEffect } from "react";
import { useState } from "react";

export function Header(){
    return (
        <header>
           <nav>
            <u>
                <li>Home</li>
                <li>Background</li>
                <li>Learning</li>
                <li>Creater Credit</li>
                
            </u>
           </nav>
        </header>
    )
}
export function Footer(){
    var date = new Date();

    return(
        <footer>
            <span>&copy;{date.getFullYear()}</span>
            <span>ML-automata</span>
        </footer>
    )
}


export function InputBox(){
    const [file, setFile] = useState<File>();
    const [parameter, setParameter] = useState("");

    var jsonData = {
        "id":1,
        "parameter":parameter,
        "file":file,
        "date": new Date().getUTCDate()
       
    }

    
    

    const handleFileChange = (e:ChangeEvent<HTMLInputElement>)=>{
        const files = e.target.files

        if (files && files.length > 0) {
            setFile(files[0]);
            console.log("files:", files)

        
    };}

    const handleParameterChange = (e:ChangeEvent<HTMLInputElement>) => {
        setParameter(e.target.value)
    }

    const handleInput = () =>{


        fetch("http://127.0.0.1:5000/files", {
            method: "POST",
            mode: "cors",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(jsonData),
          })
    
        
    }
    

    return(
        <div>
            <form>
                    <label htmlFor = "databox">Data File: </label>
                    <input type = "file" id = "databox" required onChange={handleFileChange}></input>
                    <label htmlFor = "parameter">Dependent Column Name: </label>
                    <input type = "text" id = "parameter" placeholder="Column Name here" required onChange = {handleParameterChange}></input>
                    

                    <input type= "submit" id = "datasubmit" value = "Submit" onClick={handleInput}></input>
            </form>
        </div>
    )
}




export function DisplayFile(){
    const [fileData, setFileData] = useState([]);
    useEffect(()=>{
        fetch("http://127.0.0.1:5000/files",{
            method: "GET",
            headers: {
                "Content-Type":"application/json"
            }
        })
    }).then()
}