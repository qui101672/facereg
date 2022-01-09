import { useRef, useState } from "react";
import { container, label, row } from "../components/styles";
export const Addpage = () => {
  const [nameEmp,setnameEmp ] = useState('');
  const [images, setimages] = useState(['']);
  const inputFile = useRef(null);

  const onFileChange = (e) => {
    if (e.target.files[0]) {
      console.log("picture: ", e.target.files);
      // setPicture(e.target.files[0]);
      const reader = new FileReader();
      reader.addEventListener("load", () => {
        setimages(reader.result);
      });
      reader.readAsDataURL(e.target.files[0]);
    }
  }

const onButtonClick = () => {
  inputFile.current.click();
};

  const renderPreviewImages = (array) => {
    const images = array.forEach(e => {
      return(
        <div key={e} style={{display:"flex", width:100, height: 100}}>
          <img src={e} alt="" />
        </div>
      )
    });
    return <div>{images}</div>
  }
  return (
    <div style={container}>
       <div style={{width:"100%", backgroundColor:'gray', display:'flex', justifyContent:'center'}}>
        <div style={{width:500, height:500, borderStyle:'solid', borderWidth:2, borderColor:'black', backgroundColor:'#cbe9de',display:'flex', alignItems:'center', flexDirection:'column'}}>
          <h3>Them nhan vien</h3>
          <div style={{display:'flex',flexDirection:'column'}}>
          <div>
            <label style={label} for="ten">Ten nguoi dung</label>
            <input type="text" id="ten" onChange={(e)=>setnameEmp(e.target.value)} />
          </div>

          <div>
          <label style={label} for="ten">Anh nguoi dung</label>
          <button onClick={onButtonClick}>Them anh</button>
          <input type="file" id="file" ref={inputFile} onChange={onFileChange } style={{ display: "none" }}/>  
          </div>

          <div>
          <label for="ten">Ten nhan vien da nhap:</label>
          <h3>{nameEmp !== ""? nameEmp : "Xin nhap ten nhan vien"}</h3>
          </div>

          <div>
          <label for="ten">Anh da them:</label>
          {images && renderPreviewImages(images)}
          </div>
          </div>
      </div>
      </div>
    </div>
  );
};
