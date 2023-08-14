import './App.css';
import { useState } from 'react';
import { Button, Modal } from 'react-bootstrap';
import LoginForm from './components/LoginForm';
import ProfileForm from './components/ProfileForm';
import $api, { API_URL } from './services/axios';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
    const [profileFormShown, setProfileFormState] = useState(false);
    const [loginFormShown, setLoginFormState] = useState(false);
    const [is_logined, setIsLogined] = useState(false);

    function logout(): void {
        $api.post(API_URL + 'logout/');
        setIsLogined(false);
    }

    return (
        <>
            <div className="App">
                {is_logined ?
                    <>
                        <div style={{ marginTop: "10rem" }}><b>Вы вошли в систему</b></div>

                        <Button className='m-5' onClick={() => { setProfileFormState(true) }}>
                            Show Profile
                        </Button>

                        <Button className='m-5' onClick={logout}>
                            Logout
                        </Button>
                    </>
                    :
                    <Button style={{ marginTop: "10rem" }} onClick={() => setLoginFormState(true)}>
                        Login
                    </Button>
                }
            </div>

            <Modal show={loginFormShown} fullscreen="sm-down" onHide={() => setLoginFormState(false)} >
                <LoginForm setFormState={setLoginFormState} setIsLogined={setIsLogined} />
            </Modal>

            <Modal show={profileFormShown} fullscreen="md-down" size='lg' onHide={() => setProfileFormState(false)} >
                <ProfileForm />
            </Modal>
        </>
    );
}

export default App;
