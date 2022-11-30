document.addEventListener("DOMContentLoaded", () => {
    let check = [false,false,false,false,false,false];
    document.querySelectorAll(".inp").forEach(input => {
        input.addEventListener('input', () => {

            if(input.classList.contains('usrname')){
                if(input.value.trim().length !== 0) {check[0]=true;}
                else{check[0] = false;}
            }
            if(input.classList.contains('displayName')){
                if(input.value.trim().length !== 0) {check[0]=true;}
                else{check[0] = false;}
            }
            if(input.classList.contains('github')){
                if(input.value.trim().length !== 0) {check[0]=true;}
                else{check[0] = false;}
            }
            if(input.classList.contains('pswd')){
                document.querySelector('.cpswd').value = "";
                document.querySelector('.cpswd').parentElement.querySelector('span').innerText = "";
                check[2] = false;
                if(input.value.trim().length !== 0) {check[1]=true;}
                else{check[1] = false;}
            }
            if(input.classList.contains('cpswd')){
                if(input.value.trim().length !== 0) {
                    if(input.value !== document.querySelector('.pswd').value) {
                        input.parentElement.querySelector('span').innerText = "Password must match";
                        check[2] = false;
                    }
                    else {
                        input.parentElement.querySelector('span').innerText = "";
                        check[2]=true;
                    }
                }
                else{check[2] = false;}
            }

            let i;
            for(i=0;i<2;i++) {
                if(!check[i]) {
                    break;
                }
            }

            if(i===2) {
                document.querySelector('input[type="submit"]').disabled = false;
            }
            else {
                document.querySelector('input[type="submit"]').disabled = true;
            }

        });
    });
});