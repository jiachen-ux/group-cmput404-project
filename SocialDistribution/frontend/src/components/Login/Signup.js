/* eslint-disable no-console */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../../axiosApi';
import './Form.css';
import style from './SignupLogin.module.css';



// Function to create Signup Form
function Signup() {
  // for displaying an error message for a failed api call
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();



  const loginPage = () => {
    navigate('/login');
  };

  const userNameHandeler = (event) => {
    setUserName(event.target.value);
  };


  const emailHandeler = (event) => {
    console.log(event.target.value);
    setEmail(event.target.value);
  };

  
  const passwordHandeler = (event) => {
    setPassword(event.target.value);
  };

  

  const confirmPasswordHandeler = (event) => {
    setConfirmPassword(event.target.value);
  };

  


  function registerUserHandeler(event) {
    event.preventDefault();


    const userInfo = {
      email,
      password,
      username: userName,
    };

    console.log(userInfo);

    setErrorMessage('Ooops! Something went wrong!');
    let message = '';

    // checks for input in required field.
    // If the input field is empty error message is displayed
    if (!userName) {
      setErrorFirstName('First name is required');
    } else {
      setErrorFirstName('');
    }

    if (!email) {
      setErrorEmail('Email is required');
    } else {
      setErrorEmail('');
    }

    if (!password) {
      setErrorPassword('Password is required');
    } else {
      setErrorPassword('');
    }

    if (!confirmPassword) {
      setErrorConfirmPassword('Please confirm password');
    } else {
      setErrorConfirmPassword('');
    }

    // checks is password is equal to confirm password
    // if they are user is allowed to signin
    if (confirmPassword === password) {
      userInfo.email = email.toLowerCase();
      axiosInstance.post('user/create/', userInfo)
        .then((response) => {
          console.log('Response Data', response.data);
          const state = {
            requireVerification: true,
          };
          navigate('/login', { state });
        })
        .catch((error) => {
          setIsErrorNotifOpen(true);
          if (error.response) {
          // Request made and server responded
            console.log('h');
            console.log(error.response.data);
            const res = error.response.data;

            Object.keys(res).map((keyName) => {
              console.log(keyName);// eslint-disable-line no-console
              console.log(res[keyName]);// eslint-disable-line no-console
              if (keyName === 'Errors') {
                for (let i = 0; i < res.Errors.length; i += 1) {
                  message += res.Errors[i];
                }
                setErrorMessage(message);
              }
              if (keyName === 'email') {
                setErrorEmail(res[keyName]);
              } else if (keyName === 'phone_number') {
                setErrorPhone(res[keyName]);
              } else {
                setErrorPhone('');
                setErrorEmail('');
              }
              return res[keyName];
            });

            console.log(error.response.status);
            console.log(error.response.headers);
          } else if (error.request) {
          // The request was made but no response was received
            console.log(error.request);
          } else {
          // Something happened in setting up the request that triggered an Error
            console.log('Error', error.message);
          }
        });
    } else {
      setErrorConfirmPassword('Passwords does not match');
    }
    return userInfo;
  }

  return (
      <div className={style.main_container}>
        <div className={style.button_container}>
          <button type="button" className={style.button_with_border}>SIGN UP</button>
          <button type="button" id="login-button" className={style.button} onClick={loginPage}>LOGIN</button>
        </div>
        <div className="form-container">
          <form onSubmit={registerUserHandeler}>
            <div className="login-wrapper">
              <div className="input-field">
                <>{/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}</>
                <label className="required">First Name</label>
                <input
                  type="text"
                  value={firstName}
                  onChange={firstNameHandeler}
                  onBlur={firstNameErrorHandeler}
                  placeholder="Enter your first name..."
                />
              </div>

              <div className="input-field">
                <>{/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}</>
                <label className="required">Email</label>
                <input
                  type="text"
                  value={email}
                  onChange={emailHandeler}
                  onBlur={emailErrorHandeler}
                  placeholder="johndoe@gmail.com"
                />
              </div>
              
              
              <div className="input-field">
                <>{/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}</>
                <label className="required">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={passwordHandeler}
                  onBlur={PasswordErrorHandeler}
                  placeholder="Enter password..."
                />
              </div>
              <div className="input-field">
                <>{/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}</>
                <label className="required">Confirm password</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={confirmPasswordHandeler}
                  onBlur={confirmPasswordErrorHandeler}
                  placeholder="Confirm your password..."
                />
              </div>
            </div>
            <div className="bottom-row">
              <div className="submit-button">
                <button type="submit" id="submit">SIGN UP</button>
              </div>
            </div>
          </form>
        </div>
      </div>
  );
}

export default Signup;