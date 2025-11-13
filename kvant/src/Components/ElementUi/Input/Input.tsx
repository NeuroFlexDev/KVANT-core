import styles from './input.module.css';

interface InputProps {
    type: string;
    placeholder: string;
    className?: string;
    value?: string;
    onChange?: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
    label?: string;
}

const Input = ({ type, placeholder, className, value, onChange, label }: InputProps) => {
    const inputClass = className || styles.inputFieldClassic;

    return (
        <div className={styles.inputContainer}>
            {label && <label className={styles.inputLabel}>{label}</label>}
            <input
                type={type}
                placeholder={placeholder}
                className={inputClass}
                value={value}
                onChange={onChange}
            />
        </div>
    );
};

export default Input;