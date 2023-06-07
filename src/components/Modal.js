import React from "react";

function Modal({ closeModal }) {
    return <div className="modalBackground"> 
          <div className='modalContainer'>
            <div className="titleCloseBtn">
                <button onClick={() => closeModal(false)}> X </button>
            </div>
              <div className="title">
                <h1 style={{ color: "black"}}>
                    Generative Land Use
                </h1>
              </div>
              <div className="body">
                <p> XXX </p>
              </div>
              <div className="footer">
                <button onClick={() => closeModal(false)}>Back</button>
              </div>
          </div>
    
        </div>
      
      
}

export default Modal;