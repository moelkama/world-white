import { fetchConversation, fetchAllMessage} from './chatScript.js';
function draw_statistique(lose , win)
{
    let circle = document.querySelector('.leadrboard-circle');
    document.querySelector('.leader-stats').style.display == 'flex';
    let value_win = win;
    let value_lose = lose;
    let totale = value_win + value_lose;
    let _win = value_win * 100 / totale;
    let _lose = value_lose * 100 / totale;
    let  div_white = document.querySelector('.leadrboard-div-white')
    let div_lose =  document.createElement('div');
    let number_win = document.querySelector('.leadrboard-win')
    let number_lose = document.querySelector('.leadrboard-lose')
    number_lose.textContent = `Losing ${lose}`;
    number_win.textContent = `Wining ${win}`;
    let text_lose  = document.querySelector('.lederboard-lose-statistique');
    div_lose.classList.add('leadrboard-child');
    let div_win =  document.createElement('div');
    let text_win  = document.querySelector('.lederboard-win-statistique');
    div_win.classList.add('leadrboard-child');
    text_win.textContent = '0%'
    text_lose.textContent = '0%'
    circle.append(div_lose, div_win);
    let img = div_white.querySelector('img')
    let i = 0;
    let j = 0;
    img.addEventListener('mouseover', ()=>{
        div_win.style.width = '270px';
        div_win.style.height = '270px';
        number_lose.style.display = 'flex';
        number_win.style.display = 'flex';

    });
    img.addEventListener('mouseleave', ()=>{
        div_win.style.width = '250px';
        div_win.style.height = '250px';
        number_lose.style.display = 'none';
        number_win.style.display = 'none';
    });
    div_win.style.background = `conic-gradient(#5cb85c ${value_win * 360 / totale}deg, #D8636F 0deg)`
    div_lose.style.background = `conic-gradient(#D8636F ${value_lose * 360 / totale}deg, #5cb85c 0deg)`

    circle.style.display = 'flex';
}

function my_data()
{
    fetch('/api/data/')
    .then(response => {
        if (!response.ok) {
            window.location.href = "/";
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // console.log(data);

        const userData = JSON.parse(JSON.stringify(data));
        // console.log(userData);
        if (userData.lose != 0  ||  userData.win != 0)
        {
            document.querySelector('.has-noStatistique').style.display = 'none';
            draw_statistique(userData.lose, userData.win);
        }
        else{
            document.querySelector('.has-noStatistique').style.display = 'flex'
            document.querySelector('.leader-stats').style.display == 'none';

        }
    
        // Update user information in the DOM
        document.getElementById('login').textContent = userData.username;
        document.getElementById('login').classList.add(userData.id);
        document.getElementById('content_scor').textContent = userData.score;
        // console.log(data.id);
    
        fetchConversation(data.id, data.username);
        fetchAllMessage(data.id, data.username);
        if (userData.username ) {
            document.getElementById('nameprofile').textContent = userData.username;
        }
        document.getElementById('content_rank').textContent = userData.ranking;
        
        
        const settingsForm = document.getElementById('profil');
        if (document.querySelector('.profile-settings-img') == null)
        {
            const img3 = createProfileImage(userData.photo_profile, "2px solid black");
            img3.classList.add('profile-settings-img');
            settingsForm.prepend(img3);
        }
        else{
            document.querySelector('.profile-settings-img').src = userData.photo_profile
        }
        // Add user profile picture to profileid
        if (document.querySelector('.image-profile-id') == null){
            const imgpro = document.getElementById('profileid');
            const img2 = createProfileImage(userData.photo_profile, "2px solid cyan");
            img2.classList.add('image-profile-id');
            imgpro.appendChild(img2);
        }
        else{
            document.querySelector('.image-profile-id').src = userData.photo_profile
        }
        
        // Add user profile picture to imageprofile
        if (document.querySelector('.image-profile-user') == null){
            const profiles = document.getElementById('imageprofile');
            const img = createProfileImage(userData.photo_profile, "2px solid black");
            img.classList.add('image-profile-user')
            profiles.appendChild(img);
        }
        else{
            document.querySelector('.image-profile-user').src =  userData.photo_profile;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
my_data();
// document.addEventListener('DOMContentLoaded', function() {
//     my_data();
// });



// Helper function to create profile image
function createProfileImage(src, border) {
    const img = document.createElement('img');
    img.src = src;
    img.style.borderRadius = "50%";
    img.style.border = border;
    return img;
}
export {my_data}