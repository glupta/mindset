<template>
  <div class='call'>
    <SessionTopBar :showTimer=show_timer :showLeave=show_leave :timeLimit=time_limit :sessionCopy=session_copy @timer-expired="onTimerExpired" @leave-session="leaveSession"></SessionTopBar>

    <button id='med-button' class='get-started-button' @click='unMuteButton'>Click here to start</button>
    <audio id="meditationbell" src='https://ia800607.us.archive.org/28/items/LovelyMeditationBell/STE-015.flac' muted></audio>
    <!--audio id="meditationbell" src='@/assets/meditationbell.flac' muted></audio-->
    
    <!--SessionBottomBar></SessionBottomBar-->
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import router from '../router'
export default {
  name: "Call",
  data () {
    return {
      time_limit: 0,
      session_copy: '',
      show_timer: true,
      show_leave: true
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar,
    //VideoChat
  },
  props: {
    testSession: Boolean,
    roomName: String,
    medTime: Number
  },
  methods: {

    unMuteButton() { //button clicked to start session
      
      document.getElementById('meditationbell').muted = false; //rule to override audio autoplay
      document.getElementById('med-button').style.display = 'none';
      
      document.querySelector('iframe').style.visibility = "visible"; //show vid chat

      this.show_leave = true;

      if (this.testSession) { //show copy at top for test session
        this.session_copy = "Audio & video settings good?" 
      }
      else { ////show timer and copy at top for real session
        this.session_copy = "Say hello & begin meditation.";
        this.show_timer = true;
      }
    },

    leaveSession() {
      if (this.testSession) {
        router.push({ name: 'WaitingRoom' });
      }
      else {
        router.push({ name: 'SessionEnd' });
      }
    },

    onTimerExpired() {

      if (this.debriefNext) { //set environment for debrief  

        //play ending bell
        document.getElementById('meditationbell').play();
         
        this.debriefNext = false;
        this.time_limit = 2 * 60;
        this.session_copy = "How was your session?";
      }
      else { //if debrief ended
        router.push({ name: "SessionEnd" });
      }
    }
  },

  mounted() {

    if (!this.roomName) { //kick out if room name not given
      router.push({ name: "SessionEnd" });
      return;
    }

    //hide timer & leave button to start with
    this.show_timer = false;
    this.show_leave = false;

    //set environment if test session 
    if (this.testSession) {
      //this.session_copy = "Are your video and audio settings working?";
      console.log("test session");
    }
    else { //set environment if meditation session
      this.debriefNext = true;
      console.log("med time is:",this.medTime);
      this.time_limit = (this.medTime > 0) ? this.medTime : 10 * 60;
      //this.session_copy = "Please begin meditation";
    }

    //call daily.co API to add user to assigned video chat room
    var room_url = "https://meditate-live.daily.co/";
    room_url += String(this.roomName);
    console.log("call is mounted, room url:",room_url);
    let dailycoScript = document.createElement('script');
    dailycoScript.addEventListener("load", function(event) {
      window.callFrame = window.DailyIframe.createFrame();
      callFrame.join({ url: room_url});
      var elem = document.querySelector('iframe');
      elem.style.width = "100%";
      elem.style.height = "90%";
      //elem.style.height = "100%";
      //elem.style.margin = "10px";
      //elem.style.right = "-10px";
      //elem.style.bottom = "-10px";
      //elem.style.left = "-10px";
      //elem.style.top = "-10px";
      //elem.style.bottom = "auto";     
      //elem.style.width = "375px";
      //elem.style.height = "750px";
      elem.style.top = "50px";
      elem.style.right = "0em";
      elem.style.bottom = "0em";
      //elem.style.bottom = "10px";
      elem.style.visibility = "hidden";
      //elem.style.overflow = "scroll";
      //elem.style.display = 'none';
    });
    dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
    dailycoScript.setAttribute('crossorigin','');
    dailycoScript.setAttribute('allowfullscreen',true);
    document.body.appendChild(dailycoScript);
  },

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = (this.testSession) ? 'Test Room' : 'Meditation Room' || 'Some Default Title';
      }
    }
  },

  destroyed() {
    
    //delete vid chat
    var elem = document.querySelector('iframe');
    if (elem) {
      elem.style.display = 'none';
      callFrame.leave();
      callFrame.destroy();
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}


.get-started-button {
  background-color: #2AD9FF;
  border: 1px solid #2AD9FF;
  box-sizing: border-box;
  border-radius: 6px;
  color: #FFFFFF;
  font-size: 24px;

/*
  width: 271px;
  line-height: 22px;
  height: 58px;

  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
*/

  padding-top: 18px;
  padding-bottom: 20px;
  padding-right: 40px;
  padding-left: 40px;
  cursor:pointer;
}

.iframe-container {
  margin-top: 50px;
}

</style>
