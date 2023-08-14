
export type FormControlElement = HTMLInputElement | HTMLTextAreaElement;

export interface IUserProfile {
    id: string;
    phone: string;
    email: string;
    first_name: string;
    last_name: string;
    user_ref: string;
    date_joined: string;
}

export interface IApiArray<T> {
    count: number;
    next: string;
    previous: string;
    results: T[];
}

export interface IReferal {
    phone: string;
}

export interface ILoginFormErrors {
    phone?: string,
    code?: string,
};

export interface ILoginFormProps {
    setFormState: React.Dispatch<React.SetStateAction<boolean>>
    setIsLogined: React.Dispatch<React.SetStateAction<boolean>>
}

