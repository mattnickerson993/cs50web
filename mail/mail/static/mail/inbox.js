document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email(status, id) {

  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  if (status === 'reply'){
      fetch(`/emails/${id}`)
      .then(response => response.json())
      .then(email =>{
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        document.querySelector('#compose-body').value = `\n\n\nOn ${email.timestamp} ${email.sender} wrote 
        ${email.body}`;
      })
  }
  const form = document.getElementById('compose-form')
  form.addEventListener('submit', postemail, {
    once: true
  });

  
};

function load_mailbox(mailbox) {
  
  emailsView = document.querySelector('#emails-view')
  composeView = document.querySelector('#compose-view')
  displayView = document.querySelector('#display-view')
  // Show the mailbox and hide other views
  emailsView.style.display = 'block';
  composeView.style.display = 'none';
  displayView.style.display = 'none';

  // Show the mailbox name
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => emails.forEach(email => {
    const newDiv = document.createElement('div');
    newDiv.classList.add('email')
    newDiv.innerHTML = `
      <div>${email.sender}</div>
      <div>${email.body}</div>
      <div>${email.timestamp}</div>
    `
    
    emailsView.appendChild(newDiv)
    if(email.read){
      newDiv.classList.add('emailback')
    }
    newDiv.addEventListener('click', () =>{
        fetch(`emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
      }, {
        once:true
      }
    )
    newDiv.addEventListener('click', () =>{
        
      fetch(`/emails/${email.id}`)
      .then(response => response.json())
      .then(data => {
        emailsView.style.display = 'none';
        displayView.style.display = 'block';
        displayDiv = document.createElement('div')
        displayDiv.classList.add('display-div');
        displayDiv.innerHTML = '';
        displayDiv.innerHTML = `
        <div class="email-content border-bottom border-primary">
        <div><strong>From:</strong> ${data.sender}</div>
        <div><strong>To:</strong> ${data.recipients}</div>
        <div><strong>Subject:</strong> ${data.subject}</div>
        <div><strong>Timestamp:</strong> ${data.timestamp}</div>
        <div><button id="reply-btn" class="btn btn-sm btn-outline-primary">Reply</button>
            ${mailbox === 'archive'? '<button id="unarchive-btn" class="remove btn btn-sm btn-outline-secondary">Unarchive</button>' : '<button id="archive-btn" class=" remove btn btn-sm btn-outline-secondary">Archive</button>' }
        </div>
        </div>
        <div class="email-body mt-2">
        <div>${data.body}</div>
        </div>
        `;
        displayView.innerHTML="";
        displayView.appendChild(displayDiv)
        if (mailbox === 'archive'){
            unarchivebtn = document.getElementById('unarchive-btn')
            unarchivebtn.addEventListener('click', () => {
              fetch(`emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: false
                })
              })
    
            },
            {
              once: true
            })
        }
        else{
          archivebtn = document.getElementById('archive-btn')
          archivebtn.addEventListener('click', () => {
            fetch(`emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                archived: true
              })
            })
  
          },
          {
            once: true
          })
        }

        if (mailbox === 'sent'){
          btnToRemove = document.querySelector('.remove')
          btnToRemove.style.display = 'none'
        }
        
        
        replybtn = document.getElementById('reply-btn')
        replybtn.addEventListener('click', () => 
          compose_email('reply', email.id),{
            once: true
          })

      })
    
    }, {
      once: true
    })

  })
  ) 
  
}


async function postemail(event){
  event.preventDefault()
  const content = {
    recipients: document.querySelector('#compose-recipients').value,
    subject: document.querySelector('#compose-subject').value,
    body: document.querySelector('#compose-body').value
  }
  const response = await fetch('/emails', {
    method: 'POST',
    body: JSON.stringify(content)
  })
  const json = await response.json()
  console.log(json)
  load_mailbox('sent')
}