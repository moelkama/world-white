import { create_chatRoom } from "./chatScript.js";

let map = new Map();
let previousDataSize = 0;

document.addEventListener('DOMContentLoaded', function() {
    
    fetchAndUpdateFriends();
});
export function fetchAndUpdateFriends() {
    fetch('/api/friends/')
        .then(response => {
            if (!response.ok) {
                window.location.href = "/";
            }
            return response.json();
        })
        .then(data => {
            // console.log(data);
            let chat_msg = document.querySelector('.chat-friend-name');
            let ishere =  false;
            if (data.length !== previousDataSize) {
                // console.log(data)
                previousDataSize = data.length;
                var reward = document.getElementById('list_friend_chat');
                reward.innerHTML = ""; 

                for (let i = 0; i < data.length; i++) {
                    if (chat_msg != undefined && chat_msg == data[i].username)
                        ishere = true;
                    let container = document.createElement('button');
                    let img = document.createElement('img');
                    img.src = data[i].photo_profile;
                    img.style.width = "40px";
                    img.style.height = "40px";
                    img.style.borderRadius = "50%";
                    img.style.border = "2px solid black";

                    let username = document.createElement('p');
                    username.textContent = data[i].username;
                    username.style.marginLeft = "15px";
                    container.id = data[i].id_user;
                    container.style.cssText = `
                        display: flex;
                        align-items: center;
                        width: 100%;   
                    `;
                    container.appendChild(img);
                    container.appendChild(username);
                    container.classList.add("friend-list-room");
                    reward.appendChild(container);
                    reward.appendChild(document.createElement('br'));
                    map.set(data[i].username, "block");
                }
                if (!ishere)
                {
                    document.querySelector('.chat-messages').style.display = 'none';
                    document.querySelector('.chat-input').style.display = 'none';
                    if (document.querySelector('.header-chat-photouser'))
                        document.querySelector('.header-chat-photouser').style.display = 'none'
                    if (document.querySelector('.chat-option-user'))
                        document.querySelector('.chat-option-user').style.display = 'none'
                    document.querySelector('#chat-friend-name').textContent = 'Select a friend to chat';
                    document.querySelector('#chat-friend-name').style.fontSize = '25px'
                    document.querySelector('.chat-header').style.border = 'none';
                    
                }
                create_chatRoom(map);
            }
        })
        .catch(error => {
            console.error('Error fetching friends:', error);
        });
}
