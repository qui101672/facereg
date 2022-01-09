import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Homepage } from './pages/Homepage';
import { Trainpage } from './pages/Trainpage';
import { Nav } from './components/Nav';
import { Users } from './pages/Users';

function App() {
  return (
    <Router>
      <div className='flex flex-col h-screen bg-blue-300'>
        <div className="flex items-center justify-center">
          <Nav />
        </div>
        <div className='flex justify-center bg-blue-300'>
          <Switch>
            <Route path='/' exact component={Homepage} />
            <Route path='/train' component={Trainpage} />
            <Route path='/users' component={Users} />
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;
