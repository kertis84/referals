import { useState, FormEvent, ChangeEvent } from 'react';
import {
    Button,
    Form,
    FormControl,
    FormGroup,
    FormLabel,
    Modal,
    ModalBody
} from 'react-bootstrap';
import validator from 'validator';
import OtpInput from 'react-otp-input';
import $api, { API_URL } from '../services/axios';
import { AxiosError } from 'axios';
import { FormControlElement, ILoginFormErrors, ILoginFormProps } from '../models/interfaces';


const LoginForm = (props: ILoginFormProps) => {
    const [otp, setOtp] = useState('');
    const [phone, setPhone] = useState('')
    const [smsWaiting, setSmsWaiting] = useState(false)
    const [formErrors, setFormErrors] = useState({} as ILoginFormErrors);

    // функция получения псевдо sms
    function getSms(): void {
        setTimeout(() => {
            const URL = [API_URL, 'sms/', phone, '/'].join('');
            $api.get(URL).then((response) => {
                alert('Вы получили СМС с кодом: ' + response.data.code)
            }).catch((err) => console.error(err));
        }, 1000);
    }

    // запрос на отправку sms пользователю
    async function makeNewSms(): Promise<void> {
        const URL = [API_URL, 'login/', phone].join('');
        await $api.post(URL);
        getSms();
    }

    // если телефонный номер корректный, отправляем sms и переключаем элементы на ввод 
    function handleSubmit(event: FormEvent<HTMLFormElement>): void {
        event.preventDefault();
        if (validator.isMobilePhone(phone, ['ru-RU'], { strictMode: true })) {
            makeNewSms();
            setSmsWaiting(true);
        }
    }

    // пользователь хочет изменить номер телефона
    function handleClickChangePhone(): void {
        setOtp('');
        setSmsWaiting(false);
        setFormErrors((prev) => ({ ...prev, code: undefined }))
    }

    // ввод проверочного кода и его валидация
    function handleChangeOTP(otp: string): void {
        if (otp.length === 4) {
            const URL = [API_URL, 'login/', phone].join('');
            $api.post(URL, JSON.stringify({ code: otp }))
                .then((res) => {
                    props.setFormState(false);
                    props.setIsLogined(true);
                })
                .catch((error) => error instanceof AxiosError && setFormErrors((prev) => ({ ...prev, code: 'код не верный' }))
                );
        }
        formErrors.code && setFormErrors((prev) => ({ ...prev, code: undefined }))
        setOtp(otp);
    }

    // ввод номера телефона и его валидация
    function handleChangePhone(event: ChangeEvent<FormControlElement>): void {
        setPhone(event.target.value);
        const phoneErr = validator.isMobilePhone(event.target.value, ['ru-RU'], { strictMode: true }) ? undefined : 'не корректный номер телефона';
        setFormErrors((prev) => ({ ...prev, phone: event.target.value.length === 0 ? undefined : phoneErr }))
    }


    return (
        <>
            <Modal.Header closeButton>
                <Modal.Title>Вход</Modal.Title>
            </Modal.Header>

            <ModalBody>
                <Form onSubmit={handleSubmit}>
                    {!smsWaiting ?
                        <FormGroup controlId='phone' className='my-3 w-75 mx-auto'>
                            <FormLabel>Введите номер телефона</FormLabel>
                            <FormControl size='lg' type='phone' name='phone' placeholder='+79111111111'
                                autoComplete='phone' minLength={12} maxLength={12} required
                                isInvalid={formErrors.phone !== undefined} value={phone} onChange={handleChangePhone} />
                            <div className='invalid-feedback'>*{formErrors.phone}</div>
                        </FormGroup>
                        :
                        <FormGroup controlId='code' className='my-3 w-75 mx-auto'>
                            <OtpInput numInputs={4} value={otp} onChange={handleChangeOTP} inputStyle='inputStyle' containerStyle={formErrors.code ? 'centerXY is-invalid' : 'centerXY'}
                                renderInput={(props) => <input {...props} />} shouldAutoFocus />
                            <span className='invalid-feedback text-center'>*{formErrors.code}</span>
                            {formErrors.code &&
                                <div>
                                    <small className='float-start finger text-primary' onClick={makeNewSms}>отправить повторно</small>
                                    <small className='float-end finger text-primary' onClick={handleClickChangePhone}>изменить номер</small>
                                </div>
                            }
                        </FormGroup>
                    }
                    {!smsWaiting &&
                        <Button type='submit' className='float-end' disabled={!(formErrors.phone === undefined && phone.length === 12)}>
                            Получить код
                        </Button>
                    }
                </Form>
            </ModalBody>
        </>
    )
}


export default LoginForm;