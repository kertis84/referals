import React from 'react';
import { render, screen } from '@testing-library/react';
import ProfileForm from './ProfileForm';
import { rest } from 'msw'
import { setupServer } from 'msw/node'


const server = setupServer(
    rest.get('*user/', (req, res, ctx) => {
        return res(ctx.json(''))
    }),

    rest.get('*referals/children', (req, res, ctx) => {
        return res(ctx.json(''))
    }),

    rest.get('*referals/parent', (req, res, ctx) => {
        return res(ctx.json(''))
    }),
);

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('ProfileForm', () => {

    test('render ProfileForm', () => {
        render(<ProfileForm />);
        expect(screen.getByText("Профиль")).toBeInTheDocument();
        expect(screen.getByLabelText("ID")).toBeInTheDocument();
        expect(screen.getByLabelText("Номер телефона")).toBeInTheDocument();
        expect(screen.getByLabelText("Адрес электронной почты")).toBeInTheDocument();
        expect(screen.getByLabelText("Имя")).toBeInTheDocument();
        expect(screen.getByLabelText("Фамилия")).toBeInTheDocument();
        expect(screen.getByLabelText("Ваш персональный инвайт-код")).toBeInTheDocument();
        expect(screen.getByLabelText("Дата регистрации")).toBeInTheDocument();
        expect(screen.getByLabelText("Активировать инвайт-код")).toBeInTheDocument();
        expect(screen.getByLabelText("Ваши рефералы")).toBeInTheDocument();
        expect(screen.getByText("Сохранить")).toBeDisabled();
        expect(screen.queryAllByRole("textbox").length === 9).toBeTruthy();
    });

});