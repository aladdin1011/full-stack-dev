let number = Number(prompt("Введите температуру в Цельсиях:"));
console.log("Фаренгейт:", number * 9 / 5 + 32);
let number1 = Number(prompt("Введите число:"));
if (number1 % 2 === 0) {
    console.log("Четное число");
} else {
    console.log("Нечетное число");
}


let number2 = Number(prompt("Введите простое число:"));
if (number2 <= 1) {
    console.log(number2 + " не является простым числом.");
} else {
    let flag = true; 
    for (let i = 2; i < number2; i++) {
        if (number2 % i === 0) {
            flag = false; 
            break; 
        }
    }
    if (flag) {
        console.log(number2 + " является простым числом.");
    } else {
        console.log(number2 + " не является простым числом.");
    }
}
