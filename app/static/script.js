window.addEventListener('DOMContentLoaded', ()=>{
    let date = document.querySelector('.date');
    let timer = setInterval(()=>{
        let check = (number) =>{
            if(number.toString().split('').length === 1){
                number = number.toString().split('');
                number[1] = number[0];
                number[0] = '0';
                number = number.join('');
                return number
            }
            return number
        };
        let time = new Date();
        date.innerHTML = `${check(time.getHours())}:${check(time.getMinutes())} ${check(time.getDate())}.${check(time.getMonth() + 1)}.${time.getFullYear()}`;
    },1000)
})