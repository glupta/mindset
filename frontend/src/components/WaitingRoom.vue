<template>
  <div class="waiting-room">
    <SessionTopBar :timeLimit=time_limit timerCopy='Session starts in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <div class='waiting-room-partner'>
        
        <p class='description' style='background-color:#2AD9FF;color:#FFFFFF;'>
        <br><br><br><br><br><br><br><br>
        You're here!
        <br>
        Waiting for your meditation<br>
        buddy to join.
        <br><br>

        <select v-model="user_selection">
          <option disabled selected>Pick User</option>
          <option>User1</option>
          <option>User2</option>
          <option>User3</option>
          <option>User4</option>
        </select>
        </p>
        
    </div>
    <div class='video-chat-self'></div>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import router from '../router'
export default {
  name: 'WaitingRoom',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0,
      user_selection: null
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar
  },
  mounted() {
    
    fetch('/api/timedetails') //calls backend to get time details
    .then(response => {
      if (response.status !== 200) { //server error handling
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(data => {
      
        //get current and scheduled times
        let time_current = new Date(data["time_current"]);
        let time_sched = new Date(data["time_sched"]);
        console.log("current time1: ",time_current," sched time1:",time_sched);
      
        if (time_sched.getTime() < time_current.getTime()) { //reroute if user joined waiting room too late
          this.onWaitingRoomLate();
        } else {
          //this.time_limit = parseInt((time_sched - time_current)/1000); //time until session starts
          this.time_limit = 10
          console.log("time limit:",this.time_limit);
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
  },

  watch: {
    user_selection(newValue) {
      console.log("user is:",this.user_selection);
    }
  },

  methods: {
    onWaitingRoomLate() {
      router.push({ name: "SessionEnd" });
    },
    onTimerExpired() {
      
      //create json data to send to server
      //send parameter: device/client ID
      var entry = {
        clientID: this.user_selection
      };
      
      //call the backend '/api/requestroom'
      fetch('/api/requestroom', {
        method: "POST",
        body: JSON.stringify(entry),
        headers: new Headers({
        "content-type": "application/json"
        })
      })
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => { //info about client added to active users in DB
          console.log(data);
          //this.room_name = data['room_name'];

          //dummy data
          var room_name = "";
          if (this.user_selection == "User1" || this.user_selection == "User2")
            room_name = "room1";
          else if (this.user_selection == "User3" || this.user_selection == "User4")
            room_name = "room2";

          //join video chat room (break into its own file)
          var room_url = "https://meditate-live.daily.co/";
          //room_url += room_name == "" ? 'hello' : room_name;
          if (room_name == "") {
            room_url += 'hello';
          } else {
            room_url += room_name;
          }

          console.log("passing URL to call:",room_url);
          //take user to call page
          router.push({
            name: "Call",
            params: {
              roomURL: room_url
            }
          })

          // let dailycoScript = document.createElement('script');
          // dailycoScript.addEventListener("load", function(event) {
          //   window.callFrame = window.DailyIframe.createFrame();
          //   callFrame.join({ url: room_url});
          //   var elem = document.querySelector('iframe');
          //   elem.style.width= "375px";
          //   elem.style.height = "750px";
          //   elem.style.right= "0em";
          //   elem.style.bottom= "0em";
          // });
          // dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
          // document.head.appendChild(dailycoScript);
        })
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.waiting-room {
  font-family: 'DIN Condensed', sans-serif;
  font-size: 24px;
}
</style>
