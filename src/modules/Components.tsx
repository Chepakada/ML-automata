import React, { ChangeEvent } from "react";
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


    const handleFileChange = (e:ChangeEvent<HTMLInputElement>)=>{
        if (e.target.files){
            setFile(e.target.files[0]);
            console.log(file);
        }
        
    };

    const handleInput = () =>{
        
        
    }
    

    return(
        <div>
            <form>
                    <label htmlFor = "databox">Data File: </label>
                    <input type = "file" id = "databox" required onChange={handleFileChange}></input>
                    <label htmlFor = "parameter">Dependent Column Name: </label>
                    <input type = "text" id = "parameter" placeholder="Column Name here" required></input>
                    

                    <input type= "submit" id = "datasubmit" value = "Submit" onClick={handleInput}></input>
            </form>
        </div>
    )
}




