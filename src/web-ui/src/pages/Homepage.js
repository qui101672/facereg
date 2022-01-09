import { useRef, useState } from 'react';
import { container } from '../components/styles';
import avata from '../images/avatar.png';
import { ToastContainer, toast } from 'react-toastify';

export const Homepage = () => {
  const [images, setimages] = useState(null);
  const inputFile = useRef(null);
  const [userData, setUserData] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const successCode = "1";

  const onFileChange = (e) => {
    setimages(null);
    setUserData({})
    if (e.target.files[0]) {
      console.log(e.target.files[0]);
      setimages(URL.createObjectURL(e.target.files[0]));

      const reader = new FileReader();

      reader.readAsDataURL(e.target.files[0]);

      reader.onload = async () => {
        const base64String = reader.result
          .replace('data:', '')
          .replace(/^.+,/, '');
        // setImgBase64String(base64String)
        setIsLoading(true);
        await faceRecognitionApi(base64String);
      };
    }
  };
  const axios = require('axios');
  const faceRecognitionApi = async (stringBase64) => {
    var bodyFormData = new FormData();
    bodyFormData.append('image', stringBase64);

    await axios({
      method: 'post',
      url: 'http://127.0.0.1:6868/recognition',
      data: bodyFormData,
      headers: { 'Content-Type': 'multipart/form-data' },
    })
      .then((res) => {
        setIsLoading(false);
        setUserData(res.data.data);
        if (res.data.data.status === successCode) {
          toast.success(res.data.data.message.toUpperCase());
        } else {
          toast.warn(res.data.data.message.toUpperCase());
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const onButtonClick = () => {
    inputFile.current.click();
  };
  console.log( userData.predicted !== ""? userData.predicted : 'Unidentified');
  return (
    <div className={container}>
      <div className='flex flex-row w-full justify-center bg-F6F3EF'>
        <div className='flex flex-col pl-4 w-3/7'>
          <div className='h-28'>
            <h1 className='text-5xl font-bold text-845A29 uppercase mt-6'>
              Face Recognize
            </h1>
          </div>
          <h1 className='capitalize text-2xl  text-845A29'>
            face Recognition engine.
          </h1>
          <h1 className='capitalize text-2xl text-845A29'>
            upload photo and identify yourself.
          </h1>

          <div className='w-f pt-1 pb-1 mt-28'>
            <button
              className='transform transition  hover:scale-110  rounded-full bg-bt-reg  text-845A29  font-bold py-2 px-4 items-center uppercase'
              onClick={onButtonClick}
              disabled={isLoading === true && true}
            >
              + Choose A Face For Recognition
            </button>
            <input
              type='file'
              id='file'
              ref={inputFile}
              onChange={onFileChange}
              className='hidden'
            />
          </div>
        </div>
        <div className='flex flex-col '>
          <div className='flex flex-col w-full h-2/6 justify-center items-center bg-white mt-24'>
            <div className='w-28 h-32 bg-blue-500'>
              <img
                className='w-full h-full'
                src={images ? images : avata}
                alt=''
              ></img>
            </div>
            <div
              className={
                isLoading
                  ? ''
                  : userData.status === successCode
                  ? 'bg-green-500'
                  : 'bg-red-600'
              }
            >
              <span>{isLoading ? '' : userData ? userData.message: ''}</span>
            </div>
          </div>
          <div className='flex justify-center items-center'>
            <div className='flex flex-row space-x-2'>
              <label className='text-845A29'>Predicted Name: </label>
              <input
                readOnly={true}
                disabled={true}
                type='text'
                value={
                  isLoading === true ? 'Recognizing...' : userData.status === successCode ? userData.predicted :'Unidentified'
                }
              ></input>
            </div>
          </div>
        </div>
        <ToastContainer
        position='top-center'
        autoClose={2000}
        hideProgressBar={true}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnHover={false}
      />
      </div>
    </div>
  );
};
