import { useState, useEffect } from 'react';
import { container } from '../components/styles';

export const Users = () => {
  const [userData, setUserData] = useState([]);
  const [fetchData, setFetchData] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  const axios = require('axios');

  const fecthUsers = async () => {
    axios
      .post('http://127.0.0.1:6868/users')
      .then((res) => {
        setIsLoading(false);
        setFetchData(res.data.data);
        setUserData(res.data.data.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };
  useEffect(() => {
    fecthUsers();
  }, []);
  const [searchInput, setSearchInput] = useState("")
  const userArray = userData.filter(name => name.full_name.toLowerCase().includes(searchInput.toLowerCase()))

  return (
    <div className={container}>
      <div className='flex flex-col w-full bg-F6F3EF bg-scroll pt-2  items-center'>
        <div className='flex w-full  justify-center'>
        <input
                type='text'
                className='h-14 w-96 pr-8 pl-5 rounded z-0 focus:shadow focus:outline-none'
                placeholder='Search user...'
                onChange={(e) => setSearchInput(e.target.value)}
              />
        </div>
        <div className='flex flex-wrap w-3/4 mt-3 items-center p-1'>
        {userArray.map((user) => (
          <div className='flex flex-col border-2 rounded-md bg-blue-400 w-60 h-20 text-sm p-1 justify-center transform transition hover:scale-110 m-1'>
            <div className='flex flex-row space-x-1'>
              <label className='text-845A29'>Full Name: </label>
              <p>{user.full_name}</p>
            </div>
            <div className='flex flex-row space-x-1'>
              <label className='text-845A29'>Created Date: </label>
              <p>{user.created_date}</p>
            </div>
            <div className='flex flex-row space-x-1'>
              <label className='text-845A29'>Last checked: </label>
              <p>{user.last_checked}</p>
            </div>
          </div>
        ))}
        </div>
        {isLoading && 'Loading...'}
        
      </div>
    </div>
  );
};
