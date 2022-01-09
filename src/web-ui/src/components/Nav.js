import { Link } from 'react-router-dom';
import { useState } from 'react';

export const Nav = () => {
  const [isActive, setIsActive] = useState(0);

  return (
    <div className='flex w-2/3 pt-2'>
      <ul className='flex '>
        <Link to='/'>
          <li className='-mb-px mr-1'>
            <a
              onClick={() => setIsActive(0)}
              class={
                isActive === 0
                  ? 'inline-block border-l border-t border-r rounded-t py-2 px-4 font-semibold focus:outline-none w-32 text-center bg-F6F3EF text-845A29'
                  : 'bg-white inline-block py-2 px-4 font-semibold w-28 text-center text-gray-400'
              }
              href=''
            >
              Recognize
            </a>
          </li>
        </Link>
        <Link to='/train'>
          <li className='mr-1'>
            <a
              onClick={() => setIsActive(1)}
              class={
                isActive === 1
                  ? 'inline-block border-l border-t border-r rounded-t py-2 px-4 font-semibold focus:outline-none w-32 text-center bg-F6F3EF text-845A29'
                  : 'bg-white inline-block py-2 px-4 font-semibold w-28 text-center text-gray-400'
              }
              href=''
            >
              Registration
            </a>
          </li>
        </Link>
        <Link to='/users'>
          <li className='mr-1'>
            <a
              onClick={() => setIsActive(2)}
              class={
                isActive === 2
                  ? 'inline-block border-l border-t border-r rounded-t py-2 px-4 font-semibold focus:outline-none w-32 text-center bg-F6F3EF text-845A29'
                  : 'bg-white inline-block py-2 px-4 font-semibold w-28 text-center text-gray-400'
              }
              href=''
            >
              Users
            </a>
          </li>
        </Link>
      </ul>
    </div>
  );
};
