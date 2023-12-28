
let timer: number = 0;
export const debounceInput = (fieldValue: string, callback: Function) => {
    // Clear the previous timeout before setting a new one
    clearTimeout(timer);

    timer = setTimeout(() => {
        if (fieldValue.length > 4) {
            callback();
        }
    }, 2000);
};
