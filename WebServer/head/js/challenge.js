import { view_profile } from './userInformation.js';


export function handlechalleng() {
    fetch('/api/online/')
        .then(response => {
            if (!response.ok) {
                window.location.href = "/";
            }
            return response.json();
        })
        .then(data => {
            // console.log("************************");
            // console.log(data)
            // console.log("************************");
            document.getElementById('challenge_friend').innerHTML = '';
            var reward = document.getElementById('challenge_friend');
            if (data.length === 0) {
                let container = document.createElement('div');
                container.classList.add('not-found');
                // let im = document.createElement('img');
                // im.src = "./resrc/online.png";
                let p = document.createElement('h2');
                p.textContent = "No friend online";
                // container.appendChild(im);
                container.appendChild(p);
                reward.appendChild(container);
                return;
            }

            for (let i = 0; i < data.length; i++) {
                let container = document.createElement('div');
                container.classList.add('bar_content');
                // container.style.display = 'flex';
                // container.style.alignItems = 'center';

                let img = document.createElement('img');
                img.style.objectFit = "cover";

                img.addEventListener('click', view_profile);
                img.id = data[i].username;
                img.src = data[i].photo_profile;
                img.style.width = "60px";
                img.style.height = "60px";
                img.style.borderRadius = "50%";
                img.style.border = "2px solid black";

                let div = document.createElement('div');
                div.style.width = "30%";

                let username = document.createElement('p');
                username.textContent = data[i].username;
                div.appendChild(username);

                let addfriend = document.createElement('button');
                addfriend.textContent = "Challenge";
                addfriend.id = data[i].username;
                addfriend.addEventListener('click', function (e){
                    challenge_friend(data[i].username);
                });


                container.appendChild(img);
                container.appendChild(div);
                container.appendChild(addfriend);
                reward.appendChild(container);
                reward.appendChild(document.createElement('br'));
            }
        })
        .catch(error => {
            console.error('Error fetching friends:', error);
        });
}


handlechalleng();
document.addEventListener('DOMContentLoaded', function() {
    handlechalleng(); // Initial call on page load
    // setInterval(fetchRequests, 2000); // Subsequent calls every 2 seconds
});
