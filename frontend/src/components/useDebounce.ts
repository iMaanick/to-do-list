import { useEffect, useState } from "react";

/**
 * useDebounce - a hook to add delay between requests.
 *
 * How it works:
 * In many components, there is a need to send requests to the server when some value changes,
 * for example, when typing text or numbers in an input field. Without delay, each value change
 * would result in a new request, which could overload the server and network.
 *
 * To address this, the useDebounce hook is used. You pass in the value you want to send
 * and the delay (in milliseconds) between requests. The hook returns the debounced value,
 * which you can use to send your request.
 *
 * Usage example:
 *
 * ```jsx
 * const debouncedValue = useDebounce(value, 800);
 * 
 * // Example usage inside useEffect to send an API request
 * useEffect(() => {
 *     // Your API request using debouncedValue
 *     your_API_query(debouncedValue);
 * }, [debouncedValue, your_API_query]);
 * ```
 *
 * When the value changes, useDebounce starts a delay timer. If the value does not change
 * within the specified delay, it updates debouncedValue. If the value changes again
 * within the delay, the timer resets and the delay starts over.
 *
 * @param value - The value to debounce before sending.
 * @param delay - The delay (in milliseconds) between requests.
 * @returns The value after the specified delay.
 */
function useDebounce<T>(value: T, delay?: number): T {
    const [debouncedValue, setDebouncedValue] = useState<T>(value);

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay || 500);

        return () => {
            clearTimeout(timer);
        };
    }, [value, delay]);

    return debouncedValue;
}

export default useDebounce;
