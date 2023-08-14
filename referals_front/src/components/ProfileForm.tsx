import { useState, FormEvent, useEffect, ChangeEvent, KeyboardEvent } from 'react';
import {
    Button,
    Col,
    Form,
    FormControl,
    FormGroup,
    FormLabel,
    Modal,
    ModalBody,
    Row
} from 'react-bootstrap';
import $api, { API_URL } from '../services/axios';
import moment from "moment";
import { FormControlElement, IApiArray, IReferal, IUserProfile } from '../models/interfaces';
import { AxiosError } from 'axios';


const ProfileForm = () => {
    const [userProfile, setUserProfile] = useState({} as IUserProfile);
    const [userReferals, setUserReferals] = useState([] as IReferal[]);
    const [userParent, setUserParent] = useState('');
    const [userHasNotParent, setUserHasNotParent] = useState(true);
    const [profileChanged, setProfileChanged] = useState(false);

    // однократно при запуске
    useEffect(() => {
        // получаем профиль
        $api.get<IApiArray<IUserProfile>>(API_URL + 'user/').then((res) => {
            setUserProfile(res.data.results[0]);
        }).catch((err) => { err instanceof AxiosError && err.response?.status !== 404 && console.error(err) });

        // получаем рефералов
        $api.get<IReferal[]>(API_URL + 'referals/children').then((res) => {
            setUserReferals(res.data);
        }).catch((err) => { err instanceof AxiosError && err.response?.status !== 404 && console.error(err) });

        // получаем реферера (может быть только один)
        $api.get<IReferal>(API_URL + 'referals/parent').then((res) => {
            setUserParent(res.data.phone);
            setUserHasNotParent(false);
        }).catch((err) => { err instanceof AxiosError && err.response?.status !== 404 && console.error(err) });

    }, []);

    // сохранение изменяемых данных в профиле
    function handleSubmit(event: FormEvent<HTMLFormElement>): void {
        event.preventDefault();
        const URL = [API_URL, 'user/', userProfile.id, '/'].join('');
        $api.patch<IUserProfile>(URL, JSON.stringify(userProfile)).then((res) => {
            setUserProfile(res.data);
            setProfileChanged(false);
        }).catch((err) => console.error(err));
    }

    // корректировка изменяемых данных в профиле
    function handleChangeUserProfile(event: ChangeEvent<FormControlElement>): void {
        setUserProfile((data) => ({ ...data, [event.target.name]: event.target.value }));
        setProfileChanged(true);
    }

    // ввод инвайт-кода (валидация при нажатии Enter в функции handleKeyDownParent)
    function handleChangeParent(event: ChangeEvent<FormControlElement>): void {
        setUserParent(event.target.value);
    }

    // валидация инвайт-кода. Если валидация прошла успешно деактивируем поле и выводим телефон реферера
    function handleKeyDownParent(event: KeyboardEvent<FormControlElement>): void {
        if (event.key === 'Enter') {
            event.preventDefault();
            $api.post<IReferal>(API_URL + 'referals/activate', JSON.stringify({ invite_code: event.currentTarget.value }))
                .then((res) => {
                    setUserParent(res.data.phone);
                    setUserHasNotParent(false);
                }).catch((err) => { err instanceof AxiosError && err.response?.status === 404 && alert('Инвайт-код не существует') });
        }
    }

    return (
        <>
            <Modal.Header closeButton>
                <Modal.Title>Профиль</Modal.Title>
            </Modal.Header>
            <ModalBody>
                <Form onSubmit={handleSubmit}>
                    <Row>
                        <Col>
                            <FormGroup controlId='id' className='my-3'>
                                <FormLabel>ID</FormLabel>
                                <FormControl name='id' value={userProfile.id ?? ''} disabled />
                            </FormGroup>

                            <FormGroup controlId='phone' className='my-3'>
                                <FormLabel>Номер телефона</FormLabel>
                                <FormControl type='phone' value={userProfile.phone ?? ''} disabled />
                            </FormGroup>

                            <FormGroup controlId='email' className='my-3'>
                                <FormLabel>Адрес электронной почты</FormLabel>
                                <FormControl type='email' name='email' value={userProfile.email ?? ''} onChange={handleChangeUserProfile} />
                            </FormGroup>

                            <FormGroup controlId='first_name' className='my-3'>
                                <FormLabel>Имя</FormLabel>
                                <FormControl type='text' name='first_name' value={userProfile.first_name ?? ''} onChange={handleChangeUserProfile} />
                            </FormGroup>

                            <FormGroup controlId='last_name' className='my-3'>
                                <FormLabel>Фамилия</FormLabel>
                                <FormControl type='text' name='last_name' value={userProfile.last_name ?? ''} onChange={handleChangeUserProfile} />
                            </FormGroup>

                            <FormGroup controlId='user_ref' className='my-3'>
                                <FormLabel>Ваш персональный инвайт-код</FormLabel>
                                <FormControl type='text' name='user_ref' value={userProfile.user_ref ?? ''} disabled />
                            </FormGroup>

                            <FormGroup controlId='date_joined' className='my-3'>
                                <FormLabel>Дата регистрации</FormLabel>
                                <FormControl value={moment(userProfile.date_joined).format('DD-MM-YYYY HH:mm:ss')} disabled />
                            </FormGroup>

                            <Button type='submit' className='float-end' disabled={!profileChanged}>
                                Сохранить
                            </Button>
                        </Col>
                        <Col>
                            <FormGroup controlId='parent' className='my-3'>
                                {userHasNotParent ?
                                    <FormLabel>Активировать инвайт-код</FormLabel> :
                                    <FormLabel>Вы активировали инвайт-код пользователя</FormLabel>
                                }
                                <FormControl type='text' value={userParent} disabled={!userHasNotParent} maxLength={6}
                                    onChange={handleChangeParent}
                                    onKeyDown={handleKeyDownParent} />
                            </FormGroup>

                            <FormGroup controlId='referals' className='my-3'>
                                <FormLabel>Ваши рефералы</FormLabel>
                                <FormControl as='textarea' defaultValue={userReferals.map(val => val.phone).join('\n')} disabled />
                            </FormGroup>
                        </Col>
                    </Row>
                </Form>
            </ModalBody>
        </>
    )
}


export default ProfileForm;