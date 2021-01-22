




var CLIENT_ID = config.client_id
var API_KEY = config.calendar_api_key
var gapi = window.gapi

var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"]
var SCOPES = "https://www.googleapis.com/auth/calendar.events"


const programEvent = {
  'summary':"",
  'location':"Charlottesville VA",
  'description':"",
  'start': {
    'dateTime': '',
    'timeZone': 'America/New_York'
  },
  'end': {
    'dateTime': '',
    'timeZone': 'America/New_York'
  }
}

const handleClick = () => {
 gapi.load('client:auth2', () => {
   console.log('loaded client')

   gapi.client.init({
     apiKey: API_KEY,
     clientId: CLIENT_ID,
     discoveryDocs: DISCOVERY_DOCS,
     scope: SCOPES,
   })

  //  load calendar
   gapi.client.load('calendar', 'v3', () => console.log('bam!'))

  //  sign user in
   gapi.auth2.getAuthInstance().signIn()
   .then(() => {
     
     var event = programEvent
     

     var request = gapi.client.calendar.events.insert({
       'calendarId': 'primary',
       'resource': event,
     })

     request.execute(event => {
       console.log(event)
       window.open(event.htmlLink)
     })
     

     /*
         Uncomment the following block to get events
     */
     /*
     // get events
     gapi.client.calendar.events.list({
       'calendarId': 'primary',
       'timeMin': (new Date()).toISOString(),
       'showDeleted': false,
       'singleEvents': true,
       'maxResults': 10,
       'orderBy': 'startTime'
     }).then(response => {
       const events = response.result.items
       console.log('EVENTS: ', events)
     })
     */
 

   })
 })

}
const testBtn = document.getElementById('testbtn')
testBtn.onclick= () => {
   handleInputs()
   handleClick()
}

function handleInputs(){

  let start = document.getElementById('program-start')
  let date = document.getElementById('program-date')
  let end = document.getElementById('program-end')
  
  programEvent.start.dateTime = `${date.value}T${start.value}:00-05:00`
  programEvent.end.dateTime = `${date.value}T${end.value}:00-05:00`
  
  
  
  
  
  
}

// for selecting program
programToggleButton = document.querySelector('.program-view')
programToggleButton.onclick = function(){
    items = Array.from(document.querySelectorAll('.program-item'))
    items.forEach(item => {
        item.classList.toggle('hide')
        item.addEventListener('click', () =>{
          console.log(item.dataset.id)
          console.log(item)
          toggelProgramEventData(item.dataset.id)},
          {once: true})
        })
    
}

async function toggelProgramEventData(id){
  let response = await fetch(`/exercise/programs/retrieve/${String(id)}`)
  let data = await response.json()
  console.log (data)
  programEvent.summary = data.title
  programEvent.description = data.contents.join(", ")
}

//  <!-- <a target="_blank" href="https://calendar.google.com/event?action=TEMPLATE&amp;tmeid=MTIyb2xodWNzaGc5Z2I2NGdoZTVjbDFtanMgNXVhcWtobTdpazlzYW5zMm5rYzRnYW9jdmdAZw&amp;tmsrc=5uaqkhm7ik9sans2nkc4gaocvg%40group.calendar.google.com"><img border="0" src="https://www.google.com/calendar/images/ext/gc_button1_en.gif"></a>
//  <iframe src="https://calendar.google.com/calendar/embed?height=600&amp;wkst=1&amp;bgcolor=%23ffffff&amp;ctz=America%2FNew_York&amp;src=NXVhcWtobTdpazlzYW5zMm5rYzRnYW9jdmdAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&amp;color=%23A79B8E" style="border:solid 1px #777" width="800" height="600" frameborder="0" scrolling="no"></iframe> -->