import { useRef, useState } from 'react';
import { container } from '../components/styles';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const Trainpage = () => {
  const inputFile = useRef(null);
  const [userData, setUserData] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [userName, setUserName] = useState('');
  const [imagesSend, setImagesSend] = useState([]);
  const [imagesRender, setImagesRender] = useState([]);

  const successCode = '1';

  const handleInputChange = (e) => {
    setUserName(e.target.value);
  };

  const multipleFileChoose = async (e) => {
    const fileSends = [];
    const ArrayUrl = [];
    let files = Array.from(e.target.files).map((file) => {
      fileSends.push(file);
      const url = URL.createObjectURL(file);
      ArrayUrl.push(url);
      let readers = new FileReader();
      return new Promise((res) => {
        readers.onload = async () => res(readers.result);
        readers.readAsDataURL(file);
      });
    });

    const arrayString64 = [];
    let res = await Promise.all(files);
    res.forEach((file) => {
      const fileType = file.split(';').slice(0)[0].split('/')[1];
      const base64String = file.replace('data:', '').replace(/^.+,/, '');
      const stringSend = JSON.stringify({
        data: fileType,
        base64: base64String,
      });
      // const stringSend = fileType + "-" + base64String
      arrayString64.push(stringSend);
    });
    // setImgBase64String(base64String)
    setImagesSend(fileSends);
    setImagesRender(ArrayUrl);
  };

  const axios = require('axios');

  const faceRecognitionApi = async () => {
    if (userName === '') {
      toast.warn('USER NAME IS REQUIRED');
      return;
    }

    if (imagesSend.length < 5) {
      toast.warn('PlEASE ADD MORE PHOTO');
      return;
    }
    setIsLoading(true);

    var bodyFormData = new FormData();

    for (var i = 0; i < imagesSend.length; i++) {
      bodyFormData.append('image[]', imagesSend[i]);
    }
    bodyFormData.append('name', userName);

    await axios({
      method: 'post',
      url: 'http://127.0.0.1:6868/registration',
      data: bodyFormData,
      headers: { 'Content-Type': 'multipart/form-data' },
    })
      .then((res) => {
        console.log(res.data.data);
        setUserData(res.data.data);
        if (res.data.data.status === successCode) {
          toast.success(res.data.data.message.toUpperCase());
        } else {
          toast.warn(res.data.data.message.toUpperCase());
        }
        setIsLoading(false);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const onButtonClick = () => {
    inputFile.current.click();
  };

  if (imagesSend.length < 0) {
    console.log('empty');
  }

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
            upload photo for registration
          </h1>

          <div className='w-f pt-1 pb-1 mt-10'>
            <div className='space-x-2 mb-3'>
              <label>Full Name</label>
              <input type='text' id='file' onChange={handleInputChange} />
            </div>
            <div className='mt-3'>
              <button
                className='transform transition  hover:scale-110  rounded-full bg-bt-reg  text-845A29  font-bold py-2 px-4 items-center uppercase'
                onClick={faceRecognitionApi}
                disabled={isLoading === true && true}
              >
                Registration
              </button>
            </div>
          </div>
        </div>
        <div className='flex flex-col w-3/7'>
          <div className='flex flex-col w-full h-1/3 bg-white mt-48'>
            <div className='flex w-full justify-between border-solid border-b-2'>
              <h1 className='capitalize text-2xl text-845A29'>
                {imagesSend.length > 0 ? 'Uploaded Photos' : 'Add Your Photo'}
              </h1>
              <button
                className='transform transition  hover:scale-110  rounded-full bg-bt-reg  text-845A29  font-bold py-2 px-4 items-center uppercase'
                onClick={onButtonClick}
              >
                +
              </button>
              <input
                type='file'
                id='file'
                ref={inputFile}
                onChange={multipleFileChoose}
                className='hidden'
                multiple
              />
            </div>

            <div className='flex flex-wrap w-ful'>
              {imagesRender.map((image) => (
                <div className='w-14 h-14'>
                  <img className='w-full h-full' src={image} alt=''></img>
                </div>
              ))}
            </div>
          </div>
          <span>{isLoading ? 'Please wait a moment...' : ''}</span>
        </div>
      </div>
      <ToastContainer
        position='top-center'
        autoClose={5000}
        hideProgressBar={true}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnHover={false}
      />
    </div>
  );
};
