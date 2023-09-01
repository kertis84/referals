import React from 'react';
import { act, render, screen } from '@testing-library/react';
import LoginForm from './LoginForm';
import userEvent from '@testing-library/user-event';


describe('LoginForm', () => {
    const setFormState = jest.fn();
    const setIsLogined = jest.fn();

    test('render PhoneForm', () => {
        render(<LoginForm setFormState={setFormState} setIsLogined={setIsLogined} />);
        expect(screen.getByText("Вход")).toBeInTheDocument();
        expect(screen.getByText("Введите номер телефона")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("+79111111111")).toBeInTheDocument();
        expect(screen.getByText("Получить код")).toBeInTheDocument();
        expect(screen.getByText("Получить код")).toBeDisabled();
        expect(screen.queryAllByRole("textbox").length === 1).toBeTruthy();
    });

    test('test wrong phone', () => {
        render(<LoginForm setFormState={setFormState} setIsLogined={setIsLogined} />);
        act(() => {
            userEvent.click(screen.getByPlaceholderText("+79111111111"));
            userEvent.keyboard("-79111111111");
        });
        expect(screen.getByText("Получить код")).toBeDisabled();
        expect(screen.getByText(/не корректный номер телефона/)).toBeInTheDocument();
    });

    test('render SmsForm', () => {
        render(<LoginForm setFormState={setFormState} setIsLogined={setIsLogined} />);
        act(() => {
            userEvent.click(screen.getByPlaceholderText("+79111111111"));
            userEvent.keyboard("+79111111111");
            userEvent.click(screen.getByText("Получить код"));
        });

        expect(screen.getByText("Вход")).toBeInTheDocument();
        expect(screen.queryByText("Введите номер телефона")).not.toBeInTheDocument();
        expect(screen.queryByPlaceholderText("+79111111111")).not.toBeInTheDocument();
        expect(screen.queryByText("Получить код")).not.toBeInTheDocument();

        const inputs = screen.queryAllByRole("textbox");
        expect(inputs.length === 4).toBeTruthy();
    });

});