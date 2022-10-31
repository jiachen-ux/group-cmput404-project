import logo from './logo.svg';
import './App.css';
import Register from './Register';
import { ChakraProvider } from '@chakra-ui/react'

function App() {
  return (
    <ChakraProvider>
       <Register/>
    </ChakraProvider>
  )
}

export default App;
