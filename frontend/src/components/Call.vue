
<template>
  <div class='call'>
    <SessionTopBar :showTimer=show_timer :leftCopy=left_copy :showLeave=show_leave :timeLimit=time_limit :sessionCopy=session_copy @timer-expired="onTimerExpired" @left-action="startTimer" @leave-session="leaveSession"></SessionTopBar>
    <div class='load-wrapper' id='load-wrapper'>
      <!--button id='med-button' class='get-started-button' @click='unHideButton'>{{joinButtonCopy}}</button-->
      <p>
        Connecting...
        <br><br>
        <Timer :timeLimit='time_start' @timer-expired='onLoadTimerExpired'>
      </p>
    </div>
    <!--div class='load-input' id='load-input'>
      <div class='load-input-top'>
        <p>
          Please select duration:
        </p>
      </div>
      <div class='load-input-first'>
        <p>
          Test Run for 15 seconds
        </p>
      </div>
      <div class='load-input-second'>
        <p>
          Meditation for 15 minutes
        </p>
      </div>
      <p>
        Duration of session timer?
        <br><br>
        <input v-model='med_input' placeholder='Enter in seconds'>
        <button @click='inputMedTime'>Submit</button>
      </p>
    </div-->
    <!--SessionBottomBar></SessionBottomBar-->
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import Timer from '@/components/Timer'
import router from '../router'
export default {
  name: "Call",
  data () {
    return {
      time_limit: 0,
      session_copy: '',
      left_copy: ' ',
      show_timer: true,
      show_leave: true,
      chat_height: 0,
      //med_input: 0
      //joinButtonCopy: ''
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar,
    Timer
  },
  props: {
    testSession: Boolean,
    roomName: String,
    medTime: Number
  },

  mounted() {

    this.killVidChat(); //delete any loose iframe

    if (this.roomName) { //connect if room name given

      this.room_name = this.roomName;
      this.reload_room = false;

      //hide everything to start with
      this.show_timer = false;
      this.show_leave = false;
      this.left_copy = '';

      this.sessionStatus = 'load'; //show loading page

      if (this.testSession) {
        this.test_session = true;
        //document.getElementById('load-wrapper').style.display = 'none';
        console.log("test session");
        this.time_start = 3;
      }
      else {
        //document.getElementById('load-input').style.display = 'none';
        this.time_start = 9;
      }
      this.sessionLoad();
    }
    else { //reconnect with cookie if connection lost

      if (this.$cookies.isKey('medliveorg')) { //use cookie to find room

        //reset session environment 
        this.reload_room = true;
        this.left_copy = '';
        document.getElementById('load-wrapper').style.display = 'none';
        //document.getElementById('load-input').style.display = 'none';
        this.session_copy = 'Connection lost, timer stopped.';

        this.client_id = this.$cookies.get('medliveorg');
        console.log(this.client_id,": found cookie");

        var entry = {
            clientID: this.client_id
        };

        fetch('/api/checkroom', { //call backend to get room data
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
            //console.log("data: ",data);

            if ('error' in data) { //error handling from testroom backend call
              console.log(this.client_id,": checkroom error: ",data['error']);
              alert("checkroom error: " + data['error']);
              return;
            }

            //take room name from backend call
            if ('room_name' in data && 'user_name' in data) { 
              this.room_name = String(data['room_name']);
              //console.log(this.client_id,": room name: ",this.room_name);

              if (data['user_name'] == data['room_name']) {//if both match, then test room
                this.test_session = true;
              }
            }
            else {
              alert("room and user data missing");
              return;
            }
            this.sessionLoad(); //load session now
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
      else { //kick user out if no cookie
        console.log("no cookie, kick out");
        router.push({ name: "SessionEnd" });
        return;
      }
    }
  },

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = (this.test_session) ? 'Test Room' : 'Meditation Room' || 'Some Default Title';
      }
    }
  },

  beforeDestroy() {
    
    //delete vid chat
    this.killVidChat();

    //stop bell ring
    if (this.med_bell) {
      this.med_bell.pause();
      console.log('bell paused at exit');
    }
  },

  Destroyed() {
    //delete vid chat
    this.killVidChat();
  },

  methods: {

    // unHideButton() { //button clicked to start session
      
    //   //load audio file, overcome autoplay issue
    //   this.med_bell = new Audio(require('@/assets/meditationbell.mp3'));
    //   this.med_bell.addEventListener('canplaythrough', event => {
    //     console.log("audio loaded");
    //   });

    //   //workaround to loop audio on mute
    //   this.med_bell.muted = true;
    //   this.med_bell.loop = true;
    //   this.med_bell.play();

    //   //hide button and show vid chat environment
    //   document.getElementById('load-wrapper').style.display = 'none';
    //   document.querySelector('iframe').style.visibility = "visible";
    //   this.show_leave = true;

    //   if (this.testSession) { //show bell and copy at top for test session
    //     this.session_copy = "Test Video Chat & Bell Volume";
    //     this.left_copy = "Bell";
    //   }
    //   else { //show timer and copy at top for real session
    //     this.session_copy = "Say Hello & Begin Meditation";
    //     this.show_timer = true;
    //     this.left_copy = "Timer";
    //   }
    // },

    sessionLoad() { //load video chat with room name

      var entry = {
        room_name: this.room_name
      };

      fetch('/api/roomtoken', { //call backend to get room data
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
          //console.log("data: ",data);

          if ('error' in data) { //error handling from testroom backend call
            console.log(this.client_id,": roomtoken error: ",data['error']);
            alert("roomtoken error: " + data['error']);
            return;
          }

          //take token from backend call
          if ('token' in data) {
            //console.log("token: ",data['token']);
            
            //call daily.co API to add user to assigned video chat room
            var room_url = "https://meditate-live.daily.co/" + this.room_name + "?t=" + data['token'];
            //console.log(this.room_name,", call is mounted, room url:",room_url);
            let dailycoScript = document.createElement('script');
            dailycoScript.addEventListener("load", event => {
              window.callFrame = window.DailyIframe.createFrame();
              callFrame.join({ url: room_url});
              var elem = document.querySelector('iframe');
              elem.style.position = "absolute";
              elem.style.top = "50px";
              elem.style.right = "0";
              elem.style.width = "100%";
              elem.style.height = "calc(100% - 50px)";
              elem.style.visibility = (this.reload_room) ? "visible" : "hidden";
            });
            dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
            dailycoScript.setAttribute('crossorigin','');
            dailycoScript.setAttribute('allowfullscreen',true);
            document.body.appendChild(dailycoScript);

            // if (this.test_session) {
            //   this.session_copy = "Are you in the bottom left? Press START.";
            //   this.startSession();
            //}
          }
          else {
            alert("token data missing");
            return;
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },

    inputMedTime() { //input meditation time for test session
      
      if (!isNaN(parseInt(this.med_input)) && this.med_input > 0) {
        document.getElementById('load-input').style.display = 'none';
        this.session_copy = 'Check Settings & Start Timer';
        this.startSession();  
      }
    },

    startTimer() { //timer starts when button clicked

      //load audio file, overcome autoplay issue
      if (!this.med_bell) {
        this.med_bell = new Audio(require('@/assets/meditationbell.mp3'));
        //console.log('new audio');
      }

      //workaround to loop audio on mute
      this.med_bell.muted = true;
      this.med_bell.loop = true;
      this.med_bell.play();

      this.left_copy = '';
      this.show_timer = true;
      this.session_copy = (this.test_session) ? "Let the timer run out." : "Please begin meditation.";

      if (this.test_session) {
        this.time_limit = 10;//(this.med_input > 0) ? this.med_input : 15 * 60;
      }
      else {
        console.log("med time is:",this.medTime);
        this.time_limit = (this.medTime > 0) ? this.medTime : 15 * 60;
      }
    },

    bellRings() { //bell rings after timer expires

      //reset and unmute audio
      console.log("audio played");
      this.med_bell.currentTime = 0;
      this.med_bell.muted = false;
      this.med_bell.volume = 1;
      this.med_bell.loop = false;

      this.med_bell.addEventListener('canplaythrough', event => {
        console.log("audio loaded");
      });

      this.med_bell.play();
    },

    //if test session, take user to waiting room. otherwise, session end page.
    leaveSession() {
      if (this.test_session) {
        router.push({ name: 'WaitingRoom' });
      }
      else {
        router.push({ name: 'SessionEnd' });
      }
    },

    onLoadTimerExpired() { //load timer triggers this which redirects to main expire function
      this.onTimerExpired();
    },

    onTimerExpired() { //function runs based on stage of session when timer expires

      if (this.sessionStatus == 'load') {

        document.getElementById('load-wrapper').style.display = 'none';
        document.querySelector('iframe').style.visibility = "visible";
        this.session_copy = (this.test_session) ? "Are you in the bottom left? Press START." : 'Say hello & press START together.';
        this.startSession();

      }
      else if (this.sessionStatus == 'meditate') { //set environment for debrief  
        
        //set debrief environment
        this.sessionStatus = 'debrief';
        this.time_limit = 5 * 60;
        this.show_timer = false;

        this.session_copy = (this.test_session) ? "Did the bell ring? Press LEAVE to exit." : "Thank your partner. Good bye!";

        //play ending bell
        this.bellRings();
      }
      else if (this.sessionStatus == 'debrief') { //if debrief ended
        router.push({ name: "SessionEnd" });
      }
      else {
        console.log("session status error");
        return;
      }
    },


    startSession() { //set meditate environment

      //document.querySelector('iframe').style.visibility = "visible";
      this.sessionStatus = 'meditate';
      this.show_leave = true;
      this.show_timer = false;
      this.left_copy = "START";
    },

    //disconnect from vid chat & delete iframe
    killVidChat() {
      var elem = document.querySelector('iframe');
      if (elem) {
        elem.style.display = 'none';
        callFrame.leave();
        callFrame.destroy();
        console.log("killed vid chat");
      }
      else {
        console.log("did not find vid chat");
      }
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}

.load-wrapper {

  align-items: center;
  justify-content: center;
  display: flex;
  height: 358px;
  font-size: 36px;
}

.load-input {

  align-items: center;
  justify-content: center;
  display: flex;
  height: 358px;
  font-size: 24px;

  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;

}

.load-input-top {
  position: absolute;
  top: 50px;
  left: 0;
  right: 0;
}

.load-input-first {
  position: absolute;
  top: 150px;
  left: 0;
  right: 0;
  border-style: solid;
  align-items: center;
  justify-content: center;
}

.load-input-second {
  position: absolute;
  top: 250px;
  left: 0;
  right: 0;
  border-style: solid;
  align-items: center;
  justify-content: center;
}

.get-started-button {
  background-color: #2AD9FF;
  border: 1px solid #2AD9FF;
  box-sizing: border-box;
  border-radius: 6px;
  color: #FFFFFF;
  font-size: 24px;

  width: 271px;
  height: 58px;

  box-sizing: border-box;
  cursor:pointer;
}

</style>
