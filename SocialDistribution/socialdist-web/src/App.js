import logo from './logo.svg';
import './App.css';

function loadPosts(callback) {
  const xhr = new XMLHttpRequest() //xhr =some class
  const method = 'GET' //Post
  const url = "/posts" 
  const responseType = "json"
  xhr.responseType = responseType   
  xhr.open(method, url)
  xhr.onload = function(){
    callback(xhr.response, xhr.status)
  }
  xhr.send()
}
function App() {
  const [posts, setPosts]= useState([])

  useEffect(() => {
    const myCallback =  (resonse, status) => {
      if (status === 200) {
        setPosts(resonse)
      }
    }
    loadPosts(myCallback)
    
    }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
